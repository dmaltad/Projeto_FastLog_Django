from django import forms
from .models import DeliveryMan

class DeliveryManForm(forms.ModelForm):
    class Meta:
        model = DeliveryMan
        fields = '__all__'