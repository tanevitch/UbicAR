import { Map,array, limpiarMapa, removeLastMarker } from './MapMultiMarker.js'
const submitHandler = (e) => {
    if (array.length <= 2 ){
        e.preventDefault();
        alert('Debes seleccionar al menos tres puntos en el mapa');
    }
    else {
        document.getElementById('latAndLong').setAttribute('value',array);
    }
}

window.onload = () => {
    const map = new Map({
        selector: 'mapid',
        addSearch: false
    });

const form = document.getElementById('form');
const button = document.getElementById('removeLast');

button.addEventListener('click',(e)=> {removeLastMarker(e);})
form.addEventListener('submit',(e)=> submitHandler(e))
form.addEventListener('reset',(e)=> {
    limpiarMapa()
})
}