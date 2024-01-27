from datetime import datetime

def fecha():
    fecha = datetime.now().date()
    return fecha.strftime('%Y-%m-%d')