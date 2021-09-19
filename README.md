# conference-rekognition-app

## Server

### Instalar dependencias
En Linux:
```
sudo apt install python3-pip
sudo apt install python3-flask
sudo apt install python3-waitress
sudo apt install gunicorn
```

En el directorio *server*, instalar los paquetes:
```
pip3 install -r requirements.txt
```

### Ejecutar server modo desarrollo
En el directorio *raíz* de la app (../server) (Linux y Mac):
```
export FLASK_APP=server
export FLASK_ENV=development
flask run
```

### Ejecutar server modo producción
En el directorio *raíz* de la app (../server):
```
waitress-serve --call 'server:create_app'
```

Para ejecutar en modo daemon:
```
gunicorn --bind :8080 'server:create_app()' --daemon
```