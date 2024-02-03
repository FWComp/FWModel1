from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response, session
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
import traceback
import os

# Importaciones estaticas

from Herramientas.Tools import LoggerManager, obtener_fecha, limpiar_y_convertir_a_pascal_case, traducir_texto
from Herramientas.Excepts import CustomException, UserNotFound
from FireBaseControl import FireBase

# Modelos

from Modelos.modelo_usuario import Modelo_U

# SECTION: Iniciar aplicación Flask, Firebase y Base de datos.

App = Flask(__name__) # Objeto de instancia de Flask

CORS(App)  # Habilita CORS para todos los endpoints

FireBase() # Inicializar instancia de Firebase

CSRF = CSRFProtect(App) # NOTE - Protector de formularios CSRF de WTForms de Flask #!NOTE

CARGADOR = LoginManager(App) # NOTE - Cargador de usuarios de Login Manager de Flask #!NOTE

#!SECTION

# SECTION Cargador de Flask de user_loader.
@CARGADOR.user_loader
def cargar(id):
    if Modelo_U.usuario and Modelo_U.usuario.ID == id:

        if Modelo_U.usuario_existe(id):
            return Modelo_U.usuario
        else:
            LoggerManager.obtener_logger_info().info(f'Se registró posible eliminación de cuenta de {id}.\n\nFecha: {obtener_fecha()}')
            translated = traducir_texto(('Ouh...', f'Sorry {id if id else ""}, it seems your account was deleted.'), current_user.idioma, (None, id if id else None))
            flash(translated)
            Modelo_U.eliminar_instancia()
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
    except CustomException as e: # Manejar página de error del servidor
        LoggerManager.obtener_logger_debug().exception(f'Ha ocurrido un error interno.\n\n{str(e)}\n\nFecha: {obtener_fecha()}')
        session.clear()
        translated = traducir_texto((f"Sorry. An error has occurred.\nError in:\n\n {str(e)} \nTraceback:\n{traceback.format_exc()}"), current_user.idioma, (None, None))
        return translated[0]


@App.route('/Panel', methods=['GET']) # NOTE - Panel de selección de personajes.
@login_required
def Panel():
    if request.method == 'GET' and request.args.get('to') == 'ReturnPanel':
        current_user.current_character = None
        current_user.seguimiento = None
        return redirect(url_for('Panel'))

    if current_user.is_authenticated:

        if current_user.current_character:
            translated_return = traducir_texto((f"Return to Panel"), current_user.idioma)
            html = "<a style='color: green; text-decoration: none;' href='{}'>{}</a>".format(url_for('Panel', to='ReturnPanel'), translated_return)
            translated = traducir_texto(("Hey...', '{}. For a better experience, try not to manipulate the URL of the page. If you really want to exit, just log out of the character or click here: {}"), current_user.idioma, (current_user.ID, html))
            flash(translated, 'warning')
            return redirect(url_for('Juego'))

        elif current_user.seguimiento:
            translated = traducir_texto(('Wow', 'A page reload has been detected. Please try not to do it again.'), current_user.idioma)
            flash(translated)

        current_user.seguimiento = True
        return make_response(render_template('Panel/Panel.html'))
    else:
        # REVIEW - Generar un mensaje Flash. #!REVIEW 
        return redirect(url_for('index'))
    
@App.route('/Juego')
@login_required
def Juego():
    if not current_user.is_authenticated:# Retornar al login si no se encontró por alguna razón la instancia del usuario 
        return redirect(url_for('index'))
    
    if not current_user.current_character:
        return redirect(url_for('Panel'))

    else:
        return make_response(render_template('GAME/game.html'))
    
@App.after_request # NOTE Configurar Cache-Control para la ruta Panel para evitar posibles accesos no deseados por caché.
def cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    

@App.route('/logout')
def logout():
    Modelo_U.eliminar_instancia()
    logout_user()
    return redirect(url_for('index'))
