from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes.tiempo import router as weather_router
from app.config import templates  # Importar desde config.py
# Crear la instancia de FastAPI
app = FastAPI()

# Configuración de Jinja2 para renderizar plantillas HTML
app.templates = templates
# Incluir el router de las rutas relacionadas con el clima
app.include_router(weather_router)

# Montar el directorio para archivos estáticos (CSS, JavaScript, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Aquí puedes incluir más routers o configuraciones si es necesario
