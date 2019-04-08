# Author: Alfonso Soria Muñoz, Pedro Domenech
# Servidor y cliente en python para solicitar peticiones y manejar peticiones externas.

#Importaciones:
from recomendador_basico import RecomendadorBasico
import requests 				#para hacer peticiones HTTP
import json                                     #para trabajar con JSON
from http.server import  BaseHTTPRequestHandler, HTTPServer #para atender y manejar peticiones HTTP
from collections import deque                   #Usaremos una cola en la clase ClientePeticiones
from urllib.parse import urlparse                   #para parsear los componentes del get

# query_components = { "imsi" : "Hello" }
#import conect
#import recomendador_basico


#######################################
# VARIABLES GLOBALES DE CONFIGURACIÓN #
#######################################
HOST_NAME           = "localhost"
SERVER_PORT         = 80
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
        myHandler._db=self._db
        server = HTTPServer((HOST_NAME, SERVER_PORT), myHandler)
        server.serve_forever()

"""
Clase que maneja las peticiones de nuestro servidor HTTP
"""
class myHandler(BaseHTTPRequestHandler):
    #Resuelve las peticiones GET
    def do_GET(self):
        #Creamos respuesta de cabecera estandar (protocolo http)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        #parseamos los campos del get y los transformamos a un diccionario manejable.
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        #Aqui encapsulamos la respuesta al cliente
        jsonResponseDict = {}
        jsonResponseDict["error"]=0
        #Comenzamos a leer los paramentros
        """
        parametros get aceptados:
        - idUsuario: Id de usuario a quien se le va a recomendar
            - Si no se da este parámetro, devuelve "error" + "msg_error"
        - topk: Devuelve solo los mejores K elementos, si no existe el parámetro devuelve todos ordenados. Si topK es negativo, devuelve los “k peores”
        - kvecinos: Realiza la recomendación con los Kvecinos dados. Si no existe el parametro la realiza con Kvecinos que tenga por defecto el recomendador
        """
        topKparam = 0
        kVecinosParam = CANT_KVECINOS_SR
        idUsuarioParam = -1
        #Comprobamos que existe en el get "idUsuario" si no, devolvemos error.
        if "idUsuario" not in query_components:
            jsonResponseDict["error"]=1
            jsonResponseDict["msg_error"]="No se obtuvo el ID de usuario en la petición (idUsuario)"
            self.wfile.write(json.dumps(jsonResponseDict))
            return

        #Asignamos ID usuario
        idUsuarioParam = int(query_components["idUsuario"])
        #Comprobamos que existe topK y si es asi se lo asignamos. Si topk < 0 se cogeran los k peores problemas
        if "topk" in query_components:
            topKparam = int(query_components["topK"])
        #Comprobamos que existe kvecinos y si es asi se lo asignamos.
        if "kvecinos" in query_components:
            kVecinosParam = int(query_components["kvecinos"])


        recomendador  = RecomendadorBasico(self._db)
        recomendacion = recomendador.recomendar(idUsuarioParam,kVecinosParam)
        i=0
        #Aqui basicamente iteramos los k mejores o todos para guardarlos en un json que devolveremos
        arrayTopK = []
        reverse = False
        if topkparam == 0:
            i = 1
        if topKparam < 0:
            topKparam = -topKparam
            reverse = True

        if not reverse:
            for idproblema, valor in recomendacion:
                if i == topKparam:
                    break
                dictData = {}
                dictData["problemaID"]=idproblema-100
                dictData["valor"]=valor
                arrayTopK.append(dictData)
                i = i + 1
        else:
            #TODO, NO TESTEADO REVERSED PARA COMO REPRESENTA LOS DATOS AQUI
            for idproblema, valor in reversed(recomendacion):
                if i == topKparam:
                    break
                dictData = {}
                dictData["problemaID"]=idproblema-100
                dictData["valor"]=valor
                arrayTopK.append(dictData)
                i = i + 1
        jsonResponseDict["recomendacion"] = arrayTopK
        self.wfile.write(json.dumps(jsonResponseDict))
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
                    print(resultados["msg_error"])
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
