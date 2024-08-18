from typing import Optional
from pydantic import BaseModel
from datetime import date


class Tiempo(BaseModel):
    ciudad: str
    fecha: Optional[date] = None
    fecha_inicial: Optional[date] = None
    fecha_fin: Optional[date] = None
    SensacionTermica: Optional[float] = None
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    descripcion: Optional[str] = None

    def formatFecha(self, fecha: Optional[date]) -> Optional[str]:
        if fecha:
            return fecha.strftime("%d-%m-%Y")
        return None

    def json_filtrado(self, **kwargs):
        
        if self.fecha_fin or self.fecha_inicial != None:
            self.fecha = None
        data = self.model_dump(exclude_none=True, **kwargs)
        # Aplicar formato a las fechas que queden en el diccionario
        if 'fecha' in data:
            data['fecha'] = self.formatFecha(self.fecha)
        if 'fecha_inicial' in data:
            data['fecha_inicial'] = self.formatFecha(self.fecha_inicial)
        if 'fecha_fin' in data:
            data['fecha_fin'] = self.formatFecha(self.fecha_fin)

        # Convertir a JSON
        return data