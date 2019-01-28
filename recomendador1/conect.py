#Acceso a bbdd
#Instalar MySQLdb para acceder a bases de datos
import pymysql.cursors



class JuezDB:
	def __init__(self):
		db = pymysql.connect('localhost', 'root', '', 'aceptaelreto')
		self.cursor = db.cursor()

	#Metodo obtener usuarios. Devuelve un array con id de usuarios
	def obtenerUsuarios(self):
		recs = self.cursor.execute('SELECT id, gender FROM users')

		for row in self.cursor.fetchone():
			print("UserId: "+ row[id] + "have gender: " + row[gender])

conector = JuezDB()
conector.obtenerUsuarios()
