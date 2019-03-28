import conect
# import recomendador_basico
#Ejecución de pruebas

"""
Ejecutamos nueva clase conect para generar matriz en local y probar su carga desde local, etc.
"""
db = conect.JuezDB()
print(db.matrizDatos)



"""
Pruebas de funcionamiento recomendador:

Ejecuta el recomendador para k-vecinos = cada elemento de lista valores.
cada resultado de recomendación de toda la BBDD los guarda en diferentes TXT.
Realizado para el entrenamiento del recomendador.
"""
"""
listaValores = ["3","10","20","50","100","250","500","1000","2000","4000","5000","6000","All"]
for x in listaValores:
	f = open("resultadosV3_entrenamiento"+x+".txt", "w")
	s_t = time()
	db = conect.JuezDB()
	e_t = time() - s_t
	recomendador  = RecomendadorBasico(db)
	listaUsuarios = db._obtenerTodosUsuarios()
	for usuario in np.nditer(listaUsuarios):
	        s_t = time()
	        a = recomendador.recomendar(usuario,1000)
	        e_t = time() - s_t

	        f.write('U: '+ str(usuario) +'\n')
	        for idproblema, valor in a:
	                #parseamos la pos del problema en su id con db.problems[pos]
	                f.write(str(db._problems[idproblema]) +'='+ str(valor) +'\n')
	        f.write("[time: "+ str(e_t) +"]\n")
"""