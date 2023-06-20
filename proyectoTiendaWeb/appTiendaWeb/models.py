from django.db import models


# Modelos para mi base de datos.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.nombre



class Producto(models.Model):

    nombre = models.CharField(max_length=100, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)
    valor = models.IntegerField(blank=True)
    stock = models.IntegerField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenProductos/')

    def __str__(self):
        return self.nombre

