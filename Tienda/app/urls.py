from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contacto', views.contacto, name='contacto'),
    path('galeria', views.galeria, name='galeria'),


    # estos sson los temples para ver el formulario en la pagina de termomarket se llama asi
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('listar-producto/', views.listar_productos, name='listar_producto'),

    # resive un <id> para poder modificar el producto con el id selecionado
    path('modificar-producto/<id>/',
         views.modificar_producto, name='modificar_producto'),
    path('eliminar-producto/<id>/',
         views.eliminar_producto, name='eliminar_producto'),
    path('registro',
         views.registro, name='registro'),
]
