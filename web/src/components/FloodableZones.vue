<template>
    <div>
        <div v-if="cargando">
        <Cargando/>
        </div>
        <div v-else  class="d-flex row py-2">
            <div class="col-lg-6 mapaalcostado">
            <l-map :zoom="zoom" :center="center" :maxZoom="maxZoom">
            <l-tile-layer :url="url"></l-tile-layer>
            
            <l-polygon v-for="item in zonas" :key="item" :lat-lngs="getCoords(item.coordenadas)"  :fill="true" :fillColor="item.color" :fillOpacity="1">
                <l-popup >{{item.nombre}}</l-popup>
            </l-polygon>
            
            </l-map>
            </div>
            <div class="col-lg-6 text-center">
                <div class="container shadow p-3 mb-5">
                    <div class="d-flex align-items-center">
                        <hr class="w-25 m-auto my-3">
                        <h3 class="fw-bold mx-1">ZONAS INUNDABLES</h3>
                        <hr class="w-25 m-auto my-3">
                    </div>
                
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th scope="col">Nombre</th>
                            <th scope="col">Detalle</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="zona in zonas" v-bind:key="zona">
                            <td>
                                <span class="spanConHover" @click="center=getCoords(zona.coordenadas)[0]">{{zona.nombre}}</span>
                            </td>
                            <td >
                                <button type="button" @click="cargar(zona)" class="btn btn-primary" >
                                    Ver detalle
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                
                <Paginador :page="page" @actualizarPag="page= $event; cargando=true" :tope="tope"></Paginador>    
                </div>      
            </div>
        </div>
        <Modal :zona="zona"></Modal>
  
    </div>
</template>
<script>
import {LMap, LTileLayer, LPolygon,LPopup} from '@vue-leaflet/vue-leaflet';
import axios from "@/axios";
import Cargando from '../views/Cargando.vue'
import Paginador from './Paginador.vue'
import Modal from './Modal.vue'
import swal from 'sweetalert';

export default {
    components: {
        Paginador,
        Cargando,
        LMap,
        LTileLayer,
        LPolygon,
        LPopup,
        Modal

    },
    data(){
        return {
            
            cargando: true,
            page: 1,
            zona: null,
            zonas: null,
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution:
                '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 13,
            maxZoom:19,
            center: [-34.921185, -57.954554],
        }
    },

    mounted(){
        swal("Mapa interactivo", "Click el nombre de las zonas para verlas en el mapa", "info")
        this.getZonasInundables();
    },
    methods: {

        cargar(zona){
            this.zona = zona
            swal({
                button: 'Cerrar',
                content: 
                    document.getElementById("mapa"),
                className: 'swal-wide',
            })
            
        },
        getZonasInundables(){
            axios.get('zonas_inundables?page='+this.page)
            .then(response => {
                this.zonas = response.data.zonas;
                this.cargando = false
                this.tope = response.data.total / response.data.por_pagina
            })
            .catch( (error) => {
                this.cargando = false
                if (error.response.data.error){
                    swal("Ups!", "¡No hay nada para ver aún!", "error")
                    .then(function() {
                        window.location = "/";
                    });
                }
                else{
                    swal("Ups!", "Ha ocurrido un error. Inténtelo nuevamente más tarde.", "error")
                    .then(function() {
                        window.location = "/";
                    });
                }
            })
        },

        getCoords(coords){
        let array = []
        let auxArray = []
        for (let index = 0; index < coords.length; index++) {
            auxArray[0] = coords[index].lat
            auxArray[1] = coords[index].long
            array.push(auxArray)
            auxArray = []
        }
        return array;
        },

    },
    watch:{
        page: function(){
            this.getZonasInundables()
        }
    },

    
}

</script>
