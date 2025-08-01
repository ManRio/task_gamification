<template>
  <div class="dashboard">
    <h1>¡Hola, {{ user.username }}!</h1>
    <p>Bienvenido a tu panel de control.</p>

    <section class="actions">
      <button @click="mostrarCrearTarea = true">+ Añadir nueva tarea</button>
    </section>

    <section class="tareas">
      <h2>Tareas asignadas</h2>
      <p v-if="!tareas.length">No hay tareas aún.</p>
      <ul>
        <li v-for="tarea in tareas" :key="tarea.id">
          {{ tarea.titulo }} - {{ tarea.descripcion }}
        </li>
      </ul>
    </section>

    <section class="ranking">
      <h2>Ranking de alumnos</h2>
      <p>Próximamente...</p>
    </section>

    <!-- Modal simulado -->
    <div v-if="mostrarCrearTarea" class="modal">
      <h3>Crear nueva tarea</h3>
      <form @submit.prevent="crearTarea">
        <input v-model="nuevaTarea.titulo" placeholder="Título" required />
        <textarea v-model="nuevaTarea.descripcion" placeholder="Descripción" required></textarea>
        <button type="submit">Crear</button>
        <button type="button" @click="mostrarCrearTarea = false">Cancelar</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../../api';
import { useUserStore } from '../../stores/userStore';

export default {
  data() {
    return {
      tareas: [],
      mostrarCrearTarea: false,
      nuevaTarea: {
        titulo: '',
        descripcion: '',
      },
    };
  },
  computed: {
    user() {
      const store = useUserStore();
      return store.user || {};
    },
  },
  mounted() {
    this.obtenerTareas();
  },
  methods: {
    async obtenerTareas() {
      try {
        const res = await api.get(`/tasks/profesor/${this.user.id}`);
        this.tareas = res.data;
      } catch (error) {
        console.error('Error al obtener tareas:', error);
      }
    },
    async crearTarea() {
      try {
        const res = await api.post('/tasks', {
          titulo: this.nuevaTarea.titulo,
          descripcion: this.nuevaTarea.descripcion,
          profesor_id: this.user.id,
        });
        this.tareas.push(res.data);
        this.nuevaTarea.titulo = '';
        this.nuevaTarea.descripcion = '';
        this.mostrarCrearTarea = false;
      } catch (error) {
        console.error('Error al crear tarea:', error);
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

.actions {
  margin-bottom: 2rem;
}

.tareas,
.ranking {
  margin-top: 2rem;
}

.modal {
  position: fixed;
  top: 20%;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0,0,0,0.3);
}
</style>