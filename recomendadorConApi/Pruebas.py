#import conect
# import recomendador_basico
#Ejecución de pruebas

"""
Ejecutamos nueva clase conect para generar matriz en local y probar su carga desde local, etc.
"""
"""
db = conect.JuezDB()
print(db.matrizDatos)
print(db._users)
print(db._problems)
"""

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


"""
Pruebas servidor HTTP y realizador peticiones HTTP
+
Pruebas con XML
"""
import requests 				#para peticiones HTTP
import json
# ultimoSubmitRecomender = db._lastSubmition
ultimoSubmitAceptaelreto = 1
K = 300000
iterMax = 300000//20
j=0
while j < iterMax:
    req = requests.get('https://www.aceptaelreto.com/ws/submission/?start='+str(20*j+1)+'&size=20')#Obtenemos un JSON en texto
    resultados = json.loads(req.text)   #Lo transformamos a un objeto
    for i in resultados["submission"]:
        print(i["user"]["nick"] + " ha intentado: " + i["problem"]["title"] + "- ENVÍO: " + str(i["num"]))
    j = j + 1
# ANOTACION, SOLO PUEDO OBTENER LOS 41MIL ULTIMAS ENTREGAS.




