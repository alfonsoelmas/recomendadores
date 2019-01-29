import conect

class RecomendadorBasico:

	#Crea el recomendador con una conexión a la BBDD y el usuario a recomendar
	def __init__(self, userIDowner):
		self.userIDowner = userIDowner
		self.conexionDB = JuezDB()

	#Devuelve la correlacion entre 2 usuarios
	def correlacion(user1,user2):
		#todo

	#Obtencion de los problemas válidos de un usuario X
	def obtenerProblemas(self, user):
		#todo
		#OBTENER LA MATRIZ DE PROBLEMAS/posicion. Obviar la posición de momento a la hora de calcular la correlación.
		self.conexionDB.obtenerEntregasValidasDeUser(self, user)

	#Obtiene el listado actual de usuarios
	def obtenerUsuarios():
		#todo


	#Recomienda a un usuario un lisado de 10 problemas en base al algoritmo de recomendación aplicado.
	def recomendarSimple(user):
		#todo

	
	#Devuelve una lista de los usuarios más similares respecto al que se va a recomendar (De cantidad "cantidad")
	#Esta lista implicará más precisión a la hora de recomendar.
	def filtrarNMasSimilares(cantidad):

	#Devuelve una lista de problemas comunes entre user2 y user
	def buscarProblemasComunes(user2):