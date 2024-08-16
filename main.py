from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,field_validator
from typing import Optional
from datetime import datetime,date
import requests

app = FastAPI()

api_key = 'W9T6X2VD2ZY23BB3GYXBUS7TA'
def formatFecha(fecha):
    return fecha.strftime("%d-%m-%Y")

class tiempoRespuesta(BaseModel):
    ciudad : str
    fecha : date
    SensacionTermica : float
    temperatura : float
    humedad : float
    descripcion : str


class ErrorResponse(BaseModel):
    error : str
@app.get("/{ciudad}",responses={404:{"model": ErrorResponse},200:{'model':tiempoRespuesta}})
def consultaCiudad(ciudad:str):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{ciudad}?unitGroup=metric&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        dataFormat = tiempoRespuesta(
            ciudad= data['resolvedAddress'],
            fecha=  data['days'][0]['datetime'],  # Accediendo al primer día de la lista de días
            temperatura= data['days'][0]['temp'],  # Accediendo a la temperatura del primer día
            SensacionTermica= data['days'][0]['feelslike'],
            humedad = data['days'][0]['humidity'],
            descripcion= data['description']  # Accediendo a la descripción general del clima
        )
        dataFormat.fecha = formatFecha(dataFormat.fecha)
        return dataFormat
    else:
        raise HTTPException(status_code=404, detail="City not found")