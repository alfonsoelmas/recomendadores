import conect
import numpy as np
import sys
import operator
from time import time
"""
TODO:
        Cambiar muchas iteraciones por iteraciones en numpy
        Todo lo que se pueda hacer a traves de numpy cambiarlo, ya que mejora la eficiencia de la operación.

Recomendador k-vecinos fijandonos en correlación entre usuarios
El recomendador realiza el siguiente algoritmo para recomendar:

- usuario a recomendar: Owner > O:
para un O, obtenemos una lista de los K usuarios más similares con su correlación correspondiente.
Esta lista se obtiene calculando la correlación para cada usuario Bi de la BBDD, con O.
    El cálculo de la correlación entre Bi y O se basa en:
    - pO  = conjunto problemas de Owner
    - pBi = conjunto de problemas de usuario Bi
    - X[*operacion*]Y = *operacion* realizada entre elemento de la izquierda X, elemento de la derecha Y
    - [*operacion*]X  = *operacion* realizada sobre elemento X
    correlacion = ([*tam*](pBi[*intersección*]pO))[*division*]([*tam*]pO) Sii [*tam*]pO > 0 ^ [*tam*](pBi[*intersección*]pO) > 0
- peso de recomendación: pesoDeRecomendación > pdR
Tras este cálculo, creamos un diccionario (D) de Clave=idProblema / Valor=pesoDeRecomendación.
De esta forma, obtenemos para cada Bi el resultado de restar los conjuntos pBi con pO. (Los problemas que tiene Bi y no Owner)
- rpBi = pBi[*resta-conjuntos*]pO = problemas que Bi tiene y no Owner
para cada elemento de rpBi le sumamos el peso correspondiente a la correlación de ese usuario, en el diccionario tal que:
- (rpBi)j  = elemento del conjunto rpBi
D[(rpBi)j] = D[(rpBi)j][*suma*]((Bi[*correlacion*]O)[*division*]K)
Si no existía el problema en el diccionario, se inicializa a cero y se realiza la suma.
Al dividir por K, nos aseguramos el resultado nunca sea mayor que 1.
Tras realizar la operación para cada elemento, ordenamos el diccionario por su valor de mayor a menor se devuelve esta lista ordenada y lo más ámplia posible.
a recomendar con un peso de recomendación, con su clave/valor.
Cuanto más grande sea K más precisa será la recomendación, pero al peso le costará más alcanzar el valor máximo (1).
"""
class RecomendadorBasico:

        # Crea el recomendador con la matriz de datos el id del owner y su posicion de la matriz (Su fila es su correspondiente)
        def __init__(self, db):
                self.conexionDB     = db		
                self.matrizDatos    = self.conexionDB.obtenerMatriz()
                self.grado          = 0 
                # El grado sera el grado de similitud o el máximo de usuarios posibles. Servira para calcular el peso del problema. (En recomendar). Se remodifica tanto en metodo filtrarNsimilares como en recomendar
                # self.listaProblemasOwner = self.obtenerProblemas(self.userIDowner)

        #Devuelve la correlacion entre 2 usuarios
        def correlacion(self,posUser1):
                #Anotación: la siguiente busqueda puede darse como una consulta más compleja antes que de forma algoritmica. (comprobar mejora de rendimiento)
                #AHORA ESTAMOS TRABAJANDO CON POSICIONES DE USUARIOS !!!
                posOwner = self.userPosOwner
                posUser  = posUser1

                tam_comunes     = self.tamProblemasComunes(posUser) #(pA)intersección(pB)
                self.ownerSizeCant =  self.calcularTamProblemasUser(posOwner)
                tam_pA = self.ownerSizeCant
                #todo comprobar condiciones de tamaños 0, etc.
                if tam_comunes!=0 and tam_pA!=0:
                        correl = tam_comunes/tam_pA
                        return correl
                else:
                        return 0

        #Calcula el tamaño de los problemas de un usuario. TODO: Mejorar iteración para que sea más rápida.
        def calcularTamProblemasUser(self, posUser):
                # MODIFIED
                # i = 0
                # j = 0
                """
                while i < self.matrizDatos.shape[1]:
                        if self.matrizDatos[posUser][i] == 1:
                                j = j + 1
                        i = i + 1
                """
                booleanos = (self.matrizDatos[self.userPosOwner] == 1)
                return np.where(booleanos)[0].size
                # return j


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

        # Recomienda al usuario problemas en base al algoritmo de recomendación aplicado y un grado de similitud.
        # Todo: testear
        def recomendar(self,userIDowner,gradoSimilitud):
                #obtener N mas similares
                self.userIDowner    = userIDowner
                self.userPosOwner   = self.conexionDB.obtenerPosUser(self.userIDowner)
                self.grado = gradoSimilitud
                matrizSimilares = self.filtrarNMasSimilares(gradoSimilitud)
                alterno = True #Si id = True, si correl = False
                diccionario = {}
                listaProblemas = None
                #Iteramos la matriz de una forma curiosa (Como un array de posiciones dos a dos.)
                #Esperemos no tarde tanto...
                #cantidadProblemas = self.__obtenerCantidadProblemas(matrizSimilares)
                for x in np.nditer(matrizSimilares, order='C'):
                        if alterno == True:
                                #Obtenemos lista de problemas que tiene el usuario de referencia respecto al propietario.
                                listaProblemas = self.buscarProblemasUser2MinusOwner(int(x))
                                alterno = False        
                        else:
                                #Le sumamoss el peso correspondiente (Sumar correlación del usar de referencia partido de N) al problema
                                correlProblema = x
                                for idProblema in listaProblemas:
                                        #Añadimos a nuestro diccionario: TODO, CALCULAMOS MAL LA DIVISION. DEBERIA SER PARTIDO DEL TOTAL DE PROBLEMAS QUE VAMOS A BUSCAR O ALGO ASÍ.
                                        if idProblema in diccionario:
                                                #TODO: aquí debería parsear la posDelProblema en el Id del problema. Porque no la parseo...
                                                diccionario.update({idProblema : correlProblema/gradoSimilitud + diccionario.get(idProblema)})                                                
                                        else:
                                                diccionario.update({idProblema : correlProblema/gradoSimilitud})
                                alterno = True
                
                #todo: esto no ordena. BUSCAR FORMA DE ORDENARLO.
                #diccionario.sort(key=lambda x: x[1])
                diccionario = sorted(diccionario.items(), key=operator.itemgetter(1))
                diccionario.reverse()
                #Esperemos tampoco tarde...
                return diccionario #Devolvemos una lista ordenada de recomendaciones de problemas que aún no ha resuelto. (Key=ID problema / Valor=Peso de recomendacion sobre 1)
                #TODO: CREO QUE EN VEZ DE OBTENER EL ID DE PROBLEMAS OBTENEMOS LA POSICION DE LA MATRIZ, QUE NO TIENE POR QUÉ CORRESPONDERSE CON EL ID REAL, HABRIA QUE TRADUCIR EL ID.


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



