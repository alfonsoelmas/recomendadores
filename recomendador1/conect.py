#Acceso a bbdd
#Instalar MySQLdb para acceder a bases de datos
import MySQLdb


#Creamos un cursor para navegar por la bbdd a la que nos hemos conectado
cur = db.cursor()

class JuezBD:
	def __init__(self):
		db = MySQLdb.connect(host = "localhost",
					 user = "root",
					 passwd = "root",
					 db = "aceptaelreto")

		self.cursor = db.cursor()

	#Metodo obtener usuarios. Devuelve un array con id de usuarios
	def obtenerUsuarios(self)
		self.cursor.execute("SELECT * FROM TU_TABLA *TODO")
		for row in self.cursor.fetchall():
			print row[0]