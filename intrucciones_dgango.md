## activar entorno django
source ./ruta/bin/activate

## Emepezar un proyecto django en terminal
django-admin startproject nombre_proyecto .

## Lo anterior con un codigo python crea un proyecto automaticamente con este comando
## IMPORTANTE por defecto ocupa sqlite3
python3 manage.py runserver

##############################################################################################################################################

                                                   #CREAR PROYECTO

## Empezando el proyecto, crear una aplicacion con django, en la practica es una carpeta llamada task
python3 manage.py startapp nombre_aplicacion

# Esta app esta desconectada para conectar
* En carpeta de django:
     - En settings.py:
         - buscar la seccion INSTALLED_APPS = [, , , nombre_app] agregar el nombre

# Crear registros en la base de datos de sqlite
* python manage.py makemigrations
# Ejecutar las migraciones para hacer tablas de datos
* python manage.py migrate
# Verificar si estan hechas las migraciones
* python manage.py showmigrations

# Crear un usuario administrador para hacer configuraciones
* python manage.py createsuperuser
     - introducimos nombre_del_usuario
     - introducimos cualquier_mail
     - introducimos contraseña
     - repetimos la contraseña

#############################################################################################################################################


                                                  #CONFIGURAR PROYECTO

                                                  
