# ------------------------------------------------------------
# Librerías importadas.
# ------------------------------------------------------------
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# ------------------------------------------------------------
# Vistas principales
# ------------------------------------------------------------

def inicio(request):

    # Busca todos los productos de la base de datos.
    productos = Producto.objects.filter(estado = 'aprobado')
    categorias = Categoria.objects.all()

    contexto = {
        "productos": productos,
        "categorias": categorias
    }
    return render(request, "inicio.html", contexto)



# ------------------------------------------------------------
# Autenticación y sesiones.
# ------------------------------------------------------------

def inicio_sesion(request):

    # Si existe una consulta tipo POST.
    if request.method == 'POST':

        # Obtener datos del POST.
        usuario = request.POST.get('formUsuario')
        contrasena = request.POST.get('formContrasena')

        # Crear objeto autenticacion.
        auth = authenticate(request, username=usuario, password=contrasena)

        # Validar autenticacion.
        if auth is not None:

            # Iniciar sesion y redireccionar a home.
            login(request, auth)
            return redirect(to='/')

        
    # renderiza el template inicio_sesion.html
    return render(request, "inicio_sesion.html")

def cerrar_sesion(request):

    logout(request)

    return redirect('/ingreso/')

def registro_usuario(request):

    # Si existe una consulta tipo POST.
    if request.method == 'POST':

        # Obtener datos del formulario.
        nombre = request.POST.get("formNombre")
        apellido = request.POST.get("formApellido")
        usuario = request.POST.get("formUsuario")
        email = request.POST.get("formEmail")
        contrasena = request.POST.get("formContrasena")

        # Crear usuario de Django.
        nuevo_usuario = User.objects.create_user(username=usuario, email=email, password=contrasena)

        nuevo_usuario.first_name = nombre
        nuevo_usuario.last_name = apellido
        nuevo_usuario.save()

        # Redireccionar al login.
        return redirect('/ingreso/')

    return render(request, 'registro_usuarios.html')



# ------------------------------------------------------------
# CRUD de productos y categorias.
# ------------------------------------------------------------

@login_required(login_url='/ingreso/')
def registro_producto(request):

    # Traer todas las categorias de la BD.
    categorias = Categoria.objects.all()

    # Si existe carga de formulario.
    if request.method == "POST":

        # Obtener datos del formulario.
        nombre = request.POST.get("formNombre")
        descripcion = request.POST.get("formDescripcion")
        valor = request.POST.get("formValor")
        stock = request.POST.get("formStock")
        
        # Obtener imagen u otro tipo de archivo desde el form.
        imagen = request.FILES['formImagen']

        # Obtener ID de categoria desde el form.
        id_categoria = request.POST.get("formCategoria")

        # Buscar categoría seleccionada.
        categoria = Categoria.objects.get(id = id_categoria)

        # Crear objeto producto.
        producto_nuevo = Producto()
        producto_nuevo.nombre = nombre
        producto_nuevo.descripcion = descripcion
        producto_nuevo.valor = valor
        producto_nuevo.stock = stock
        producto_nuevo.categoria = categoria
        producto_nuevo.imagen = imagen
        producto_nuevo.save()

        contexto = {
            "mensaje": "¡Producto registrado exitosamente!",
            "categorias": categorias
        }
        return render(request, 'registro_productos.html', contexto)

    
    contexto = {
        "categorias": categorias
    }
    return render(request, 'registro_productos.html', contexto)

def categorias(request, id_categoria):

    categoria = Categoria.objects.get(id = id_categoria)
    productos = Producto.objects.filter(categoria = categoria)

    contexto = {
        "productos": productos,
        "categoria": categoria
    }
    return render(request, 'categorias.html', contexto)

def aprobacion_productos(request):

    productos = Producto.objects.all()

    contexto = {
        "productos": productos
    }
    return render(request, 'aprobacion_productos.html', contexto)

def aprobar_producto(request, id_producto):

    producto = Producto.objects.get(id = id_producto)
    producto.estado = 'aprobado'
    producto.save()
    
    return redirect('/aprobacion-productos/')

