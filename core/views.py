# render: función que combina una plantilla con datos y arma la respuesta HTTP
# redirect: manda al navegador a otra URL · get_object_or_404: busca un registro o responde 404
from django.shortcuts import render, redirect, get_object_or_404
# login_required: decorador que exige sesión iniciada, si no manda a LOGIN_URL
from django.contrib.auth.decorators import login_required
# messages: mensajes "flash" que se muestran una sola vez en la siguiente página
from django.contrib import messages
# login/logout: abren y cierran la sesión del usuario
from django.contrib.auth import login, logout
# UserCreationForm/AuthenticationForm: formularios de registro y login que Django ya trae
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# connection: objeto de Django que expone la configuración de la base de datos activa
from django.db import connection
# Paginator: parte una lista larga en páginas de N elementos
from django.core.paginator import Paginator
from .models import Servicio
from .forms import ServicioForm

# def: toda vista es una función que recibe "request" (la petición del navegador)
def inicio(request):
    # settings_dict: diccionario interno con ENGINE, HOST, NAME, etc. de la conexión activa
    info_bd = connection.settings_dict
    # contexto: los datos que la plantilla va a poder usar con {{ variable }}
    contexto = {
        'motor': info_bd['ENGINE'],
        'host': info_bd['HOST'],
    }
    # render: junta el template "core/inicio.html" con el contexto y devuelve el HTML final
    return render(request, 'core/inicio.html', contexto)

# servicios: el listado (la "R" de CRUD)
@login_required
def servicios(request):
    # filter(propietario=request.user): solo los servicios del usuario logueado
    # order_by: el Paginator necesita un orden fijo (los más nuevos primero)
    lista_servicios = Servicio.objects.filter(propietario=request.user).order_by('-creado_en')
    # q: lo que el usuario escribió en el buscador (?q=...), sin espacios sobrantes
    q = request.GET.get('q', '').strip()
    if q:
        # titulo__icontains: el título contiene el texto, sin importar mayúsculas
        lista_servicios = lista_servicios.filter(titulo__icontains=q)
    # Paginator(lista, 5): páginas de 5 servicios
    paginador = Paginator(lista_servicios, 5)
    # get_page: si ?page no existe o es inválido (ej. 99), devuelve una página válida
    pagina = paginador.get_page(request.GET.get('page'))
    contexto = {'servicios': pagina, 'q': q}
    return render(request, 'core/servicios.html', contexto)

# crear_servicio: la "C" de CRUD
@login_required
def crear_servicio(request):
    # POST: el usuario envió el formulario
    if request.method == 'POST':
        # request.POST: los datos que escribió el usuario
        form = ServicioForm(request.POST)
        # is_valid(): revisa tipos, campos obligatorios y clean_precio
        if form.is_valid():
            # commit=False: arma el objeto pero todavía no lo guarda en MySQL
            servicio = form.save(commit=False)
            # propietario no está en el formulario, se lo asignamos al usuario logueado
            servicio.propietario = request.user
            servicio.save()
            # redirect: después de un POST exitoso se redirige para no reenviar al recargar
            return redirect('servicios')
    # GET: el usuario solo abrió la página, se muestra el formulario vacío
    else:
        form = ServicioForm()
    # si el POST no fue válido, se vuelve a pintar el form con sus errores
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Nuevo servicio'})

# editar_servicio: la "U" de CRUD · pk: el id que llega desde la URL
@login_required
def editar_servicio(request, pk):
    # dos condiciones: el id Y que el dueño sea el usuario actual; si es ajeno → 404
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    if request.method == 'POST':
        # instance=servicio: actualiza ese registro en vez de crear uno nuevo
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('servicios')
    else:
        # instance=servicio: el formulario aparece rellenado con los datos actuales
        form = ServicioForm(instance=servicio)
    # reutiliza la misma plantilla que crear_servicio
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Editar servicio'})

# eliminar_servicio: la "D" de CRUD
@login_required
def eliminar_servicio(request, pk):
    # mismo filtro que en editar: solo el dueño puede borrar su servicio
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    # solo se borra con POST (al confirmar), nunca con solo abrir el enlace
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicios')
    # GET: muestra la página de confirmación
    return render(request, 'core/servicio_confirm_delete.html', {'servicio': servicio})

# registro: crea un usuario nuevo (la contraseña se guarda con hash, no en texto plano)
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # login: deja al usuario con sesión iniciada justo después de registrarse
            login(request, usuario)
            messages.success(request, f'Cuenta creada. Bienvenido, {usuario.username}.')
            return redirect('servicios')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

# iniciar_sesion: valida usuario y contraseña con AuthenticationForm
def iniciar_sesion(request):
    if request.method == 'POST':
        # AuthenticationForm recibe request como primer argumento y los datos en data=
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # get_user(): el usuario que ya pasó la validación
            login(request, form.get_user())
            messages.success(request, 'Sesión iniciada.')
            return redirect('servicios')
    else:
        form = AuthenticationForm(request)
    return render(request, 'core/login.html', {'form': form})

# cerrar_sesion: solo con POST, para que un simple enlace no te saque de la sesión
def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Cerraste sesión correctamente.')
    return redirect('login')
