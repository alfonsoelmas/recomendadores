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
#La base de datos SOLO se usa para cargar una unica vez los datos desde la BBDD de aceptaelreto
#el resto de veces lo carga desde local y lo actualiza con las entregas
#estas variables globales para la clase sirven para configurar los campos de la BBDD para conectarte a un juez en línea
#bajo un servidor MySQL. Para otras modificaciones sobre el servidor de BBDD habría que modificar partes de esta clase
DATABASEDOMAIN = 'localhost'
DATABASEUSER = 'root'
DATABASEPASS = ''
DATABASENAME = 'aceptaelreto'

# =======================================
# VALORES Y NOMBRES DE CAMPOS PARA LA BBDD SOBRE LA QUE SE VAN A PRECARGAR LOS DATOS AL RECOMENDADOR
# (Esta configuración nos permite hacer mas portable el recomendador sobre otros jueces en línea)
# ========================================
USERS_TABLENAME         = 'users'
USER_IDNAME             = 'id'
USER_REGISTRATIONDATE   = 'registrationDate'
# ========================================
SUBMITS_TABLENAME       = 'submission'
SUBMIT_IDUSER           = 'user_id'
SUBMIT_IDPROBLEM        = 'problem_id'
SUBMIT_STATUS           = 'status'
SUBMIT_STATUSOK         = 'AC'
SUBMIT_DATE             = 'submissionDate'
SUBMIT_ID               = 'id'
# ========================================        
PROBLEMS_TABLENAME      = 'problem'
PROBLEM_ID              = 'internalId'
PROBLEM_PUBLICATIONDATE = 'publicationDate'
        


# ===============================================
# ===Nombres archivos locales y fecha de corte===
# ===============================================
FECHACORTE                      = "2017-10-23 08:00:00"
MATRIZACSLOCAL                  = "matrizACs.dat"
PROBLEM_PARSER_LOCAL            = "problemParser.dat"
USER_PARSER_LOCAL               = "userParser.dat"
LASTSUBMIT_LOCAL                = "lastSubmition.dat"

# =========================================
# =========================================
# ==================FIN====================
# ===============VARIABLES=================
# ===============GLOBALES!=================
# =========================================
# =========================================






