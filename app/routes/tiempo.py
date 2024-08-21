from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from app.schemas.tiempo import Tiempo
from app.config import templates  # Importar desde config.py
import requests

router = APIRouter()
api_key = 'W9T6X2VD2ZY23BB3GYXBUS7TA'
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@router.get("/consulta", response_class=HTMLResponse)
async def consultaCiudad(request: Request, ciudad: str):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{ciudad}?unitGroup=metric&key={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Crear instancia del modelo tiempoRespuesta
        dataFormat = Tiempo(
            ciudad=data['resolvedAddress'],
            fecha=data['days'][0]['datetime'],  # Accediendo al primer día de la lista de días
            temperatura=data['days'][0]['temp'],  # Accediendo a la temperatura del primer día
            SensacionTermica=data['days'][0]['feelslike'],
            humedad=data['days'][0]['humidity'],
            descripcion=data['description']  # Accediendo a la descripción general del clima
        )
        
        # Filtrar los campos según los datos disponibles
        dataFormat = dataFormat.json_filtrado()
        
        # Renderizar la plantilla con los datos filtrados
        return templates.TemplateResponse("consulta.html", {"request": request, "datos": dataFormat})
    else:
        raise HTTPException(status_code=404, detail="City not found")
    
@router.get("/acercaDe", response_class=HTMLResponse)
async def acercaDe(request: Request):
    return templates.TemplateResponse("acercaDe.html", {"request": request})
