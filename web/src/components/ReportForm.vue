<template>
<section class="container py-5">
    <form ref="formulario" >
    <div class="row align-items-center">
        <div class="col-lg-6">
            <h1>Crear una denuncia</h1>
                <div class="mb-3">
                    <label for="title" class="form-label">Titulo</label>
                    <input name="title" id="title" v-model="titulo" type="text" class="form-control" placeholder="Alcantarilla tapada" required>
                </div>
                <div class="mb-3">
                    <label for="category" class="form-label">Categoría</label>
                    <select class="form-select" name="category" id="category" v-model="categoria" required>
                        <option selected disabled value="">Seleccione una categoría...</option>
                        <option v-for="(item, key) in categorias" :value="key" :key="key">
                            {{item}}
                        </option>
                    </select>
                </div>

                <div class="mb-3">
                    <label for="fname" class="form-label">Nombre denunciante</label>
                    <input name="fname" id="fname" v-model="nombre" type="text" class="form-control" placeholder="Juan" required>

                </div>
                <div class="mb-3">
                    <label for="lname" class="form-label">Apellido denunciante</label>
                    <input name="lname" id="lname" type="text" v-model="apellido" class="form-control" placeholder="Perez" required>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email denunciante</label>
                    <input name="email" id="email" type="email" class="form-control" v-model="email" placeholder="juanperez@gmail.com" required>
                </div>
                <div class="mb-3">
                    <label for="phone" class="form-label">Teléfono denunciante</label>
                    <input name="phone" id="phone" type="text" v-model="telefono" class="form-control" placeholder="2212222222" required>
                </div>

                <div class="mb-3">
                    <label for="description" class="form-label">Descripción</label>
                    <textarea name="description" id="description" v-model="descripcion" class="form-control" maxlength="500"
                        placeholder="Describe el problema en max. 500 caracteres.." rows="7" required></textarea>
                </div>
                <div class="mb-3" id="grupo_cordLat">
                    <input type="hidden" class="form-control" name="coords" id="coords" />
                </div>
        </div>
        <div class="col-lg-6 mb-3 mapaalcostado">
            <l-map :zoom="zoom" :maxZoom="maxZoom" :center="center" @click="marcar">
                <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>         
                <l-marker :lat-lng="markerLatLng"></l-marker>           
            </l-map>
        </div>
        <div class="col-lg-2">
            <button type="button" @click.prevent="enviar()" class="btn btn-primary">Crear</button>
        </div>
    </div>
    </form>
</section>


</template>

<script>
import axios from '@/axios';
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet';
import 'leaflet/dist/leaflet.css';
import swal from 'sweetalert';

export default {
    components: {
        LMap, LTileLayer, LMarker
    },
    data(){
        return {
            titulo: '',
            categorias: '',
            categoria: '',
            nombre: '',
            apellido: '',
            telefono: '',
            email: '',
            descripcion: '',
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution:
                '&&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 13,
            maxZoom:19,
            center: [-34.9187, -57.956],
            markerLatLng: {
                lat: null,
                lng: null
            }
        }
    },
    mounted(){
        axios.get('categorias')
        .then( res => this.categorias = res.data )
        .catch( () => {
            swal("Ups!", "Ha ocurrido un error. Inténtelo nuevamente más tarde.", "error");
        })

    },
    methods: {
        marcar(e){
            this.markerLatLng= e.latlng
        },
        reset(){
            this.titulo = '',
            this.categoria  = '',
            this.nombre  = '',
            this.apellido  = '',
            this.telefono = '',
            this.email  = '',
            this.descripcion  = '',
            this.markerLatLng  = {
                lat: null,
                lng: null
            }
        },
        enviar(){
            if (this.validar()){
                var data = JSON.stringify({
                    coordenadas: this.markerLatLng.lat + ","+this.markerLatLng.lng,
                    titulo: this.titulo,
                    categoria_id: this.categoria,
                    nombre_denunciante: this.nombre,
                    apellido_denunciante: this.apellido,
                    telcel_denunciante: this.telefono,
                    email_denunciante: this.email ,
                    descripcion: this.descripcion,
                })
    
                axios.post('denuncias/', data, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(() => {
                    swal("¡Atención!", "¡Denuncia creada exitosamente!", "success");
                    this.reset();
                })    
                .catch( () =>{
                    swal("Ups!", "Ha ocurrido un error. Inténtelo nuevamente más tarde.", "error");
                })

            }
            
        },
        validar(){
            if (!(this.categoria && this.nombre && this.apellido && this.telefono && this.email && this.descripcion && this.markerLatLng.lat && this.markerLatLng.lng && this.titulo)){
                swal("¡Atención!", "Todos los campos son requeridos", "warning");
                return false
            }

            if (isNaN(parseInt(this.categoria))){
                swal("¡Atención!", "Categoría inválida. Seleccione una del listado", "warning");
                return false
            }

            if (! /^(?:(?:00)?549?)?0?(?:11|[2368]\d)(?:(?=\d{0,2}15)\d{2})??\d{8,10}$/.test(this.telefono)){
                swal("¡Atención!", "El teléfono es inválido", "warning");
                return false
            }

            if (! /^[a-zA-ZÀ-ÿ\s]{1,100}$/.test(this.nombre) || ! /^[a-zA-ZÀ-ÿ\s]{1,100}$/.test(this.apellido)){
                swal("¡Atención!", "Nombre y apellido no pueden contener números, y deben tener como máximo 100 caracteres", "warning");
                return false
            }

            if (! /^(?=^.{1,100}$)^[\w.]+@([\w-]+\.)+[\w-]{2,4}$/.test(this.email)){
                swal("¡Atención!", "El email es inválido", "warning");
                return false
            }

            if (! /^(.{1,500})$/.test(this.descripcion)){
                swal("¡Atención!", "La descripción puede tener a lo sumo 500 caracteres", "warning");
                return false
            }

            if (! /^(.{1,100})$/.test(this.titulo)){
                swal("¡Atención!", "El título puede tener a lo sumo 100 caracteres", "warning");
                return false
            }

            return true
        }

    },
    

  
}
</script>