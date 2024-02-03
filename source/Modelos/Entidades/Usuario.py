from flask_login import UserMixin
import random
import asyncio
from Herramientas.Tools import limpiar_y_convertir_a_pascal_case
from .Items import Item

from ..modelos_C_I import Modelo_C, Modelo_I

class Usuario(UserMixin):
    def __init__(self, ID, Apellido, Nombre, Registro, Estado, personajes = {}, Email = '', Telefono = '', Theme_color = 'Default', Panel_song = [1.0, True, 'Default'], ONLSTT = 'show', hiddes = [False, False, False, False], others = None, idioma = 'en'):
        self.ID = ID
        self.Apellido = Apellido
        self.Nombre = Nombre
        self.correo = Email
        self.Registro = Registro
        self.telefono = Telefono
        self.color_tema_preferido = Theme_color
        self.musica_del_panel = Panel_song
        self.estado_en_linea = ONLSTT #
        self.ocultos = hiddes # ocultar region, ocultar correo, ocultar telefono, ocultar perfil
        self.otros = others # cumpleaños, edad, genero, orientación, región
        self.photo = None

        # Personajes
        self.current_character = None
        self.Personajes = personajes if personajes else {}

        # Banderas de seguimiento
        self.idioma = idioma
        self.Estado = Estado
        self.Eliminada = False
        self.seguimiento = False
        self.Instancia_Personajes = {}

        # SECTION: LLamadas

        self.cargar_personajes()

        # !SECTION

    def cargar_personajes(self):
        try:
            if self.Personajes:
                personajes_data = Modelo_C.extraer_personajes(self.Personajes)
                if personajes_data:
                    for personaje_data in personajes_data:
                        # Crear una instancia de Personaje
                        nueva_instancia = Personaje(
                            personaje_data['Info'],
                            personaje_data['Estatus'],
                            personaje_data['Poderes'],
                            personaje_data['Inventario'],
                            f"{self.ID}_{personaje_data['Nombre']}" # Identidicador
                        )
                        
                        # Asignar la instancia al diccionario usando el nombre/ID del personaje como clave
                        self.Instancia_Personajes[f'{self.ID}_{personaje_data["Nombre"]}'] = nueva_instancia
        except Exception as e:
            raise e
        
    def eliminar_personaje(self, id):
        nuevo_diccionario = Modelo_C.eliminar(id, self.ID, self.Personajes)
        self.Personajes = nuevo_diccionario
        self.Instancia_Personajes = {}
        self.cargar_personajes()


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
    
    def usar_personaje(self, id):
        self.current_character = self.Instancia_Personajes[id]


    
class Personaje:
    def __init__(self, Info, Estatus, Poderes, Inventario, id): # Optimizar código: recursividad, documentación, adición, definición

        #REVIEW - INFO hecho, Estatus hecho, Poderes faltante, Inventario a medias.
        # print(Estatus)
        # print(Poderes)
        # print(Inventario)
        # print(Info)
        self.ID = id
        self.Genero = Info['Genero']
        self.Edad = Info['Edad']
        self.Nombre = Info['Nombre']
        self.Orientacion = Info['Orientacion']
        self.Clase = limpiar_y_convertir_a_pascal_case(Info['Clase'])
        self.Registro = Info['Registro']
        
        self.Oro = 0
        self.Nivel = Estatus['Nivel']
        self.PS = Estatus['PS']
        self.PM = Estatus['PM']
        self.EXP = Estatus['EXP']
        self.Defensa =Estatus['Defensa']
        self.Ataque = Estatus['Daño']
        self.Agilidad = Estatus['Agilidad']

        self.objetivo = self

        self.efectos = {'envenenamiento_1': ['INSTANCIA']} # Prueba, #REVIEW -  Diseñar la plantilla de efectos y subirlo a Firebase RT.
        
        self.Equipamiento = {
            'Arma': [self.Clase, self.Orientacion],
            'Escudo': None,
            'Cabeza': None,
            'Botas': None,
            'Torso': None,
            'Piernas': None,
        }

        self.Inventario = {

        }

        self.Aliados = {
            self.Nombre: self
        }

        self.obtener_items(Inventario)

    def obtener_items(self, Inventario):
        for item, info in Inventario.items():
            data = Modelo_I.obtener_item_id(item)
            ItemInstancia = Item(data, info, self, item)
            self.Inventario[ItemInstancia.ID] = ItemInstancia
    
    def puntero(self):
        return self

    def eliminar_item(self, id, cantidad = 1):
        try:
            estado = self.Inventario[id].eliminar(cantidad)
            if estado:
                self.Inventario.pop(id, None)
        except Exception as e:
            print('Error ')
            print(e)


    def quitar_efecto(self, efectos):
        num = []
        for efecto in efectos:
            if efecto in self.efectos:
                self.efectos.pop(efecto, None)
                num.append(efecto)
        return num


        
                