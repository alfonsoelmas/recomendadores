Resultados de entrenamiento para diferentes configuraciones del recomendador de N-similares más próximos.
Contiene diversos TXT con N=(2-All].

El contenido de los TXT es el resultado de hacer un str(diccionario) en python por lo que tiene el formato original de las estructuras de
diccionarios de python y se puede cargar como tal directamente a memoria para trabajar con él.

EL CORTE QUE SE HA REALIZADO EN ESTE ENTRENAMIENTO ES 1 AÑO PREVIO A LA ÚLTIMA ENTREGA, por lo que las consultas para obtener usuarios, problemas, y entregas son las siguientes:

Obtener entregas validas de user:
'SELECT DISTINCT problem_id FROM submission WHERE user_id = '+str(user)+' AND status = "AC" AND submissionDate <= "2017-10-23 08:00:00" group by problem_id'
Obtener entregas validas de user post entrenamiento:
'SELECT DISTINCT problem_id FROM submission WHERE user_id = '+str(user)+' AND status = "AC" AND submissionDate > "2017-10-23 08:00:00" group by problem_id'
Obtener todos los usuarios:
'SELECT id from users WHERE registrationDate <= "2017-10-23 08:00:00" ORDER BY id ASC'
Obtener todos los problemas:
'SELECT internalId from problem WHERE publicationDate <= "2017-10-23 08:00:00" ORDER BY internalId ASC'

**Se necesita:

- Calcular tus TP,FP,TN,FN para obtener las métricas recall, precision, 1-hit, MMR... etc