# importamos un metodo para el caso de un error
from django.shortcuts import render, redirect, get_object_or_404
from . import models  # llamamos al models
from .forms import ContactForm, ProductForm, CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required


# esta es la forma de llamar los html y agrega funcione spara guardar informacion en una base de datos


def home(request):
    # colocamos una variable para almacenar productos
    productos = models.Product.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/home.html', data)


def galeria(request):
    return render(request, 'app/galeria.html')

# se agrega una variable para poder guardar la informacion en una base de dato y mostrarla


def contacto(request):
    data = {
        'form': ContactForm()
    }

    if request.method == 'POST':
        formulario = ContactForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto guardado"
        else:
            data["form"] = formulario

    return render(request, 'app/contacto.html', data)


# Estes es la funcion para llamar al agregar porducto que se vera en la pagina sin necesidad que entrar al administrador para ver el html igual
@permission_required('app.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductForm()
    }

    if request.method == 'POST':
        formulario = ProductForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto Registrado")
        else:
            data["form"] = formulario

    return render(request, 'app/producto/agregar.html', data)
    # data siempre se envia como tercer parametro


# funsion para ver el listar producto
@permission_required('app.view_producto')
def listar_productos(request):

    productos = models.Product.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 3)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        # este es para darle el numero a la pagina enpity es lo que esta en paginator
        'entity': productos,
        'paginator': paginator,
    }

    return render(request, 'app/producto/listar.html', data)

# se agregar despues del request un id es modificar producto


@permission_required('app.change_producto')
def modificar_producto(request, id):
    # models.Product.objects.get(id=id)
    # se coloca el get_object_or_404 para modificar el producto para mostrar la informacion
    producto = get_object_or_404(models.Product, id=id)

    data = {
        'form': ProductForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductForm(
            data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            # estes es el mensaje que se le colocara para cambiar de pagina
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_producto")
        data["form"] = formulario
    return render(request, 'app/producto/modificar.html', data)


# eliminar producto
@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(models.Product, id=id)
    producto.delete()
    messages.success(request, " Eliminado correctamente")
    return redirect(to="listar_producto")


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(
                username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado Correctamente")
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)
