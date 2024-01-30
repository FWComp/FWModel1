from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
import logging
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os

from Herramientas import Tools
from FireBaseControl import FireBase

from Modelos.modelo_usuario import Modelo_U

# SECTION: Iniciar aplicación Flask, Firebase y Base de datos.

App = Flask(__name__) # Objeto de instancia de Flask

# Logger de nivel Info
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
logger_debug.setLevel(logging.DEBUG)  # Corregido a DEBUG

archivo_logger_debug = logging.FileHandler('Debug.log')
archivo_logger_debug.setLevel(logging.DEBUG)
consola_logger_debug = logging.StreamHandler()
consola_logger_debug.setLevel(logging.DEBUG)
formato_debug = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
archivo_logger_debug.setFormatter(formato_debug)
consola_logger_debug.setFormatter(formato_debug)
logger_debug.addHandler(archivo_logger_debug)
logger_debug.addHandler(consola_logger_debug)

FireBase()

CSRF = CSRFProtect(App) # NOTE - Protector de formularios csrf de WTForms de Flask #!NOTE

CARGADOR = LoginManager(App) # NOTE - Cargador de usuarios de Login Manager de Flask #!NOTE

#!SECTION

# SECTION Cargador de Flask de user_loader.
@CARGADOR.user_loader
def cargar(id):
    if Modelo_U.usuario and Modelo_U.usuario.ID == id:

        if Modelo_U.usuario_existe(id):
            return Modelo_U.usuario
        else:
            logger_info.info(f'Se registró posible eliminación de cuenta de {id}.\n\nFecha: {Tools.fecha()}')
            flash(['Vaya', f'Lo sentimos {id if id else ""}, al parecer tu cuenta fue eliminada.'])
            Modelo_U.Eliminar()
            logout_user()
            session.clear()
    return None

    
#!SECTION
    
#SECTION - Rutas de la aplicación
    
@App.route('/') # NOTE - Redireccionar al píe del directorio /index #!NOTE
def index():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('Panel'))
        return render_template('login/Login_es.html')
    except Exception as e:
        logger_debug.exception(f'Ha ocurrido un error interno.\n\n{str(e)}\n\nFecha: {Tools.fecha()}')
        session.clear()
        return f"Lo sentimos. Ha ocurrido un error.\nError en:\n\n {str(e)}"


@App.route('/Panel') # NOTE - Panel de selección de personajes.
@login_required
def Panel():
    if current_user.is_authenticated:
        repro = True
        if current_user.seguimiento == True and current_user.seguimiento != 'creando_personaje':
            repro = False
            flash(['Vaya', 'Se ha detectado una recarga de la página. Intenta no volver hacerlo.'])    
        current_user.seguimiento == True
        Response = make_response(render_template('Panel/Panel.html', repro=repro))
        return Response
    else:
        # REVIEW - Generar un mensaje Flash. #!REVIEW 
        return redirect(url_for('index'))
    
@App.route('/Juego')
@login_required
def Juego():
    if current_user.current_character and current_user.is_authenticated:
        Response = make_response(render_template('GAME/game.html'))
        return Response
    
    current_user.current_character = None

    if current_user.is_authenticated:
        return redirect(url_for('Panel'))
    else:
        return redirect(url_for('index'))
    
@App.after_request # NOTE Configurar Cache-Control para la ruta Panel para evitar posibles accesos no deseados por caché.
def cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    

@App.route('/logout')
def logout():
    Modelo_U.Eliminar()
    logout_user()
    return redirect(url_for('index'))



#!SECTION
    
# SECTION - Funciones de manejo de formularios GET/POST.

@App.route('/login_method', methods=["GET", "POST"]) 
def metodo_login():
    if request.method == "GET":
        #NOTE - Redireccionar a Panel si se ha intentado manejar la URL y el usuario está autenticado de alguna manera.
        # De lo contrario, redireccionar a index si ha intentado manipular la URL.
        logger_info.info(f'Un usuario. {current_user.ID if current_user.is_authenticated else "Desconocido"} intentó manipular la URL en el login.\n\nFecha: {Tools.fecha()}')
        return redirect(url_for('Panel')) if current_user.is_authenticated else redirect(url_for('index'))
    elif request.method == "POST":
        try:
            obtener_nombre = Tools.Limpiar(request.form['nombre_login'])
            obtener_passwrd = request.form['contraseña_login']

            Estado = Modelo_U.verificar_usuario(obtener_nombre, obtener_passwrd)
            if Estado:
                login_user(Estado)
                logger_info.info(f'Un usuario. {Estado.ID} se ha loggeado correctamente.\n\nFecha: {Tools.fecha()}')
                flash(['¡Bienvenido!', f'Te damos la bienvenida {current_user.ID}. Si ya has llegado hasta aquí es por que has aceptado nuestros terminos al loggearte.'])
                return redirect(url_for('Panel'))
            elif Estado == False:
                logger_info.info(f'Un usuario. {obtener_nombre} intentó iniciar sesión. Operación Fallidad por credenciales(Contraseña).\n\nFecha: {Tools.fecha()}')
                flash(['Ups', 'La contraseña es incorrecta.'])
                return redirect(url_for('index'))
            else:
                #REVIEW - Hacer una clase 'visor_login', 'login_handler' para manejar los errores de credenciales y ataques de fuerza bruta.

                flash(['Error', 'Este usuario no existe. Intenta nuevamente'])
                logger_info.info(f'Un usuario. {obtener_nombre} intentó iniciar sesión. Operación Fallida por credenciales(Identificador)\n\nFecha: {Tools.fecha()}')
                return redirect(url_for('index'))
        except Exception as e:
            logger_debug.debug(f'Hubo un error al intentar iniciar sesión. Error en:\n\n{str(e)}.\n\nFecha: {Tools.fecha()}')
            flash(['Error Interno', f'Lo sentimos. Ha pasado un error desconocido.'])
            return redirect(url_for('index'))



