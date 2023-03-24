# UbicAR

Aplicación realizada para la materia Proyecto de Software, año 2021

![Pantalla de inicio de la aplicación](home.png?raw=true "Pantalla de Inicio")


## Objetivo
Proveer a los ciudadanos de La Plata y zonas aledañas un mapa de evacuación en caso de inundación, y la posibilidad de realizar denuncias que involucren eventos que podrían afectar el correcto funcionamiento del sistema de drenaje pluvial.

_La autenticación por google se encuentra desactivada._

## Acceso
Los usuarios por defecto son los siguientes:
```sh
- usuario: mariar@example.com contraseña: 1234 rol: administrador
- usuario: juanp@example.com contraseña: 1234 rol: operario
- usuario: marcosg@example.com contraseña: 1234 rol: administrador y operario
```

## Funcionalidades
* ABM usuarios, habilitación de usuarios, asignación de roles
* ABM puntos de encuentro, zonas inundables y recorridos de evacuación
* ABM de denuncias, seguimiento de denuncias 
* Configuración de paginación, colores y orden de los resultados


## Instalación 
```sh
git clone https://github.com/tanevitch/UbicAR.git && cd UbicAR
```

### Backend (:5000)
```sh
pip install -r requirements.txt
set FLASK_ENV=development
set DB_HOST=tudbhost
set DB_USER=tudbuser
set DB_PASS=tudbpass
set DB_NAME=tudbname
flask run
```

### Frontend (:8080)
```sh
cd web 
npm i
npm run serve
```