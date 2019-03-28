import sys, os

"""nombreCSV = #todo
csvGuardo = #todo
"""


listaValores = ["3","10","20","50","100","250","500","1000","2000","4000","5000","6000","All"]

for i in listaValores:
        nombreTXT = "resultadosV3_entrenamiento"+i+".txt"
        guardoTXT = nombreTXT[0:len(nombreTXT)-4]+"_parseadoTOP10.txt"
        leo = open(nombreTXT,"r")

        usuarioString = leo.readline()
        usersDict = {}
        while usuarioString:
                usuarioId = int(usuarioString[3:len(usuarioString)])
                listaProblemas = {}

                linea = leo.readline()
                top=0
                while len(linea)>1 and linea[0]!="[":
                        if top <= 10:
                                tamIdProb = linea.find("=")
                                idProb = int(linea[0:tamIdProb])
                                pesoProb = float(linea[tamIdProb+1:len(linea)])
                                listaProblemas[idProb]=pesoProb
                        linea = leo.readline()
                        top = top + 1
                usersDict[usuarioId] = listaProblemas
                usuarioString = leo.readline()
                
        leo.close()
        guardo = open(guardoTXT,"w")
        guardo.write(str(usersDict))
        guardo.close()
