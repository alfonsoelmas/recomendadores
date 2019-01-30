# recomendadores

Código fuente de los estudios sobre los recomendadores.
El proyecto contiene varios recomendadores hasta llegar a un recomendador definitivo y complejo, que se retroalimenta y mejora.

## Estructura
  ### Recomendador 1
  Recomendador simple que aplica el coeficiente de correlación entre usuarios en base a la cantidad de problemas similares y recomienda problemas que tengan otros usuarios con un coeficiente de correlación alto entre ambos.
  + Clase conect: Implementa conexión a bbdd > En java implementará una interfaz. En python no es necesario.
  + Clase recomendador: Implementa la clase que actúa de recomendador.


## Comentarios e ideas a futuro:
En un futuro el recomendador tendrá una BBDD propia (Pueda ser MONGODB o SQL según lo que veamos más óptimo y eficaz) que almacenará recomendaciones previas de cada usuario a modo de "historia" y esa BBDD se vaya actualizando en base a su éxito "a modo de predictor".
+ P. ejemplo:
  + Si el usuario quiere hacer un problema de los recomendados, y lo acierta, el predictor se actualiza.
+ Esto se puede trasnformar también a varias matrices, una de ellas estará ligada a la probabilidad de cada usuario por cada 	problema almacenado en una BBDD de filas=IDuser columnas=IDproblema y valor=prob. éxito (Grado de recomendación)
  + Esta idea viene ligada al recomendador bayesiano final que se realizará.
+ Leer sobre funcionamiento red neuronal para implementar en posible recomendador (Una vez se haya realizado el bayesiano)

### Enlaces de interés
  + https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html#array-methods > Documentación y uso numpy
  + https://github.com/ricval/Documentacion/blob/master/Guias/GitHub/mastering-markdown.md > Guía formato README github
  + https://docs.scipy.org/doc/numpy-1.10.1/reference/arrays.nditer.html > Iteraciones con matrices
