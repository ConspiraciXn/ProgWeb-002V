# ------------------------------------------------------------
# Librerías importadas.
# ------------------------------------------------------------

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from appTiendaWeb.views import *



# ------------------------------------------------------------
# Patrón o lista de URLS.
# ------------------------------------------------------------

urlpatterns = [

    # ------------------------------------------------------------
    # Zona de administración.
    # ------------------------------------------------------------

    path('admin/', admin.site.urls),


    # ------------------------------------------------------------
    # Vistas principales.
    # ------------------------------------------------------------

    path('', inicio, name='inicio'),    # home.


    # ------------------------------------------------------------
    # Sistema de autenticación y sesiones.
    # ------------------------------------------------------------

    path('ingreso/', inicio_sesion, name='inicio_sesion'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('registro/', registro_usuario, name='registro_usuario'),


    # ------------------------------------------------------------
    # CRUD de productos y categorias.
    # ------------------------------------------------------------

    path('productos/registrar/', registro_producto, name='registro_producto'),
    path('categorias/<id_categoria>/', categorias, name='categorias'),


    # ------------------------------------------------------------
    # Carrito de compra.
    # ------------------------------------------------------------

    path('mi-carrito/', carrito_compra, name='carrito_compra'),


# Permite servir los estáticos y media.

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
