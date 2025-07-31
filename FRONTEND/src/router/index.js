import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/userStore';

import LandingLogin from '../views/LandingLogin.vue';
import DashboardProfesor from '../views/profesor/DashboardProfesor.vue';
import DashboardAlumno from '../views/alumno/DashboardAlumno.vue';

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingLogin,
  },
  {
    path: '/profesor',
    name: 'DashboardProfesor',
    component: DashboardProfesor,
    meta: { requiresAuth: true, role: 'profesor' },
  },
  {
    path: '/alumno',
    name: 'DashboardAlumno',
    component: DashboardAlumno,
    meta: { requiresAuth: true, role: 'alumno' },
  },
  // Redirección por defecto
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const store = useUserStore();

  // Si la ruta no requiere autenticación, pasa directamente
  if (!to.meta.requiresAuth) return next();

  // Si no está autenticado, redirige a /
  if (!store.token) return next({ name: 'Landing' });

  // Si tiene un rol específico requerido
  if (to.meta.role && store.user?.role !== to.meta.role) {
    return next({ name: 'Landing' }); // O una página de error si quieres
  }

  // Si todo está bien, continúa
  next();
});

export default router;
