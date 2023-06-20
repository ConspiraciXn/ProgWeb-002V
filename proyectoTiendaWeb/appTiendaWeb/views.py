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
    productos = Producto.objects.all()
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


# ------------------------------------------------------------
# Carrito de compra.
# ------------------------------------------------------------

def carrito_compra(request):
    return render(request, 'carrito_compra.html')

