
<template>
  <div>
    <main>
      <Cargando v-if="cargando"/>
      <div v-else>
        <nav id="header-nav" class="navbar navbar-expand-lg navbar-light">
          <Navbar/>
        </nav>
        
        <router-view/>
      </div>
    </main>
    <footer class="w-100 ">
      <div class="container">
        <div class="row pt-4">
          <div class="col-lg-6 col-sm-12">
            <p class="text-lg-start text-center text-footer">
              © Copyright 2021 <b>Proyecto de Software</b>. Todos los derechos reservados.
            </p>
          </div>
          <div class="col-lg-6 col-sm-12">
            <p class="text-lg-end text-center text-footer">
              Diseñado por <a class="text-decoration-none text-black-50"
                href="https://gitlab.catedras.linti.unlp.edu.ar/proyecto2021/proyectos/grupo1" target="_blank"><strong
                  class="text-footer">Grupo 1</strong></a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import Navbar from './views/Navbar.vue';
import axios from '@/axios';
import Cargando from './views/Cargando.vue'

export default {
  components: {
    Navbar, 
    Cargando
  },
   data(){
      return {
          cargando: true,
          color: null,
      }
  },
  mounted(){
    axios.get("color")
    .then(response => {
      document.getElementById(`body`).classList.add(response.data.color);
      this.cargando= false

    })
    
  }  
}
</script>

