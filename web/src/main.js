import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '../src/assets/css/style.css'
import AOS from 'aos';
import 'aos/dist/aos.css';
import './registerServiceWorker'
AOS.init();
createApp(App).use(router).mount('#app')
