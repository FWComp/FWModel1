from FireBaseControl import FB
from Herramientas.Tools import obtener_fecha, LoggerManager
from Herramientas.Excepts import ErrorEliminarPersonaje

class Modelo_C:
    @classmethod
    def extraer_personajes(cls, lista):
        """
        Extrae información detallada de los personajes dados en la lista.

        Parameters:
        - lista (dict): Un diccionario de personajes con sus valores asociados.

        Returns:
        - list: Una lista con los datos de los personajes.
        """
        data = []
        for personaje, valores in lista.items():
            doc_personaje = FB.objeto_firestore().document(f'personajes/{personaje}').get()
            if doc_personaje.exists:
                personaje_datos = doc_personaje.to_dict()
                data.append(personaje_datos)

        return data if data else None

    @classmethod
    def eliminar(cls, id, user_id, diccionario):
        """
        Elimina un personaje de la base de datos y actualiza el diccionario de personajes del usuario.

        Parameters:
        - id (str): El ID del personaje a eliminar.
        - user_id (str): El ID del usuario al que pertenece el personaje.
        - diccionario (dict): El diccionario de personajes del usuario.

        Returns:
        - dict: El diccionario actualizado de personajes del usuario.
        """
        try:
            # Eliminar el personaje de la colección 'personajes'
            doc_personaje = FB.objeto_firestore().collection('personajes').document(id)
            doc_personaje.delete()

            # Obtener y actualizar el documento del usuario
            doc_usuario = FB.objeto_firestore().collection('usuarios').document(user_id)

            # Eliminar la referencia al personaje en el diccionario de personajes del usuario
            diccionario.pop(id, None)
            doc_usuario.update({'Personajes': diccionario})

            return diccionario
        except ErrorEliminarPersonaje as e:
            LoggerManager.obtener_logger_debug().exception(f'Hubo un error al intentar eliminar el personaje {id} de {user_id}.\n\nErro en: {str(e)}\n\n[ - - Fecha: {obtener_fecha()} - -]')
            raise f'Hubo un error al intentar eliminar el personaje. Intenta de nuevo más tarde.'



class Modelo_I:
    @classmethod
    def obtener_item_id(cls, id):
        """
        Obtiene la información de un ítem con el ID proporcionado.

        Parameters:
        - id (str): El ID del ítem.

        Returns:
        - dict: La información del ítem.
        """
        referencia_item = FB.objeto_realtimedb().child(f'Items/{id}')
        item = referencia_item.get()
        return item
