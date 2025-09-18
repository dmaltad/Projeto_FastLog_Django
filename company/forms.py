from django import forms
from order.models import DeliveryMan, Product, Client, DeliveryOrder, OrderItem
# -----------------------------------------------------------------------------
# 1. Formulário para Cadastro de Entregadores
# -----------------------------------------------------------------------------

class DeliveryManForm(forms.ModelForm):
    class Meta:
        model = DeliveryMan
        # Incluímos todos os campos que o usuário deve preencher.
        # O campo 'user' será atribuído automaticamente na view.
        fields = [
            'fullname', 'contact_phone', 'cpf', 'plate', 'profile_photo',
            'public_place', 'cep', 'city', 'state', 'property_number', 
            'complement_address'
        ]

    def __init__(self, *args, **kwargs):
        """
        Sobrescreve o __init__ para adicionar classes CSS e placeholders,
        facilitando a estilização no front-end (ex: com Bootstrap).
        """
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'fullname': 'Nome completo do entregador',
            'contact_phone': '(DD) 99999-9999',
            'cpf': '000.000.000-00',
            'plate': 'ABC1D23',
            'public_place': 'Ex: Rua das Flores',
            'cep': '00000-000',
            'city': 'Nome da cidade',
            'state': 'UF',
            'property_number': 'Nº',
            'complement_address': 'Ex: Apto 101, Bloco B',
        }

        for field_name, placeholder_text in placeholders.items():
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholder_text
            })
            
        # Para o campo de foto, não usamos placeholder
        self.fields['profile_photo'].widget.attrs.update({'class': 'form-control-file'})


# -----------------------------------------------------------------------------
# 2. Formulário para Cadastro de Pedidos (e seus itens)
# -----------------------------------------------------------------------------

class DeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = DeliveryOrder
        # Campos que serão preenchidos pelo usuário da empresa.
        # 'user', 'order_code', 'total_price' e 'delivery_status' são excluídos
        # pois serão gerenciados pelo sistema.
        fields = [
            'receiver', 'delivery_man', 'delivery_fee', 'payment_method',
            'is_paid', 'note'
        ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, user, *args, **kwargs):
        """
        O __init__ customizado é ESSENCIAL para a multi-tenancy.
        Ele recebe o 'user' logado para filtrar os dropdowns.
        """
        super().__init__(*args, **kwargs)

        # Filtra o campo 'Destinatário' (receiver) para mostrar apenas os clientes
        # cadastrados pela empresa (user) que está logada.
        self.fields['receiver'].queryset = Client.objects.filter(user=user)

        # Filtra o campo 'Entregador' (delivery_man) para mostrar apenas os entregadores
        # ativos e cadastrados pela empresa (user) logada.
        self.fields['delivery_man'].queryset = DeliveryMan.objects.filter(user=user, is_active=True)
        
        # Adiciona classes CSS para estilização
        for field_name in self.fields:
            if field_name != 'is_paid': # O checkbox já foi estilizado no widget
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control'
                })


# --- Formulário para os Itens do Pedido (para usar com Formsets) ---

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, user, *args, **kwargs):
        """
        Também filtramos os produtos para garantir que a empresa
        só possa selecionar os seus próprios produtos.
        """
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(user=user)
        
        # Adiciona classes CSS para estilização
        self.fields['product'].widget.attrs.update({'class': 'form-control product-selector'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control quantity-input', 'min': '1'})