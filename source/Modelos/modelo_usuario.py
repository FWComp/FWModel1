from flask import jsonify
from Herramientas import Tools
from FireBaseControl import Objetos_firebase
from .Entidades import Usuario

DBStore = Objetos_firebase.objeto_firestore()
DBRealTime = Objetos_firebase.objeto_realtimedb()
Storage = Objetos_firebase.objeto_storage()

class Modelo_U:

    usuario = None

    @classmethod
    def usuario_existe(cls, id):
        if isinstance(id, str):
            return True if DBStore.document(f'usuarios/{id}').get().exists else False

    @classmethod
    def verificar_usuario(cls, nombre, passwrd):
        documento_usuario = DBStore.document(f'usuarios/{nombre}').get()

        if documento_usuario.exists:
            data = documento_usuario.to_dict()
            if data['Contraseña']:
                if Tools.check_password(data['Contraseña'], passwrd):
                    cls.usuario = Usuario.Usuario(
                        ID = nombre,
                        Nombre = data['Nombre'],
                        Apellido = data['Apellido'],
                        Email = data['Correo'],
                        Estado = data['Estado'],
                        personajes = data['Personajes'],
                        Registro = data['Registro'],
                        Telefono = data['Telefono']
                    )
                    return cls.usuario
                else:
                    return False
            else:
                return False #REVIEW Manejar error de manera más robusta después
        return None

    @classmethod
    def crear_cuenta(cls, datos):
        nombre_completo = f'{datos[0]} {datos[1]}'

        #NOTE -  Verificar si el usuario existe.
        doc_verificacion_usuario = DBStore.document(f'usuarios/{nombre_completo}')
        if doc_verificacion_usuario.get().exists:
            return False
        
        doc = {
            "Nombre": datos[0],
            "Apellido": datos[1],
            "Contraseña": Tools.create_password(datos[2]),
            "Registro": Tools.fecha(),
            "Personajes": [],
            "Correo": None,
            "Telefono": None,
            "Estado": "Normal"
        }

        DBStore.document(f'usuarios/{nombre_completo}').set(doc)
        return cls.verificar_usuario(nombre_completo, datos[2]) #Nombre, Contraseña. Retorno: Instancia, None

    @classmethod
    def crear_personaje(cls, Nombre, Edad, Genero, orientacion, clase):
        weapons = {
            'Assassing': 'Bokken',
            'Tank': 'Small Maze',
            'warrior': 'Small Sword'
        }

        weapon = weapons.get(clase)

        if not weapon:
            # La clase no tiene un arma asociada
            return False

        # Verificar límite de personajes y si el usuario ya tiene el personaje
        if cls.usuario.Personajes and len(cls.usuario.Personajes) >= 2 and Nombre in cls.usuario.Personajes:
            return False

        try:
            # Acceder a la información de la clase desde la base de datos
            referencia_clase = DBRealTime.child(f'Class/levels/{clase}/1')
            Estatus = referencia_clase.get()

            if Estatus is None:
                # El nodo no existe
                return False

            # Crear documentos para el personaje
            docInfo = {
                'Nombre': Nombre,
                'Edad': Edad,
                'Genero': Genero,
                'Orientacion': orientacion,
                'Clase': clase,
                'Registro': Tools.fecha()  # Suponiendo que Tools.fecha() devuelve un objeto datetime
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
                'Herb': 5,
                'Antidote': 2,
                weapon: ['equipped', 1]
            }

            docPoderes = {
                poder: 'Aprendido en nivel 1' for poder in Estatus.get('Learn', [])
            }

            # Actualizar Personajes de Usuario.
            doc_usuario = DBStore.collection('usuarios').document(cls.usuario.ID)
            personajes = cls.usuario.Personajes
            nuevo_personaje = {f'{cls.usuario.ID}_{Nombre}': [Tools.fecha(), Nombre]}
            personajes.append(nuevo_personaje)

            # Actualizar el campo 'Personajes' con la lista actualizada
            doc_usuario.update({'Personajes': personajes})

            # Crear el personaje.
            id_personaje = f'{cls.usuario.ID}_{Nombre}'  # Asegurar ID único
            doc_verificacion_usuario = DBStore.document(f'personajes/{id_personaje}')
            
            doc_personaje = {
                "Nombre": Nombre,
                "Info": docInfo,
                "Estatus": docEstatus,
                "Poderes": docPoderes,
                "Inventario": docInventario,
            }

            # Insertar el documento del personaje en Firestore
            doc_verificacion_usuario.set(doc_personaje)

            return True
        except Exception as e:
            # Manejar la excepción o simplemente dejar que se propague
            raise e


    @classmethod
    def Eliminar(cls):
        cls.usuario = None