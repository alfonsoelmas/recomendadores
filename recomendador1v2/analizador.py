import numpy as np
import conect
import sys
import operator
from time import time

db = conect.JuezDB()

fichero = "resultadosV2_2.txt"
leo = open(fichero, "r")

leo.readline() #primera linea se descarta
leo.readline() #segunda linea se descarta


#TODO: ver como guardo estos datos en memoria


#while no lleguemos a fin de documento
usuarioString   = leo.readline()
while usuarioString:
    usuarioId       = int(usuarioString[9:len(usuarioString)])
    leo.readline() #"================" Descartamos esta línea
    linea = leo.readline()
    while len(linea)>1 and linea[0]!="[":
        #while no encontremos "[..."
        tamPosProb = linea.find("-->")
        posProb = int(linea[0:tamPosProb])      #pos del problema en matriz
        idProb  = db._problems[posProb]         #id del problema (Traducido)
        pesoProb = float(linea[tamPosProb+3:len(linea)]) #peso del problema
        linea = leo.readline()
    leo.readline() #"====..." Descartamos esta linea
    usuarioString   = leo.readline()




