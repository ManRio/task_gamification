<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();

const items = [
  { to: '/profesor', label: 'Panel Principal' },
  { to: '/profesor/tareas', label: 'Tareas' },
  { to: '/profesor/alumnos', label: 'Alumnos' },
  { to: '/profesor/ranking', label: 'Ranking' },
  { to: '/profesor/canjes', label: 'Histórico de canjes' },
  { to: '/profesor/recompensas', label: 'Recompensas' },
];

const isActive = (path) => {
  // Si estamos en /profesor, activa "Tareas" solamente si es exactamente eso
  return route.path === path;
};
</script>

<template>
  <nav class="sidebar">
    <ul>
      <li
        v-for="item in items"
        :key="item.to"
        :class="{ activo: isActive(item.to) }"
      >
        <router-link :to="item.to">{{ item.label }}</router-link>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
.sidebar {
  width: 220px;
  height: calc(100vh - 60px);
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 6px;
}

.sidebar li.activo {
  background-color: #1abc9c;
  font-weight: bold;
}

.sidebar a {
  color: white;
  text-decoration: none;
  display: block;
}
</style>
