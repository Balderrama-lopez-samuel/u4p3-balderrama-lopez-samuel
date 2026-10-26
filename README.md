<!-- título del repo: cambia por tus nombres reales -->
# U4S8 — Balderrama López Samuel

<!-- sección con la URL pública de Render -->
## Demo en vivo (producción)
<!-- tu dirección real de Render de esta práctica -->
https://u4s8-balderrama-lopez-samuel.onrender.com

- Servicios: https://u4s8-balderrama-lopez-samuel.onrender.com/servicios/
- Panel de administración: https://u4s8-balderrama-lopez-samuel.onrender.com/admin/

<!-- sección que explica el proyecto a quien lo visite -->
## Qué hace este proyecto
<!-- reemplaza el texto entre corchetes por tu descripción -->
Es una vitrina de servicios hecha con Django: cada persona se registra, inicia sesión y administra su propio catálogo de servicios (título, descripción, precio y categoría) desde pantallas propias, sin entrar al panel `/admin`. Puede crear, listar, editar y eliminar sus servicios, con validación en el formulario (el precio debe ser mayor a 0) y confirmación antes de borrar.

El listado de `/servicios/` está paginado (5 por página), tiene un buscador por título que no distingue mayúsculas y muestra mensajes claros cuando todavía no hay servicios o la búsqueda no encuentra resultados. La interfaz está construida con Tailwind CSS, es responsiva y cuida la accesibilidad (etiquetas, `aria-label` y botones de al menos 44 px). Los datos viven en MySQL (Aiven) y el sitio está publicado en Render con HTTPS y `DEBUG=False`.

<!-- sección con las tecnologías usadas -->
## Stack técnico
<!-- las 4 herramientas del curso -->
Django + MySQL (Aiven) + Tailwind CSS + Render

<!-- sección con la prueba de seguridad de la Semana 6 -->
## Cómo se prueba el aislamiento por usuario
<!-- pega aquí la explicación que escribiste en el README de la Semana 6 -->
Cada servicio tiene un `propietario` (`ForeignKey` a `User`) que se asigna con `request.user` al crearlo. Las vistas están protegidas con `@login_required` y solo trabajan con los servicios del usuario en sesión:

- El listado usa `Servicio.objects.filter(propietario=request.user)`.
- Editar y eliminar usan `get_object_or_404(Servicio, pk=pk, propietario=request.user)`, así que un servicio ajeno responde 404.

Para probarlo:
1. Inicia sesión con el usuario A y crea un servicio; anota su número en la URL de editar (`/servicios/<pk>/editar/`).
2. Cierra sesión, regístrate como usuario B y entra a `/servicios/`: el servicio de A no aparece.
3. Con B, abre a mano `/servicios/<pk>/editar/` y `/servicios/<pk>/eliminar/` del servicio de A: ambas responden 404.
4. Sin sesión, entra a `/servicios/`: redirige a `/login/`.

<!-- sección con el recorrido del curso -->
## Historial de unidades
<!-- Unidad 1 -->
- Unidad 1: portafolio estático con HTML5 + Tailwind
<!-- Unidad 2 -->
- Unidad 2: modelo Servicio migrado a MySQL, deploy dinámico en Render
<!-- Unidad 3 -->
- Unidad 3: CRUD completo con ModelForms + autenticación y sesiones
<!-- Unidad 4 -->
- Unidad 4: paginación, búsqueda, UI review y defensa final

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
- **Variables de entorno:** `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=u4s8-balderrama-lopez-samuel.onrender.com`, `CSRF_TRUSTED_ORIGINS=https://u4s8-balderrama-lopez-samuel.onrender.com`

## Evidencia
- Semana 3 (Django + MySQL en Aiven): capturas de `migrate`, tablas en Aiven y vistas locales en la carpeta [/evidencia](evidencia).
- Semana 4 (modelo Servicio + Render): capturas del panel /admin, /servicios/ en producción y el Web Service en Render en la carpeta [/evidencia/unidad2_Django_OnRender](evidencia/unidad2_Django_OnRender).