def rechazar_producto(request, id_producto):

    producto = Producto.objects.get(id = id_producto)
    producto.estado = 'rechazado'
    producto.save()
    
    return redirect('/aprobacion-productos/')


# ------------------------------------------------------------
# Carrito de compra.
# ------------------------------------------------------------

def carrito_compra(request):

    usuario = request.user

    # Validar si existe un carrito de compra para el usuario.
    existencia_carrito = CarritoCompra.objects.filter(comprador = usuario)
    
    # Si existe un carrito de compra.
    if len(existencia_carrito) > 0:
        carrito = CarritoCompra.objects.get(comprador = usuario)
        productos = ItemCarrito.objects.filter(carrito = carrito)

        contexto = {
            "carrito": carrito,
            "productos": productos
        }
        return render(request, 'carrito_compra.html', contexto)
    
    # Si no existe un carrito de compra.
    else:
        return render(request, 'carrito_compra.html')

def agregar_producto(request, id_producto):

    usuario = request.user
    producto = Producto.objects.get(id = id_producto)

    # Validar si existe un carrito de compra.
    existencia_carrito = CarritoCompra.objects.filter(comprador = usuario)

    # Si existe de carrito de compra.
    if len(existencia_carrito) > 0:

        carrito = CarritoCompra.objects.get(comprador = usuario)
        carrito.cantidad_productos += 1
        carrito.total += producto.valor
        carrito.save()

        # Validar si ya existe el producto en el carrito.
        existencia_producto = ItemCarrito.objects.filter(carrito = carrito).filter(producto = producto)

        # Si el producto ya existe en el carrito.
        if len(existencia_producto) > 0:

            item = ItemCarrito.objects.get(producto = producto)
            item.cantidad += 1
            item.total += producto.valor
            item.save()

        # Si el producto no existe en el carrito, lo creamos.
        else:

            item = ItemCarrito()
            item.carrito = carrito
            item.producto = producto
            item.valor_unitario = producto.valor
            item.cantidad = 1
            item.total = producto.valor
            item.save()

    # Si no existe carrito de compra.
    else:

        carrito = CarritoCompra()
        carrito.comprador = usuario
        carrito.cantidad_productos = 1
        carrito.total = producto.valor
        carrito.save()

        item = ItemCarrito()
        item.carrito = carrito
        item.producto = producto
        item.valor_unitario = producto.valor
        item.cantidad = 1
        item.total = producto.valor
        item.save() 


    # Misma funcionalidad del inicio.
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    contexto = {
        "productos": productos,
        "categorias": categorias,
        "alerta_producto" : True
    }
    return render(request, "inicio.html", contexto)

def aumentar_cantidad(request, id_item):

    # Obtener item de carrito.
    item = ItemCarrito.objects.get(id = id_item)

    # Aumentar cantidad y valor total.
    item.cantidad += 1
    item.total += item.valor_unitario
    item.save()

    # Actualizar carrito de compra.
    carrito = item.carrito
    carrito.cantidad_productos += 1
    carrito.total += item.valor_unitario
    carrito.save()

    return redirect('/mi-carrito/')

def disminuir_cantidad(request, id_item):

    # Obtener item de carrito.
    item = ItemCarrito.objects.get(id = id_item)

    # Disminuir cantidad y valor total.
    item.cantidad -= 1
    item.total -= item.valor_unitario
    item.save()

    # Actualizar carrito de compra.
    carrito = item.carrito
    carrito.cantidad_productos -= 1
    carrito.total -= item.valor_unitario
    carrito.save()

    return redirect('/mi-carrito/')

def remover_producto(request, id_item):

    # Obtener item de carrito.
    item = ItemCarrito.objects.get(id = id_item)

    # Actualizar carrito de compra.
    carrito = item.carrito
    carrito.cantidad_productos -= 1
    carrito.total -= item.valor_unitario
    carrito.save()

    # Eliminar item de carrito.
    item.delete()

    return redirect('/mi-carrito/')

def finalizar_compra(request, id_carrito):

    # Obtener carrito.
    carrito = CarritoCompra.objects.get(id = id_carrito)
    carrito.delete()

    return redirect('/mi-carrito/')

