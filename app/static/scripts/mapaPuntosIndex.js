document.body.onload = function () { 
    var flaskData = $('#my-data').data();
    var mymap = L.map('mapid').setView([-34.9187, -57.956], 13);
    const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' //https://tile.openstreetmap.org/${z}/${x}/${y}.png https://{s}.title.openstreetmap.org/{z}/{x}/{y}.png'
    L.tileLayer(mapLayerUrl, {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            maxZoom:18
    }).addTo(mymap);


    var a=0
    while(flaskData["name"][a+"coords"]!=undefined) {
        L.marker(JSON.parse(flaskData["name"][a+"coords"])).addTo(mymap)
        .bindPopup("<b>"+flaskData["name"][a+"n"]+"</b>")
        .addTo(mymap)
        a= a + 1
    }
}
