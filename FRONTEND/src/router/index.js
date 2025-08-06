import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/userStore';

import LandingLogin from '../views/LandingLogin.vue';

import DashboardAlumno from '../views/alumno/DashboardAlumno.vue';
import ProfesorLayout from '../layouts/ProfesorLayout.vue';

import Alumnos from '../views/profesor/Alumnos.vue';
import Ranking from '../views/profesor/Ranking.vue';
import Canjes from '../views/profesor/Canjes.vue';
import Recompensas from '../views/profesor/Recompensas.vue';
import DashboardProfesor from '../views/profesor/DashboardProfesor.vue';
import Tareas from '../views/profesor/Tareas.vue';

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingLogin,
  },
  {
    path: '/profesor',
    component: ProfesorLayout, // 👈 Aquí usamos el layout que contiene Sidebar + Header
    children: [
      {
        path: '',
        name: 'DashboardProfesor',
        component: DashboardProfesor,
      },
      {
        path: '/profesor/tareas',
        name: 'Tareas',
        component: Tareas,
      },
      {
        path: 'alumnos',
        name: 'Alumnos',
        component: Alumnos,
      },
      {
        path: 'ranking',
        name: 'Ranking',
        component: Ranking,
      },
      {
        path: 'canjes',
        name: 'Canjes',
        component: Canjes,
      },
      {
        path: 'recompensas',
        name: 'Recompensas',
        component: Recompensas,
      },
    ],
  },
  {
    path: '/alumno',
    name: 'DashboardAlumno',
    component: DashboardAlumno,
  }, // Redirección por defecto
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
