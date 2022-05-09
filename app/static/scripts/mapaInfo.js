var flaskData = $('#my-data').data();
var mymap = L.map('mapid').setView(JSON.parse(flaskData["name"]["coords"]), 13);
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' //https://tile.openstreetmap.org/${z}/${x}/${y}.png https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png'
L.tileLayer(mapLayerUrl, {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        maxZoom:18
}).addTo(mymap);

var marker = L.marker(JSON.parse(flaskData["name"]["coords"]))
marker.addTo(mymap)
