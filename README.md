<!-- título del repo: práctica final de la Unidad 4 -->
# U4P3 — Balderrama López Samuel

<!-- sección con la URL pública de Render -->
## Demo en vivo (producción)
<!-- tu dirección real de Render de esta práctica -->
https://u4p3-balderrama-lopez-samuel.onrender.com

- Servicios: https://u4p3-balderrama-lopez-samuel.onrender.com/servicios/
- Categorías: https://u4p3-balderrama-lopez-samuel.onrender.com/categorias/
- Facturas: https://u4p3-balderrama-lopez-samuel.onrender.com/facturas/
- Reportes SQL: https://u4p3-balderrama-lopez-samuel.onrender.com/reportes/
- Panel de administración: https://u4p3-balderrama-lopez-samuel.onrender.com/admin/

<!-- sección que explica el proyecto a quien lo visite -->
## Qué hace este proyecto
<!-- descripción general del sistema -->
Es una vitrina de servicios hecha con Django: cada persona se registra, inicia sesión y administra su propio catálogo de servicios (título, descripción, precio y categoría) desde pantallas propias, sin entrar al panel `/admin`. Puede crear, listar, editar y eliminar sus servicios, con validación en el formulario (el precio debe ser mayor a 0) y confirmación antes de borrar.

En la práctica final u4p3 el CRUD creció a 5 tablas relacionadas: la categoría dejó de ser texto libre y pasó a su propia tabla, y se agregaron facturas con su detalle. Además, la página `/reportes/` ejecuta 6 consultas SQL escritas a mano directamente en MySQL, con su plan `EXPLAIN` y descarga en CSV.

El listado de `/servicios/` está paginado (5 por página) y busca por título o por nombre de categoría. La interfaz está construida con Tailwind CSS y es responsiva. Los datos viven en MySQL (Aiven) y el sitio está publicado en Render con HTTPS y `DEBUG=False`.

<!-- sección con las tecnologías usadas -->
## Stack técnico
<!-- las 4 herramientas del curso -->
Django + MySQL 8 (Aiven) + Tailwind CSS + Render

<!-- sección con el modelo de datos de la u4p3 -->
## Las 5 tablas y sus relaciones
<!-- cada flecha es una llave foránea (FK) -->
| Relación | Se lee así | Al borrar |
|---|---|---|
| `Servicio → User` | Un usuario tiene muchos servicios | `CASCADE`: se borran sus servicios |
| `Servicio → Categoria` | Una categoría agrupa muchos servicios | `PROTECT`: no se borra una categoría con servicios |
| `Factura → User` | Un usuario emite muchas facturas | `CASCADE` |
| `DetalleFactura → Factura` | Una factura tiene muchos renglones | `CASCADE`: se van sus renglones |
| `DetalleFactura → Servicio` | Un servicio aparece en muchos renglones | `PROTECT`: no se borra un servicio ya facturado |

<!-- cómo se pasó la categoría de texto a tabla sin perder datos -->
La categoría de texto se convirtió en llave foránea sin perder datos en 3 migraciones:
1. `0002`: crea la tabla `Categoria` y una FK temporal `categoria_ref`.
2. `0003`: migración de datos (`RunPython`) que copia el texto de cada servicio a la tabla nueva, sin duplicar mayúsculas/minúsculas.
3. `0004`: borra la columna de texto (`RemoveField`) y renombra `categoria_ref` a `categoria` (`RenameField`).

La migración `0005` agrega `Factura`, `DetalleFactura` y dos índices compuestos: `servicio_prop_precio_idx` (propietario, precio) y `factura_usuario_fecha_idx` (usuario, fecha).

<!-- sección con las 6 consultas de reportes.py -->
## Reportes SQL
<!-- todas usan %(uid)s como parámetro, nunca texto concatenado -->
| # | Reporte | Técnica SQL |
|---|---|---|
| 1 | Ingresos por categoría | `SUM()` + `GROUP BY` |
| 2 | Servicios por categoría | `COUNT()` + `GROUP BY` + `LEFT JOIN` |
| 3 | Servicio más barato y más caro (con empates) | `MIN()` + `MAX()` en subconsulta |
| 4 | Servicios que nunca se han facturado | `LEFT JOIN` + `IS NULL` (anti-join) |
| 5 | Clientes que gastan más que el promedio | `HAVING` + subconsulta con `AVG()` |
| 6 | Ranking de servicios más vendidos por categoría | `WITH` (CTE) + `RANK() OVER (PARTITION BY …)` |

