# Generated by Django 4.2.9 on 2024-04-18 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_cliente_valor_da_renda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processo',
            name='tags',
        ),
    ]
