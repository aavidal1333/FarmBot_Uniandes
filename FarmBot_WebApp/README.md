## Cómo se utiliza

Para correr la WebApp se debe correr el archivo "main.py"
## Requerimientos

Para hacer uso de la WebApp debe haber una conexión serial con el FarmBot o con el FarmBot Simulator.

Además de esto hay una lista de requerimientos a continuación:

1. Python 3.8.5: Se recomienda hacer uso de pyenv para el control de versiones de python.
2. PIP actualizado: Pip se puede actualizar utilizando el comando "pip install --upgrade pip"
3. Flask: Se instala usando "pip install flask"
4. Serial: Se instala usando "pip install pyserial"

Para utilizar la WebApp en el FarmBot directamente se recomienda el uso de un Raspberry Pi. Éste debe contar con [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/) (se recomienta la versión con escritorio para desarrollo y la versión Lite para utilizar la herramienta) ya que los desarrollos se hicieron en base a este. Se deben instalar los requerimientos mencionados anteriormente. Finalmente el uso de una conexión remota ha mostrado ser útil para el manejo directo del robot y para el manejo de posibles errores a la hora de utilizar la aplicación (Se recomienda VNC para desarrollo y SSH para uso del producto terminado).

## Construcción

El desarrollo de la WebApp se basó en los códigos de comunicación serial que se enuentran en el [repositorio del firmware de FarmBot](https://github.com/FarmBot/farmbot-arduino-firmware) (al igual que el FarmBor Controller).

1. Se instaló todo el entorno de desarrollo necesario para python 3.8.5.
2. Para lograr la comunicación serial (que es la que requiere el firmware del farmduino), se hizo uso de la librería "Serial".
3. Se hizo uso de la librería "Flask" para crear un servidor virtual en el cual se va a desplegar la WebApp.
4. Se creó una interfaz en HTML para la WebApp usando el framework [Materialize](https://materializecss.com).
4. Se hicieron pruebas con los métodos usados en el FarmBot Controller individualmente.
5. Los métodos que funcionaron, se agregaron directamente a la WebApp, creando un botón en la interfaz y conectándolo con el método en cuestión.
6. Los métodos que tengan errores se corrigieron o se desecharon por la incompatibilidad con el firmware de farmduino 1.5.

# Nuevas funcionalidades

Para agregar nuevas funcionalidades a la WebApp, se debe primero revisar la documentación del [firmware del farmduino](https://github.com/FarmBot/farmbot-arduino-firmware) (al igual que el FarmBor Controller) por si existe algún código con el que se puedan recrear estas funciones en el robot. En el caso contrario, se puede desarrollar la funcionalidad directamente a la WebApp y en caso de requerir hardware adicional, este deberá ser conectado a Raspberry Pi directamente.
