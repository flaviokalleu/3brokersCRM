const express = require("express");
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const app = express();
const client = new Client({
  puppeteer: {
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  },
  auth: {
    session: false, // Remova options.session
    clientID: 'your-client-id', // Adicione o clientID, substitua com seu próprio
    clientToken: 'your-client-token', // Adicione o clientToken, substitua com seu próprio
    clientTokenEncKey: 'your-client-token-enc-key', // Adicione o clientTokenEncKey, substitua com seu próprio
  },
});

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("authenticated", (session) => {
  console.log("Cliente autenticado!");
  // Salve a sessão se necessário
});

client.on("disconnected", (reason) => {
  console.log(`Cliente desconectado: ${reason}`);
  // Implemente lógica de reconexão aqui, se necessário
  // client.initialize();  // Descomente se quiser tentar uma reconexão imediata
});

client.on("auth_failure", (msg) => {
  console.error("Falha na autenticação:", msg);
  // Implemente lógica de reconexão aqui
  // client.initialize();  // Descomente se quiser tentar uma reconexão imediata
});

client.on("ready", () => {
  console.log("Cliente está pronto!");
});

client.initialize();

app.use(express.json());

app.post("/send-message", (req, res) => {
  const number = req.body.number;
  const message = req.body.message;

  client
    .sendMessage(number, message)
    .then(() => {
      return res.json({ success: true });
    })
    .catch((err) => {
      return res.json({ success: false, error: err.message });
    });
});

app.post("/notify-correspondente", (req, res) => {
  const cliente_nome = req.body.cliente_nome;

  // Dummy data para o exemplo. Na vida real, você provavelmente consultaria o banco de dados aqui.
  const whatsapp_num = "556196551446@c.us";

  const message = `O cliente *${cliente_nome}* foi cadastrado com sucesso no sistema.`;

  client
    .sendMessage(whatsapp_num, message)
    .then(() => {
      return res.json({ success: true });
    })
    .catch((err) => {
      return res.json({ success: false, error: err.message });
    });
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
