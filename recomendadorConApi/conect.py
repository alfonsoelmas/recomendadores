#Acceso a bbdd
#Instalar MySQLdb para acceder a bases de datos
import pymysql
import numpy as np
#Importamos la libreria time para medir cuanto tarda cada función que llamamos y calcular eficiencias
from time import time
import sys
import os.path as path

"""
VARIABLES GLOBALES PARA LA CLASE CONECT
_______________________________________
ESTARÍA BIEN ESTE TIPO DE "CONFIGURACIONES" QUE ACTUAN COMO CTES GLOBALES
TENERLOS DESDE UN ARCHIVO PYTHON APARTE
"""
#La base de datos SOLO se usa para cargar una unica vez los datos desde la BBDD de aceptaelreto, el resto de veces lo carga desde local y lo actualiza con las entregas
DATABASEDOMAIN = 'localhost'
DATABASEUSER = 'root'
DATABASEPASS = ''
DATABASENAME = 'aceptaelreto'


class JuezDB:
        def __init__(self):
                #Fecha de corte por si se quiere trabajar con un subconjunto de datos inferior al total acotado por fechas. (Para entrenamiento del recomendador)
                self.fechaCorteTraining = "2017-10-23 08:00:00"
                #Nombre del fichero local que contiene la matriz de ACs de usuario guardada
                self.matrizLocal = "matrizACs.dat"
                self.problemParserLocal = "problemParser.dat"
                self.userParserLocal = "userParser.dat"
                self.lastSubmitionLocal = "lastSubmition.dat"
                self.lastSubmition = 1
                if path.exists(self.userParserLocal) and path.exists(self.problemParserLocal) and path.exists(self.matrizLocal):
                        self.isCreatedLocal = True
                else:
                        self.isCreatedLocal = False

                if not self.isCreatedLocal:
                        db = pymysql.connect(DATABASEDOMAIN, DATABASEUSER, DATABASEPASS, DATABASENAME)
                        self.cursor = db.cursor()

                #Carga la matriz de datos desde la BBDD o desde local según el atributo isCreatedLocal == false/true
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

        #Metodo obtener entregas validas de un determinado usuario
        def _obtenerEntregasValidasDeUser(self, user):
                        #Mi user ID es 847 (Para posibles pruebas)
                        recs = self.cursor.execute('SELECT DISTINCT problem_id FROM submission WHERE user_id = '+str(user)+' AND status = "AC" AND submissionDate <= "'+self.fechaCorteTraining+'" group by problem_id')
                        listaProblemas = np.empty([recs],dtype=int)
                        i=0
                        for row in self.cursor.fetchall():
                                listaProblemas[i] = row[0]
                                i=i+1
                        return listaProblemas

        #Metodo para obtener Entregas Válidas tras el entrenamiento.
        def _obtenerEntregasValidasDeUserPostTraining(self, user):
                        #Mi user ID es 847 (Para posibles pruebas)
                        recs = self.cursor.execute('SELECT DISTINCT problem_id FROM submission WHERE user_id = '+str(user)+' AND status = "AC" AND submissionDate > "2'+self.fechaCorteTraining+'" group by problem_id')
                        listaProblemas = np.empty([recs],dtype=int)
                        i=0
                        for row in self.cursor.fetchall():
                                listaProblemas[i] = row[0]
                                i=i+1
                        return listaProblemas


        #Obtener todos los usuarios de la BBDD
        #Almacena el listado de posicion/id para parsear la posicion por el ID correspondiente
        def _obtenerTodosUsuarios(self):
                recs = self.cursor.execute('SELECT id from users WHERE registrationDate <= "'+self.fechaCorteTraining+'" ORDER BY id ASC')
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
                recs = self.cursor.execute('SELECT internalId from problem WHERE publicationDate <= "'+self.fechaCorteTraining+'" ORDER BY internalId ASC')
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
                #para cada usuario, le ponemos a 1 los problemas resueltos
                if not self.isCreatedLocal:
                        listaUsers = self._obtenerTodosUsuarios()
                        tamProblemas = self._obtenerTodosProblemas()
                        tamUsers = listaUsers.size
                        #Creamos la matriz de tamUsers x tamProblemas y la inicializamos a cero
                        self.matrizDatos = np.zeros((tamUsers,tamProblemas), dtype=np.uint8)
                        i=0
                        for user in listaUsers:
                                entregas = self._obtenerEntregasValidasDeUser(user)
                                for idProblema in entregas:
                                        pos = self._obtenerPos(idProblema,"problems")
                                        self.matrizDatos[i,pos] = 1
                                i = i + 1
                        self._guardarMatrizEnLocal()
                        return
                else:
                        self._cargarMatrizDesdeLocal()

        def _guardarMatrizEnLocal(self):
            # guardamos con 1 decimal ya que nuestros datos son UINT8
            # TODO: HAY QUE GUARDAR MI ULTIMO SUBMITION
            np.savetxt(self.matrizLocal, self.matrizDatos, fmt='%.1e')
            np.savetxt(self.problemParserLocal, self._problems)
            np.savetxt(self.userParserLocal, self._users)

        def _cargarMatrizDesdeLocal(self):
            # Cargamos matriz desde archivo .dat local
            self.matrizDatos = np.loadtxt(self.matrizLocal)
            self.matrizDatos = self.matrizDatos.astype(np.uint8)
            self._users = np.loadtxt(self.userParserLocal)
            self._users = self._users.astype(int)
            self._problems = np.loadtxt(self.problemParserLocal)
            self._problems = self._problems.astype(int)

        # Devuelve a matriz de datos
        def obtenerMatriz(self):
                return self.matrizDatos

        # Devuelve la posición en la matriz de un ID de usuario dado
        def obtenerPosUser(self, idUser):
                return self._obtenerPos(idUser,"users")

        # Actualiza la matriz de datos con las nuevas entregas que recibe desde el juez en línea
        def actualizarEntregas(self,nuevasEntregas):
                #TODO: Debemos guardar la ultima entrega de la que tenemos info


"""
Pruebas funcionamiento clase conect
Tarda 30 segundos en crear la clase conect y cargar en memoria la matriz
La matriz en memoria ocupa 3.5Mb siendo uint8, y 14Mb siendo int.
Todo:
    Por hacer un metodo que guarde matriz en txt por si es necesario
"""

