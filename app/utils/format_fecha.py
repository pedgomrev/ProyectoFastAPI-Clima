from datetime import datetime

def convertir_a_fecha(fecha_str):
    formatos_posibles = [
        '%m/%d/%Y',  # Formato estadounidense: 08/22/2024
        '%Y/%m/%d',  # Formato con puntos: 2024/08/22
        '%d/%m/%Y',  # Formato europeo: 22/08/2024
        '%Y-%m-%d',  # Formato con guiones: 2024-08-22
        '%d-%m-%Y',  # Formato con guiones: 22-08-2024
        '%m-%d-%Y',  # Otro formato con guiones: 08-22-2024
        '%d.%m.%Y',  # Formato con puntos: 22.08.2024
        '%m.%d.%Y',  # Otro formato con puntos: 08.22.2024
        
    ]
    
    for formato in formatos_posibles:
        try:
            fecha = datetime.strptime(fecha_str, formato)
            return fecha.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    raise ValueError(f"El formato de fecha '{fecha_str}' no es compatible con los formatos esperados.")