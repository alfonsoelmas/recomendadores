import conect
import numpy as np

class RecomendadorBasico:

	#Crea el recomendador con una conexión a la BBDD y el usuario a recomendar
	def __init__(self, userIDowner):
		self.userIDowner = userIDowner
		self.conexionDB = JuezDB()

	#Devuelve la correlacion entre 2 usuarios
	def correlacion(user1,user2):
		#todo: Sin terminar
		usuarios = obtenerUsuarios()
		for user in usuarios:
			prob_comunes = buscarProblemasComunes(user)
			#todo

	#Obtencion de los problemas válidos de un usuario X
	def obtenerProblemas(self, user):
		#todo: Sin terminar (Debemos solo usar de momento una array simple y no una matriz)
		#OBTENER LA MATRIZ DE PROBLEMAS/posicion. Obviar la posición de momento a la hora de calcular la correlación.
		return self.conexionDB.obtenerEntregasValidasDeUser(self, user)


	#Obtiene el listado actual de usuarios
	def obtenerUsuarios():
		#todo: testear
		return self.conexionDB.obtenerUsuarios()



	#Recomienda a un usuario un lisado de 10 problemas en base al algoritmo de recomendación aplicado.
	def recomendarSimple(user):
		#todo: sin completar

	
	#Devuelve una lista de los usuarios más similares respecto al que se va a recomendar (De cantidad "cantidad")
	#Esta lista implicará más precisión a la hora de recomendar.
	def filtrarNMasSimilares(cantidad):
		#todo: sin completar

	#Devuelve una lista de problemas comunes entre user2 y user
	def buscarProblemasComunes(self,user2):
		#todo: Testear
		problemasOwner = obtenerProblemas(self.userIDowner)
		problemasUser2 = obtenerProblemas(user2)
		tam = 0
		listaComunes = np.empty([0]) #Inicializamos listaComunes a 0
		#El tamaño máximo de nuestro array comun será el mínimo del nº de problemas de uno de los dos
		if problemasOwner.size > problemasUser2.size:
			#El propietario tiene más problemas
			listaComunes = np.empty([problemasUser2.size])
		else:
			#El propietario tiene menos problemas
			listaProblemas = np.empty([problemasOwner.size])
			
		#Itero de tal forma que para cada problema del propietario busco en el otro usuario sus problemas. Si está lo añado a la lista y dejo de buscar ese problema.
		comp = false
		for problemaOwner in problemasOwner:
			for problema in problemasUser2 and not comp:
				if problemaOwner == problema:
					listaComunes[tam] = problema
					tam = tam + 1
					comp = true
			comp = false
		tamListaFinal = 0
		listaFinal = np.empty([tam]) #Creamos un listado final con el tamaño adecuado
		while tamListaFinal != tam:
			listaFinal[tamListaFinal] = listaComunes[tamListaFinal]
			tamListaFinal = tamListaFinal + 1
		
		return listaFinal

