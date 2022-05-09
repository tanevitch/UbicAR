# UbicAR

Aplicación realizada para la materia Proyecto de Software, año 2021

## Objetivo
Proveer a los ciudadanos de La Plata y zonas aledañas un mapa de evacuación en caso de inundación, y la posibilidad de realizar denuncias que involucren eventos que podrían afectar el correcto funcionamiento del sistema de drenaje pluvial.

_La autenticación por google se encuentra desactivada._

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