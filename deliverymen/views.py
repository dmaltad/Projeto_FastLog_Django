from django.shortcuts import render

def delivery_men_view(request):
    return render(request, 'entregadores.html')
