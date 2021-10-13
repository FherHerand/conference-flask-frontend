# conference-flask-frontend

## Server

### Instalar dependencias
Instalar dependencias y python (Linux):
```
# Linux
sudo apt install python3-pip
sudo apt install python3-flask
sudo apt install python3-waitress
sudo apt install gunicorn

# Windows
Solo instalar python3 desde la página de python* o de la Microsoft Store
```

En el directorio *server*, instalar los paquetes:
```
pip3 install -r requirements.txt
```

### Ejecutar server modo desarrollo
En el directorio *raíz* de la app (../server):
```
# Linux
export FLASK_APP=server
export FLASK_ENV=development
flask run

# Windows (cmd)
set FLASK_APP=server
set FLASK_ENV=development
python -m flask run

# Windows (Powershell)
$env:FLASK_APP="server"
$env:FLASK_ENV="development"
python -m flask run
```

### Ejecutar server modo producción (Linux)
En el directorio *raíz* de la app (../server):
```
waitress-serve --call 'server:create_app'
```

Para ejecutar en modo daemon:
```
gunicorn --bind :8080 'server:create_app()' --daemon
```

### Links
* [Página de python](https://www.python.org/downloads/)