# Generated by Django 4.2.9 on 2024-04-13 09:43

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='valor_da_renda',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[users.utils.validate_renda], verbose_name='Valor de Renda'),
        ),
    ]