# Este archivo se encarga de mostrar las páginas HTML al usuario
# Cuando escribes una dirección en el navegador, este archivo decide qué HTML enviarte.

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Creamos un "Router", que es como un grupo de rutas para organizar mejor el código
route = APIRouter()

# Configuramos dónde están los archivos HTML (los "templates")
# Buscamos la carpeta 'frontend/templates' dentro del proyecto
dir_raiz = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=dir_raiz / "frontend" / "templates")

# Ruta para el login (Inicio)
# Cuando entras a la raíz del sitio "/"
@route.get("/", tags=["maquinas"])
def plantilla_login(request: Request):
    # Devuelve el archivo index_session.html
    return templates.TemplateResponse(
        "index_session.html",
        {"request": request}
    )

# ruta para la pagina principal
@route.get("/home", tags=["maquinas"])
def plantilla_ventana1(request: Request):
    return templates.TemplateResponse(
        "index_ventana1.html",
        {"request": request}
    )

# ruta para ver la lista de maquinas
@route.get("/home/maquinas", tags=["maquinas"])
def plantilla_ventana2(request: Request):
    return templates.TemplateResponse(
        "index_ventana2.html",
        {"request": request}
    )

# ruta para el formulario de agregar maquina
@route.get("/home/maquinas/formulario", tags=["maquinas"])
def formulario_maquina(request: Request):
    return templates.TemplateResponse(
        "index_formulario1.html",
        {"request": request}
    )

# ruta para el formulario de mantenimiento
@route.get("/home/maquinas/formulario/mantenimiento", tags=["maquinas"])
def formulario_mantenimiento(request: Request):
    return templates.TemplateResponse(
        "index_formulario2.html",
        {"request": request}
    )

# ruta para ver reportes
@route.get("/home/maquinas/reporte", tags=["maquinas"])
def plantilla_ventana3(request: Request):
    return templates.TemplateResponse(
        "index_ventana3.html",
        {"request": request}
    )

# ruta para el historial de cambios
@route.get("/home/maquinas/historial")
def ver_historial(request: Request):
    return templates.TemplateResponse("index_historial.html", {"request": request})

# ruta para el registro de nuevos usuarios
# Funciona tanto con /registro como con /register
@route.get("/registro", tags=["maquinas"])
@route.get("/register", tags=["maquinas"])
def plantilla_registro(request: Request):
    return templates.TemplateResponse(
        "index_register.html",
        {"request": request}
    )
