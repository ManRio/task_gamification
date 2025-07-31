import { createRouter, createWebHistory } from 'vue-router';
import LandingLogin from '../views/LandingLogin.vue';

const routes = [
  { path: '/', name: 'Login', component: LandingLogin },
  // ... otras rutas como /alumno o /profesor
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
