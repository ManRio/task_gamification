<template>
  <div class="contenedor">
    <h1 class="principal_title">Recompensas</h1>

    <table v-if="recompensas.length" class="tabla">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Descripción</th>
          <th>Coste</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in recompensas" :key="r.id">
          <td>{{ r.name }}</td>
          <td>{{ r.description }}</td>
          <td>{{ r.cost }} 🪙</td>
          <td>
            <button @click="canjear(r.id)" :disabled="enviandoId === r.id">
              🎁 Canjear
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay recompensas disponibles.</p>

    <h2 class="title">Historial de canjes</h2>
    <table v-if="historial.length" class="tabla">
      <thead>
        <tr>
          <th>Recompensa</th>
          <th>Coste</th>
          <th>Fecha</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="h in historial" :key="h.id">
          <td>{{ h.reward_name }}</td>
          <td>{{ h.reward_cost }} 🪙</td>
          <td>{{ formatearFecha(h.redeemed_at) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No has canjeado recompensas.</p>
  </div>
</template>

<script>
import api from '../../api';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      recompensas: [],
      historial: [],
      enviandoId: null,
    };
  },
  mounted() {
    this.cargarTodo();
  },
  methods: {
    async cargarTodo() {
      await Promise.all([this.obtenerRecompensas(), this.obtenerHistorial()]);
    },
    async obtenerRecompensas() {
      const res = await api.get('/rewards/list');
      this.recompensas = res.data;
    },
    async obtenerHistorial() {
      const res = await api.get('/rewards/history'); // ← ruta correcta
      this.historial = res.data; // ← ya viene plano
    },
    async canjear(id) {
      if (!confirm('¿Canjear esta recompensa?')) return;
      this.enviandoId = id;
      try {
        await api.post(`/rewards/redeem/${id}`);
        useToast().success('Recompensa canjeada');
        this.cargarTodo();
      } catch (err) {
        useToast().error('No se pudo canjear');
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
