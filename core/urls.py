from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from deliverymen.views  import delivery_men_view
from login.views import login_view
from order.views  import order_view
from panel.views  import panel_view
from reports.views  import reports_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('entregadores/', delivery_men_view, name='entregadores'),
    path('', login_view, name='login'),
    path('pedidos/', order_view, name='pedidos'),
    path('painel/', panel_view, name='painel'),
    path('relatorios/', reports_view, name='relatorios'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
