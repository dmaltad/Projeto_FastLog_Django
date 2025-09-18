from django.db import models
from django.contrib.auth.models import User
from order.validators import validate_cep, validate_phone_number, validate_cpf, validate_cnpj, validate_plate # <-- Importe aqui

class DeliveryMan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100,verbose_name='Nome Completo')
    contact_phone = models.CharField(max_length=15, verbose_name='Número de Telefone', validators=[validate_phone_number])
    public_place = models.CharField(max_length=200,verbose_name='Logradouro')
    cep = models.CharField(max_length=9, blank=True, null=True,verbose_name='CEP', validators=[validate_cep])
    city = models.CharField(max_length=100, blank=True, null=True,verbose_name='Município')
    state = models.CharField(max_length=50, blank=True, null=True,verbose_name='Estado')
    property_number = models.CharField(max_length=5, blank=True, null=True,verbose_name='Número do Endereço')
    complement_address = models.CharField(max_length=300, blank=True, null=True,verbose_name='Complemento de Endereço')
    cpf = models.CharField(max_length=14,unique=True, verbose_name='CPF',validators=[validate_cpf])
    plate = models.CharField(
        max_length=8, # Aumentar para 8 para permitir o hífen (ex: ABC-1234)
        verbose_name='Placa da Moto', 
        validators=[validate_plate] # Adicionado aqui
    )
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    profile_photo = models.ImageField(upload_to='entregadores/', blank=True, null=True, verbose_name='Foto do Entregador')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Entregador'
        verbose_name_plural = 'Entregadores'

    def __str__(self):
        return self.fullname
    
