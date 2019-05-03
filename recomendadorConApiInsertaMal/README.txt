RECOMENDADOR COMPLETO
=====================

Contiene:
"conect": encargada del almacenamiento de datos y la carga de datos
	- necesario configurar datos de servidor BBDD para obtener por primera vez la matriz de usuarios/problemas/ACs
"server": API encargada de recibir solicitudes de recomendacion de un user, y leer periodicamente las entregas para actualizar el recomendador y conect.

"recomendador_basico": Núcleo de la aplicación
	- Realiza una recomendación de un usuario que le pide "server"
	