#!SECTION


    
# SECTION - Funciones de manejo de formularios GET/POST.
@App.route('/login_method', methods=["GET", "POST"]) 
def metodo_login():
    if request.method == "GET":
        #NOTE - Redireccionar a Panel si se ha intentado manejar la URL y el usuario está autenticado de alguna manera.
        # De lo contrario, redireccionar a index si ha intentado manipular la URL.
        LoggerManager.obtener_logger_info().info(f'Un usuario. {current_user.ID if current_user.is_authenticated else "Desconocido"} intentó manipular la URL en el login.\n\n[ - - Fecha: {obtener_fecha()} - - ]')
        return redirect(url_for('Panel')) if current_user.is_authenticated else redirect(url_for('index'))
    
    elif request.method == "POST":
        try:
            obtener_nombre = limpiar_y_convertir_a_pascal_case(request.form['nombre_login'])

            Estado = Modelo_U.verificar_usuario(
                                                obtener_nombre,
                                                request.form['contraseña_login'])
            
            if Estado:

                login_user(Estado)
                LoggerManager.obtener_logger_info().info(f'Un usuario. {Estado.ID} se ha loggeado correctamente.\n\n[ - -  Fecha: {obtener_fecha()} - -]')
                translated = traducir_texto(('Welcome!', "Welcome {}. If you've made it this far, it's because you've accepted our terms when logging in."), current_user.idioma, (current_user.Nombre))
                flash(translated)
                return redirect(url_for('Panel'))
            
        except CustomException as e:

            LoggerManager.obtener_logger_debug().debug(f'Hubo un error al intentar iniciar sesión. Error en:\n\n{str(e)}.\n\nTraceback: \n{traceback.format_exc()}\n\n[ - - Fecha: {obtener_fecha()} - - ]')
            translated = traducir_texto(('An error ocurred', f'{str(e)}'), 'en', (None))
            flash(translated)
            return redirect(url_for('index'))

# Fetch
@App.route('/config_js_endpoint', methods=['POST', 'GET'])
def config_js_endpoint():
    try:
        message = Modelo_U.actualizar_configuraciones(request.json, current_user)
        if message:
            flash(message)
        else:
            translated_return = traducir_texto((f"Yes, return"), current_user.idioma)
            html = "<br><br><a style='color: green; text-decoration: none;' href='{}'>{}</a>".format(url_for('logout'), translated_return[0])
            flash(traducir_texto(('Success!', 'To see the new changes, it is necessary to restart. Do you want to restart?, This action will close your account, and you will have to log in again. {}'), current_user.idioma, html))


        return jsonify({'redirect_url': '/Panel'})
    except Exception as e:
        print(f"Error en la solicitud: {str(e)}")
        return jsonify({'redirect_url': '/Panel'})



@App.route('/signup_method', methods=["GET", "POST"])
def metodo_signup():
    if request.method == "GET":

        #NOTE: Redireccionar a Login si se ha intentado manejar la URL y el usuario está autenticado de alguna manera.
        # De lo contrario, redireccionar a index si ha intentado manipular la URL.
        LoggerManager.obtener_logger_info().info(f'Un usuario. {current_user.id if current_user.is_authenticated else "Desconocido"} intentó manipular la URL en el login.\n\n[ - - Fecha: {obtener_fecha()} - - ]')
        return redirect(url_for('Panel')) if current_user.is_authenticated else redirect(url_for('index'))
    
    elif request.method == "POST":

        try:
            lista_datos = [limpiar_y_convertir_a_pascal_case(request.form['nombre_registro']), limpiar_y_convertir_a_pascal_case(request.form['alias_registro']), request.form['contraseña_registro']]

            if lista_datos[2] != request.form['contraseña_verificación']:
                translated = traducir_texto(('Uh', 'The passwords do not match. Please try again.'), current_user.idioma)
                flash(translated)
                LoggerManager.obtener_logger_info().info(f'Se detuvo la verificación de {lista_datos[0]} {lista_datos[1]} por contraseñas desiguales.\n\n[ - - Fecha: {obtener_fecha()} - - ]')
                return redirect(url_for('index'))
            
            Estado = Modelo_U.crear_cuenta(lista_datos) #NOTE - Return: False (Nombre en uso), Instancia del usuario.

            if Estado:

                login_user(Estado)
                LoggerManager.obtener_logger_info().info(f'Un usuario. {Estado.ID} ha creado su cuenta y ha iniciado sesión el: {obtener_fecha()}.\n\n[ - - Fecha: {obtener_fecha()} - - ]')
                translate = traducir_texto(('Welcome', 'You have created an account to access {}. We hope you enjoy it.'), current_user.idioma, ('FW M-1'))
                flash(translate)
                return redirect(url_for('index'))
            
            else:
                translate = traducir_texto(('Ups...', 'There is already an account named "{}".'), current_user.idioma, (f'{lista_datos[0]} {lista_datos[1]}'))
                flash(translate)
                return redirect(url_for('index'))

        except CustomException as e:

            LoggerManager.obtener_logger_debug().debug(f'Hubo un error al intentar registrar a un usuario o iniciar sesión. Error en:\n\n{str(e)}\n\nTraceback: {traceback.format_exc()}\n\n[ - - Fecha: {obtener_fecha()} - - ]')
            translated = traducir_texto(('An error ocurred', f'{str(e)}'), 'en', (None))
            flash(translated)
            return redirect(url_for('index'))

