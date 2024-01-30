from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


def fecha():
    fecha = datetime.now().date()
    return fecha.strftime('%Y-%m-%d')

def Limpiar(cadena):
    # Eliminar espacios adicionales en blanco y convertir a minúsculas
    string_limpio = ' '.join(cadena.split()).lower()
    # Capitalizar la primera letra de cada palabra
    string_limpio = ' '.join(word.capitalize() for word in string_limpio.split())
    return string_limpio


def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def create_password(password):
    return generate_password_hash(password)