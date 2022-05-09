<template>
        <div id="mapa" >    
            <div  v-if="zona" class="container py-5">
                <h1 ><strong>{{zona.nombre}}</strong></h1>
                <h5 >Código de zona: {{zona.codigo_area}}</h5>
    
                <l-map class="mapa" :zoom="zoom" :center="center" :maxZoom="maxZoom">
                    <l-tile-layer :url="url2" :attribution="attribution"></l-tile-layer>
                    <l-polygon  :lat-lngs="getCoordenadasZona"  :fill="true" :fillColor="zona.color" :fillOpacity="1">
                        
                    </l-polygon>
                </l-map>
            </div>
        </div>
</template>

<script>
import {LMap, LTileLayer, LPolygon} from '@vue-leaflet/vue-leaflet';

export default {
    props: ['zona'],
    components:{
        LMap,
        LTileLayer,
        LPolygon
    },
    data(){
        return{
            url2: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution:
                '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 13,
            maxZoom:19,
            center: [-34.921185, -57.954554],
        }
    },

    computed:{

        getCoordenadasZona: function(){
            
            let myTarget = JSON.parse(JSON.stringify(this.zona))
            let array = []
            let auxArray = []
            if (myTarget != null){
                for (let index = 0; index < myTarget.coordenadas.length; index++) {
                    auxArray[0] = myTarget.coordenadas[index].lat
                    auxArray[1] = myTarget.coordenadas[index].long
                    array.push(auxArray)
                    auxArray = []
                }   
            }
            
            return array;
        },
    },
    watch:{
        zona: function(){
            this.center = this.getCoordenadasZona[0]
        }
    }
}
</script>

