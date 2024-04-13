import re
import os
import base64
import time
import fitz  # PyMuPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from config import CONVENIO, USERNAME, PASSWORD
from selenium.webdriver.common.keys import Keys


def remove_phrases_from_pdf(pdf_file, output_file):
    doc = fitz.open(pdf_file)

    phrases_to_remove = [
        "Código do Correspondente: 000703230",
        "Código do Convênio 00070323-0 Identificação do Operador Flavio"
    ]

    for page_num in range(doc.page_count):
        page = doc[page_num]

        for phrase in phrases_to_remove:
            rects = page.search_for(phrase)
            for rect in rects:
                annot = page.add_redact_annot(rect)

        page.apply_redactions()
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    doc.save(output_file)
    doc.close()

def login(browser):
    time.sleep(2)
    browser.get('https://caixaaqui.caixa.gov.br/caixaaqui/CaixaAquiController')
    time.sleep(2)
    convenio_input = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#convenio')))
    convenio_input.send_keys(CONVENIO)
    
    login_input = browser.find_element(By.CSS_SELECTOR, '#login')
    login_input.send_keys(USERNAME)
    
    password_input = browser.find_element(By.CSS_SELECTOR, '#password')
    password_input.send_keys(PASSWORD)
    
    submit_button = browser.find_element(By.CSS_SELECTOR, '.btn-azul')
    submit_button.click()
    time.sleep(5)
    
def handle_alert_and_login(browser):
    try:
        alert = browser.switch_to.alert
        alert_text = alert.text
        print(f"Alert Text: {alert_text}")
        alert.accept()  # Aceitar o alerta
        print("Realizando login novamente...")
        login(browser)
    except:
        print("Não foi possível lidar com o alerta ou nenhum alerta encontrado.")


def consulta_cpf_func(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    browser = webdriver.Chrome(options=chrome_options)

    try:
        login(browser)

        try:
            time.sleep(2)
            submit_button_sim = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-azul")))
            submit_button_sim.click() 
            # Depois de enviar o CPF, envie a tecla "Enter"
            cpf_input.send_keys(Keys.ENTER)  
                 
        except:
            handle_alert_and_login(browser)
        
        
        browser.get('https://caixaaqui.caixa.gov.br/caixaaqui/CaixaAquiController/consulta_cadastral/consulta_cadastral1')

        cpf_input = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/center/div[2]/div[2]/table/tbody/tr[3]/td/div[1]/input')))
        cpf_input.send_keys(cpf)

        submit_button_cpf = browser.find_element(By.CSS_SELECTOR, '#spanCPF .btn-azul')
        submit_button_cpf.click()

        directory = 'static/uploads/PDF'

        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, f"{cpf}.pdf")

        pdf_content = browser.execute_cdp_cmd("Page.printToPDF", {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
        })

        with open(filename, 'wb') as f:
            f.write(base64.b64decode(pdf_content['data']))

        output_filename = os.path.join(directory, f"{cpf}_modified.pdf")
        remove_phrases_from_pdf(filename, output_filename)

        file_url = f"static/uploads/PDF/{cpf}_modified.pdf"
        return {"message": "Consulta concluída com sucesso.", "file_url": file_url}

    except Exception as e:
        print(f"Exception encountered: {e}")

    finally:
        browser.quit()