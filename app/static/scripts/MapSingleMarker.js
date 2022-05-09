const initialLat = -34.9187;
const initialLng = -57.956;
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'; //https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png

export function Map({selector,addSearch}) {
//propiedades
    var marker;
    let map;
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
        if (marker) {
            marker.remove()
        };

        marker = L.marker([lat,lng]).addTo(map);
    }; 
    function addSearchControl() {
        L.control.scale().addTo(map);
        let searchControl = new L.esri.Controls.Geosearch().addTo(map);
        let results = new L.LayerGroup().addTo(map);
        searchControl.on('results',(data) => {
            results.clearLayers();
            if (data.results.lenght > 0) {
                addMarker(data.results[0].latlng);
            }
        });
    };
    return {
        get marker() { return marker },
        addMarker: addMarker
    };
}
    