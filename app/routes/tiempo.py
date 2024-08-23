from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from app.utils.format_fecha import convertir_a_fecha as format_fecha
from app.schemas.tiempo import Tiempo
from app.config import templates  # Importar desde config.py
import requests
from datetime import date
import datetime


router = APIRouter()
api_key = 'W9T6X2VD2ZY23BB3GYXBUS7TA'


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/consulta", response_class=HTMLResponse)
async def consultaCiudad(request: Request, ciudad: str):
    tiempoActual = datetime.datetime.now()
    tiempoActual = str(tiempoActual).replace(" ", "T").split(".")[0]
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{ciudad}/{tiempoActual}?unitGroup=metric&key={api_key}'
    print(url)
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
        ciudadConsulta = dataFormat.ciudad
        # Filtrar los campos según los datos disponibles
        dataFormat = [dataFormat.json_filtrado()]
        
        # Renderizar la plantilla con los datos filtrados
        return templates.TemplateResponse("consulta.html", {"request": request, "datos": dataFormat, "ciudad": ciudadConsulta})
    else:
        raise HTTPException(status_code=404, detail="City not found")

@router.get("/consulta_rango", response_class=HTMLResponse)
async def consultaRango(request: Request, ciudad: str, fechaInicio: str, fechaFin: str):
    if fechaInicio == "" :
        fechaInicio = str(date.today())
    if fechaFin == "" :
            fechaInicio = format_fecha(fechaInicio)
            url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{ciudad}/{fechaInicio}?unitGroup=metric&key={api_key}'
    else:
        if fechaFin < fechaInicio:
            raise HTTPException(status_code=404, detail="Fecha de fin no puede ser menor a la fecha de inicio")
        else:
            fechaFin = format_fecha(fechaFin)
            fechaInicio = format_fecha(fechaInicio)
            url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{ciudad}/{fechaInicio}/{fechaFin}?unitGroup=metric&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ciudad = data['resolvedAddress']
        dias = data['days']
        dataFormat = []
        for dia in dias:
            dataFormat.append(
                Tiempo(
                    ciudad=ciudad,
                    fecha=dia['datetime'],
                    temperatura=dia['temp'],
                    SensacionTermica=dia['feelslike'],
                    humedad=dia['humidity'],
                ).json_filtrado()
            )
    else:
        raise HTTPException(status_code=404, detail="Algo salió mal")

    return templates.TemplateResponse("consulta.html", {"request": request, "datos": dataFormat, "ciudad": ciudad, "fechaInicio": fechaInicio, "fechaFin": fechaFin,"longitud": len(dataFormat)})

@router.get("/acercaDe", response_class=HTMLResponse)
async def acercaDe(request: Request):
    return templates.TemplateResponse("acercaDe.html", {"request": request})

