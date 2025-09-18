import re
from django.core.exceptions import ValidationError

def validate_cep(value):
    """
    Valida se o CEP está no formato XXXXX-XXX ou XXXXXXXX.
    """
    # Remove qualquer caractere que não seja dígito
    cep = re.sub(r'[^0-9]', '', str(value))
    if len(cep) != 8:
        raise ValidationError('O CEP deve conter 8 dígitos.', code='invalid_cep')
    return value

def validate_phone_number(value):
    """
    Valida se o telefone está no formato (XX) XXXXX-XXXX ou XXXXXXXXXXX.
    """
    phone = re.sub(r'[^0-9]', '', str(value))
    if len(phone) not in [10, 11]:
        raise ValidationError('O número de telefone deve conter 10 ou 11 dígitos, incluindo o DDD.', code='invalid_phone')
    return value

def validate_cpf(value):
    """
    Valida um CPF brasileiro.
    """
    cpf = re.sub(r'[^0-9]', '', str(value))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido.', code='invalid_cpf')

    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito_1 = (soma * 10 % 11) % 10
    if digito_1 != int(cpf[9]):
        raise ValidationError('CPF inválido.', code='invalid_cpf')

    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito_2 = (soma * 10 % 11) % 10
    if digito_2 != int(cpf[10]):
        raise ValidationError('CPF inválido.', code='invalid_cpf')
        
    return value

def validate_cnpj(value):
    """
    Valida um CNPJ brasileiro.
    """
    cnpj = re.sub(r'[^0-9]', '', str(value))

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        raise ValidationError('CNPJ inválido.', code='invalid_cnpj')

    # Validação do primeiro dígito verificador
    soma = 0
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        soma += int(cnpj[i]) * pesos[i]
    resto = soma % 11
    digito_1 = 0 if resto < 2 else 11 - resto
    if digito_1 != int(cnpj[12]):
        raise ValidationError('CNPJ inválido.', code='invalid_cnpj')

    # Validação do segundo dígito verificador
    soma = 0
    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        soma += int(cnpj[i]) * pesos[i]
    resto = soma % 11
    digito_2 = 0 if resto < 2 else 11 - resto
    if digito_2 != int(cnpj[13]):
        raise ValidationError('CNPJ inválido.', code='invalid_cnpj')
        
    return value

# ... (validadores de CEP, Telefone, CPF, CNPJ que já existem) ...

def validate_plate(value):
    """
    Valida placas de veículos nos formatos brasileiro antigo (ABC-1234)
    e Mercosul (ABC1D23).
    """
    # Remove espaços e hífens, e converte para maiúsculas
    plate = str(value).upper().replace('-', '').strip()

    if len(plate) != 7:
        raise ValidationError(
            'A placa deve conter 7 caracteres.',
            code='invalid_plate_length'
        )

    # Padrão para placas antigas: 3 letras e 4 números (ex: ABC1234)
    pattern_antigo = re.compile(r'^[A-Z]{3}[0-9]{4}$')

    # Padrão para placas Mercosul: 3 letras, 1 número, 1 letra, 2 números (ex: ABC1D23)
    pattern_mercosul = re.compile(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$')

    if pattern_antigo.match(plate) or pattern_mercosul.match(plate):
        return value  # A placa é válida
    else:
        raise ValidationError(
            'Formato de placa inválido. Use o padrão ABC1234 ou ABC1D23.',
            code='invalid_plate_format'
        )