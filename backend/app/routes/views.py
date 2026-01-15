from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

route = APIRouter()

# Subimos los niveles necesarios para llegar a la raíz del proyecto y luego a frontend/templates
dir_raiz = Path(__file__).resolve().parents[3] 
templates = Jinja2Templates(directory=dir_raiz / "frontend" / "templates")

#Rutas para paginas renderizadas
@route.get("/", tags=["maquinas"])
def plantilla_login(request: Request):
    return templates.TemplateResponse(
        "index_session.html",
        {"request": request}
    )
@route.get("/home", tags=["maquinas"])
def plantilla_ventana1(request: Request):
    return templates.TemplateResponse(
        "index_ventana1.html",
        {"request": request}
    )
@route.get("/home/maquinas", tags=["maquinas"])
def plantilla_ventana2(request: Request):
    return templates.TemplateResponse(
        "index_ventana2.html",
        {"request": request}
    )
@route.get("/home/maquinas/formulario", tags=["maquinas"])
def formulario_maquina(request: Request):
    return templates.TemplateResponse(
        "index_formulario1.html",
        {"request": request}
    )
@route.get("/home/maquinas/formulario/mantenimiento", tags=["maquinas"])
def formulario_mantenimiento(request: Request):
    return templates.TemplateResponse(
        "index_formulario2.html",
        {"request": request}
    )
@route.get("/home/maquinas/reporte", tags=["maquinas"])
def plantilla_ventana3(request: Request):
    return templates.TemplateResponse(
        "index_ventana3.html",
        {"request": request}
    )
@route.get("/home/maquinas/historial")
def ver_historial(request: Request):
    return templates.TemplateResponse("index_historial.html", {"request": request})
