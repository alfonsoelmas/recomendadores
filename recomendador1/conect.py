#Acceso a bbdd
#Instalar MySQLdb para acceder a bases de datos
import pymysql
import numpy as np


class JuezDB:
        def __init__(self):
                db = pymysql.connect('localhost', 'root', '', 'aceptaelreto')
                self.cursor = db.cursor()

        #Metodo obtener usuarios. Devuelve un array con id de usuarios
        def obtenerUsuarios(self):
                recs = self.cursor.execute('SELECT id FROM users')
                listaUsers = np.empty([recs])
                i=0
                for row in self.cursor.fetchall():
                        listaUsers[i] = row[0]
                        i=i+1
                return listaUsers

#Programa principal (Main)
conector = JuezDB()
conector.obtenerUsuarios()
