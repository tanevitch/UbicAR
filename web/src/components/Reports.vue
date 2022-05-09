<template>
  <l-map id="mapafixed" :zoom="zoom" :center="center" :maxZoom="maxZoom">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-marker v-for="item in denuncias" :key="item" :lat-lng="item.coordenadas" @l-add="$event.target.openPopup()">
        <l-popup class="text-center">
            <h5>{{item.titulo}}</h5>
            <p>Estado: {{item.estado}}</p>
        </l-popup>
    </l-marker>
  </l-map>
</template>

<script>
import axios from '@/axios'
import swal from 'sweetalert';

import {LMap, LTileLayer, LMarker, LPopup} from '@vue-leaflet/vue-leaflet';
import 'leaflet/dist/leaflet.css';

export default {
    components: {
        LMap,
        LTileLayer,
        LMarker,
        LPopup
    },
    data(){
        return{
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution:
                '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 15,
            center: [-34.9187, -57.956],
            maxZoom:19,
            denuncias: [],              
            
        }
    },
    async mounted(){
        
        var page=1
        var cant_cargadas = 0
        var total = 1
        while (cant_cargadas < total){
            let response = await axios.get('denuncias?page='+page)
            .catch(()=>{
                swal("Ups!", "¡No hay nada para ver aún!", "error")
                .then(function() {
                        window.location = "/";
                    });
            });
            this.denuncias.push(...response.data.denuncias) 
            cant_cargadas= this.denuncias.length
            total = response.data.total
            page++
        }

        
        swal("Mapa interactivo", "Click en los puntos para ver el detalle", "info")
        
    }
}
</script>