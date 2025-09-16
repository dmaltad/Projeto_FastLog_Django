from django.db import models
from deliverymen.models import DeliveryMan
from django.contrib.auth.models import User


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=200, verbose_name='Nome da Empresa')
    cnpj = models.CharField(max_length=14,verbose_name='CNPJ')
    public_place = models.CharField(max_length=200,verbose_name='Logradouro')
    cep = models.CharField(max_length=8,verbose_name='CEP')
    city = models.CharField(max_length=100,verbose_name='Município')
    state = models.CharField(max_length=50,verbose_name='Estado')
    property_number = models.CharField(max_length=5,verbose_name='Número')
    complement_address = models.CharField(max_length=300,verbose_name='Complemento de Endereço')
    phone_number = models.CharField(max_length=11, verbose_name='Número de Telefone')
    email = models.EmailField()
    whatsapp_contact = models.CharField(max_length=11, verbose_name='Contato do Whatsapp')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.company_name
