# Proyecto Django — Balderrama López Samuel

Proyecto Django conectado a MySQL en Aiven y desplegado en Render.

## Semana 5 (Unidad 3): CRUD completo con ModelForms
Pantallas propias para crear, listar, editar y eliminar servicios sin entrar a `/admin`:
- `ServicioForm` (ModelForm) en `core/forms.py`, con validación personalizada `clean_precio` (el precio debe ser mayor a 0).
- Vistas `crear_servicio`, `editar_servicio` y `eliminar_servicio` protegidas con `@login_required`; el propietario se asigna con `request.user`.
- Plantillas `base.html`, `servicio_form.html` (crear y editar) y `servicio_confirm_delete.html` (confirmación antes de borrar).
- Mientras llega el login propio (Semana 6), el inicio de sesión usa `/admin/login/`.

## Semana 6 (Unidad 3): registro, login y aislamiento de datos
- Registro con `UserCreationForm`, inicio de sesión con `AuthenticationForm` y cierre de sesión solo por POST.
- Cada usuario ve, edita y elimina únicamente sus propios servicios (`filter(propietario=request.user)` y `get_object_or_404(..., propietario=request.user)`).

## Semana 7 (Unidad 4): pulido funcional y UX
- **Paginación:** `/servicios/` muestra 5 servicios por página con `Paginator` y `get_page()`, que además evita errores con páginas inválidas (`?page=99`, `?page=abc`).
- **Búsqueda:** formulario GET que filtra por título con `titulo__icontains` (sin distinguir mayúsculas); los controles Anterior/Siguiente conservan el parámetro `q`.
- **Estado vacío:** `{% empty %}` muestra un mensaje distinto si el usuario aún no tiene servicios o si la búsqueda no encontró resultados.
- **Accesibilidad y responsividad:** `label` y `aria-label` en el buscador y en los enlaces Editar/Eliminar, `nav` con `aria-label` en la paginación, botones de al menos 44 px de alto y tabla dentro de `overflow-x-auto` para pantallas angostas.
- Sin cambios en el modelo, por lo que no se generaron migraciones nuevas.

### Pruebas en producción
| Prueba | Resultado |
|---|---|
| 9 servicios: página 1 con 5 y página 2 con 4 | ✅ |
| Búsqueda `clases` / `CLASES` → 3 resultados | ✅ |
| Búsqueda `zzzz` → mensaje "No se encontraron servicios" | ✅ |
| `?page=99` → última página, `?page=abc` → página 1 | ✅ |
| Otro usuario no ve los servicios ajenos y recibe 404 al abrir `/servicios/<pk>/editar/` de otro | ✅ |

## Producción
https://u4s7-balderrama-lopez-samuel.onrender.com

- Servicios: https://u4s7-balderrama-lopez-samuel.onrender.com/servicios/
- Panel de administración: https://u4s7-balderrama-lopez-samuel.onrender.com/admin/

## Rutas
| URL | Vista | name |
|---|---|---|
| `/` | `inicio` | `inicio` |
| `/servicios/` | `servicios` | `servicios` |
| `/servicios/nuevo/` | `crear_servicio` | `crear_servicio` |
| `/servicios/<pk>/editar/` | `editar_servicio` | `editar_servicio` |
| `/servicios/<pk>/eliminar/` | `eliminar_servicio` | `eliminar_servicio` |
| `/registro/` | `registro` | `registro` |
| `/login/` | `iniciar_sesion` | `login` |
| `/logout/` | `cerrar_sesion` | `logout` |

## Cómo correrlo localmente
1. Crear y activar un entorno virtual
2. pip install -r requirements.txt
3. Copiar .env.example a .env y completar con credenciales propias de Aiven, un SECRET_KEY y DEBUG=True
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver

## Despliegue en Render
- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command:** `gunicorn miproyecto.wsgi`
- **Variables de entorno:** `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=u4s7-balderrama-lopez-samuel.onrender.com`, `CSRF_TRUSTED_ORIGINS=https://u4s7-balderrama-lopez-samuel.onrender.com`

## Evidencia
- Semana 3 (Django + MySQL en Aiven): capturas de `migrate`, tablas en Aiven y vistas locales en la carpeta [/evidencia](evidencia).
- Semana 4 (modelo Servicio + Render): capturas del panel /admin, /servicios/ en producción y el Web Service en Render en la carpeta [/evidencia/unidad2_Django_OnRender](evidencia/unidad2_Django_OnRender).
