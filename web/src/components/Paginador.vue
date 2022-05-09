<template>
    <nav class="d-flex justify-content-center" aria-label="Page navigation example">
        <ul class="pagination">
            <li class="page-item" v-if="page>1" ><a class="page-link" @click="actualizarPagina(page-1)">Anterior</a></li>
            <li class="page-item" v-if="page<tope"><a class="page-link" @click="actualizarPagina(page+1)">Siguiente</a></li>
        </ul>
    </nav>
</template>
<script>
export default {
    props:[
        "page",
        "tope"
    ],

    methods: {
        actualizarPagina(pagina){
            this.$emit("actualizarPag", pagina)
        }
    },
}
</script>