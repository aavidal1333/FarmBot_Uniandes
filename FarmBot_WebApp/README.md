## Cómo se utiliza

Para correr la WebApp se debe correr el archivo "main.py"
## Requerimientos

Para hacer uso de la WebApp debe haber una conexión serial con el FarmBot o con el FarmBot Simulator.

Además de esto hay una lista de requerimientos a continuación:

1. Python 3.8.5: Se recomienda hacer uso de pyenv para el control de versiones de python.
2. PIP actualizado: Pip se puede actualizar utilizando el comando "pip install --upgrade pip"
3. Flask: Se instala usando "pip install flask"

## Construcción

1. El desarrollo de la WebApp se basó en los códigos de comunicación serial que se enuentran en el [repositorio del firmware de FarmBot](https://github.com/FarmBot/farmbot-arduino-firmware) (al igual que el FarmBor Controller).
2. Para lograr la comunicación serial (que es la que requiere el firmware del farmduino), se hace uso de la librería "Serial".
3. Se hizo uso de la librería "Flask" para crear un servidor virtual en el cual se va a desplegar la WebApp.
4. Se hicieron pruebas con los métodos usados en el FarmBot Controller individualmente.
5. Los métodos que funcionan se agregan directamente a la WebApp, creando un botón en la interfaz y conectándolo con el método en cuestión.
6. Los métodos que tengan errores se procede a corregirlos.

# Nuevas funcionalidades

Para agregar nuevas funcionalidades a la WebApp, se debe primero revisar la documentación del [firmware del farmduino](https://github.com/FarmBot/farmbot-arduino-firmware) (al igual que el FarmBor Controller) por si existe algún código con el que se puedan recrear estas funciones en el robot. En el caso contrario, se puede desarrollar la funcionalidad directamente a la WebApp y en caso de requerir hardware adicional, este deberá ser conectado a Raspberry Pi directamente.
