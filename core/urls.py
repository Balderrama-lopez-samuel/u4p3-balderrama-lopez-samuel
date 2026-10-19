# path: función para definir una ruta individual
from django.urls import path
# views: el archivo de vistas, en la misma carpeta
from . import views

# urlpatterns: lista de rutas que esta app entiende
urlpatterns = [
    # '': la URL vacía (la raíz de esta app) · views.inicio: la función que la atiende
    # name='inicio': un alias interno para referirse a esta ruta sin escribir la URL a mano
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('servicios/nuevo/', views.crear_servicio, name='crear_servicio'),
    # <int:pk>: captura un número de la URL y se lo pasa a la vista como pk
    path('servicios/<int:pk>/editar/', views.editar_servicio, name='editar_servicio'),
    path('servicios/<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),
    # rutas de autenticación (Semana 6)
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]