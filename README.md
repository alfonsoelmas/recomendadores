# recomendadores

Código fuente de los estudios sobre los recomendadores.
El proyecto contiene varios recomendadores hasta llegar a un recomendador definitivo y complejo, que se retroalimenta y mejora.

## Estructura
  ### Recomendador simple con correlación entre usuarios
  #### Subdirectorio "recomendador1"
  Recomendador simple que aplica el coeficiente de correlación entre usuarios en base a la cantidad de problemas similares y recomienda problemas que tengan otros usuarios con un coeficiente de correlación alto entre ambos.
  + Clase conect: Implementa conexión a bbdd > En java implementará una interfaz. En python no es necesario.
  + Clase recomendador: Implementa la clase que actúa de recomendador.
  + Coeficiente de correlacion entre dos usuarios> coef(A,B):
    + Sea pA el conjunto de problemas del usuario A a recomendar, pB el conjunto de problemas del usuario B sobre el que observar. (pA ∩ pB) los problemas en comun de pA y pB... Definimos el grado de relación de un usuario B respecto a A sobre 1 como |(pA ∩ pB)|/|pA|.
   + Grado o N:
     + Definimos el grado de recomendación (o N) como el número de usuarios sobre el que vamos a referenciar la recomendación siendo este el máximo posible el total de usuarios de la Base de datos. El grado 
   + Problemas a recomendar:
     + Dados N usuarios con coeficiente de correlación alto sobre el usuario a recomendar A. Sean pBi los problemas de un usuario Bi, y pA los problemas de pA. Los problemas a recomendar al usuario A vienen dados calculando coef. correl de Bi sobre A para cada problema t.q (pBi-pA) * coef.Correl/(grado). Obteniendo una tabla de id, n, listado coeficientes (por problema). para obtener una media(En realidad no habría que aplicar una media como tal, seguramente) de correlación de problemas y ordenarlos de mayor a menor. Posteriormente, se podrán recomendar varios problemas con diferente grado de recomendación. Además tendrán diferentes recomendaciónes segun el conjunto N de usuarios a elegir. (Máximo toda la base de datos> Esto no es óptimo en rendimiento, pero si es mejor en precisión)
   + Genera problemas de recomendacion si usuario nuevo, ya que recomendará los más realizados y seguirá un patrón tras ello probablemente.
   > Solucionar haciendo un random correl muy ligero para dar un poco más de peso aleatorio a algunos problemas y que no siempre recomiende lo mismo dentro de una recomendación mínimamente acertada. (O si tengo N problemas con un grado de recomendación similar, hacer un random pa recomendar uno de ellos).

  ### Recomendador basado en redes neuronales
  #### Subdirectorio "recomendadorNeuronal"
  
  + Por hacer y estructurar
  + Intenciones de crear subdirectorio con pruebas de redes neuronales antes de pasar a usarlas para recomendar.

## Comentarios e ideas a futuro:

En un futuro el recomendador tendrá una BBDD propia (Pueda ser MONGODB o SQL según lo que veamos más óptimo y eficaz) que almacenará recomendaciones previas de cada usuario a modo de "historia" y esa BBDD se vaya actualizando en base a su éxito "a modo de predictor".
+ P. ejemplo:
  + Si el usuario quiere hacer un problema de los recomendados, y lo acierta, el predictor se actualiza.
+ Esto se puede trasnformar también a varias matrices, una de ellas estará ligada a la probabilidad de cada usuario por cada 	problema almacenado en una BBDD de filas=IDuser columnas=IDproblema y valor=prob. éxito (Grado de recomendación)
  + Esta idea viene ligada al recomendador bayesiano final que se realizará.
+ Leer sobre funcionamiento red neuronal para implementar en posible recomendador (Una vez se haya realizado el bayesiano)

+ **ATENCION**: Mejorar algoritmo ordenacion de normal a QuickShort y ver rendimiento nuevo. (En filtrarNmassimilares)
  + En otro caso coger un subconjunto más pequeño al obtener usuarios similares... descartar los que correl == 0... etc...

### Enlaces de interés
  + https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html#array-methods > Documentación y uso numpy
  + https://github.com/ricval/Documentacion/blob/master/Guias/GitHub/mastering-markdown.md > Guía formato README github
  + https://docs.scipy.org/doc/numpy-1.10.1/reference/arrays.nditer.html > Iteraciones con matrices
  + Resto enlaces de interés en documentos de google docs (Apuntes y cuaderno bitácoras)
  + http://webs.ucm.es/info/aocg/python/modulos_cientificos/numpy/index.html > Pequeña guía básica sobre numpy