from flask import jsonify
from Herramientas import Tools
from FireBaseControl import Objetos_firebase

DBStore = Objetos_firebase.objeto_firestore()
DBRealTime = Objetos_firebase.objeto_realtimedb()
Storage = Objetos_firebase.objeto_storage()

class Modelo_C:
    @classmethod
    def extraer_personajes(usuario, lista):
        for ID in lista:
            constructor = f'{usuario}_{ID}'
            document_personaje = DBStore.document(f'personajes/{constructor}').get()

            if document_personaje.exists:
                documento = document_personaje.to_dict()
                return documento['Info'], documento['Estatus'], documento['Poderes'], documento['Inventario'], documento['Nombre']
            else: None
            

class Modelo_I:
    pass