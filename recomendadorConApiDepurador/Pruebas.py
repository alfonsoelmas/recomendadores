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

#Creamos diccionario de "nuevas entregas a actualizar"

#Se las pasamos  LA BBDD y vemos que hace