# recomendadores

Código fuente de los estudios sobre los recomendadores.
El proyecto contiene varios recomendadores hasta llegar a un recomendador definitivo y complejo, que se retroalimenta y mejora.




## Comentarios e ideas a futuro:
En un futuro el recomendador tendrá una BBDD propia (Pueda ser MONGODB o SQL según lo que veamos más óptimo y eficaz) que almacenará recomendaciones previas de cada usuario a modo de "historia" y esa BBDD se vaya actualizando en base a su éxito "a modo de predictor".
+ P. ejemplo:
++ Si el usuario quiere hacer un problema de los recomendados, y lo acierta, el predictor se actualiza.
+ Esto se puede trasnformar también a varias matrices, una de ellas estará ligada a la probabilidad de cada usuario por cada 	problema almacenado en una BBDD de filas=IDuser columnas=IDproblema y valor=prob. éxito (Grado de recomendación)
++ Esta idea viene ligada al recomendador bayesiano final que se realizará.
+ Leer sobre funcionamiento red neuronal para implementar en posible recomendador (Una vez se haya realizado el bayesiano)
