from django.db import models

class DeliveryMan(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=300,verbose_name='Nome Completo')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    plate = models.CharField(max_length=7, verbose_name='Placa da Moto')
    is_active = models.BooleanField(verbose_name='Está ativo')
    public_place = models.CharField(max_length=200,verbose_name='Logradouro')
    cep = models.CharField(max_length=8,verbose_name='CEP')
    city = models.CharField(max_length=100,verbose_name='Município')
    state = models.CharField(max_length=50,verbose_name='Estado')
    property_number = models.CharField(max_length=5,verbose_name='Número')
    complement_address = models.CharField(max_length=300,verbose_name='Complemento de Endereço')
    phone_number = models.CharField(max_length=11, verbose_name='Número de Telefone')
    email = models.EmailField()
    whatsapp_contact = models.CharField(max_length=11,verbose_name='Contato do Whatsapp')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Entregador'
        verbose_name_plural = 'Entregadores'

    def __str__(self):
        return self.fullname
    
