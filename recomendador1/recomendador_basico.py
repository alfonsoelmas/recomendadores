import conect
import numpy as np

class RecomendadorBasico:

	#Crea el recomendador con una conexión a la BBDD y el usuario a recomendar y los problemas del usuario
	def __init__(self, userIDowner):
		self.userIDowner = userIDowner
		self.conexionDB = JuezDB()
		self.listaProblemasOwner = self.obtenerProblemas(self.userIDowner)

	#Devuelve la correlacion entre 2 usuarios
	def correlacion(self,user1):
		prob_comunes = self.buscarProblemasComunes(user1)
		#Todo: Completar.

	#Obtencion de los problemas válidos de un usuario X
	#Todo: Testear
	def obtenerProblemas(self, user):
		#Obener Array de problemas.
		return self.conexionDB.obtenerEntregasValidasDeUser(self, user)


	#Obtiene el listado actual de usuarios
	#Todo: Testear
	def obtenerUsuarios():
		return self.conexionDB.obtenerUsuarios()



	#Recomienda al usuario problemas en base al algoritmo de recomendación aplicado.
	def recomendar():
		#todo: sin completar

	
	#Devuelve una lista de los usuarios más similares respecto al que se va a recomendar (De cantidad "cantidad")
	#Esta lista implicará más precisión a la hora de recomendar.
	def filtrarNMasSimilares(self,cantidad):
		listaUsuarios = self.obtenerUsuarios()
		for user in listaUsuarios:
			self.correlacion(user)
			#todo una vez la correlacion, mirar sus disjuntos y si tiene... añadir a matriz con grado de correlacion y lista de disjuntos
		#todo: sin completar

	#Devuelve una lista de problemas comunes entre user2 y user
	#Todo: Testear
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
			listaProblemas = np.empty([problemasOwner.size],dtype=int)
			
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
	
	#Devuelve una lista de problemas que tiene user2 y no owner.
	def buscarProblemasUser2MinusOwner(self, user2):
		problemasOwner = self.listaProblemasOwner
		problemasUser2 = self.obtenerProblemas(user2)
		tam = 0
		listaComunes = np.empty([0]) #Inicializamos listaComunes a 0
		#El tamaño máximo de nuestro array comun será como mucho el numero de problemas de user2
		listaComunes = np.empty([problemasUser2.size],dtype=int)
			
		#Itero de tal forma que para cada problema del propietario busco en el otro usuario sus problemas. Si está lo añado a la lista y dejo de buscar ese problema.
		comp = false
		for problemaUser in problemasUser2: #TODO ITERAR PARA VER Q NO LO TIENE...
			for problemaOwner in problemasOwner:
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
