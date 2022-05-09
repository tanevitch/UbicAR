const initialLat = -34.9187;
const initialLng = -57.956;
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'; //https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png

export function Map({selector,coords}) {
//propiedades
    var marker;
    let map;
    initializeMap(selector);
    
    function initializeMap(selector) {
        map = L.map(selector).setView([initialLat,initialLng],13);
        L.tileLayer(mapLayerUrl).addTo(map);
    }
    marker = L.marker(JSON.parse(coords)).addTo(map);
    map.addEventListener('click', (e) => {addMarker(e.latlng) });
    //comportamiento chequea un unico marcador esto se elimina en index
    function addMarker({lat, lng}){
        if (marker) {
            marker.remove()
        };

        marker = L.marker([lat,lng]).addTo(map);
    };  
    return {
        get marker() { return marker },
        addMarker: addMarker
    };
}
    