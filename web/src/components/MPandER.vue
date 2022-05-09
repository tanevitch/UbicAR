<template>
    <div>
        <div v-if="cargando">
            <Cargando/>
        </div>

        <div v-else  class="d-flex py-2 row">
            <div class="col-lg-6 mapaalcostado">
            <l-map  :zoom="zoom" :center="center" :maxZoom="maxZoom">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-polyline v-for="item in ERoutes" :key="item" :lat-lngs="getCoordsER(item.coordenadas)" :color="item.color" @l-add="$event.target.openPopup()">
                    <l-popup class="text-center">
                        <p class="fs-5 bold">{{item.nombre}}</p>
                        <p >{{item.descripcion}}</p>
                    </l-popup>
                </l-polyline>

                <l-marker v-for="item in MPoints" :key="item" :lat-lng="getCoordsMP(item)">
                    <l-popup class="text-center">
                        <p class="fs-5 bold">{{item.nombre}}</p>
                        <p class="fs-6">Dirección: {{item.direccion}}</p>
                        <p>Teléfono: {{item.telefono}} <br> Email: {{item.email}}</p>
                    </l-popup>
                </l-marker>
                
                
                <l-circle :lat-lng="posicionInicial" :radius="circle.radius" :color='circle.color' :fill="true" :visible='this.changedPos'>
                    <l-popup class="text-center">
                        <p class="fs-5 bold">Ubicación actual</p>
                    </l-popup>
                </l-circle>

                </l-map>
            </div>
            <div class="col-lg-6 text-center container ">
                <div v-if="MPoints.length>0" class="shadow p-3 mb-3">
                    <div class="d-flex align-items-center">
                    <hr class="w-25 m-auto my-3">
                    <h3 class="fw-bold">PUNTOS DE ENCUENTRO</h3>
                    <hr class="w-25 m-auto my-3">
                    </div>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th scope="col">Nombre</th>
                                <th scope="col">Información</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="punto in MPoints" v-bind:key="punto">
                                <td>
                                    <span class="spanConHover" @click="center=getCoordsMP(punto)">{{punto.nombre}}</span>
                                </td>
                                <td >
                                    Dirección: {{punto.direccion}}
                                    <br>
                                    Email: {{punto.email}}
                                    <br>
                                    Teléfono: {{punto.telefono}}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <Paginador :page="pageMP" @actualizarPag="pageMP= $event; cargando=true" :tope="topeMP"></Paginador>          
                </div>
                <div v-if="ERoutes.length>0" class="shadow p-3 mb-5">
                    <div class="d-flex align-items-center">
                    <hr class="w-25 m-auto my-3">
                    <h3 class="fw-bold">RUTAS DE EVACUACION</h3>
                    <hr class="w-25 m-auto my-3">

                    </div>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th scope="col">Nombre</th>
                                <th scope="col">Descripción</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="ruta in ERoutes" v-bind:key="ruta">
                                <td>
                                    <span class="spanConHover" @click="center=getCoordsER(ruta.coordenadas)[0]">{{ruta.nombre}}</span>
                                </td>
                                <td >
                                    {{ruta.descripcion}}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <Paginador :page="pageER" @actualizarPag="pageER= $event; cargando=true" :tope="topeER"></Paginador>    
                </div>          
            </div>

            
        </div>
    </div>
</template>
<script>
import axios from "@/axios";
import {LMap, LTileLayer, LPolyline,LMarker, LPopup,LCircle} from '@vue-leaflet/vue-leaflet';
import Cargando from '../views/Cargando.vue'
import Paginador from './Paginador.vue'
import swal from 'sweetalert';

export default {
    components: {
        LCircle,
        LPopup,
        Paginador,
        Cargando,
        LMap,
        LTileLayer,
        LPolyline,
        LMarker
    },
    data(){
        return {
            posicionInicial: null,
            cargando: true,
            topeMP: 0,
            topeER: 0,
            pageMP: 1,
            pageER: 1,
            queries: 0,
            MPoints: [],
            ERoutes: [],
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution:
                '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 15,
            maxZoom:19,
            changedPos: false,
            circle: {
                radius: 100,
                color: 'red'
            },
            center: [-34.921185, -57.954554],
        }
    },

    mounted(){
        this.getMPs()
        this.getER()
        
        var options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        };

        navigator.geolocation.getCurrentPosition(this.success, this.error, options);
        swal("Mapa interactivo", "Click el nombre de los puntos y recorridos para verlos en el mapa. \n Click en los marcadores para ver el detalle", "info")
    },
    methods: {
        success(pos) {
        var crd = pos.coords;

        this.posicionInicial = [crd.latitude,crd.longitude]
        this.center = [crd.latitude,crd.longitude]
        this.changedPos = true
        },

        error() {
        swal("Geolocalización no permitida","Se mostrará el centro de La Plata", "warning")
        },

        getMPs(){
            axios.get('puntos_encuentro?page='+this.pageMP)
            .then(response => {
                this.MPoints = response.data.puntos_encuentro;
                this.cargando = false
                this.topeMP = response.data.total / response.data.por_pagina
            })
            .catch( () => this.queries++ )
        },
        getER(){
            axios.get('recorridos_evacuacion?page='+this.pageER)
            .then( response => {
                this.ERoutes = response.data.recorridos
                this.cargando = false
                this.topeER = response.data.total / response.data.por_pagina
            })
            .catch( () => {
                if (this.queries == 1){
                    swal("Ups!", "¡No hay nada para ver aún!", "error")
                    .then(function() {
                            window.location = "/";
                        });
                    
                }
            })
        },
        getCoordsER(coords){
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

        getCoordsMP(coords){
            let array = []
            array.push(coords.coordenadas[0].lat)
            array.push(coords.coordenadas[0].long)
            return array
        }
    },
    computed: {
         contenidoTablaMP(){
            let array = []
            let aux =[]
            for (let index = 0; index < this.MPoints.length; index++) {
                aux.push(this.MPoints[index].nombre)
                aux.push("Direccion: "+this.MPoints[index].direccion+ " \nTelefono: " + this.MPoints[index].telefono + " \nEmail: " + this.MPoints[index].email)
                array.push(aux)
                aux=[]
            }

            return array
        },
        contenidoTablaER(){
            let array = []
            let aux =[]
            for (let index = 0; index < this.ERoutes.length; index++) {
                aux.push(this.ERoutes[index].nombre)
                aux.push(this.ERoutes[index].descripcion)
                array.push(aux)
                aux=[]
            }

            return array
        }
    },
    watch:{
        pageER: function(){
            this.getER()
        },
        pageMP: function(){
            this.getMPs()
        },
        center: function(){
            window.scrollTo(0, 0);
        }
    }
    
}
</script>