@App.route('/eliminar_cuenta', methods=['POST', 'GET'])
def eliminar_cuenta():

    if request.method == 'POST':
        # args = [limpiar_y_convertir_a_pascal_case(request.form['NOMBRE']), request.form['PASSWRD']]
        translated = traducir_texto(('Goodbye...', 'You have deleted your account. We hope to see you around here again later.'), current_user.idioma, ())
        flash(translated)
    return redirect(url_for('Panel'))
    
@App.route('/cambiar_atributo', methods=['POST', 'GET'])
def cambiar_atributo():
    print('usando', request.args.get('to'))
    print('Se ha cambiado', request.args.get('attr'))
    return redirect(url_for('Panel'))


# SECTION: Personajes 
@App.route('/nuevo_personaje', methods=['POST'])
def nuevo_personajes():
    if request.method == 'POST':
        current_user.seguimiento = 'creando_personaje'
        try:
            if current_user.is_authenticated:
                Modelo_U.crear_personaje(
                                        limpiar_y_convertir_a_pascal_case(request.form['Name']), 
                                        request.form['age'],
                                        request.form['gender'],
                                        request.form['os'],
                                        request.form['class'])
                
                translated = traducir_texto(('Success', '{}, your character {} has been created successfully. You can now use it from the character panel.'), current_user.idioma, (current_user.Nombre, limpiar_y_convertir_a_pascal_case(request.form["Name"])))
                flash(translated)
                return redirect(url_for('Panel'))
            
            else:
                flash(('Something happened.', 'You have been returned to Log In due to an unknown error.'))
                return redirect(url_for('logout'))
        
        except CustomException as e:
            LoggerManager.obtener_logger_debug().exception(f'\n{current_user.ID} intentó crear un personaje. Pero hubo un error en: {str(e)}.\n\nTraceback: {traceback.format_exc()}\n\n[- - Fecha: {obtener_fecha()} - -]')
            translated = traducir_texto(('An error ocurred', f'{str(e)}'), current_user.idioma, (None))
            flash(translated)
    return redirect(url_for('Panel'))

@App.route('/borrar_personaje', methods=['GET'])
def borrar_personaje():
    try:
        current_user.eliminar_personaje(request.args.get('to'))
        flash('Se ha eliminado tu personaje correctamente.')
        return redirect(url_for('Panel'))
    except CustomException as e:
        flash(traducir_texto(('An error ocurred', f'{str(e)}'), current_user.idioma, (None))) if current_user.is_authenticated else ('Something happened', 'You were removed from the page due to a server reload.')

        LoggerManager.obtener_logger_debug().exception(f'\n{current_user.ID} intentó eliminar un personaje. Pero hubo un error en: {str(e)}.\n\nTraceback: {traceback.format_exc()}\n\n[- - Fecha: {obtener_fecha()} - -]')
        return redirect(url_for('Panel')) if current_user.is_authenticated else redirect(url_for('index'))
        


@App.route('/usar_personaje', methods=['GET'])
def usar_personaje():
    try:
        current_user.usar_personaje(request.args.get('to'))
        return redirect(url_for('Juego'))
    except CustomException as e:
        translated = traducir_texto(('An error ocurred', f'{str(e)}'), current_user.idioma, (None))
        flash(translated)
        LoggerManager.obtener_logger_debug(f'Hubo un error cuando {current_user.ID} intentaba usar al personaje {request.args.get("to")}.\n\nError en: {str(e)}.\n\nTraceback: {traceback.format_exc()}\n\n[- - Fecha: {obtener_fecha()} - -]')
        return redirect(url_for('Panel'))


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
