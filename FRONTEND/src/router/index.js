import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/userStore';

import LandingLogin from '../views/LandingLogin.vue';

// Layouts
import ProfesorLayout from '../layouts/ProfesorLayout.vue';
import AlumnoLayout from '../layouts/AlumnoLayout.vue';

// Vistas Profesor
import DashboardProfesor from '../views/profesor/DashboardProfesor.vue';
import Tareas from '../views/profesor/Tareas.vue';
import Alumnos from '../views/profesor/Alumnos.vue';
import RankingProfesor from '../views/profesor/Ranking.vue';
import Canjes from '../views/profesor/Canjes.vue';
import RecompensasProfesor from '../views/profesor/Recompensas.vue';

// Vistas Alumno
import DashboardAlumno from '../views/alumno/DashboardAlumno.vue';
import TareasAlumno from '../views/alumno/TareasAlumno.vue';
import RecompensasAlumno from '../views/alumno/RecompensasAlumno.vue';
import RankingAlumno from '../views/alumno/RankingAlumno.vue';

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingLogin,
  },
  {
    path: '/profesor',
    component: ProfesorLayout,
    meta: { requiresAuth: true, role: 'profesor' },
    children: [
      { path: '', name: 'DashboardProfesor', component: DashboardProfesor },
      { path: 'tareas', name: 'Tareas', component: Tareas },
      { path: 'alumnos', name: 'Alumnos', component: Alumnos },
      { path: 'ranking', name: 'RankingProfesor', component: RankingProfesor },
      { path: 'canjes', name: 'Canjes', component: Canjes },
      {
        path: 'recompensas',
        name: 'RecompensasProfesor',
        component: RecompensasProfesor,
      },
    ],
  },
  {
    path: '/alumno',
    component: AlumnoLayout,
    meta: { requiresAuth: true, role: 'alumno' },
    children: [
      { path: '', name: 'DashboardAlumno', component: DashboardAlumno },
      { path: 'tareas', name: 'TareasAlumno', component: TareasAlumno },
      {
        path: 'recompensas',
        name: 'RecompensasAlumno',
        component: RecompensasAlumno,
      },
      { path: 'ranking', name: 'RankingAlumno', component: RankingAlumno },
    ],
  },
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

  if (!to.meta.requiresAuth) return next();

  if (!store.token) return next({ name: 'Landing' });

  if (to.meta.role && store.user?.role !== to.meta.role) {
    return next({ name: 'Landing' });
  }

  next();
});

export default router;
