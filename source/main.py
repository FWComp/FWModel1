from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import logging
from flask_wtf.csrf import CSRFProtect
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from Herramientas import Tools
from Modelos.modelos_uci.Modelo_U import m_u_instancia

# SECTION: Iniciar aplicación Flask, Firebase y Base de datos.

App = Flask(__name__) # Objeto de instancia de Flask

logger_info = logging.getLogger('info_logger') # Inicializar un Logger con Logging para información 
logger_info.setLevel(logging.INFO)

#NOTE - Logger de nivel Info
archivo_logger_info = logging.FileHandler('App.log')
archivo_logger_info.setLevel(logging.INFO)
consola_logger_info = logging.StreamHandler()
consola_logger_info.setLevel(logging.INFO)
formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
archivo_logger_info.setFormatter(formato)
consola_logger_info.setFormatter(formato)
logger_info.addHandler(archivo_logger_info)
logger_info.addHandler(consola_logger_info)

logger_debug = logging.getLogger('info_debug') # Inicializar un Logger con Logging para información 
logger_debug.setLevel(logging.INFO)

#NOTE - Logger de Nivel Debug
archivo_logger_debug = logging.FileHandler('Debug.log')
archivo_logger_debug.setLevel(logging.DEBUG)
consola_logger_debug = logging.StreamHandler()
consola_logger_debug.setLevel(logging.DEBUG)
formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
archivo_logger_debug.setFormatter(formato)
consola_logger_debug.setFormatter(formato)
logger_debug.addHandler(archivo_logger_debug)
logger_debug.addHandler(consola_logger_debug)


CSRF = CSRFProtect(App) # NOTE - Protector de formularios csrf de WTForms de Flask #!NOTE

CARGADOR = LoginManager(App) # NOTE - Cargador de usuarios de Login Manager de Flask #!NOTE

#!SECTION

# SECTION Cargador de Flask de user_loader.

@CARGADOR.user_loader
def cargar(instancia):
    if m_u_instancia:
        if m_u_instancia.usuario_existe(instancia.id):
            return m_u_instancia.instancia()
        else:
            logger_info.info(f'Se resgistró posible eliminación de cuenta de {instancia.id}.\n\nFecha: {Tools.fecha()}')
            flash(['Vaya', 'Lo sentimos, al parecer tu cuenta fue eliminada.'])
    else:
        logger_info.info(f'No se encontró la instancia del usuario {instancia.id if instancia else "Desconocido"}.\n\nFecha: {Tools.fecha}')
        flash('Aviso', 'Se ha cerrado sesión correctamente. Si no fuiste tú, puedes avisar a soporte.')
        return None
    
#!SECTION
    
#SECTION - Rutas de la aplicación
    
@App.route('/') # NOTE - Redireccionar al píe del directorio /index #!NOTE
def index():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('Panel'))
        return render_template('Auth/Login.html')
    except Exception as e:
        return f"Lo sentimos. Ha ocurrido un error.\nError en:\n\n {str(e)}"


@App.route('/Panel') # NOTE - Panel de selección de personajes.
def Panel():
    if current_user.is_authenticated:
        Response = make_response(render_template('Panel/Panel.html'))
        return Response
    else:
        # REVIEW - Generar un mensaje Flash. #!REVIEW 
        return render_template('Auth/Login.html')
    
@App.after_request # NOTE Configurar Cache-Control para la ruta Panel para evitar posibles accesos no deseados por caché.
def cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    
#!SECTION
    
# SECTION - Funciones de manejo de formularios GET/POST.

@App.route('/login_method', methods=["GET", "POST"]) 
def metodo_login():
    if request.method == "GET":
        #NOTE - Redireccionar a Panel si se ha intentado manejar la URL y el usuario está autenticado de alguna manera.
        # De lo contrario, redireccionar a index si ha intentado manipular la URL.
        logger_info.info(f'Un usuario. {current_user.id if current_user.is_authenticated else "Desconocido"} intentó manipular la URL en el login.\n\nFecha: {Tools.fecha}')
        return redirect(url_for('Panel')) if current_user.is_authenticated else redirect(url_for('index'))
    elif request.method == "POST":
        try:
            obtener_nombre = Tools.Limpiar(request.form['nombre_login'])
            obtener_passwrd = request.form['contraseña_login']

            Estado = Modelo_U.verificar_usuario(obtener_nombre, obtener_passwrd)
            if Estado:
                login_user(Estado)
                logger_info.info(f'Un usuario. {Estado.id} se ha loggeado correctamente.\n\nFecha: {Tools.fecha()}')
                return redirect(url_for('Panel'))
            elif Estado == False:
                logger_info.info(f'Un usuario. {obtener_nombre} intentó iniciar sesión. Operación Fallidad por credenciales(Contraseña).\n\nFecha: {Tools.fecha}')
                flash(['Ups', 'La contraseña es incorrecta.'])
                return redirect(url_for('index'))
            else:
                #REVIEW - Hacer una clase 'visor_login', 'login_handler' para manejar los errores de credenciales y ataques de fuerza bruta.

                flash(['Error', 'Este usuario no existe. Intenta nuevamente'])
                logger_info.info(f'Un usuario. {obtener_nombre} intentó iniciar sesión. Operación Fallida por credenciales(Identificador)\n\nFecha: {Tools.fecha}')
                return redirect(url_for('index'))
        except Exception as e:
            logger_debug.debug(f'Hubo un error al intentar iniciar sesión. Error en:\n\n{str(e)}.\n\nFecha: {Tools.fecha}')
            flash(['Error Interno', f'Lo sentimos. Ha pasado un error desconocido.'])
            return redirect(url_for('index'))



@App.route('signup_method', methods=["GET", "POST"])
def metodo_signup():
    if request.method == "GET":
        #NOTE: Redireccionar a Login si se ha intentado manejar la URL y el usuario está autenticado de alguna manera.
        # De lo contrario, redireccionar a index si ha intentado manipular la URL.
        logger_info.info(f'Un usuario. {current_user.id if current_user.is_authenticated else "Desconocido"} intentó manipular la URL en el login.\n\nFecha: {Tools.fecha}')
        return redirect(url_for('Panel')) if current_user.is_authenticated else redirect(url_for('index'))
    elif request.method == "POST":
        try:
            lista_datos = [Tools.Limpiar(request.form['nombre_registro']), Tools.Limpiar(request.form['alias_registro']), request.form['contraseña_registro']]

            if lista_datos[2] != request.form['verificacion_pswrd_registro']:
                flash('Uh', 'Las contraseñas no son iguales. Intenta nuevamente.')
                logger_info.info(f'Se detuvo la verificación de {lista_datos[0]} {lista_datos[1]} por contraseñas desiguales.\n\nFecha: {Tools.fecha}')
            
            Estado = Modelo_U.crear_cuenta(lista_datos) #NOTE - Return: False (Nombre en uso), Instancia del usuario.
            if Estado:
                login_user(Estado)
                logger_info.info(f'Un usuario. {Estado.id} ha creado su cuenta y ha iniciado sesión el: {Tools.fecha}.\n\nFecha: {Tools.fecha}')
                return redirect(url_for('index'))
            else:
                flash(['Vaya', f'Ya existe una cuenta llamada {lista_datos[0]} {lista_datos[1]}'])
                return redirect(url_for('index'))

        except Exception as e:
            logger_debug.debug(f'Hubo un error al intentar registrar a un usuario o iniciar sesión. Error en:\n\n{str(e)}\n\nFecha: {Tools.fecha}')
            flash(['Error Interno', 'Lo sentimos. Ha pasado un error desconocido.'])
            return redirect(url_for('index'))