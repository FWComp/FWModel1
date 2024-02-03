from firebase_admin import initialize_app, credentials, firestore, db, storage, get_app
import os
import json

# Sección para la gestión de Firebase

# Definición de excepciones personalizadas
class InitializationError(Exception):
    pass

class FirebaseDBError(Exception):
    pass

# Clase principal para la gestión de Firebase
class FireBase:
    _initialized = False

    try:
        # Inicialización de Firebase solo si no está inicializado previamente
        if not _initialized:
            with open("source/fw-comm-firebase-adminsdk-qgb36-64b3d8994d.json") as json_cred:
                cred = credentials.Certificate(json.load(json_cred))
                initialize_app(cred)
                _initialized = True

                # Inicialización de instancias adicionales para Realtime Database y Storage
                initialize_app(cred, options={'databaseURL': os.getenv('RealTimeDBEURL')}, name='realtime')
                initialize_app(cred, options={'storageBucket': os.getenv('StorageDBURL')}, name='storage')

                # Instancias de Firestore, Realtime Database y Storage
                DB_fs = firestore.client()
                DB_rtdb = db.reference(app=get_app(name='realtime'))
                Storage = storage.bucket(app=get_app(name='storage'))
    except Exception as e:
        raise InitializationError(f'Error en la inicialización de Firebase. Detalles: {str(e)}')

# Fin de la sección de Firebase

# Clase que hereda de FireBase y proporciona métodos para obtener instancias de Firestore, Realtime Database y Storage
class FB(FireBase):
    try:
        @classmethod
        def objeto_firestore(cls):
            if not getattr(cls, 'DB_fs', None):
                raise FirebaseDBError('Firestore no inicializado. Asegúrate de que Firebase esté configurado correctamente.')
            return cls.DB_fs

        @classmethod
        def objeto_realtimedb(cls):
            if not getattr(cls, 'DB_rtdb', None):
                raise FirebaseDBError('Realtime Database no inicializado. Asegúrate de que Firebase esté configurado correctamente.')
            return cls.DB_rtdb

        @classmethod
        def objeto_storage(cls):
            if not getattr(cls, 'Storage', None):
                raise FirebaseDBError('Storage no inicializado. Asegúrate de que Firebase esté configurado correctamente.')
            return cls.Storage
    except Exception as e:
        raise FirebaseDBError(f'Error al obtener el objeto de Firebase. Detalles: {str(e)}')
