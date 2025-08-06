import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import { useUserStore } from './stores/userStore';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import './style.css';

const app = createApp(App);
const pinia = createPinia();
app.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
});
app.use(pinia);
app.use(router);

const userStore = useUserStore();
userStore.loadUserFromStorage(); // ✅ importante para cargar el usuario al iniciar

app.mount('#app');
