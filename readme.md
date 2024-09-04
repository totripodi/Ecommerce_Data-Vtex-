Flask_t
#Tomas Tripodi

#contacto: 
-Email: tomastripodi99@gmail.com
-Tel: +54 011 33315761

#Flask_t es una aplicación web desarrollada en python con el framework Flask, que permite interactuar con la API de VTEX para obtener información relacionada con clientes, pedidos y productos.

#Instalación: -Clona el repositorio en tu máquina local.
https://github.com/totripodi/Ecommerce_Data-Vtex

#Crea un entorno virtual e instala las dependencias del proyecto:

#Creamos el entorno virtual  (IMPORTANTE: los comandos utilizados son para una terminal Git Bash)
python -m venv env

#Activamos el entorno virtual:
source env/Scripts/activate

#Instalamos las dependencias
pip install flask
pip install requests
pip install json

#Ejecuta la aplicación utilizando el comando: 
python .\app\app.py

#Accede a la aplicación en tu navegador utilizando la dirección local proporcionada.

#Uso:
-Abre la aplicación en tu navegador.
-Ingresa las credenciales de la API de VTEX para autenticarte.
-Interactúa con la aplicación para seleccionar el tipo de información que deseas obtener: datos del cliente, detalles de pedidos o búsqueda de productos.
-Explora las diferentes funcionalidades y características de la aplicación, visualizando los datos obtenidos de la API en la interfaz de usuario.
