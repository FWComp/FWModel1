from flask_login import UserMixin
import random
import asyncio

from ..modelos_uci import Modelo_C

class Usuario(UserMixin):
    def __init__(self, ID, Apellido, Nombre, Registro, Estado, personajes = [], Email = '', Telefono = ''):
        print(personajes)
        self.ID = ID
        self.Apellido = Apellido
        self.Nombre = Nombre
        self.Email = Email
        self.Registro = Registro
        self.Tel = Telefono
        self.current_character = None
        self.Personajes = personajes if personajes else []
        self.Estado = Estado
        self.Eliminada = False
        
        self.Instancia_Personajes = {}

        # SECTION: LLamadas

        self.obtener_personajes()

        # !SECTION

    def obtener_personajes(self):
        if self.Personajes and self.Estado == 'JJJJ':
            personajes_info = Modelo_C.extraer_personajes(self.ID, self.Personajes)
            for personaje in personajes_info:
                Instancia = Personaje(personaje[0], personaje[1], personaje[2], personaje[3], personaje[4]) #Info, Estatus, Poderes, Inventario, ID/Nombre
                if Instancia:
                    self.Instancia_Personajes[personaje[4]] = Instancia # Nombre/Id del personaje.

    def get_id(self):
        if self.Eliminada:
            return None
        return self.ID

    def is_authenticated(self):
        if self.Estado != 'Banned':
            return True
        return False
    
    def Instancia(self):
        return self
    
    def EliminarInstancia(self):
        self.Eliminada = True

    
class Personaje:
    def __init__(self, Info, Estatus, Poderes, Inventario, id):
        self.ID = id
        print(self.ID)
        
                