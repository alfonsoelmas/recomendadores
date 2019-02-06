import conect
import numpy as np

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
                matrizSimilares = self.filtrarNMasSimilartes(gradoSimilitud)
                alterno = True #Si id = True, si correl = False
                diccionario = 0
                listaProblemas = None
                #Iteramos la matriz de una forma curiosa (Como un array de posiciones dos a dos.)
                for x in np.nditer(matrizSimilares):
                        if alterno == True:
                                #Obtenemos lista de problemas que tiene el usuario de referencia respecto al propietario.
                                listaProblemas = buscarProblemasUser2MinusOwner(x)
                                alterno = False        
                        else:
                                #Le sumamoss el peso correspondiente (Sumar correlación del usar de referencia partido de N) al problema
                                correlProblema = x
                                for idProblema in listaProblemas:
                                        #Añadimos a nuestro diccionario
                                        if(diccionario.get(idProblema)==None):
                                                diccionario[idProblema] = correlProblema/self.grado
                                        else:
                                                diccionario[idProblema] = correlProblema/self.grado + diccionario[idProblema]
                                alterno = True
                
                diccionario.sort(key=lambda x: x[1])
                return diccionario #Devolvemos una lista ordenada de recomendaciones de problemas que aún no ha resuelto. (Key=ID problema / Valor=Peso de recomendacion sobre 1)

        

        #Metodo privado para ordenar los arrays
        #Todo, sin completar.
		def __sort(arrayOrdenar,arrayParalelo):
		    less = []
		    equal = []
		    greater = []

		    if len(array) > 1:
		        pivot = array[0]
		        for x in array:
		            if x < pivot:
		                less.append(x)
		            elif x == pivot:
		                equal.append(x)
		            else x > pivot:
		                greater.append(x)
		        # Don't forget to return something!
		        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
		    # Note that you want equal ^^^^^ not pivot
		    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
		        return array



        # Devuelve una lista de los usuarios más similares respecto al que se va a recomendar (De cantidad "cantidad")
        # Esta lista implicará la precisión a la hora de recomendar.
        # Todo: Testear
        def filtrarNMasSimilares(self,cantidad):
                listaUsuarios = self.obtenerUsuarios()
                
                # Generamos una lista de correlacion asociada a la lista de Usuarios.
                #TODO> ALGORITMO POCO EFICAZ> DESCARTAR USUARIOS CULLA CORRELACION SEA 0...
                usuariosCorrel = np.empty([listaUsuarios.size])
                if cantidad > listaUsuarios.size:
                        cantidad = listaUsuarios.size
                        self.grado = listaUsuarios.size
                i = 0
                for user in listaUsuarios:
                        correl = self.correlacion(user)
                        usuariosCorrel[i] = correl
                        i = i + 1
                # Ordenamos la lista de correlación y paralelamente el array de IDs de usuario. (Quizas poco óptimo el algoritmo.)
                
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

                #Probamos con QuickShort...



                # TODO > TENER EN CUENTA MATRIZ DEBE TENER TODO EL MISMO TIPO (FLOAT PARSEO EL ID)
                # TODO > TRASPONER MATRIZ, LUEGO ORDENARLA POR SEGUNDA FILA> matriz.view('i8,i8,i8').sort(order=['f1'], axis=0) > quedarnos con las N primeras filas.
                # TODO > SI TRAS ESTO SIGUE TARDANDO, HACER ALMACENAMIENTO "TEMPORAL" Y PERIODICO DE ESTE PASO PARA AGILIZAR > DESVENTAJA : RECOMENDADOR UN POCO MAS FLOJO.
                #Queremos los N usuarios más similares.
                usuariosCorrelCant = np.empty([cantidad])
                listaUsuariosCant = np.empty([cantidad],dtype=int)
                i=0
                while i<cantidad:
                        usuariosCorrelCant[i] = usuariosCorrel[i]
                        listaUsuariosCant[i] = listaUsuarios[i]
                        i = i + 1
                #lo transformamos en una matriz de 2 columnas (Fusión de ambos arrays en 1 matriz) (Cada array es una columna)
                matrizResultado = np.array(listaUsuariosCant,usuariosCorrelCant)
                matrizResultado.transpose() #Lo trasponemos para hacer que cada columna sea un array y no cada fila sea un array como se genera por defecto.
                return matrizResultado


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

#Todo: pruebas que se quitarán.
recomendador = RecomendadorBasico(847)
recomendador.filtrarNMasSimilares(10)
