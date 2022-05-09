import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import NotFound from './views/NotFound.vue'
import MPandER from './components/MPandER'
import Reports from './components/Reports.vue'
import ReportForm from './components/ReportForm.vue'
import FZ from './components/FloodableZones.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/gestion_evacuacion',
    name: 'MPandER',
    component: MPandER
  },
  {
    path: '/denuncias',
    name: 'Reports',
    component: Reports
  },
  {
    path: '/realizar_denuncia',
    name: 'ReportForm',
    component: ReportForm,
  },
  {
    path: '/zonas_inundables',
    name: 'FlodableZones',
    component: FZ
  },

  {
    path: "/:catchAll(.*)",
    component: NotFound,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
