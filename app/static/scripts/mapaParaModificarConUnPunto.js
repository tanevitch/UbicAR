import { Map } from './MapSingleMarkerSetter.js'
var flaskData = $('#my-data').data();
const submitHandler = (e,map) => {
    
    if (!map.marker){
        e.preventDefault();
        alert('Debes seleccionar una ubicacion en el mapa');
    }
    else {       
        var latlng = map.marker.getLatLng(); 
        document.getElementById('coords').setAttribute('value',"["+latlng.lat +","+ latlng.lng+"]");
    }
}
window.onload = () => {
    const map = new Map({
        selector: 'mapid',
        coords: flaskData["name"]['coords'],
    });

const form = document.getElementById('formulario');
form.addEventListener('submit',(e)=> submitHandler(e, map))
}