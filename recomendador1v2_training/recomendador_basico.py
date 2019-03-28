import conect
import numpy as np
import sys
import operator
from time import time

"""
Recomendador k-vecinos fijandonos en correlación entre usuarios.
Realizado por Alfonso Soria Muñoz y Pedro Domenech.
"""
class RecomendadorBasico:

        """
        Constructora del recomendador
                - Crea el recomendador cargando la matriz de datos de DB.
        Params:
                - db: Objeto BBDD que contiene la matriz y el parseo de posiciones/IDs de problemas. Además de otros métodos útiles sobre la BBDD
        Returns:
                - Nothing
        """
        def __init__(self, db):
                self.conexionDB     = db		
                self.matrizDatos    = self.conexionDB.obtenerMatriz()
                self.grado          = 0 
                # El grado sera el grado de similitud o el máximo de usuarios posibles. Servira para calcular el peso del problema. (En recomendar). Se remodifica tanto en metodo filtrarNsimilares como en recomendar

        """
        Método correlación
                - Calcula la correlación entre posUser1, y el usuario al que se está recomendando.
                - Tiene en cuenta que existan problemas en User1 y Owner, en otro caso devuelve correlación = 0.
        Params:
                - posUser1: posición de usuario con quien Owner va a calcular su correlación, en la matriz de datos. (Fila=información de 1 usuario)
        Returns:
                - type-double: valor entre 0 y 1 que representa la correlación entre los dos usuarios.
        """
        def correlacion(self,posUser1):
                # Obtenemos las posiciones de ambos usuarios
                posOwner = self.userPosOwner
                posUser  = posUser1
                # Calculamos el tamaño de la cantidad de problemas comunes
                tam_comunes     = self.tamProblemasComunes(posUser) #(pA)intersección(pB)
                # Obtenemos la cantidad de problemas resueltos por Owner
                self.ownerSizeCant =  self.calcularTamProblemasUser(posOwner)
                tam_pA = self.ownerSizeCant
                # Si los tamaños son mayores que 0, calculamos y devolvemos la correlación
                if tam_comunes!=0 and tam_pA!=0:
                        correl = tam_comunes/tam_pA
                        return correl
                # En otro caso, la correlación siempre será 0
                else:
                        return 0

        """
        Método calcularTamProblemasUser
                - Calcula el tamaño de los problemas a 1(Resueltos) de un usuario.
        Params:
                - posUser: posición de usuario en la matriz de datos sobre la que hacer el cálculo
        Returns:
                - type-int: valor del conjunto de los Naturales que indica la cantidad de problemas resueltos por un usuario.
        """
        def calcularTamProblemasUser(self, posUser):
                #Código previo a la optimización:
                """ 
                i = 0
                j = 0
                
                while i < self.matrizDatos.shape[1]:
                        if self.matrizDatos[posUser][i] == 1:
                                j = j + 1
                        i = i + 1
                return j
                """
                #Código optimizado usando mejor NumPy:
                booleanos = (self.matrizDatos[self.userPosOwner] == 1)
                return np.where(booleanos)[0].size


        """
        Método recomendar
                - Recomienda un usuario userIDowner, con un grado de similitud, devolviendo un diccionario de problemas ordenado.
        Params:
                - userIDowner: ID del usuario a recomendar
                - gradoSimilitud: con que grado de similitud calcular
        Returns:
                - diccionario: Diccionario ordenado de clave/valor = idProblema/pesoProblema.
        """
        def recomendar(self,userIDowner,gradoSimilitud):
                #obtener N mas similares
                self.userIDowner    = userIDowner
                self.userPosOwner   = self.conexionDB.obtenerPosUser(self.userIDowner)
                self.grado = gradoSimilitud
                matrizSimilares = self.filtrarNMasSimilares(gradoSimilitud)
                alterno = True #Si id = True, si correl = False
                diccionario = {}
                listaProblemas = None
                # Iteramos la matriz de una forma curiosa (Como un array de posiciones dos a dos.)
                # Esperemos no tarde tanto...
                # cantidadProblemas = self.__obtenerCantidadProblemas(matrizSimilares)
                for x in np.nditer(matrizSimilares, order='C'):
                        if alterno == True:
                                # Obtenemos lista de problemas que tiene el usuario de referencia respecto al propietario.
                                listaProblemas = self.buscarProblemasUser2MinusOwner(int(x))
                                alterno = False        
                        else:
                                # Le sumamoss el peso correspondiente (Sumar correlación del usar de referencia partido de N) al problema
                                correlProblema = x
                                for idProblema in listaProblemas:
                                        # Añadimos a nuestro diccionario partiendo por N-similares
                                        if idProblema in diccionario:
                                                #TODO: aquí debería parsear la posDelProblema en el Id del problema. Porque no la parseo...De momento trabajamos con posiciones en la matriz, no veo esencial lo otro.
                                                diccionario.update({idProblema : correlProblema/gradoSimilitud + diccionario.get(idProblema)})                                                
                                        else:
                                                diccionario.update({idProblema : correlProblema/gradoSimilitud})
                                alterno = True
                #Ordena de menor a mayor y se le da la vuelta.
                diccionario = sorted(diccionario.items(), key=operator.itemgetter(1))
                diccionario.reverse()
                #Esta parte puede quizás ahora ser el mayor cuello de botella del algoritmo completo.
                #Devuelve la posicion de la matriz, no su ID como tal. Habra que parsearlo con la clase conect para obtener el id correspondiente.
                return diccionario #Devolvemos una lista ordenada de recomendaciones de problemas que aún no ha resuelto. (Key=ID problema / Valor=Peso de recomendacion sobre 1)

