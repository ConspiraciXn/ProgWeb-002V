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
    path('aprobacion-productos/', aprobacion_productos, name='aprobacion_productos'),
    path('productos/aprobar/<id_producto>/', aprobar_producto, name='aprobar_producto'),
    path('productos/rechazar/<id_producto>/', rechazar_producto, name='rechazar_producto'),


    # ------------------------------------------------------------
    # Carrito de compra.
    # ------------------------------------------------------------

    path('mi-carrito/', carrito_compra, name='carrito_compra'),
    path('mi-carrito/agregar-prod/<id_producto>/', agregar_producto, name='agregar_producto'),
    path('mi-carrito/aumentar/<id_item>/', aumentar_cantidad, name='aumentar_cantidad'),
    path('mi-carrito/disminuir/<id_item>/', disminuir_cantidad, name='disminuir_cantidad'),
    path('mi-carrito/eliminar/<id_item>/', remover_producto, name='remover_producto'),
    path('mi-carrito/finalizar/<id_carrito>/', finalizar_compra, name='finalizar_compra'),


# Permite servir los estáticos y media.

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
