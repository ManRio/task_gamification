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
          {{ tarea.title }} - {{ tarea.description }} (🎯
          {{ tarea.reward }} monedas)
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
      <form @submit.prevent="crearTarea" class="formulario-tarea">
        <div class="campo">
          <label for="titulo">Título</label>
          <input v-model="nuevaTarea.titulo" id="titulo" required />
        </div>

        <div class="campo">
          <label for="descripcion">Descripción</label>
          <textarea
            v-model="nuevaTarea.descripcion"
            id="descripcion"
            required
          ></textarea>
        </div>

        <div class="campo">
          <label for="monedas">Monedas</label>
          <input
            v-model.number="nuevaTarea.monedas"
            id="monedas"
            type="number"
            min="1"
            required
          />
        </div>

        <div class="acciones">
          <button type="submit">Crear</button>
          <button type="button" @click="mostrarCrearTarea = false">
            Cancelar
          </button>
        </div>
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
        monedas: 1,
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
        const res = await api.get(`/tasks/mine`);
        this.tareas = res.data;
      } catch (error) {
        console.error('Error al obtener tareas:', error);
      }
    },
    async crearTarea() {
      try {
        const res = await api.post('/tasks/create', {
          title: this.nuevaTarea.titulo,
          description: this.nuevaTarea.descripcion,
          reward: this.nuevaTarea.monedas,
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
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

.formulario-tarea {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.campo {
  display: flex;
  flex-direction: column;
}

.campo label {
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.campo input,
.campo textarea {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.acciones {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
