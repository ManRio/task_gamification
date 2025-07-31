<template>
  <div class="dashboard profesor">
    <header class="dashboard-header">
      <h1>Panel del Profesor</h1>
    </header>

    <main class="dashboard-main">
      <section class="task-summary">
        <h2>Tareas Asignadas</h2>
        <ul>
          <li v-for="task in tasks" :key="task.id">{{ task.title }}</li>
        </ul>
        <button @click="crearTarea">➕ Nueva Tarea</button>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'ProfesorDashboard',
  data() {
    return {
      tasks: [
        { id: 1, title: 'Tarea de Matemáticas' },
        { id: 2, title: 'Trabajo de Historia' },
      ],
    };
  },
  methods: {
    crearTarea() {
      alert('Aquí irá la lógica para crear una tarea');
    },
  },
};
</script>

<style scoped>
.dashboard-header {
  background-color: #1e90ff;
  color: white;
  padding: 1rem;
  text-align: center;
}

.dashboard-main {
  padding: 2rem;
}

.task-summary {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.task-summary ul {
  list-style: none;
  padding: 0;
}

.task-summary li {
  margin: 0.5rem 0;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}
</style>