class JuezDB:
    def __init__(self):
        #Fecha de corte por si se quiere trabajar con un subconjunto de datos inferior al total acotado por fechas. (Para entrenamiento del recomendador)
        self.fechaCorteTraining = FECHACORTE
        #Nombre del fichero local que contiene la matriz de ACs de usuario guardada
        self.matrizLocal = MATRIZACSLOCAL
        self.problemParserLocal = PROBLEM_PARSER_LOCAL
        self.userParserLocal = USER_PARSER_LOCAL
        self.lastSubmitionLocal = LASTSUBMIT_LOCAL
        self.lastSubmition = 1
        if path.exists(self.userParserLocal) and path.exists(self.problemParserLocal) and path.exists(self.matrizLocal) and path.exists(self.lastSubmitionLocal):
            self.isCreatedLocal = True
            print("La bbdd existe en local-")
        else:
            self.isCreatedLocal = False
            print("La bbdd no existe en local-")

        if not self.isCreatedLocal:
            db = pymysql.connect(DATABASEDOMAIN, DATABASEUSER, DATABASEPASS, DATABASENAME)
            self.cursor = db.cursor()

        #Carga la matriz de datos desde la BBDD o desde local según el atributo isCreatedLocal == false/true
        self._cargarMatrizDatos()

    #Metodo privado obtener usuarios. Devuelve un array con id de usuarios obtenido de la BBDD
    def _obtenerUsuarios(self):
        #Hacemos una consulta eficaz y descartamos aquellos usuarios que tengan 1 o menos entregas aceptadas.
        #Hemos reducido a la mitad el numero de usuarios!
        recs = self.cursor.execute('SELECT DISTINCT '+USERS_TABLENAME+'.'+USER_IDNAME+' from '+USERS_TABLENAME+' INNER JOIN '+SUBMITS_TABLENAME+' ON '+ USERS_TABLENAME+ '.'+USER_IDNAME+' = '+SUBMITS_TABLENAME+'.'+SUBMIT_IDUSER+' WHERE '+SUBMITS_TABLENAME+'.'+SUBMIT_STATUS+' = "'+SUBMIT_STATUSOK+'"')
        listaUsers = np.empty([recs],dtype=int)
        i=0
        for row in self.cursor.fetchall():
            listaUsers[i] = row[0]
            i=i+1
        return listaUsers

    #Metodo obtener entregas validas de un determinado usuario
    def _obtenerEntregasValidasDeUser(self, user):
            #Mi user ID es 847 (Para posibles pruebas)
            recs = self.cursor.execute('SELECT DISTINCT '+SUBMIT_IDPROBLEM+' FROM '+SUBMITS_TABLENAME+' WHERE '+SUBMIT_IDUSER+' = '+str(user)+' AND '+SUBMIT_STATUS+' = "'+SUBMIT_STATUSOK+'" AND '+SUBMIT_DATE +' <= "'+self.fechaCorteTraining+'" group by '+SUBMIT_IDPROBLEM)
            listaProblemas = np.empty([recs],dtype=int)
            i=0
            for row in self.cursor.fetchall():
                listaProblemas[i] = row[0]
                i=i+1
            return listaProblemas

    #Metodo para obtener Entregas Válidas tras el entrenamiento.
    def _obtenerEntregasValidasDeUserPostTraining(self, user):
            #Mi user ID es 847 (Para posibles pruebas)
            recs = self.cursor.execute('SELECT DISTINCT '+SUBMIT_IDPROBLEM+' FROM '+SUBMITS_TABLENAME+' WHERE '+SUBMIT_IDUSER+' = '+str(user)+' AND '+SUBMIT_STATUS+' = "'+SUBMIT_STATUSOK+'" AND '+SUBMIT_DATE +' > "'+self.fechaCorteTraining+'" group by '+SUBMIT_IDPROBLEM)
            listaProblemas = np.empty([recs],dtype=int)
            i=0
            for row in self.cursor.fetchall():
                listaProblemas[i] = row[0]
                i=i+1
            return listaProblemas


    #Obtener todos los usuarios de la BBDD
    #Almacena el listado de posicion/id para parsear la posicion por el ID correspondiente
    def _obtenerTodosUsuarios(self):
        recs = self.cursor.execute('SELECT '+USER_IDNAME+' from '+USERS_TABLENAME+' WHERE '+USER_REGISTRATIONDATE+' <= "'+self.fechaCorteTraining+'" ORDER BY '+USER_IDNAME+' ASC')
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
        #TODO, CUIDADO CON ESTA PARTE, TRABAJAMOS CON EL INTERNAL ID, PERO EL JSON NOS DA EL ID EXTERNO...
        recs = self.cursor.execute('SELECT '+PROBLEM_ID+' from '+PROBLEMS_TABLENAME+' WHERE '+PROBLEM_PUBLICATIONDATE+' <= "'+self.fechaCorteTraining+'" ORDER BY '+PROBLEM_ID+' ASC')
        listaProblems = np.empty([recs],dtype=int)
        i=0
        for row in self.cursor.fetchall():
            listaProblems[i] = row[0]
            i=i+1
        self._problems = listaProblems
        return listaProblems.size
    
    #Obtiene el último submit que contiene la BBDD del servidor
    # *Solo se usará para precargar la BBDD del servidor, luego gestiona todo a nivel local
    def _obtenerUltimoSubmitServerDB(self):
        """
        Consulta que nos devuelve el último submit de la BBDD
        Lo debemos devolver como entero.                
        """
        recs = self.cursor.execute('SELECT MAX('+SUBMIT_ID+') FROM '+SUBMITS_TABLENAME)
        self.lastSubmition = self.cursor.fetchone()[0]
        return self.lastSubmition

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

        # Emular una lista con 4 usuarios que se repiten 100 veces cada uno, ver q ha insertado. 4 usuarios q ya existen repetidos 100 veces y 4 usuarios que no existen repetidos 100 veces.
        while primero <= ultimo: #TODO TESTEAR ESTE ALGORITMO.
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
    def _cargarMatrizDatos(self):
        #para cada usuario, le ponemos a 1 los problemas resueltos
        if not self.isCreatedLocal:
            listaUsers = self._obtenerTodosUsuarios()
            tamProblemas = self._obtenerTodosProblemas()
            self._obtenerUltimoSubmitServerDB()
            tamUsers = listaUsers.size
            #Creamos la matriz de tamUsers x tamProblemas y la inicializamos a cero
            self.matrizDatos = np.zeros((tamUsers,tamProblemas), dtype=np.int8)
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

    # guardamos con 1 decimal ya que nuestros datos son INT8
    # TODO: HAY QUE GUARDAR MI ULTIMO SUBMITION
    def _guardarMatrizEnLocal(self):
        np.savetxt(self.matrizLocal, self.matrizDatos, fmt='%.1e')
        np.savetxt(self.problemParserLocal, self._problems)
        np.savetxt(self.userParserLocal, self._users)
        manejadorArchivo = open (self.lastSubmitionLocal, "w")
        print(str(self.lastSubmition))
        manejadorArchivo.write(str(self.lastSubmition))
        manejadorArchivo.close()
        

    # Cargamos matriz desde archivo .dat local
    def _cargarMatrizDesdeLocal(self):
        self.matrizDatos    = np.loadtxt(self.matrizLocal)
        self.matrizDatos    = self.matrizDatos.astype(np.int8)
        self._users         = np.loadtxt(self.userParserLocal)
        self._users         = self._users.astype(int)
        self._problems      = np.loadtxt(self.problemParserLocal)
        self._problems      = self._problems.astype(int)
        manejadorArchivo    = open(self.lastSubmitionLocal, 'r')
        self.lastSubmition  = int(manejadorArchivo.readline())
        manejadorArchivo.close()

    # Devuelve la matriz de datos
    def obtenerMatriz(self):
        return self.matrizDatos

    # Devuelve la posición en la matriz de un ID de usuario dado
    def obtenerPosUser(self, idUser):
        return self._obtenerPos(idUser,"users")

    # Actualiza la matriz de datos con las nuevas entregas que recibe desde el juez en línea
    # Param "nuevasEntregas": objeto JSON ordenado de menor a mayor por ID de entregas de últimas entregas que no tenemos.
    # TODO: TESTEAR
    def actualizarEntregas(self,nuevasEntregas, ultimaEntrega):
        self.lastSubmition = ultimaEntrega

        for elem in nuevasEntregas:
            userId          = elem["userID"]
            problemPos      = elem["problemPos"]
            estado          = elem["estado"]
            """
            El external ID corresponde a la Posicion del problema... los problemas nuevos no sabremos
            Su internal ID, por lo que nos inventamos uno que sea x ejemplo ultimoProblemId de nuestra lista de parseador
            + 3... por ejemplo (en la bbdd el internal ID tiene un incremento aleatorio de 1, 2 o 3... incluso 30)

            En realidad el internal ID tampoco lo necesitamos para recomendar ya que con el external nos sirve
            por lo que el internal solo lo usaremos al cargar la bbdd desde el servidor de bbdd oficial y poco más
            """
            #Creo esta variable por si mas adelante lo tenemos en cuenta, pero quizas ni se use despues
            compUser = True
            if self.obtenerPosUser(userId) == -1: #TODO: testear nuevamente esto. Quizás esta insertando de más
                # Este usuario no existía
                compUser = False
                # añadir usuario nuevo al final de parseador de usuarios
                self._users = np.append(self._users, userId)
                # añadir fila nueva de usuarios en matriz de datos e inicializarla a 0
                problemas = np.zeros(self._problems.size, dtype=np.int8)
                #ver bien el insert TODO
                self.matrizDatos = np.insert(self.matrizDatos, self.matrizDatos.shape[0], problemas, 0)
            
            #Creo esta variable por si mas adelante lo tenemos en cuenta, pero quizas ni se use despues
            compProblem = True
            if self._problems.size <= problemPos:
                #Este problema no existía
                compProblem = False
                # crearIDproblemaInternal
                # añadir problema nuevo al final de parseador de problemas
                """
                Nota: Como tenemos POSICIONES, si nuestra posicion de problema es N veces más
                que el Size de _problems, es que hay 10 problemas nuevos
                por lo que creamos todos los nuevos...
                """
                sizeP = self._problems.size-1
                diferencia = problemPos - sizeP
                increment = 0
                while increment != diferencia:
                    #Le añado a problems un nuevo elemento.
                    #El ID correspondera a su tamaño en ese momento.. problema: PUEDEN DUPLICARSE IDS!
                    #Para el estado actual de aceptaelreto le sumamos 10mil para evitar duplicados con los originales, ¡pero no es una solucion A LARGO PLAZO!
                    self._problems = np.append(self._problems, self._problems.size+10000)
                    # creamos las columnas correspondientes a la matriz de datos y las inicializamos a 0
                    userss = np.zeros(self._users.size,dtype=np.int8)
                    #ver bien el insert TODO
                    self.matrizDatos = np.insert(self.matrizDatos, self.matrizDatos.shape[1], userss, 1)
                    increment = increment + 1 

            #compResuelto == true? (Está resuelto? -AC-)
            posUser = self.obtenerPosUser(userId) #La llamamos previamente, podemos aprovechar y usar esa llamada para no volver a iterar sobre un array tan grande...
            if estado == 1:
                self.matrizDatos[posUser, problemPos] = 1
        self._guardarMatrizEnLocal()
        #TODO EN PRINCIPIO EL SERVER HA ACTUALIZADO A CONECT LA ULTIMA ENTREGA

        """
        Lo que hace actualizar entregas en alto nivel>
        - para cada elemento de nuevasEntregas:
            cogerIDproblema
            cogerIDuser
            
            compProblem = comprobar si ID problema existe en self_problems
            compUser = comprobar si ID user existe en problems
            compResuelto = comprobar si resuelto cogiendo estado == "AC" del elemento mirando de nuevasEntregas
            - existen ambos?
              Si:
                - Do nothing
              No:
                - existe user?
                  Si:
                    crearIDproblemaInternal
                    añadir problema nuevo al final de parseador de problemas
                    añadir columna nueva de problemas en matriz de datos e inicializarla a 0
                  No:
                    añadir usuario nuevo al final de parseador de usuarios
                    añadir fila nueva de problemas en matriz de datos e inicializarla a 0
            - compResuelto == true? (Está resuelto? -AC-)
              Si:
                - Añadir en pos. correspondiente matriz un 1
              No:
                - Do nothing
        llamar a guardarMatrizEnLocal
        """


    #Como solo tenemos el external ID que corresponde a una lista ordenada de creacion con incremento = 1
    #Nos inventamos las internal ID, que en principio no deberiamos usar... pero no estaría mal una funcion que
    #se conecte a la BBDD y le asigne a ese external su internal correspondiente, de momento no la creamos porque no nos resulta util.        
    def asignarIDsAproblemas(self):
        #TODO
        return -1
"""
Pruebas funcionamiento clase conect
Tarda 30 segundos en crear la clase conect y cargar en memoria la matriz
La matriz en memoria ocupa 3.5Mb siendo int8, y 14Mb siendo int.

"""

