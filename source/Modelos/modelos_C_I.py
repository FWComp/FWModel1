from flask import jsonify
from Herramientas import Tools
from FireBaseControl import Objetos_firebase
from flask import flash

DBStore = Objetos_firebase.objeto_firestore()
DBRealTime = Objetos_firebase.objeto_realtimedb()
Storage = Objetos_firebase.objeto_storage()

class Modelo_C:
    @classmethod
    def extraer_personajes(cls, lista):
        data = []
        for personaje, valores in lista.items():
                doc_personaje = DBStore.document(f'personajes/{personaje}').get()
                if doc_personaje.exists:
                    personaje_datos = doc_personaje.to_dict()
                    data.append(personaje_datos)       
        if data:
            return data
        return None

    @classmethod
    def eliminar(cls, id, user_id, diccionario):
        try:
            # Eliminar el personaje de la colección 'personajes'
            doc_personaje = DBStore.collection('personajes').document(id)
            doc_personaje.delete()

            # Obtener y actualizar el documento del usuario
            doc_usuario = DBStore.collection('usuarios').document(user_id)

            diccionario_nuevo = diccionario
            # Eliminar la referencia al personaje en el diccionario de personajes del usuario
            diccionario_nuevo.pop(id, None)
            doc_usuario.update({'Personajes': diccionario_nuevo})
            
            flash(['¡Bien!', 'Se ha eliminado a tu personaje correctamente.'])
            return diccionario_nuevo
        except Exception as e:
            print(e)
            # Manejar otras excepciones según sea necesario
            flash(['Vaya...', 'Lo sentimos, no se pudo eliminar a tu personaje.'])
                    

class Modelo_I:

    @classmethod
    def obtener_item_id(cls, id):
        referencia_item = DBRealTime.child(f'Items/{id}')
        item = referencia_item.get()
        return item