Las consultas viven en `core/reportes.py` y se ejecutan con `connection.cursor()`, pasando el id del usuario como parámetro `%(uid)s` para evitar inyección SQL. Una sola plantilla (`reporte.html`) dibuja cualquier resultado porque toma los nombres de columna de `cursor.description`.

<!-- sección con la prueba de seguridad de la Semana 6 -->
## Cómo se prueba el aislamiento por usuario
<!-- explicación de la Semana 6, ampliada con facturas y reportes -->
Cada servicio tiene un `propietario` y cada factura un `usuario` (`ForeignKey` a `User`), que se asignan con `request.user` al crearlos. Las vistas están protegidas con `@login_required` y solo trabajan con los datos del usuario en sesión:

- Los listados usan `filter(propietario=request.user)` y `filter(usuario=request.user)`.
- Editar, eliminar y ver el detalle de una factura usan `get_object_or_404(..., pk=pk, propietario/usuario=request.user)`, así que un registro ajeno responde 404.
- En una factura nueva, la lista de servicios de cada renglón solo trae los servicios propios, y el precio unitario lo copia la vista desde el servicio (no viene del formulario).
- Los 6 reportes filtran por `%(uid)s` = `request.user.id`.

Para probarlo:
1. Inicia sesión con el usuario A y crea un servicio y una factura; anota sus números en la URL.
2. Cierra sesión, regístrate como usuario B y entra a `/servicios/`, `/facturas/` y `/reportes/`: no aparece nada de A.
3. Con B, abre a mano `/servicios/<pk>/editar/` y `/facturas/<pk>/` de A: ambas responden 404.
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
<!-- Práctica final de la Unidad 4 -->
- Práctica final u4p3: categorías como tabla, facturas con detalle, 6 reportes SQL escritos a mano e índices revisados con `EXPLAIN`

## Rutas
| URL | Vista | name |
|---|---|---|
| `/` | `inicio` | `inicio` |
| `/servicios/` | `servicios` | `servicios` |
| `/servicios/nuevo/` | `crear_servicio` | `crear_servicio` |
| `/servicios/<pk>/editar/` | `editar_servicio` | `editar_servicio` |
| `/servicios/<pk>/eliminar/` | `eliminar_servicio` | `eliminar_servicio` |
| `/categorias/` | `categorias` | `categorias` |
| `/categorias/<pk>/editar/` | `editar_categoria` | `editar_categoria` |
| `/categorias/<pk>/eliminar/` | `eliminar_categoria` (solo POST) | `eliminar_categoria` |
| `/facturas/` | `facturas` | `facturas` |
| `/facturas/nueva/` | `crear_factura` | `crear_factura` |
| `/facturas/<pk>/` | `detalle_factura` | `detalle_factura` |
| `/reportes/` | `reportes` | `reportes` |
| `/reportes/<clave>/` | `reporte` (`?plan=1` = EXPLAIN, `?formato=csv` = descarga) | `reporte` |
| `/registro/` | `registro` | `registro` |
| `/login/` | `iniciar_sesion` | `login` |
| `/logout/` | `cerrar_sesion` (solo POST) | `logout` |

## Cómo correrlo localmente
1. Crear y activar un entorno virtual
2. pip install -r requirements.txt
3. Copiar .env.example a .env y completar con credenciales propias de Aiven, un SECRET_KEY y DEBUG=True
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py cargar_demo tu_usuario (opcional: carga categorías, servicios y facturas de prueba para ver los reportes)
7. python manage.py runserver

## Despliegue en Render
- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command:** `gunicorn miproyecto.wsgi`
- **Variables de entorno:** `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=u4p3-balderrama-lopez-samuel.onrender.com`, `CSRF_TRUSTED_ORIGINS=https://u4p3-balderrama-lopez-samuel.onrender.com`

## Evidencia
- Semana 3 (Django + MySQL en Aiven): capturas de `migrate`, tablas en Aiven y vistas locales en la carpeta [/evidencia](evidencia).
- Semana 4 (modelo Servicio + Render): capturas del panel /admin, /servicios/ en producción y el Web Service en Render en la carpeta [/evidencia/unidad2_Django_OnRender](evidencia/unidad2_Django_OnRender).
- Práctica final u4p3: capturas de cada paso en la carpeta [/evidencias](evidencias) y minutos del video en `EVIDENCIAS.md`.