"""
TODO VOY POR AQUI
"""
        # Devuelve una lista de los usuarios más similares respecto al que se va a recomendar (De cantidad "cantidad")
        # Esta lista implicará la precisión a la hora de recomendar.
        # Todo: Testear
        def filtrarNMasSimilares(self,cantidad):

                # Generamos una lista de correlacion asociada a la lista de Usuarios.
                if cantidad > self.matrizDatos.shape[0]:
                        cantidad    = self.matrizDatos.shape[0]
                        self.grado  = self.matrizDatos.shape[0]
                i = 0
                
                # Creamos matriz de posicionUser-correlacion y posteriormente la ordenaremos, la creamos teniendo encuenta que
                # los usuarios tienen problemas disjuntos
                matrizCorrelPos = np.empty([self.matrizDatos.shape[0],2])
                while i < self.matrizDatos.shape[0]:
                        if self.buscarProblemasUser2MinusOwner(i).size > 0:
                                correl = self.correlacion(i)
                                matrizCorrelPos[i][0] = i
                                matrizCorrelPos[i][1] = correl
                        else:
                                matrizCorrelPos[i][0] = i
                                matrizCorrelPos[i][1] = 0
                        i = i + 1
                        """if cantidad > matrizCorrelPos.shape[0]:
                                cantidad    = matrizCorrelPos.shape[0]
                                self.grado  = matrizCorrelPos.shape[0]"""

                #Ordenamos la matriz por nuestra segunda columna y obtenemos la submatriz de N elementos mas similares.
                matrizCorrelPos         = matrizCorrelPos[matrizCorrelPos[:,1].argsort()]
                matrizCorrelPos         = matrizCorrelPos[::-1]
                _cantidad               = np.arange(cantidad)
                matrizCorrelPos         = matrizCorrelPos[_cantidad,:]
                #Devolvemos los N usuarios mas similares en una matriz de dos columnas
                #Columna 0 = posicion usuario en matriz de datos, Columna 1 = correlación del usuario respecto nuestro Owner.
                return matrizCorrelPos



        #Devuelve array de posiciones comunes
        def buscarProblemasComunes(self,user2):
                posOwner = self.userPosOwner
                posUser  = user2
                """
                # MODIFIED
                i = 0
                j = 0
                arrayProvisionalPos = np.empty([self.matrizDatos.size],dtype=int)

                while i < self.matrizDatos.shape[1]:
                        if(self.matrizDatos[posOwner][i] == 1 and self.matrizDatos[posUser][i] == 1):
                                arrayProvisionalPos[j] = i
                                j = j + 1
                        i = i + 1

                arrayPosComun = np.empty([j],dtype=int)
                i = 0
                while i < j:
                        arrayPosComun[i] = arrayProvisionalPos[i]
                        i = i + 1
                """
                booleanos = (self.matrizDatos[posOwner] == 1) & (self.matrizDatos[posUser] == 1)
                return np.where(booleanos)[0]
                # return arrayPosComun

        #Devuelve el tamaño de problemas comunes. Se ha creado para ser un poco mas eficientes que obtener el listado como
        #La funcion previa a esta
        def tamProblemasComunes(self,user2):
                posOwner = self.userPosOwner
                posUser  = user2
                """
                i = 0
                j = 0

        
                while i < self.matrizDatos.shape[1]:
                        if(self.matrizDatos[posOwner][i] == 1 and self.matrizDatos[posUser][i] == 1):
                                j = j + 1
                        i = i + 1

                return j
                """
                booleanos = (self.matrizDatos[posOwner] == 1) & (self.matrizDatos[posUser] == 1)
                return np.where(booleanos)[0].size


        #Devuelve una lista de problemas que tiene user2 y no owner.
        #TODO: Testear
        def buscarProblemasUser2MinusOwner(self, user2):
                posOwner = self.userPosOwner
                posUser2 = user2
                booleanos = (self.matrizDatos[posOwner] == 0) & (self.matrizDatos[posUser2] == 1)
                return np.where(booleanos)[0]
                """
                tam = 0
                listaNoComunes = np.empty(self.matrizDatos.shape[1], dtype=int) #Inicializamos listaNoComunes al tamaño máximo de problemas en total
                
                #ahora deberia empezar a iterar: TODO
                
                maxSize = self.matrizDatos.shape[1]
                i = 0
                j = 0
                
                while i < maxSize:
                        if(self.matrizDatos[posUser2][i] == 1 and self.matrizDatos[posOwner][i] == 0):
                                listaNoComunes[j] = i
                                j = j + 1
                        i = i + 1
                listaFinal = np.empty(j,dtype=int)
                listaFinal = np.split(listaNoComunes, [j,maxSize])[0]
                """
                """with np.nditer(listaFinal,op_flags=['readwrite']) as it:
                        for x in it:
                                x[...] = 
                """
                
                """
                problemasOwner = self.listaProblemasOwner
                problemasUser2 = self.obtenerProblemas(user2)
                tam = 0
                listaNoComunes = np.empty([0]) #Inicializamos listaNoComunes a 0
                #El tamaño máximo de nuestro array comun será como mucho el numero de problemas de user2
                listaNoComunes = np.empty([problemasUser2.size],dtype=int)
                        
                #Itero de tal forma que para cada problema del otro usuario, busco en el propietario sus problemas. Si está lo añado a la lista y dejo de buscar ese problema.
                comp = False
                for problemaUser in problemasUser2:
                        for problemaOwner in problemasOwner:
                                if problemaOwner == problemaUser:
                                        comp = True
                                if comp == True:
                                        break
                        if comp == False:
                                listaNoComunes[tam] = problemaUser
                                tam = tam + 1
                        comp = False
                tamListaFinal = 0
                listaFinal = np.empty([tam],dtype=int) #Creamos un listado final con el tamaño adecuado
                while tamListaFinal < tam:
                        listaFinal[tamListaFinal] = listaNoComunes[tamListaFinal]
                        tamListaFinal = tamListaFinal + 1
                """
                # return listaFinal
                
        # Métodos de la V1
        # Obtencion de los problemas válidos de un usuario X
        # Llamar a esta funcion periodicamente y dejarla en memoria cada T tiempo actualizarla. (para agilizar calculo obtener correlacion de cada usuario, etc)
        """
        def obtenerProblemas(self, user):
                #Obener Array de problemas.
                return self.conexionDB.obtenerEntregasValidasDeUser(user)
        """


        # Obtiene el listado actual de usuarios
        """
        def obtenerUsuarios(self):
                return self.conexionDB.obtenerUsuarios()
        """


"""
Prueba funcionamiento y tiempo de funciones recomendador v2
"""

# np.count_nonzero(y == 1) >> ESTA FUNCION CUENTA CUANTAS VECES SE REPITE EL VALOR UNO EN EL ARRAY Y
# np.any(a!=0)
# np.all(a==a)

