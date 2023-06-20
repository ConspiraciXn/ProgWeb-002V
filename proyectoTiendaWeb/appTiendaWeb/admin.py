from django.contrib import admin
from .models import *


# Registro de modelos de BD en sitio de administracion.
admin.site.register(Categoria)
admin.site.register(Producto)