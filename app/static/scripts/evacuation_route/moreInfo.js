var flaskData = $('#my-data').data();
var inicio = $('#my-data2').data();
var mymap = L.map('mapid').setView(inicio["name"], 16);
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' //https://tile.openstreetmap.org/${z}/${x}/${y}.png https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png'
L.tileLayer(mapLayerUrl, {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        maxZoom:18
}).addTo(mymap);



    var poly = L.polyline(JSON.parse(flaskData["name"]["coords"]))
    poly.bindPopup("<b>"+flaskData["name"]["name"]+"</b>")
    poly.setStyle({color: flaskData["name"]["color"],
    fillOpacity:1});
    poly.addTo(mymap)
