from Herramientas import Tools
import random
import re

class Item:
    def __init__(self, data, info, personaje_instancia, id):
        self.personaje_instancia = personaje_instancia

        if isinstance(info, list):
            self.cantidad = info[1]
            self.equipado = True if info[0] == 'equipped' else False
        else:
            self.cantidad = info
            self.equipado = False

        self.ID = id
        self.Nombre = data.get('Nombre', None)
        self.Tipo = data.get('Tipo', None)
        self.Compatibilidad = data.get('Compatibilidad', None)
        self.EquipableEn = data.get('EquipableEn', None)
        self.Max_Stock = data.get('Acumulable', 1)
        self.Consumible = data.get('Consumible', False)
        self.Equipable = data.get('Equipable', False)
        self.Fabricable = data.get('EsFabricable', False)
        self.NivelReq = data.get('NivelRequerido', 1)
        self.Rareza = data.get('Rareza', 'comun')
        self.Genero = data.get('Genero', 'unisex')
        self.Precio = data.get('Precio', 10)
        self.Devolucion = data.get('Devolucion', 0)
        self.Objetivo = data.get('Objetivo', None)
        self.NumeroObjetivos = data.get('NumObjetivos', 1)
        self.SoloUsableCuando = data.get('SoloUsableCuando', None)
        self.Diccionario = data.get('DICCIONARIO', None)

        self.MetaDatos = data.get('MetaDatos', None)
        self.Efectos = data.get('Efectos', None)
        self.SoloUsableEn = data.get('SoloUsableEn', None)
        self.Invocaciones = data.get('Invocaciones', None)
        self.Fabricacion = data.get('Fabricacion', None)
        self.Devolver = data.get('Devolver', None)

        self.RequisitosAdd = data.get('RequisitosAdicionales', None)

        self.Eventos = data.get('Eventos', None)

        # CONSTRUCTOR DE FLUJO.
        self.stop = False #NOTE Bandera de STOP
        self.print_message = None
        self.construct = {}
        self.evento_target = None

        # Manejador de Errores
        self.error_message = ''
        self.event_stop_message = ''
        self.ERROR_PRIMARY = ''

        self.Data = data.get('AlUsarse', None)

    def eliminar(self, quantity):
        self.cantidad = max(0, self.cantidad - quantity)
        if self.cantidad == 0:
            return True
        return False

    # FLUJOS DE USAR y Equipar

    def Usar(self, Flujo):
        if not self.Data:
            return
        elif self.cantidad == 0:
            self.personaje_instancia.eliminar_item(self, 1)
            return
        
        for flujo, llamadas in Flujo.items(): # Flujo del dato AlUsarse y eventos de Evento.
            self.desenvolver_flujo(flujo, llamadas) # Mandar Flujo y Llamadas (Lista o String)

    def desenvolver_argumento_string(self, string):
        mensaje = string
        patron = r'\{([^\}]*)\}'
        patrones_encontrados = re.findall(patron, string)
        try:
            for reemplazable in patrones_encontrados:
                if '.' in reemplazable:
                    command, arg = reemplazable.split('.')
                    inst = self.GET(command, True)
                    llamable = getattr(inst, arg)
                    mensaje = mensaje.replace('{' + reemplazable + '}', f'{str(llamable)}')
                else:
                    if self.construct['GET']:
                        llamable = getattr(self.construct['GET'], reemplazable)
                        mensaje = mensaje.replace('{' + reemplazable + '}', f'{str(llamable)}')
        except Exception as e:
            print(e)
            return
        
        return mensaje

    def desenvolver_flujo(self, flujo, eventos_llamadas):
        if flujo == 'IF': #NOTE Un comprobador de FLUJO.
            eventos_llamadas = eventos_llamadas if isinstance(eventos_llamadas, list) else [eventos_llamadas]  #NOTE Convertir en una lista si no es una lista
            CallNotFound = next((llamada for llamada in eventos_llamadas if llamada not in self.Eventos), None) #NOTE Buscar si falta un Evento

            if CallNotFound: # NOTE: Retornar si hay una llamada que no existe en los eventos.
                message = f'No se encontró el evento {CallNotFound} llamado en el flujo'
                self.error_message = message
                return
            
            for evento in eventos_llamadas: # Mandar el flujo del evento completo desde self.Eventos
                self.generar_evento(self.Eventos[evento])

                if self.stop == True: # Si el evento funcionó pero no era lo esperado.
                    print(self.event_stop_message)
                    print('Corriendo ElSE')
                    # Correr ELSE
                
                elif self.stop == None: # Si hubo un error interno
                    print(self.ERROR_PRIMARY)
                    print(self.error_message)
                    print('Deteniendo Flujo')
                    return
                
        elif flujo == 'ELSE' and self.stop == True: # Flujo Else, en caso de que el IF no haya terminado su flujo.
            #REVIEW -  Implementar el flujo ELSE del documento JSON.
            pass

    def generar_evento(self, evento):
        # NOTE: RESET
        self.construct = {}
        self.FINALCOMMAND = False
        self.stop == False

        for comando, argumento in evento.items():
            self.evento_target = evento
            self.desenvolver_evento(comando, argumento)
            self.evento_target = None
            if self.stop and self.event_stop_message:
                self.ERROR_PRIMARY = f'No se pudo cumplir el evento "{evento}"' if self.stop == None else None
                return
        

    def GET(self, argumento, call_on_struct_string = False):
        if argumento.lower() == 'usuario':
            self.construct['GET'] = self.personaje_instancia
            return True
        else:
            transformar_a_llamable = getattr(self.personaje_instancia, argumento, None)
            try:
                if callable(transformar_a_llamable):
                    if call_on_struct_string:
                        return transformar_a_llamable()
                    self.construct['GET'] = transformar_a_llamable()
                    return True
                else:
                    message = 'No se pudo generar el metódo.'
                    self.error_message = message
                    self.stop = None
                    return
            except Exception as e:
                message = f'Error en el metódo {argumento}. No existe el metódo o el atributo llamado.\n\nError en: {str(e)}'
                self.error_message = message
                self.stop = None
                return 

    def desenvolver_evento(self, comando, argumento):
        comando = comando.lower()
        if 'print' == comando:
            self.print_message = argumento

        if self.FINALCOMMAND and not comando in ['PRINT', "RETRASO"]:
            message = 'Después de RUN no puede haber más comandos. Solamente PRINT y RETRASO para el manejo de mensajes.'
            self.error_message = message
            self.stop = None
            return

        if comando == 'get':
            state = self.GET(argumento)
            if not state:
                return
        
        if comando == 'objetivo': # Usado para items.
            OBJETIVOS = []
            if argumento == 'get': # Especialmente usado para entidades
                if self.construct['GET']:
                    self.construct['Objetivo'] = self.construct['GET']
                else:
                    message = 'No se encontró un comando GET en el evento.'
                    self.error_message = message
                    self.stop = None
                    return
                    
            objetivos = argumento if isinstance(argumento, list) else [argumento]
            for objetivo in objetivos: 
                if self.construct['GET']:
                    if objetivo in self.construct['GET'].Inventario:
                        OBJETIVOS.append(self.construct['GET'].Inventario)
                        self.construct['Objetivo'] = OBJETIVOS
                    else:
                        message = f'El objeto {objetivo} no existe en el inventario de {self.construct["GET"].Nombre}'
                        self.event_stop_message = message
                        self.stop = True
                        return
                else:
                    message = 'No se encontró un comando GET en el evento.'
                    self.error_message = message
                    self.stop = None
                    return

        if comando == 'run':
            self.FINALCOMMAND = True
            # FINAL DEL EVENTO
            transformar_a_llamable = getattr(self.construct['GET'], argumento[0].lower())
            if callable(transformar_a_llamable):
                try:
                    arg = None
                    if argumento[1] == '{MetaDatos}':
                        arg = self.desenvolver_metadatos()
                    elif argumento[1] == 'THIS':
                        arg = self.ID

                    resultado = transformar_a_llamable(
                        argumento[1:] if not arg else arg
                    )
                
                    if self.print_message:
                        self.PRINT()

                except Exception as e:
                    message = f'Error en el metódo {argumento}. No existe el metódo o el atributo llamado.\n\nError en: {str(e)}'
                    self.error_message = message
                    self.stop = None
                    return
            else:
                self.stop = None
                self.error_message = 'No se pudo generar el metódo'
                return
        
    def desenvolver_metadatos(self):
        Args_list = []
        Args_dict = {}
        MetaType = None
        for elemento, valor in self.MetaDatos.items():
            if elemento.lower() in ['envenenamiento', 'quemadura', 'congelamiento', 'maldicion', 'paralisis', 'nauseas']:
                if MetaType == 'plus':
                    message = 'No se puede manejar un evento que proporcione efectos cómo plus. Intenta crear otro evento.'
                    self.error_message = message
                    self.stop = None
                    return
                
                MetaType = 'efecto'
                listado = valor if isinstance(valor, list) else [valor]
                Args_list.extend(f'{elemento}_{objeto}' for objeto in listado)

            elif elemento.lower() in ['ataque', 'defensa', 'ps', 'exp', 'pm', 'agilidad', 'oro']:
                    if MetaType == 'efecto':
                        message = 'No se puede manejar un evento que proporcione efectos cómo plus. Intenta crear otro evento.'
                        self.error_message = message
                        self.stop = None
                        return

                    MetaType = 'plus'
                    Args_dict[Tools.Limpiar(elemento.lower())] = valor if isinstance(valor, int) else random.choice(valor)

            else:
                message = f'No se encontró el metadato {elemento}'
                self.error_message = message
                self.stop = None
                return None

        return Args_list if MetaType == 'efecto' else Args_dict
    
    def PRINT(self):
        for instance, messages in self.print_message.items():
            mensajes = messages if isinstance(messages, list) else [messages]
            for mensaje in mensajes:
                args = self.desenvolver_argumento_string(mensaje)
                print(args)



                        
                    
        
            

            


                




