from django.contrib import admin
from .models import Company
from order.models import *

admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(DeliveryOrder)
admin.site.register(DeliveryMan)

