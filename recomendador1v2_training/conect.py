#Acceso a bbdd
#Instalar MySQLdb para acceder a bases de datos
import pymysql
import numpy as np
#Importamos la libreria time para medir cuanto tarda cada función que llamamos y calcular eficiencias
from time import time
import sys


class JuezDB:
        def __init__(self):
                db = pymysql.connect('localhost', 'root', '', 'aceptaelreto')
                self.cursor = db.cursor()
                self.cargarMatrizDatos()

        #Metodo privado obtener usuarios. Devuelve un array con id de usuarios obtenido de la BBDD
        def _obtenerUsuarios(self):
                #Hacemos una consulta eficaz y descartamos aquellos usuarios que tengan 1 o menos entregas aceptadas.
                #Hemos reducido a la mitad el numero de usuarios!
                recs = self.cursor.execute('SELECT DISTINCT users.id from users INNER JOIN submission ON users.id = submission.user_id WHERE submission.status = "AC"')
                listaUsers = np.empty([recs],dtype=int)
                i=0
                for row in self.cursor.fetchall():
                        listaUsers[i] = row[0]
                        i=i+1
                return listaUsers

        #Metodo obtener entregas validas de un determinado usuario - Todo (Comprobar correcto funcionamiento)
        def _obtenerEntregasValidasDeUser(self, user):
                        #Mi user ID es 847 (Para posibles pruebas)
                        recs = self.cursor.execute('SELECT DISTINCT problem_id FROM submission WHERE user_id = '+str(user)+' AND status = "AC" AND submissionDate <= "2017-10-23 08:00:00" group by problem_id')
                        listaProblemas = np.empty([recs],dtype=int)
                        i=0
                        for row in self.cursor.fetchall():
                                listaProblemas[i] = row[0]
                                i=i+1
                        return listaProblemas

        def _obtenerEntregasValidasDeUserPostTraining(self, user):
                        #Mi user ID es 847 (Para posibles pruebas)
                        recs = self.cursor.execute('SELECT DISTINCT problem_id FROM submission WHERE user_id = '+str(user)+' AND status = "AC" AND submissionDate > "2017-10-23 08:00:00" group by problem_id')
                        listaProblemas = np.empty([recs],dtype=int)
                        i=0
                        for row in self.cursor.fetchall():
                                listaProblemas[i] = row[0]
                                i=i+1
                        return listaProblemas
        """
        LO QUE HAY SOBRE ESTE COMENTARIO DEBE DUPLICARSE
        PERO TRABAJANDO SOBRE LA MATRIZ Y NO SOBRE CONSULTAS
        """

        #Obtener todos los usuarios de la BBDD
        #Almacena el listado de posicion/id para parsear la posicion por el ID correspondiente
        def _obtenerTodosUsuarios(self):
                recs = self.cursor.execute('SELECT id from users WHERE registrationDate <= "2017-10-23 08:00:00" ORDER BY id ASC')
                listaUsers = np.empty([recs],dtype=int)
                i=0
                for row in self.cursor.fetchall():
                        listaUsers[i] = row[0]
                        i=i+1
                self._users = listaUsers
                return listaUsers

        #Obtiene la lista de problemas con su ID. Devolvemos el tamaño de la lista
        #Guardamos en un atributo el listado para usarlo como parseador de posicion a ID en la matriz de datos
        def _obtenerTodosProblemas(self):
                recs = self.cursor.execute('SELECT internalId from problem WHERE publicationDate <= "2017-10-23 08:00:00" ORDER BY internalId ASC')
                listaProblems = np.empty([recs],dtype=int)
                i=0
                for row in self.cursor.fetchall():
                        listaProblems[i] = row[0]
                        i=i+1
                self._problems = listaProblems
                return listaProblems.size

        # Nos sirve para hacer busqueda de un id sobre nuestro listado de problemas o usuarios
        # Obtenemos la posicion del id en nuestro array
        # Util para "parsear" el id de los problemas/usuarios por su posicion en nuestros vectores de la matriz
        # Búsqueda binaria
        def _obtenerPos(self, id, tipoListado):
                pos = -1
                lista = None
                if(tipoListado == "users"):
                        lista = self._users
                else:
                        lista = self._problems
                primero = 0
                ultimo = lista.size-1

                while primero <= ultimo:
                        puntoMedio = (primero + ultimo)//2
                        if lista[puntoMedio] == id:
                                return puntoMedio
                        else:
                                if id < lista[puntoMedio]:
                                        ultimo = puntoMedio-1
                                else:
                                        primero = puntoMedio+1
                return pos



        #Carga una matriz de filas = usuarios / columnas = problemas con valores binarios 1 si hecho 0 si no hecho para cada (fila,col)
        def cargarMatrizDatos(self):
                listaUsers = self._obtenerTodosUsuarios()
                tamProblemas = self._obtenerTodosProblemas()
                tamUsers = listaUsers.size
                #Creamos la matriz de tamUsers x tamProblemas y la inicializamos a cero
                self.matrizDatos = np.zeros((tamUsers,tamProblemas), dtype=np.uint8)
                #para cada usuario, le ponemos a 1 los problemas resueltos
                i=0
                for user in listaUsers:
                        entregas = self._obtenerEntregasValidasDeUser(user)
                        for idProblema in entregas:
                                pos = self._obtenerPos(idProblema,"problems")
                                self.matrizDatos[i,pos] = 1
                        i = i + 1

        # Devuelve a matriz de datos
        def obtenerMatriz(self):
                return self.matrizDatos

        # Devuelve la posición en la matriz de un ID de usuario dado
        def obtenerPosUser(self, idUser):
                return self._obtenerPos(idUser,"users")


"""
Pruebas funcionamiento clase conect
Tarda 37 segundos en crear la clase conect y cargar en memoria la matriz
La matriz en memoria ocupa 3.5Mb siendo uint8, y 14Mb siendo int.
Todo:
    Por hacer un metodo que guarde matriz en txt por si es necesario
"""
