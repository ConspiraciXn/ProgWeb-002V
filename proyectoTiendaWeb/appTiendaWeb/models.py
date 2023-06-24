from django.db import models
from django.contrib.auth.models import User


# Modelos para mi base de datos.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):

    nombre = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, blank=True, default='pendiente')
    descripcion = models.CharField(max_length=200, blank=True)
    valor = models.IntegerField(blank=True)
    stock = models.IntegerField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenProductos/')

    def __str__(self):
        return self.nombre

class CarritoCompra(models.Model):

    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad_productos = models.IntegerField(blank=True)
    total = models.IntegerField(blank=True)

    def __str__(self):
        return "Carrito de " + str(self.comprador.username)
    
class ItemCarrito(models.Model):

    carrito = models.ForeignKey(CarritoCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor_unitario = models.IntegerField(blank=True)
    cantidad = models.IntegerField(blank=True)
    total = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.producto.nombre) + " / " + str(self.carrito)
