//import { Map } from 'MapSingleMarker.js'
var flaskData = $('#my-data').data();
var inicio = $('#my-data2').data();
var mymap = L.map('mapid').setView(inicio["name"], 13);
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' //https://tile.openstreetmap.org/${z}/${x}/${y}.png https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png'
L.tileLayer(mapLayerUrl, {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        maxZoom:18
}).addTo(mymap);



    var poly = L.polygon(JSON.parse(flaskData["name"]["0coords"]))
    poly.bindPopup("<b>"+flaskData["name"]["0name"]+"</b>")
    poly.setStyle({fillColor: flaskData["name"]["0color"],
    fillOpacity:1});
    poly.addTo(mymap)
