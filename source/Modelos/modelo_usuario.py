# Externas
from google.cloud.exceptions import NotFound
import traceback
import io
import base64

# Estaticas
from Herramientas.Excepts import FirebaseStorageError, UsuarioVerificationError, ErrorCrearPersonaje, FaltaDeDatos, ErrorDesconocido
from Herramientas.Tools import LoggerManager, obtener_fecha, chequear_password, crear_password, traducir_texto
from FireBaseControl import FB
from Modelos.Entidades import Usuario
class Modelo_U:

    usuario = None

    @staticmethod
    def usar_bucket_principal(item, root):
        """
        Obtiene el contenido de un archivo desde Firebase Storage y lo devuelve como base64.

        Args:
            item (str): Nombre del objeto.
            root (str): Ruta en el bucket de Firebase Storage.

        Returns:
            str or None: Contenido del archivo en base64 o None si no se encuentra el archivo.
        
        Raises:
            FirebaseStorageError: Excepción personalizada para errores relacionados con Firebase Storage.
        """
        try:
            archivo_blob = FB.objeto_storage().download(root)

            if not archivo_blob.exists():
                raise FileNotFoundError(f'El objeto {archivo_blob.name} no existe en el bucket {archivo_blob.bucket.name}')

            # Convertir a base64
            file_content = io.BytesIO(archivo_blob.download_as_bytes())
            encoded_content = base64.b64encode(file_content.read()).decode('utf-8')

            return encoded_content

        except NotFound as not_found_error:
            # Manejar el error de objeto no encontrado de manera específica
            LoggerManager.obtener_logger_debug().exception(f'Error al buscar el objeto {item} en Firebase Storage.\n\nError en {str(not_found_error)}\n\nTraceback: {traceback.format_exc()}\n\n[ - - Fecha: {obtener_fecha()}]')
            raise FirebaseStorageError(f"Error al buscar el objeto {item} en Firebase Storage.")
        except Exception as e:
            LoggerManager.obtener_logger_debug().exception(f'Hubo un error desconocido.\n\nError en {str(e)}\n\nTraceback: {traceback.format_exc()}\n\n[ - - Fecha: {obtener_fecha()} - - ]')
            raise FirebaseStorageError("Error desconocido al buscar el objeto en Firebase Storage.")

            
    @classmethod
    def usuario_existe(cls, id):
        """
        Verifica si un usuario con el ID proporcionado existe en la base de datos.

        Args:
            id (str): ID del usuario.

        Returns:
            bool: True si el usuario existe, False si no.

        Raises:
            ValueError: Se lanza si el ID no es una cadena.
        """
        if not isinstance(id, str):
            raise ValueError("El ID del usuario debe ser una cadena.")
        
        return FB.objeto_firestore().document(f'usuarios/{id}').get().exists

    @classmethod
    def verificar_usuario(cls, nombre, passwrd):
        """
        Verifica las credenciales de un usuario y devuelve una instancia de Usuario si son válidas.

        Args:
            nombre (str): Nombre de usuario.
            passwrd (str): Contraseña del usuario.

        Returns:
            Usuario or bool: Instancia de Usuario si las credenciales son válidas, False si no.

        Raises:
            UsuarioVerificationError: Excepción personalizada para errores de verificación de usuario.
        """
        documento_usuario = FB.objeto_firestore().document(f'usuarios/{nombre}').get()

        if documento_usuario.exists:
            data = documento_usuario.to_dict()
            if data.get('Contraseña') and chequear_password(data['Contraseña'], passwrd):
                cls.usuario = Usuario.Usuario(
                    ID=nombre,
                    Nombre=data['Nombre'],
                    Apellido=data['Apellido'],
                    Email=data['Correo'],
                    Estado=data['Estado'],
                    personajes=data['Personajes'],
                    Registro=data['Registro'],
                    Telefono=data['Telefono'],
                    Theme_color=data['Tema_preferido'],
                    Panel_song=data['Panel_song'],
                    ONLSTT=data['OnLineState'],
                    idioma = data['idioma'],
                    hiddes=[
                        data['hiddes'][0],
                        data['hiddes'][1],
                        data['hiddes'][2],
                        data['hiddes'][3]
                    ],
                    others=[
                        data['cumpleaños'],
                        data['Edad'],
                        data['Gender'],
                        data['OS'],
                        data['Country']
                    ]
                )

                return cls.usuario
            else:
                raise UsuarioVerificationError("Credenciales de usuario inválidas.")
        raise UsuarioVerificationError('Este usuario no existe.')

    @classmethod
    def crear_cuenta(cls, datos):
        """
        Crea una nueva cuenta de usuario en la base de datos.

        Args:
            datos (list): Lista con información del usuario (nombre, apellido, contraseña).

        Returns:
            Usuario or bool: Instancia de Usuario si la cuenta se crea correctamente, False si ya existe.

        Raises:
            ValueError: Se lanza si la lista de datos no tiene la longitud esperada.
        """
        if len(datos) != 3:
            raise ValueError("La lista de datos debe contener nombre, apellido y contraseña.")

        nombre_completo = f'{datos[0]} {datos[1]}'

        # Verificar si el usuario ya existe.
        doc_verificacion_usuario = FB.objeto_firestore().document(f'usuarios/{nombre_completo}')
        if doc_verificacion_usuario.get().exists:
            raise UsuarioVerificationError('Este usuario no existe. Intenta nuevamente.')

        doc = {
            "Nombre": datos[0],
            "Apellido": datos[1],
            "Contraseña": crear_password(datos[2]),
            "Registro": obtener_fecha(),
            "Personajes": [],
            "Correo": None,
            "Telefono": None,
            "Estado": "Normal",
            "Tema_preferido": "Default",
            "Panel_song": ['1.0', True, 'Default'],
            "OnLineState": "show",
            "hiddes": [False, False, False, False],            
            "cumpleaños": False,
            "Edad": None,
            "Gender": None,
            "OS": None,
            "Country": None,
            "idioma": 'en'

        }

        FB.objeto_firestore().document(f'usuarios/{nombre_completo}').set(doc)
        return cls.verificar_usuario(nombre_completo, datos[2])  # Nombre, Contraseña. Retorno: Instancia, None

    @classmethod
    def crear_personaje(cls, Nombre, Edad, Genero, orientacion, clase):
        """
        Crea un nuevo personaje para el usuario en la base de datos.

        Args:
            Nombre (str): Nombre del personaje.
            Edad (str): Edad del personaje.
            Genero (str): Género del personaje.
            orientacion (str): Orientación del personaje.
            clase (str): Clase del personaje.

        Returns:
            bool: True si se crea el personaje correctamente, False si no.

        Raises:
            Exception: Se lanza si hay un error durante la creación del personaje.
        """
        weapons = {
            'Assassing': 'bokken',
            'Tank': 'small_maze',
            'warrior': 'small_sword'
        }

        weapon = weapons.get(clase)

        if not weapon:
            # La clase no tiene un arma asociada
            raise FaltaDeDatos(f'No existen datos suficientes de la clase {clase} o la clase no existe.')

        # Verificar límite de personajes y si el usuario ya tiene el personaje
        if cls.usuario.Personajes and len(cls.usuario.Personajes) >= 2:
            raise ErrorCrearPersonaje (f'Ya tienes el máximo de personajes que se pueden utilizar {len(cls.usuario.Personajes)}. Intenta borrar uno.')
        elif f'{cls.usuario.ID}_{Nombre}' in cls.usuario.Personajes:
            raise ErrorCrearPersonaje(f'Ya tienes a un personaje llamado {Nombre}. Intenta usar otro nombre diferente.')

        try:
            # Acceder a la información de la clase desde la base de datos
            referencia_clase = FB.objeto_realtimedb().child(f'Class/levels/{clase}/1')
            Estatus = referencia_clase.get()

            if Estatus is None:
                # El nodo no existe
                raise f'No existen datos suficientes de la clase {clase} o la clase no existe.'

            # Crear documentos para el personaje
            docInfo = {
                'Nombre': Nombre,
                'Edad': Edad,
                'Genero': Genero,
                'Orientacion': orientacion,
                'Clase': clase,
                'Registro': obtener_fecha()
            }

            docEstatus = {
                'Nivel': 1,
                'PS': Estatus.get('HP', 0),
                'EXP': Estatus.get('XP', 0),
                'PM': Estatus.get('PM', 0),
                'Daño': Estatus.get('Damage', 0),
                'Defensa': Estatus.get('Defense', 0),
                'Agilidad': Estatus.get('Agility', 0),
            }

            docInventario = {
                'herb': 5,
                'antidote': 2,
                weapon: ['equipped', 1]
            }

            docPoderes = {
                poder: 'Aprendido en nivel 1' for poder in Estatus.get('Learn', [])
            }

            # Actualizar Personajes de Usuario.
            doc_usuario = FB.objeto_firestore().collection('usuarios').document(cls.usuario.ID)
            id_personaje = f'{cls.usuario.ID}_{Nombre}'
            diccionario_personajes = cls.usuario.Personajes
            diccionario_personajes[id_personaje] = [obtener_fecha(), Nombre]
            doc_usuario.update({'Personajes': diccionario_personajes})

            # Crear el personaje en el documento personajes de Firestore
            doc_personaje = FB.objeto_firestore().document(f'personajes/{id_personaje}')
            coleccion_personaje = {
                "Nombre": Nombre,
                "Info": docInfo,
                "Estatus": docEstatus,
                "Poderes": docPoderes,
                "Inventario": docInventario,
            }

            # Insertar el documento del personaje en Firestore
            doc_personaje.set(coleccion_personaje)
            cls.usuario.cargar_personajes()
        except Exception as e:
            # Manejar la excepción o simplemente dejar que se propague
            LoggerManager.obtener_logger_debug().exception(f'Hubo un error desconocido.\n\n{str(e)}.\n\n[- -  Fecha: {obtener_fecha()} - - ]')
            raise ErrorDesconocido('Lo sentimos. Hubo un error desconocido.')

    @classmethod
    def eliminar_instancia(cls):
        """
        Elimina la instancia de usuario actual estableciendo la variable de clase 'usuario' en None.
        """
        cls.usuario = None


    @classmethod
    def actualizar_configuraciones(cls, data, user):
        try:
            doc_usuario = FB.objeto_firestore().collection('usuarios').document(user.ID)
            volume = int(data['song'][0]) / 100
            act = {
                "Tema_preferido": data['theme'],
                "idioma": data['lang'],
                "Panel_song": [volume, data['song'][2], data['song'][1]],
                "OnLineState": data['online_state'],
                "hiddes": [data['hiddes'][0], data['hiddes'][1], data['hiddes'][2], data['hiddes'][3]]
            }

            state = doc_usuario.update(act)
            if state:
                user.idioma = act['idioma']
                user.Panel_song = act['Panel_song']
                user.ONLSTT = act['OnLineState']
                user.hiddes = act['hiddes']
                user.color_tema_preferido = act['Tema_preferido']
            else:
                raise 'Hubo un problema al intentar actualizar los datos. Intenta de nuevo más tarde.'

        except ErrorDesconocido as e:
            LoggerManager.obtener_logger_debug().exception(f'Hubo un error inesperado en {str(e)}')
            return traducir_texto(('An error ocurred', 'The data could not be updated. Please try again later'), user.idioma, (None))