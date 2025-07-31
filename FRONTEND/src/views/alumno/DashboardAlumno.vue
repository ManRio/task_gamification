<template>
  <div class="dashboard alumno">
    <header class="dashboard-header">
      <h1>Panel del Alumno</h1>
    </header>

    <main class="dashboard-main">
      <section class="task-list">
        <h2>Tareas Pendientes</h2>
        <ul>
          <li v-for="task in tasks" :key="task.id">
            {{ task.title }} - <strong>{{ task.estado }}</strong>
          </li>
        </ul>
      </section>

      <section class="stats">
        <p>
          Monedas acumuladas: <strong>{{ monedas }}</strong>
        </p>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AlumnoDashboard',
  data() {
    return {
      monedas: 120,
      tasks: [
        { id: 1, title: 'Resumen de biología', estado: 'Pendiente' },
        { id: 2, title: 'Ejercicio de inglés', estado: 'Completada' },
      ],
    };
  },
};
</script>

<style scoped>
.dashboard-header {
  background-color: #28a745;
  color: white;
  padding: 1rem;
  text-align: center;
}

.dashboard-main {
  padding: 2rem;
}

.task-list,
.stats {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
