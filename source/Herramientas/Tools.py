from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from googletrans import Translator

def obtener_fecha():  # Devuelve la fecha de hoy.
    fecha = datetime.now().date()
    return fecha.strftime('%Y-%m-%d')

def limpiar_y_convertir_a_pascal_case(cadena):
    """
    Limpia espacios y convierte la cadena a pascal case.
    """
    # Eliminar espacios adicionales en blanco y convertir a minúsculas
    string_limpio = ' '.join(cadena.split()).lower()
    # Capitalizar la primera letra de cada palabra
    string_limpio = ' '.join(word.capitalize() for word in string_limpio.split())
    return string_limpio

def chequear_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def crear_password(password):
    return generate_password_hash(password)

class LoggerManager:
    """
    Clase para gestionar los loggers de información y debug.
    """
    logger_info = logging.getLogger('info_logger')
    logger_info.setLevel(logging.INFO)

    archivo_logger_info = logging.FileHandler('App.log')
    archivo_logger_info.setLevel(logging.INFO)
    consola_logger_info = logging.StreamHandler()
    consola_logger_info.setLevel(logging.INFO)
    formato_info = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    archivo_logger_info.setFormatter(formato_info)
    consola_logger_info.setFormatter(formato_info)
    logger_info.addHandler(archivo_logger_info)
    logger_info.addHandler(consola_logger_info)

    # Logger de Nivel Debug
    logger_debug = logging.getLogger('debug_logger')
    logger_debug.setLevel(logging.DEBUG)

    archivo_logger_debug = logging.FileHandler('Debug.log')
    archivo_logger_debug.setLevel(logging.DEBUG)
    consola_logger_debug = logging.StreamHandler()
    consola_logger_debug.setLevel(logging.DEBUG)
    formato_debug = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    archivo_logger_debug.setFormatter(formato_debug)
    consola_logger_debug.setFormatter(formato_debug)
    logger_debug.addHandler(archivo_logger_debug)
    logger_debug.addHandler(consola_logger_debug)

    @classmethod
    def obtener_logger_debug(cls):
        return cls.logger_debug
    
    @classmethod
    def obtener_logger_info(cls):
        return cls.logger_info

def traducir_texto(mensaje, idioma_destino, args=None):
    translator = Translator()
    idioma_destino = idioma_destino

    if not idioma_destino:
        idioma_destino = 'en'
    # Mapear abreviaturas de idiomas a códigos de idioma
    if idioma_destino == 'co':
        idioma_destino = 'ko'
    elif idioma_destino == 'jp':
        idioma_destino = 'ja'
    elif idioma_destino == 'ch':
        idioma_destino = 'zh-CN'

    # Transformar el mensaje a tupla si no lo es
    if not isinstance(mensaje, tuple):
        mensaje = (mensaje,)
    
    # Transformar args a tupla si no lo es
    if args is None:
        args = tuple()
    elif not isinstance(args, tuple):
        args = (args,)
    # Traducir cada elemento del mensaje y formatear con los argumentos
    try:
       mensaje_traducido = [translator.translate(m, dest=idioma_destino).text for m in mensaje]
    except Exception as e:
        print(f"Error al traducir texto: {e}")
        mensaje_traducido = mensaje  # O proporciona un valor predeterminado

    mensaje_formateado = tuple(m.format(*args) for m in mensaje_traducido)
    return mensaje_formateado

# Only:

"""
Coreano: ko
Español: es
Japonés: ja
Inglés: en
Chino: zh-CN (para chino simplificado)
Portugués: pt

"""