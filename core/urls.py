from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from login.views import login_view, logout_view
from order.views  import order_view
from panel.views  import painel_view
from reports.views  import reports_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('painel/', painel_view, name='painel'),
    path('entregadores/',include('deliverymen.urls')),
    path('pedidos/', order_view, name='pedidos'),
    path('relatorios/', reports_view, name='relatorios'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
