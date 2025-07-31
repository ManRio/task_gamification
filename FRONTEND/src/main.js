import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './style.css';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount('#app');

// Cargar usuario desde localStorage
import { useUserStore } from './stores/userStore';
const userStore = useUserStore();
userStore.loadUserFromStorage();
