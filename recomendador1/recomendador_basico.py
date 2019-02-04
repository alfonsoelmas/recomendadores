import conect
import numpy as np

class RecomendadorBasico:

        #Crea el recomendador con una conexión a la BBDD y el usuario a recomendar y los problemas del usuario
        def __init__(self, userIDowner):
                self.userIDowner = userIDowner
                self.conexionDB = conect.JuezDB()
                self.listaProblemasOwner = self.obtenerProblemas(self.userIDowner)

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



        # Recomienda al usuario problemas en base al algoritmo de recomendación aplicado.
        def recomendar():
                return
                #todo: sin completar
                #obtener N mas similares.
                #inicializar array de problemas de tamaño N
                #para cada problema en concreto (id) su valor "peso" p[i] = p[i] + pesoCorrelUsuariomirando, siendo p[i] un problema concreto del array de problemas y mirando la lista de problemas disjuntos del usuario
                #obtener problemas de cada usuario
                #

        
        # Devuelve una lista de los usuarios más similares respecto al que se va a recomendar (De cantidad "cantidad")
        # Esta lista implicará la precisión a la hora de recomendar.
        # Todo: Testear
        def filtrarNMasSimilares(self,cantidad):
                listaUsuarios = self.obtenerUsuarios()
                # Generamos una lista de correlacion asociada a la lista de Usuarios.
                usuariosCorrel = np.empty([listaUsuarios.size])
                if cantidad > listaUsuarios.size:
                        cantidad = listaUsuarios.size
                i = 0
                for user in listaUsuarios:
                        correl = self.correlacion(user)
                        usuariosCorrel[i] = correl
                        i = i + 1
                # Ordenamos la lista de correlación y paralelamente el array de IDs de usuario. (Quizas poco óptimo el algoritmo.)
                i=0
                while i < usuariosCorrel.size:
                        j = i
                        while j < usuariosCorrel.size:
                                if(usuariosCorrel[j] > usuariosCorrel[i]):
                                        reserva = usuariosCorrel[i]
                                        usuariosCorrel[i] = usuariosCorrel[j]
                                        usuariosCorrel[j] = reserva
                                        reserva = listaUsuarios[i]
                                        listaUsuarios[i] = listaUsuarios[j]
                                        listaUsuarios[j] = reserva
                                j = j + 1
                        i = i + 1
                #Queremos los N usuarios más similares.
                usuariosCorrelCant = np.empty([cantidad])
                listaUsuariosCant = np.empty([cantidad],dtype=int)
                i=0
                while i<cantidad:
                        usuariosCorrelCant[i] = usuariosCorrel[i]
                        listaUsuariosCant[i] = listaUsuarios[i]
                        i = i + 1
                #lo transformamos en una matriz de 2 columnas (Fusión de ambos arrays en 1 matriz) (Cada array es una columna)
                matrizResultado = np.array(usuariosCorrelCant,listaUsuariosCant)
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
                listaFinal = np.empty([tam+1],dtype=int) #Creamos un listado final con el tamaño adecuado
                while tamListaFinal <= tam:
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


recomendador = RecomendadorBasico(847)
recomendador.correlacion(2742)