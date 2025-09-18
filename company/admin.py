from django.contrib import admin
from .models import Company
from order.models import DeliveryMan, Product, Client, DeliveryOrder, OrderItem

# -----------------------------------------------------------------------------
# Configurações para Models Auxiliares
# -----------------------------------------------------------------------------

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Configuração da visualização de Empresas no Admin.
    """
    list_display = ('company_name', 'user', 'cnpj', 'city', 'state')
    search_fields = ('company_name', 'cnpj', 'user__username')
    list_filter = ('state', 'city')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DeliveryMan)
class DeliveryManAdmin(admin.ModelAdmin):
    """
    Configuração da visualização de Entregadores no Admin.
    """
    list_display = ('fullname', 'user', 'contact_phone', 'plate', 'is_active')
    search_fields = ('fullname', 'cpf', 'plate', 'user__username')
    list_filter = ('is_active', 'user')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuração da visualização de Produtos no Admin.
    """
    list_display = ('product_name', 'user', 'product_price', 'product_quantity')
    search_fields = ('product_name', 'user__username')
    list_filter = ('user',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Configuração da visualização de Clientes no Admin.
    """
    list_display = ('fullname', 'user', 'contact_phone', 'city')
    search_fields = ('fullname', 'contact_phone', 'user__username')
    list_filter = ('city', 'state', 'user')
    readonly_fields = ('created_at', 'updated_at')

# -----------------------------------------------------------------------------
# Configuração para Ordem de Entrega (com Itens de Pedido inline)
# -----------------------------------------------------------------------------

class OrderItemInline(admin.TabularInline):
    """
    Permite adicionar e editar Itens de Pedido diretamente na tela da Ordem de Entrega.
    'TabularInline' oferece uma visualização mais compacta em formato de tabela.
    """
    model = OrderItem
    extra = 1  # Quantidade de formulários extras para novos itens
    autocomplete_fields = ['product'] # Melhora a busca de produtos se houver muitos
    
    # É uma boa prática preencher o preço automaticamente, mas para um admin simples,
    # deixamos editável. Em um sistema mais complexo, isso seria preenchido via JavaScript.
    fields = ('product', 'quantity', 'unit_price')

@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    """
    Configuração avançada da visualização de Ordens de Entrega.
    """
    list_display = (
        'order_code',
        'receiver',
        'delivery_man',
        'delivery_status',
        'is_paid',
        'created_at',
        'total_price' # Mostra o valor calculado pela @property
    )
    list_filter = ('delivery_status', 'is_paid', 'user', 'created_at')
    search_fields = ('order_code', 'receiver__fullname', 'delivery_man__fullname')
    list_per_page = 20
    
    # Campos que não devem ser editados diretamente no admin
    readonly_fields = ('order_code', 'total_price', 'created_at', 'updated_at')
    
    # Permite adicionar os itens do pedido na mesma tela
    inlines = [OrderItemInline]
    
    # Organiza os campos em seções para melhor usabilidade
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('user', 'order_code', 'receiver')
        }),
        ('Detalhes da Entrega', {
            'fields': ('delivery_man', 'delivery_status', 'delivery_fee')
        }),
        ('Pagamento', {
            'fields': ('payment_method', 'is_paid', 'total_price')
        }),
        ('Datas de Controle', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Observações', {
            'fields': ('note',)
        }),
    )
    
    # Para o campo 'receiver' funcionar bem com muitos clientes
    autocomplete_fields = ['receiver', 'delivery_man', 'user']

# Se você não precisar de uma visualização customizada para OrderItem,
# não é necessário registrá-lo separadamente, pois ele já é gerenciável
# através da DeliveryOrderAdmin com o inline.
# admin.site.register(OrderItem)