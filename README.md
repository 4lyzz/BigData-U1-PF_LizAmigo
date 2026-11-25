# BigData-U1-PF_LizAmigo
Link PythonAnywhere: https://4lyzz.pythonanywhere.com/

Que ha hecho que funcione en PythonAnywhere||Que diferencia hay sobre el codigo de versión local:
En local, el csv funcionaba porque estaba dentro de la carpeta del proyecto, mientras que en PythonAnywhere, como el servidor arranca desde otra carpeta distinta y por tanto no funcionaba. Al añadir BASE_DIR como ruta completa donde vive cada archivo, el programa logra leer el csv.
