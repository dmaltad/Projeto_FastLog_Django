from django.urls import path
from .views import *

urlpatterns = [
    path('', delivery_men_view, name='entregadores'),
    path('adicionar', new_delivery_man_view, name='adicionar_entregadores'),
    
]
