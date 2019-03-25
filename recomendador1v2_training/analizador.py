import numpy as np
import conect
import os
import sys
import operator
from time import time
"""
    Este programilla se encarga de analizar el accuracy, precision, recall y F1 Score sobre los resultados generados
    en el entrenamiento con corte 1 año previo a la BBDD actual.
    Consideramos el estado de un predicción como:
        TP - True Positive: El usuario ha hecho a posteriori uno de los problemas que el recomendador ha recomendado
        FP - False Positive: El usuario no ha hecho a posteriori uno de los problemas que el recomendador ha recomendado
        FN - False Negative: El usuario ha hecho a posteriori uno de los problemas que el recomendador no ha recomendado
        TN - True Negative: El usuario no ha hecho a posteriori uno de los problemas que el recomendador no ha recomendado (No lo vamos a considerar para nuestras métricas).
    **Para cada caso habría que descartar aquellos usuarios que NO han realizado entregas

    Calculo sobre diferentes métricas:
        - accuracy: todo. comentar. (DE MOMENTO ESTA NO LA CALCULAMOS)
        - precision: TP / TP + FP
        - recall: TP / TP + FN
        - f1 Score: 2*(Recall*Precision)/(Recall + Precision)

    #Contar conjunto de usuarios validos para calcular la precisión
    #Calcular con TOP - 1, 3, 5, 10... N
    #calcular con filtrar N mas similares de todos, todos/2 todos/3...

    ESTO ES SUPER RANDOM, O SEA, SI CAMBIAMOS EL CORTE A OTRAS FECHAS, ETC, ETC, ETC, LAS METRICAS VARIAN MAZO...:
        Añadir en el tfg esto, y por lo tanto determinar que sirva solo para comparar entre recomendadores.
"""

TopN            = 1
#TODO: ver como guardo estos datos en memoria
fguardo = "resultados_TOP1-12_optimized_pedro_500.txt"
guardo = open(fguardo, "w")
# Conectamos la BBDD
db = conect.JuezDB()

while TopN <= 12:

    guardo.write("======TOP "+str(TopN)+" ============\n")
    #   Variables globales
    #   ==================
    TP              = 0
    FP              = 0
    FN              = 0
    TN              = 0 # No lo consideramos por el momento
    totalUsers      = 0
    descartados     = 0
    aceptados       = 0
    hits            = 0
    #   =================

    fichero         = "resultadosV3_entrenamiento500.txt"
    #   =================





    leo = open(fichero, "r")





    #while no lleguemos a fin de documento
    usuarioString   = leo.readline()
    while usuarioString:
        usuarioId       = int(usuarioString[3:len(usuarioString)])
        hastaTop = 1
        listaProblemas = []
        
        linea = leo.readline()
        
        while len(linea)>1 and linea[0]!="[":
            #while no encontremos siguiente usuario...
            tamIdProb = linea.find("=")
            idProb = int(linea[0:tamIdProb])                 #id del problema recomendado
            pesoProb = float(linea[tamIdProb+1:len(linea)]) #peso del problema
            if(hastaTop<=TopN):
                listaProblemas.append(idProb)
                hastaTop = hastaTop + 1        
            linea = leo.readline()
        #Leo siguiente usuario y se lo paso a usuarioString al final de la iteracion
        linea = leo.readline()
        #Obtengo lista problemas hechos a posteriori
        problemasPosteriori = db._obtenerEntregasValidasDeUserPostTraining(usuarioId)

        #Descarto al usuario si no ha resuelto un minimo de TopN problemas
        #Si no, compruebo si existe cada valor de listaProblemas en problemasPosteriori
        if(problemasPosteriori.size>=TopN):
            posRecomendados = 0
            posPosterioriList = 0
            while posRecomendados < len(listaProblemas):
                enc = False
                while posPosterioriList < problemasPosteriori.size:
                    if listaProblemas[posRecomendados] == problemasPosteriori[posPosterioriList]:
                        # Incrementamos true positive (Dfinicion a comienzo del codigo)
                        TP = TP + 1
                        enc = True
                    if posPosterioriList == problemasPosteriori.size-1 and enc == False:
                        # Incrementamos false positive (Definicion a comienzo del codigo)
                        FP = FP + 1
                    posPosterioriList = posPosterioriList + 1
                
                posRecomendados = posRecomendados + 1

            #Calulo false negative cases...
            posRecomendados = 0
            posPosterioriList = 0
            while posPosterioriList < problemasPosteriori.size:
                enc = False
                while posRecomendados < len(listaProblemas):
                    if listaProblemas[posRecomendados] == problemasPosteriori[posPosterioriList]:
                        enc = True
                    if posRecomendados == len(listaProblemas)-1 and enc == False:
                        # Incrementamos false negative
                        FN = FN + 1
                    posRecomendados = posRecomendados + 1
                
                posPosterioriList = posPosterioriList + 1
            aceptados = aceptados + 1
            

        else:
            descartados = descartados + 1
        totalUsers = totalUsers + 1
        cteUsers = 6533
        print("TOP "+str(TopN)+": "+str((totalUsers/cteUsers)*100)+"%")
        
        #Vuelvo a iterar
        usuarioString   = linea
        

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1Score = 2*(recall*precision)/(recall + precision)
    
    guardo.write("Total Users: "+ str(totalUsers) +"\n")
    guardo.write("Aceptados:   "+ str(aceptados) +"\n")
    guardo.write("Descartados: "+ str(descartados) +"\n")
    guardo.write("====================\n")
    guardo.write("Precision: "+ str(precision) +"\n")
    guardo.write("Recall: "+ str(recall) +"\n")
    guardo.write("f1 score: "+ str(f1Score) +"\n")
    guardo.write("====================\n")
    guardo.write("True positive: "+ str(TP) +"\n")
    guardo.write("False positive: "+ str(FP) +"\n")
    guardo.write("False negative: "+ str(FN) +"\n")
    leo.close()
    TopN = TopN+1
guardo.close()

