const initialLat = -34.9187;
const initialLng = -57.956;
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'; //https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png
var array = [];
var mapMarkers = []
var index = -1
export {array,mapMarkers,index}
let map;

export function limpiarMapa(){
    for(var i = 0; i < mapMarkers.length; i++){
        map.removeLayer(mapMarkers[i]);
        array= []
    }
}

export function removeLastMarker(){
    if (mapMarkers.length > 0){
        map.removeLayer(mapMarkers[index])
    
        index--
        mapMarkers.pop()
        array.pop()
    }
    else{
        alert('No hay puntos a borrar')
    }
}

export function Map({selector,addSearch}) {
//propiedades

    let marker;
    
    initializeMap(selector);
    if (addSearch) {
        addSearchControl();
    };

    function initializeMap(selector) {
        map = L.map(selector).setView([initialLat,initialLng],13);
        L.tileLayer(mapLayerUrl).addTo(map);
        
    }
    map.addEventListener('click', (e) => {addMarker(e.latlng) });
    //comportamiento chequea un unico marcador esto se elimina en index
    function addMarker({lat, lng}){
        marker = L.marker([lat,lng]).addTo(map);
        mapMarkers.push(marker)
        array.push("[" + lat + "," + lng + "]")
        index++
    }; 
    function addSearchControl() {
        L.control.scale().addTo(map);
        let searchControl = new L.esri.Controls.Geosearch().addTo(map);
        let results = new L.LayerGroup().addTo(map);
        searchControl.on('results',(data) => {
            results.clearLayers();
            if (data.results.length > 0) {
                addMarker(data.results[0].latlng);
            }
        });
    };
    return {
        get marker() { return marker },
        addMarker: addMarker
    };
}
    