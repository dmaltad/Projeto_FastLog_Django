from django.db import models
from django.contrib.auth.models import User
from deliverymen.models import DeliveryMan
from .validators import validate_cep, validate_phone_number, validate_cpf, validate_cnpj # <-- Importe aqui
from django.utils import timezone
import random
import string



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, verbose_name='Nome do Produto')
    product_quantity = models.PositiveIntegerField(verbose_name='Quantidade em Estoque')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor do Produto') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['product_name']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.product_name
    
class Client(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, verbose_name='Nome do Cliente')
    contact_phone = models.CharField(max_length=15, verbose_name='Telefone de Contato',validators=[validate_phone_number])
    public_place = models.CharField(max_length=200,verbose_name='Logradouro')
    cep = models.CharField(max_length=9,verbose_name='CEP', validators=[validate_cep])
    city = models.CharField(max_length=100,verbose_name='Município')
    state = models.CharField(max_length=50,verbose_name='Estado')
    property_number = models.CharField(max_length=5,verbose_name='Número do Endereço')
    complement_address = models.CharField(max_length=300,verbose_name='Complemento de Endereço')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['fullname']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.fullname
     
class DeliveryOrder(models.Model):
    class DeliveryStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'Em rota de entrega'
        DELIVERED = 'DELIVERED', 'Entregue'
        CANCELLED = 'CANCELLED', 'Cancelado'

    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Dinheiro'
        CREDIT_CARD = 'CREDIT', 'Cartão de Crédito'
        DEBIT_CARD = 'DEBIT', 'Cartão de Débito'
        PIX = 'PIX', 'PIX'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=20, verbose_name='Código de Pedido', unique=True, blank=True)
    receiver = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='orders', verbose_name='Destinatário')
    delivery_man = models.ForeignKey(DeliveryMan, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries', verbose_name='Entregador')
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='Taxa de Entrega')
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, verbose_name='Forma de Pagamento')
    is_paid = models.BooleanField(default=False, verbose_name='Pago?')
    note = models.TextField(max_length=500, blank=True, verbose_name='Observações')
    delivery_status = models.CharField(max_length=50, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _generate_order_code(self):
        """
        Gera um código único para o pedido no formato AAMMDD-XXXXXX.
        """
        # Formato da data: Ano com 2 dígitos, Mês, Dia
        date_part = timezone.now().strftime('%y%m%d')
        # 6 caracteres aleatórios (letras maiúsculas e dígitos)
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{date_part}-{random_part}"

    def save(self, *args, **kwargs):
        # Verifica se o objeto é novo (ainda não tem uma chave primária)
        if not self.pk:
            # Gera um novo código e verifica se ele já existe,
            # embora a chance de colisão seja extremamente baixa.
            while True:
                code = self._generate_order_code()
                # A validação de unicidade deve considerar todos os pedidos,
                # não apenas os do mesmo usuário, para ser mais segura.
                if not DeliveryOrder.objects.filter(order_code=code).exists():
                    self.order_code = code
                    break
        
        # Chama o método save() original da classe pai
        super().save(*args, **kwargs)


    @property
    def total_price(self):
        """Calcula o preço total do pedido dinamicamente."""
        items_total = sum(item.subtotal for item in self.items.all())
        return items_total + self.delivery_fee

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ordem de Entrega'
        verbose_name_plural = 'Ordens de Entrega'

    def __str__(self):
        return f"Pedido {self.order_code} - {self.receiver.fullname}"

# NOVO MODEL - Essencial para o sistema funcionar
class OrderItem(models.Model):
    order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantidade')
    # É uma boa prática salvar o preço no momento da compra
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Unitário')

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        # Garante que não haja o mesmo produto duas vezes no mesmo pedido
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.product_name}"
