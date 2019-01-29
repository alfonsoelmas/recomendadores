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

        #Metodo obtener entregas validas de un determinado usuario - Todo (Comprobar correcto funcionamiento)
        def obtenerEntregasValidasDeUser(self, user):
                        #TODO MEJORAR CONSULTA PARA OBTENER SOLAMENTE LA MEJOR ENTREGA. ADEMAS METERLO EN UNA MATRIZ DE 2 COLUMNAS POR N FILAS. CADA FILA[0] SERA ID DEL PROBLEMA, FILA[1] SERÁ LA POSICIÓN
        		recs = self.cursor.execute('SELECT id FROM submission WHERE user_id = ' + str(user) + ' AND status = AC')
        		listaProblemas = np.empty([recs])
        		i=0
        		for row in self.cursor.fetchall():
        			listaProblemas[i] = row[0]
        			i=i+1
        		return listaProblemas

#Programa principal (Main)
conector = JuezDB()
conector.obtenerUsuarios()
