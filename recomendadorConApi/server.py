# Author: Alfonso Soria Muñoz, Pedro Domenech
# Servidor y cliente en python para solicitar peticiones y manejar peticiones externas.

#Importaciones:
import requests 				#para hacer peticiones HTTP
import json                                     #para trabajar con JSON
from http.server import  BaseHTTPRequestHandler, HTTPServer #para atender y manejar peticiones HTTP
from collections import deque                   #Usaremos una cola en la clase ClientePeticiones
#import conect
#import recomendador_basico


#######################################
# VARIABLES GLOBALES DE CONFIGURACIÓN #
#######################################
SERVER_PORT         = 5050
CANT_KVECINOS_SR    = 100

#Obtencion JSON para actualizar recomendadorDB
#LINK_JSON          = TODO, DE MOMENTO NO LO VAMOS A TRANSFORMAR COMO VARIABLE GLOBAL DE CONFIGURACION
#PARAMETROS_JSON    = LO MISMO QUE EL ANTERIOR COMENTARIO DE ARRIBA

"""
======================
======================
FIN VARIABLES GLOBALES
======================
======================
"""



"""
Clase que acogera al servidor
Crea un servidor en el puerto
"""
class http_server:
    def __init__(self, db):
        self._db = db
        server = HTTPServer(('', SERVER_PORT), myHandler)
        server.serve_forever()

"""
Clase que maneja las peticiones de nuestro servidor HTTP
"""
class myHandler(BaseHTTPRequestHandler):
    #Resuelve las peticiones GET
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # TODO:
        # CAMPOS QUE RESUELVE EL GET:
        # KVECINOS: Indica la configuracion de similitud KVECINOS con los que llamar al recomendador
        # KMEJORES: Solicita los K problemas más similares, si K mejores < 0 solicitará los K menos similares, si == 0 devuelve T0D0
        # 
        # Hacer lo que queramos con la petición...
        # SI ISSET KVECINOS: Llamarlo con ese set siempre que comprenda entre 2 y 10mil
        # Else: Llamarlo con KVECINOS = 100
        """
        Obtener del GET lo que pida y ver como lo devolvemos
        """
        recomendador  = RecomendadorBasico(self._db)
        recomendacion = recomendador.recomendar(usuario,CANT_KVECINOS_SR)
        return

"""
Class server recomendador
Actúa como cliente de peticiones GET a aceptaelreto para obtener las últimas entregas y actualizarse
Actúa como servidor para ejecutarse en segundo plano
"""
class ClientePeticiones:
        """
        Crea la clase conect y la inicializa
        Actualiza la clase conect con las nuevas entregas que haya habido
        Posteriormente, crea el servidor HTTP para recibir solicitudes GET de clientes
        """
        def __init__(self, db):
            #Creamos la clase que gestiona los datos de la recomendación
            self._db = db
            #Actualizamos los últimos envíos
            self._actualizarUltimosEnvios()


        """
        Este método se encarga de esperar a que aceptaelreto le responda, si es asi, actualiza los ultimos envios
        A modo de canal de escucha que se queda esperando hasta que aceptaelreto quiera responder.
        """
        def _esperarNuevaRespuesta(self):
            # TODO
            return -1
            
        """
        Actualiza los ultimos envíos.
        Obtiene el último que tenía nuesta clase conect y se pone a actualizarla hasta la última información
        que tenía.
        *TODO: Quizas habría que bloquear el metodo "recomendar" cada vez que este se llame usando MUTEX en python...
        """
        def _actualizarUltimosEnvios(self):
            ultimoSubmitRecomender = self._db.lastSubmition
            
            resultados={}
            req = requests.get('https://www.aceptaelreto.com/ws/submission/')
            while '"submission":[' not in req.text:
                print("Error al conectarse con el juez en línea para obtener nuevas entregas: \n")
                print(req.text)
                print("\nREINTENTANDO...")
                req = requests.get('https://www.aceptaelreto.com/ws/submission/')
                
            resultados = json.loads(req.text)   #Lo transformamos a un objeto JSON
            resultados["error_get"]=0
            # Ultimo submit que hemos obtenido, lo metemos al final de la funcion en la clase conect
            actualizadorUltimoSubmit = resultados["submission"][0]["num"] #Luego actualizamos en db
            print("actualizamos a ultimo submit\n")
            # Vamos a iterar hasta encontrar el que teniamos previo
            j = 0
            enc = False
            colaDeDatos = deque()
            while not enc:
                if resultados["error_get"] == 0:
                    for i in resultados["submission"]:
                        if i["num"] == ultimoSubmitRecomender:
                            enc = True
                            break
                        else:
                            #Actualizamos
                            userId = i["user"]["id"]
                            problemId = i["problem"]["num"] #TODO: no se si se corresponde al ID original
                            estadoString = i["result"]
                            estado = 0
                            if estadoString == "AC":
                                estado = 1

                            dictData = {}
                            dictData["userID"]      = userId
                            dictData["problemPos"]  = problemId-100 #TODO, creo que corresponde a la posicion del problema ya parseado, pero restandole 100 o algo así (El external ID)
                            dictData["estado"]      = estado
                            colaDeDatos.appendleft(dictData)

                else:
                    print("No se han cargado las entregas debido al siguiente error obtenido del servidor: ")
                    print(data["msg_error"])
                    print("\nREINTENTANDO SOLICITUD: "+str(j))
                j = j + 1
                resultados = self._obtener20entregas(j)
                print("Cargar de web siguientes 20 entregas: "+str(j*20+1)+" de "+str(actualizadorUltimoSubmit-ultimoSubmitRecomender))

            l = list(colaDeDatos)
            self._db.actualizarEntregas(l,actualizadorUltimoSubmit)

                

        #Obtiene las 20 entregas de la posicio "posicion"*20+1 (Desplazamiento) y devuelve un objeto XML tree como resultado
        def _obtener20entregas(self, posicion):
                req = requests.get('https://www.aceptaelreto.com/ws/submission/?start='+str(posicion*20+1)+'&size=20')
                resultados = {}
                resultados["error_get"] = 0
                #Obtenemos un JSON en texto
                if '"submission":[' not in req.text: #Esto es ajustado a lo que leemos de aceptaelreto pero el json o xml de otro juez en línea será diferente por lo que habría que hacerlo adaptable en unas variables de config.
                    resultados["error_get"] = 1      #En otras lineas de este archivo tambien nos ocurre lo mismo que en este if
                    resultados["msg_error"] = req.text
                else:
                    resultados = json.loads(req.text)   #Lo transformamos a un objeto
                    resultados["error_get"] = 0 
                return resultados
