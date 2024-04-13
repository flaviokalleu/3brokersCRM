from django.core.exceptions import ValidationError

def validate_renda(value):
    # Remove pontos de milhares, se presentes
    value = value.replace('.', '')

    # Substitui vírgulas por pontos, se necessário
    value = value.replace(',', '.')

    # Verifica se o valor pode ser convertido em float
    try:
        float_value = float(value)
    except ValueError:
        raise ValidationError('O valor da renda deve ser numérico.')

    # Verifica se o valor é positivo
    if float_value < 0:
        raise ValidationError('O valor da renda deve ser positivo.')
