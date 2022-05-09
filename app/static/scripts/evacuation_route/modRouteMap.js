var flaskData = $('#my-data').data();
var inicio = $('#my-data2').data();
var array = JSON.parse(flaskData["name"]["coords"])
var markers = []
var index= -1
const submitHandler = (e) => {
        if (array.length <= 2 ){
            e.preventDefault();
            alert('Debes seleccionar al menos tres puntos en el mapa');
        }
        else {
            document.getElementById('latAndLong').setAttribute('value',array);
        }
    }

    function removeLastMarker(){
        if (markers.length > 0){
            
            mymap.removeLayer(markers[index])
        
            index--
            markers.pop()
            array.pop()
        }
        else{
            alert('No hay puntos a borrar')
        }
        
    
    
    }

function removeMarkers(){
    index = -1
    for (let i = 0; i < markers.length; i++) {
        mymap.removeLayer(markers[i])
    }
    markers = []

}

var mymap = L.map('mapid').setView(inicio["name"], 16);
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' //https://tile.openstreetmap.org/${z}/${x}/${y}.png https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png'
L.tileLayer(mapLayerUrl, {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        maxZoom:18
}).addTo(mymap);

for (let i = 0; i < array.length; i++) {
    array[i] = "[" + array[i] + "]"
}



mymap.addEventListener('click', (e) => {addMarker(e.latlng) });
    function addMarker({lat, lng}){
        markers.push(L.marker([lat,lng]).addTo(mymap)) ;
        array.push("[" + lat + "," + lng + "]")  
        index++  
    }; 




var poly = L.polyline(JSON.parse(flaskData["name"]["coords"]))
poly.setStyle({color: flaskData["name"]["color"],
fillOpacity:1});
poly.addTo(mymap)

const form = document.getElementById('form');
const button = document.getElementById('removeLast');
document.getElementById("removeLast").disabled = true;

button.addEventListener('click',(e)=> removeLastMarker(e))
form.addEventListener('reset',(e)=> {mymap.removeLayer(poly);array=[];removeMarkers()})
form.addEventListener('submit',(e)=> submitHandler(e) )
