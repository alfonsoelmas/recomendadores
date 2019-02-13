import conect
import numpy as np
import sys
import operator


class RecomendadorBasico:

        #Crea el recomendador con una conexión a la BBDD y el usuario a recomendar y los problemas del usuario
        def __init__(self, userIDowner):
                self.userIDowner = userIDowner
                self.conexionDB = conect.JuezDB()
                self.listaProblemasOwner = self.obtenerProblemas(self.userIDowner)
                self.grado = 0 #El grado sera el grado de similitud o el máximo de usuarios posibles. Servira para calcular el peso del problema. (En recomendar). Se remodifica tanto en metodo filtrarNsimilares como en recomendar

        #Devuelve la correlacion entre 2 usuarios
        def correlacion(self,user1):
                #Anotación: la siguiente busqueda puede darse como una consulta más compleja antes que de forma algoritmica. (comprobar mejora de rendimiento)
                prob_comunes = self.buscarProblemasComunes(user1) #(pA)intersección(pB)
                tam_comunes = prob_comunes.size #|(pA)intersección(pB)|
                tam_pA = self.listaProblemasOwner.size #|pA|
                #todo comprobar condiciones de tamaños 0, etc.
                if tam_comunes!=0 and tam_pA!=0:
                        correl = tam_comunes/tam_pA
                        return correl
                else:
                        return 0

        # Obtencion de los problemas válidos de un usuario X
        # Llamar a esta funcion periodicamente y dejarla en memoria cada T tiempo actualizarla. (para agilizar calculo obtener correlacion de cada usuario, etc)
        def obtenerProblemas(self, user):
                #Obener Array de problemas.
                return self.conexionDB.obtenerEntregasValidasDeUser(user)


        # Obtiene el listado actual de usuarios
        def obtenerUsuarios(self):
                return self.conexionDB.obtenerUsuarios()


        # Recomienda al usuario problemas en base al algoritmo de recomendación aplicado y un grado de similitud.
        # Todo: testear
        def recomendar(self,gradoSimilitud):
                #obtener N mas similares
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

        #ObtenerTotalProblemasARecomendar
        #No hace falta.
        #def __obtenerCantidadProblemas(self, matrizUsuarios):
        #        alterno =True
        #        cantidad = 0
        #        for x in np.nditer(matrizUsuarios):
        #                if alterno==True:
        #                        #Obtenemos lista de problemas que tiene el usuario de referencia respecto al propietario.
        #                        listaProblemas = self.buscarProblemasUser2MinusOwner(int(x))
        #                        cantidad = cantidad + listaProblemas.size
        #                        alterno = False
        #                else:
                                #Obviamos esta iteración... (Iteramos 1 vez más de lo necesario... :S) 2n vs n (No importa para valores pequeños)
                                #La obviamos porque es el "contenido" del
        #                        alterno = True
        #        return cantidad

        #Metodo privado para ordenar los arrays
        #Todo, sin completar.
        def __partition(self,arr, arrp, low,high): 
            i = ( low-1 )         # index of smaller element 
            pivot = arr[high]     # pivot 
          
            for j in range(low , high): 
          
                # If current element is smaller than or 
                # equal to pivot 
                if   arr[j] >= pivot: 
                  
                        # increment index of smaller element 
                        i = i+1 
                        arr[i],arr[j] = arr[j],arr[i]
                        arrp[i],arrp[j] = arrp[j],arrp[i]
          
            arr[i+1],arr[high] = arr[high],arr[i+1]
            arrp[i+1],arrp[high] = arrp[high],arrp[i+1] 
            return ( i+1 ) 
          
        # The main function that implements QuickSort 
        # arr[] --> Array to be sorted, 
        # low  --> Starting index, 
        # high  --> Ending index 
          
        # Function to do Quick sort 
        def __quickSort(self,arr,arrp,low,high): 
                if low < high: 
          
                        # pi is partitioning index, arr[p] is now 
                        # at right place 
                        pi = self.__partition(arr, arrp,low,high) 
          
                        # Separately sort elements before 
                        # partition and after partition 
                        self.__quickSort(arr, arrp, low, pi-1) 
                        self.__quickSort(arr, arrp, pi+1, high)

        def __sortArrays(self,array,arrayp):
                sys.setrecursionlimit(50000)
                self.__quickSort(array,arrayp,0,array.size-1)
                sys.setrecursionlimit(1500)

        # ===========================================================



        # Devuelve una lista de los usuarios más similares respecto al que se va a recomendar (De cantidad "cantidad")
        # Esta lista implicará la precisión a la hora de recomendar.
        # Todo: Testear
        def filtrarNMasSimilares(self,cantidad):
                nlistaUsuarios = self.obtenerUsuarios()
                
                # Generamos una lista de correlacion asociada a la lista de Usuarios.

                if cantidad > nlistaUsuarios.size:
                        cantidad = nlistaUsuarios.size
                        self.grado = nlistaUsuarios.size
                i = 0

                #TODO> ALGORITMO POCO EFICAZ> DESCARTAR USUARIOS CULLA CORRELACION SEA 0...
                nusuariosCorrel = []
                nusersValidos = []
                #Para esto tarda casi un minuto... OPTIMIZAR ALGORITMO CORRELACION.
                for user in nlistaUsuarios:
                        correl = self.correlacion(user)
                        if correl > 0:
                            nusuariosCorrel.append(correl)
                            nusersValidos.append(user)
                            i = i + 1
                usuariosCorrel = np.array(nusuariosCorrel)
                listaUsuarios = np.array(nusersValidos)

                # Ordenamos la lista de correlación y paralelamente el array de IDs de usuario. (Quizas poco óptimo el algoritmo.)
                # Hemos descartado usuarios no válidos previamente al realizar el ordenamiento.
                
                #Antiguo algoritmo de ordenacion (Complejidad cuadratica.)
                #i=0
                # while i < usuariosCorrel.size:
                #         j = i
                #         while j < usuariosCorrel.size:
                #                 if(usuariosCorrel[j] > usuariosCorrel[i]):
                #                         reserva = usuariosCorrel[i]
                #                         usuariosCorrel[i] = usuariosCorrel[j]
                #                         usuariosCorrel[j] = reserva
                #                         reserva = listaUsuarios[i]
                #                         listaUsuarios[i] = listaUsuarios[j]
                #                         listaUsuarios[j] = reserva
                #                 j = j + 1
                #         i = i + 1

                #Probamos con QuickShort... parece que mejora bastante el ordenamiento.
                #Todo, comprobar que ordena de mayor a menor.
                self.__sortArrays(usuariosCorrel, listaUsuarios)

                #Queremos los N usuarios más similares y que tengan problemas que el propietario no.
                usuariosCorrelCant = np.empty([cantidad])
                listaUsuariosCant = np.empty([cantidad],dtype=int)
                i=0
                j=0
                while i < cantidad and j < listaUsuarios.size:
                        if self.buscarProblemasUser2MinusOwner(listaUsuarios[j]).size > 0:
                                usuariosCorrelCant[i] = usuariosCorrel[j]
                                listaUsuariosCant[i] = listaUsuarios[j]
                                i = i + 1
                        j = j + 1

                #lo transformamos en una matriz de 2 columnas (Fusión de ambos arrays en 1 matriz) (Cada array es una columna)
                matrizResultado = np.array([listaUsuariosCant,usuariosCorrelCant],dtype = float) #TODO esto no va bien, quizas porque necesito parsear el tipo int...
                return matrizResultado.transpose() #Lo trasponemos para hacer que cada columna sea un array y no cada fila sea un array como se genera por defecto.


        #Devuelve una lista de problemas comunes entre user2 y user
        def buscarProblemasComunes(self,user2):
                problemasOwner = self.listaProblemasOwner
                problemasUser2 = self.obtenerProblemas(user2)
                tam = 0
                listaComunes = np.empty([0]) #Inicializamos listaComunes a 0
                #El tamaño máximo de nuestro array comun será el mínimo del nº de problemas de uno de los dos
                if problemasOwner.size > problemasUser2.size:
                        #El propietario tiene más problemas
                        listaComunes = np.empty([problemasUser2.size],dtype=int)
                else:
                        #El propietario tiene menos problemas
                        listaComunes = np.empty([problemasOwner.size],dtype=int)
                        
                #Itero de tal forma que para cada problema del propietario busco en el otro usuario sus problemas. Si está lo añado a la lista y dejo de buscar ese problema.
                comp = False
                for problemaOwner in problemasOwner:
                        for problema in problemasUser2:
                                if comp == True:
                                        break
                                if problemaOwner == problema:
                                        listaComunes[tam] = problema
                                        tam = tam + 1
                                        comp = True
                        comp = False
                tamListaFinal = 0
                listaFinal = np.empty([tam],dtype=int) #Creamos un listado final con el tamaño adecuado
                while tamListaFinal < tam:
                        listaFinal[tamListaFinal] = listaComunes[tamListaFinal]
                        tamListaFinal = tamListaFinal + 1
                return listaFinal

        #Devuelve una lista de problemas que tiene user2 y no owner.
        def buscarProblemasUser2MinusOwner(self, user2):
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
                return listaFinal

# Todo: pruebas que se quitarán.
f = open("resultados2.txt", "w")



conexion = conect.JuezDB()
listaTodosUsuarios = conexion.obtenerTodosUsuarios()

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
