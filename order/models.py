from django.db import models
from deliverymen.models import DeliveryMan

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100,verbose_name='Nome de Produto')
    product_quantity = models.PositiveIntegerField(verbose_name='Quantidade de Produto')
    product_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True, verbose_name='Valor do Produto')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.product_name
    
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Nome do Cliente')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='client_product', verbose_name='Produto do Cliente')
    public_place = models.CharField(max_length=200,verbose_name='Logradouro')
    cep = models.CharField(max_length=8,verbose_name='CEP')
    city = models.CharField(max_length=100,verbose_name='Município')
    state = models.CharField(max_length=50,verbose_name='Estado')
    property_number = models.CharField(max_length=5,verbose_name='Número')
    complement_address = models.CharField(max_length=300,verbose_name='Complemento de Endereço')
    phone_number = models.CharField(max_length=11, verbose_name='Número de Telefone')
    whatsapp_contact = models.CharField(max_length=11, verbose_name='Contato do Whatsapp')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200, verbose_name='Nome da Empresa')
    cnpj = models.CharField(max_length=14,verbose_name='CNPJ')
    delivery_men = models.ForeignKey(DeliveryMan, on_delete=models.PROTECT, related_name='company_deliveryman', verbose_name='Entregador')
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
    
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    payment_method = models.CharField(max_length=50,verbose_name='Forma de Pagamento')
    payment_status = models.BooleanField(verbose_name='Status de Pagamento')

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return self.payment_method
     
class DeliveryOrder(models.Model):
    id = models.AutoField(primary_key=True)
    # user_company = None
    # user_deliveryman = None
    total_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True, verbose_name='Preço Total')
    order_code = models.PositiveIntegerField(verbose_name='Código de Pedido')
    receiver = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='deliveryorder_client', verbose_name='Destinatário')
    payment_mehtod = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='deliveryorder_payment', verbose_name='Metódo de Pagamento')
    note = models.TextField(max_length=500, verbose_name='Observações')
    delivery_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Ordem de Entrega'
        verbose_name_plural = 'Ordens de Entregas'

    def __str__(self):
        return self.order_code