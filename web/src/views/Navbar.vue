<template>
    <div class="container">
        <router-link class="navbar-brand h1 logo-head" to="/"><i class="fas fa-map-marked-alt"></i> Ubicar</router-link> 
        <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
            aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavAltMarkup">
            <ul class="navbar-nav align-items-center">
                <li class="nav-item btn-nav rounded-pill nav-link">
                    <router-link to="/zonas_inundables">Zonas Inundables</router-link> 
                </li>
                <li class="nav-item btn-nav rounded-pill nav-link">
                    <router-link to="/gestion_evacuacion">Puntos de Encuentro y Rutas</router-link> 
                </li>
                <li class="nav-item btn-nav rounded-pill nav-link">
                    <router-link to="/denuncias">Estado Denuncias</router-link> 
                </li>
                 <li class="nav-item btn-nav rounded-pill nav-link">
                    <router-link to="/realizar_denuncia">Cargar Denuncias</router-link> 
                </li>
            </ul>
        </div>
    </div>
</template>