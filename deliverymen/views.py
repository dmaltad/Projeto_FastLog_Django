from django.shortcuts import render, redirect
from .forms import DeliveryManForm
def delivery_men_view(request):
    return render(request, 'entregadores.html')

def new_delivery_man_view(request):
    if request.method == 'POST':
        new_delivery_man = DeliveryManForm(request.POST, request.FILES)
        if new_delivery_man.is_valid():
            new_delivery_man.save()
            return redirect("entregadores")
    else:
        new_delivery_man = DeliveryManForm()
    return render(request, 'adicionar_entregadores.html',)
    