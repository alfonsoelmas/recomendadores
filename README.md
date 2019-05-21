# recomendadores

Código fuente del recomendador de pesos por K-Vecinos más similares realizado con el fin de ser aplicado para Jueces en línea como _¡Aceptaelreto!_.

El proyecto contiene varias versiones del recomendador K-Vecinos según procesos de mejora que ha ido obteniendo, así como sus fases para el entrenamiento y evaluación.

## Estructura y arquitectura de este repositorio

El repositorio está dividido en diferentes directorios, según las versiones y mejoras que ha ido sufriendo el recomendador. A continuación se lista el contenido de cada directorio.

+ _recomendador1_: contiene una primera versión del recomendador, haciendo consultas directas a un servidor de BBDD y trabajando directamente sobre esas consultas.
+ _recomendador1v2_: contiene la versión optimizada del recomendador, cargando primeramente la información de la BBDD del servidor de la BBDD y trabajando posteriormente con una Matriz cargada en memoria que representa la información de usuarios y problemas necesaria para operar sobre el recomendador.
+ _recomendador1v2\_training_: contiene una versión del directorio _recomendador1v2_ pero con ligeras modificaciones para la fase de entrenamiento y generación de resultados para la evaluación. Dentro del directorio se pueden encontrar otros dos subdirectorios:
  + _otrosEjecutables_: sontiene ejecutables extras para analizar resultados de recomendación así como reformatear la información a otra necesaria para que Pedro(el otro miembro del grupo) pudiese aplicarle el programa de evaluación que realizó.
  + _resultados_: subdirectorio con información varia de resultados del recomendador según diferentes parámetros con los que se realizó el entrenamiento, y diferentes preprocesados de la información resultante de recomendación.
+ _recomendadorConApiFinal_: recomendador por K-Vecinos con API integrada y mejoras sobre la carga de la matriz de datos en memoria. Este recomendador contiene ficheros .dat que representan la BBDD que cargan primeramente en memoria y posteriormente la API y la clase JuezDB se encargan de hacer las actualizaciones necesarias para después dejar un servidor web que pueda recibir peticiones y generar recomendaciones en base a las peticiones recibidas. El ejecutable para su uso es el fichero "Pruebas.py"
+ _recomendadorConApiInsertaMal_: Una versión con fallos de inserción al actualizar en la matriz de datos, del directorio _recomendadorConApiFinal_.


## Dependencias de ejecución

Este recomendador funciona correctamente bajo la versión *3.7* de Python. Se ha probado en SO Windows 10 pro, sin MV. No nos hacemos responsables del correcto funcionamiento en otras versiones de Python u otras versiones de Linux. Se ha comprobado que para Python *3.6* no funcionaba correctamente.

Este recomendador hace uso de las librerías externas "_pymysql_" y "_numpy_".

+ pymysql:  <https://pymysql.readthedocs.io/en/latest/>
+ numpy:    <https://www.numpy.org/>

  
El uso de pymysql se ha realizado para las consultas MySQL al servidor de BBDD MySQL alojado en local con XAMPP