"""
Prueba funcionamiento y tiempo de funciones recomendador v2
"""

# np.count_nonzero(y == 1) >> ESTA FUNCION CUENTA CUANTAS VECES SE REPITE EL VALOR UNO EN EL ARRAY Y
# np.any(a!=0)
# np.all(a==a)
f = open("resultadosV3_entrenamiento2000.txt", "w")
s_t = time()
db = conect.JuezDB()
e_t = time() - s_t
recomendador  = RecomendadorBasico(db)
listaUsuarios = db._obtenerTodosUsuarios()
for usuario in np.nditer(listaUsuarios):
        s_t = time()
        a = recomendador.recomendar(usuario,2000)
        e_t = time() - s_t

        f.write('U: '+ str(usuario) +'\n')
        for idproblema, valor in a:
                #parseamos la pos del problema en su id con db.problems[pos]
                f.write(str(db._problems[idproblema]) +'='+ str(valor) +'\n')
        f.write("[time: "+ str(e_t) +"]\n")

"""
# Entorno de pruebas: Resultados recomendador optimizado en formato txt para los primeros N usuarios de la BBDD
listaTodosUsuarios = conexion._obtenerTodosUsuarios()
# Todo: pruebas que se quitarán.
f = open("resultados2.txt", "w")



conexion = conect.JuezDB()
salto = 100
for usuario in np.nditer(listaTodosUsuarios):
        if(salto>0): #Nos saltamos los 100 primeros usuarios ya que hemos recomendado varios
                salto = salto - 1
        else:
                recomendador = RecomendadorBasico(usuario)
                a = recomendador.recomendar(10000)
                f.write('USUARIO: '+ str(usuario) +'\n')
                f.write('===========================\n')
                for idproblema, valor in a:
                        f.write(str(idproblema) +'-->'+ str(valor) +'\n')
                f.write('===========================\n')

f.close()
"""

"""

tiempo de calculo
discriminaria problemas con menos entregas quizas, y sería más costoso que recomendase esos problemas a no ser que el usuario a recomendar ya halla realizado problemas con muchas entregas...
menos eficaz para aquellos usuarios que tengan menos problemas resueltos. (Ya que recomendaría problemas que mas AC tienen principalmente)...


Para un N pequeño es poco preciso ya que hay bastantes usuarios cuya correlacion es casi 1 por haber resuelto casi todos los problemas. Para grandes precisiones... mejor un N casi del maximo.

Probemos...

si N = maximo usuarios que cumplen condicion de tener algun problema diferente...
obtenemos un grado de fiabilidad alto, pero el tiempo de calculo empeora un poco

para un N suficientemente fiable, podemos calcularlo estimando cuantos usuarios deberíamos observar sobre el total.

Si N = 10 de 5000 > Muy poco fiable y valores similares
Si N = 1000 de 5000, aumenta la fiabilidad pero nuestra "fuerza" de recomendacion sobre los problemas desciende bastante (Si antes teniamos valores de casi 1 sobre 1, ahora tenemos valores de 0.07 los mas altos)
 (Todo esto bajo el usuario de prueba "alfonsoelmas" con un total de 122 problemas resueltos (Una cantidad medio-alta sobre el total)

**TODO:
        Y para un usuario con cantidad medio-baja?
        como estimar un grado de recomendacion optimo?
        Multiplicar por algo el resultado para que no tenga tantos decimales?...
    
    CREAR VERSION EN LA QUE CARGUEMOS UNA MATRIZ DE FILAS(USERS)COLUMNAS(PROBLEMAS) EN MEMORIA PARA REDUCIR LAS CONSULTAS Y POR ENDE LA SOBRECARGA DE LA BBDD Y POR ENDE EL TIEMPO.
    CONSIDERAR QUE PARA UNA BBDD MUY GRANDE CARGAR TODO EN MEMORIA NOS SUPONDRÍA UN PROBLEMA DEBIDO A LA EXISTENCIA DE RECURSOS LIMITADOS DEL ORDENADOR.

"""
