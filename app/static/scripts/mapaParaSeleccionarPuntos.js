import { Map } from './MapSingleMarker.js'
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
        addSearch: false
    });
const form = document.getElementById('formulario');
form.addEventListener('submit',(e)=> submitHandler(e, map))

}