#import recomendador_basico
#Ejecución de pruebas

"""
Pruebas de actualizacion de clase juezDB conect pidiendo desde server de clase clientePeticiones las nuevas
entregas. pruebas de actualizaciones y de carga de BBDD en memoria desde local y desde MySQL
"""

from conect import JuezDB
from server import ClientePeticiones
from server import http_server
from server import myHandler
db = JuezDB()
print("Conectada la BBDD y cargada")
cliente = ClientePeticiones(db)
print("cargada la BBDD al ultimo estado de entregas de la web - ¡fake, nos hemos saltado unas 40mil entregas!")
print("Activamos servidor...")
servidor = http_server(db)

"""
Ejecutamos nueva clase conect para generar matriz en local y probar su carga desde local, etc.
"""
"""
db = conect.JuezDB()
print(db.matrizDatos)
print(db._users)
print(db._problems)
"""

"""
Pruebas de funcionamiento recomendador:

Ejecuta el recomendador para k-vecinos = cada elemento de lista valores.
cada resultado de recomendación de toda la BBDD los guarda en diferentes TXT.
Realizado para el entrenamiento del recomendador.
"""
"""
import recomendador_basico
import conect
from time import time
s_t = time()
db = conect.JuezDB()
e_t = time() - s_t
recomendador  = recomendador_basico.RecomendadorBasico(db)
s_t = time()
a = recomendador.recomendar(847,100)
e_t = time() - s_t
print('U: '+ str(847) +'\n')
for idproblema, valor in a:
    #parseamos la pos del problema en su id con db.problems[pos]
    print(str(idproblema+100) +'='+ str(valor) +'\n')
    print("[time: "+ str(e_t) +"]\n")
"""


"""
Pruebas servidor HTTP y realizador peticiones HTTP
+
Pruebas con XML
"""
"""
import requests 				#para peticiones HTTP
import json
# ultimoSubmitRecomender = db._lastSubmition
ultimoSubmitAceptaelreto = 1
K = 300000
iterMax = 300000//20
j=0
while j < iterMax:
    req = requests.get('https://www.aceptaelreto.com/ws/submission/?start='+str(20*j+1)+'&size=20')#Obtenemos un JSON en texto
    resultados = json.loads(req.text)   #Lo transformamos a un objeto
    for i in resultados["submission"]:
        print(i["user"]["nick"] + " ha intentado: " + i["problem"]["title"] + "- ENVÍO: " + str(i["num"]))
    j = j + 1
# ANOTACION, SOLO PUEDO OBTENER LOS 41MIL ULTIMAS ENTREGAS.

"""