@App.route('/signup_method', methods=["GET", "POST"])
def metodo_signup():
    if request.method == "GET":
        #NOTE: Redireccionar a Login si se ha intentado manejar la URL y el usuario está autenticado de alguna manera.
        # De lo contrario, redireccionar a index si ha intentado manipular la URL.
        logger_info.info(f'Un usuario. {current_user.id if current_user.is_authenticated else "Desconocido"} intentó manipular la URL en el login.\n\nFecha: {Tools.fecha()}')
        return redirect(url_for('Panel')) if current_user.is_authenticated else redirect(url_for('index'))
    elif request.method == "POST":

        try:
            lista_datos = [Tools.Limpiar(request.form['nombre_registro']), Tools.Limpiar(request.form['alias_registro']), request.form['contraseña_registro']]

            if lista_datos[2] != request.form['contraseña_verificación']:
                flash('Uh', 'Las contraseñas no son iguales. Intenta nuevamente.')
                logger_info.info(f'Se detuvo la verificación de {lista_datos[0]} {lista_datos[1]} por contraseñas desiguales.\n\nFecha: {Tools.fecha()}')
            
            Estado = Modelo_U.crear_cuenta(lista_datos) #NOTE - Return: False (Nombre en uso), Instancia del usuario.
            if Estado:
                login_user(Estado)
                logger_info.info(f'Un usuario. {Estado.ID} ha creado su cuenta y ha iniciado sesión el: {Tools.fecha()}.\n\nFecha: {Tools.fecha()}')
                flash(['¡Bienvenido!', f'Te damos la bienvenida {current_user.ID}. Si ya has llegado hasta aquí es por que has aceptado nuestros terminos al loggearte.'])
                return redirect(url_for('index'))
            else:
                flash(['Vaya', f'Ya existe una cuenta llamada {lista_datos[0]} {lista_datos[1]}'])
                return redirect(url_for('index'))

        except Exception as e:
            logger_debug.debug(f'Hubo un error al intentar registrar a un usuario o iniciar sesión. Error en:\n\n{str(e)}\n\nFecha: {Tools.fecha()}')
            flash(['Error Interno', 'Lo sentimos. Ha pasado un error desconocido.'])
            session.clear()
            return redirect(url_for('index'))
        
@App.route('/nuevo_personaje', methods=['POST'])
def nuevo_personajes():
    if request.method == 'POST':
        current_user.seguimiento = 'creando_personaje'
        try:
            Nombre = Tools.Limpiar(request.form['Name'])
            Edad = request.form['age']
            Genero = request.form['gender']
            orientacion = request.form['os']
            clase = request.form['class']
            if current_user.is_authenticated:
                Modelo_U.crear_personaje(Nombre, Edad, Genero, orientacion, clase)
                return redirect(url_for('Panel'))
            return redirect(url_for('index'))
        except Exception as e:
            logger_debug.exception(f'\n{current_user.ID} intentó crear un personaje. Pero hubo un error en: {str(e)}.\n\nFecha: {Tools.fecha()}')
    return redirect(url_for('Panel'))

@App.route('/borrar_personaje', methods=['GET'])
def borrar_personaje():
    Name = request.args.get('to')
    current_user.eliminar_personaje(Name)
    return redirect(url_for('Panel'))

@App.route('/usar_personaje', methods=['GET'])
def usar_personaje():
    Name = request.args.get('to')
    current_user.usar_personaje(Name)
    return redirect(url_for('Juego'))


if __name__ == '__main__':
    configure = {
        'Appcnfg': {
            'DEBUG': True, #NOTE: Quitar cuando sea subido al Hosting.
            'SECRET_KEY': os.getenv('SECRETKEY'),
            'SESSION_PROTECTION': False
        }
    }
    App.config.update(configure['Appcnfg'])
    CSRF.init_app(App)
    App.run(host='0.0.0.0')
