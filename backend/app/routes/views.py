from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles

route = APIRouter()

dir = Path(__file__).resolve().parents[3]
route.mount(
    "/static",
    StaticFiles(directory=dir /"frontend"/"static"),
    name="static"
)
dir = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=dir / "frontend"/"templates")

#Rutas para paginas renderizadas
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
