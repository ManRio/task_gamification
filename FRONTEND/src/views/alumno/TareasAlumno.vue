<template>
  <div class="contenedor">
    <h1 class="principal_title">Mis Tareas</h1>

    <!-- Tareas disponibles -->
    <section>
      <h2 class="title">Tareas disponibles</h2>
      <table v-if="tareasDisponibles.length" class="tabla">
        <thead>
          <tr>
            <th>Título</th>
            <th>Descripción</th>
            <th>Monedas</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tareasDisponibles" :key="t.id">
            <td>{{ t.title }}</td>
            <td>{{ t.description }}</td>
            <td>{{ t.reward }}</td>
            <td>
              <button
                @click="marcarCompletada(t.id)"
                :disabled="enviandoId === t.id"
              >
                ✅ Entregar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay tareas disponibles.</p>
    </section>

    <!-- Historial -->
    <!-- Historial -->
    <section style="margin-top: 2rem">
      <h2 class="title">Historial de Tareas Completadas</h2>
      <table v-if="tareasCompletadas.length" class="tabla">
        <thead>
          <tr>
            <th>Título</th>
            <th>Monedas</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tareasCompletadas" :key="t.completion_id">
            <td>{{ t.title }}</td>
            <td>{{ t.reward }}</td>
            <td>{{ formatearFecha(t.completed_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No has completado tareas aún.</p>
    </section>
  </div>
</template>

<script>
import api from '../../api';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      tareasDisponibles: [],
      tareasCompletadas: [],
      enviandoId: null,
    };
  },
  mounted() {
    this.cargarTodo();
  },
  methods: {
    async cargarTodo() {
      await Promise.all([this.obtenerDisponibles(), this.obtenerCompletadas()]);
    },
    async obtenerDisponibles() {
      const res = await api.get('/tasks/available');
      this.tareasDisponibles = res.data;
    },
    async obtenerCompletadas() {
      const res = await api.get('/tasks/completed'); // <-- ruta correcta
      // Si quieres ver solo las aprobadas, descomenta la línea de abajo:
      this.tareasCompletadas = res.data.filter(
        (x) => x.is_validated && x.is_approved
      );
      // Si quieres ver todas las entregas (pendientes, aprobadas, rechazadas):
      // this.tareasCompletadas = res.data;
    },
    async marcarCompletada(id) {
      if (!confirm('¿Marcar esta tarea como completada?')) return;
      this.enviandoId = id;
      try {
        await api.post(`/tasks/complete/${id}`);
        useToast().success('Tarea enviada para revisión');
        this.cargarTodo();
      } catch (err) {
        useToast().error('Error al enviar tarea');
      } finally {
        this.enviandoId = null;
      }
    },
    formatearFecha(iso) {
      return new Date(iso).toLocaleString();
    },
  },
};
</script>

<style scoped>
.contenedor {
  padding: 2rem;
}
.principal_title {
  margin: 0 auto;
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1rem;
}
.title {
  margin-top: 2rem;
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 1rem;
}
.tabla {
  width: 100%;
  border-collapse: collapse;
}
.tabla th,
.tabla td {
  padding: 0.75rem;
  border: 1px solid #ccc;
}
</style>
