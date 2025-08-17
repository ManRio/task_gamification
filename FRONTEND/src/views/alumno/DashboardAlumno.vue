<template>
  <div class="dashboard">
    <h1 vlass="principal_title">Mi Resumen</h1>

    <!-- Tarjetas estadísticas -->
    <div class="tarjetas">
      <div class="tarjeta">
        <h3>MONEDAS</h3>
        <p>{{ estadisticas.coins }}</p>
      </div>
      <div class="tarjeta">
        <h3>TAREAS COMPLETADAS</h3>
        <p>{{ estadisticas.tasks_completed }}</p>
      </div>
      <div class="tarjeta">
        <h3>RECOMPENSAS CANJEADAS</h3>
        <p>{{ estadisticas.rewards_redeemed }}</p>
      </div>
    </div>

    <!-- Últimas tareas -->
    <div class="bloque">
      <h2 class="title">Últimas Tareas Completadas</h2>
      <table v-if="ultimasTareas.length" class="tabla">
        <thead>
          <tr>
            <th>Título</th>
            <th>Monedas</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in ultimasTareas" :key="t.id">
            <td>{{ t.task_title }}</td>
            <td>{{ t.task_reward }}</td>
            <td>{{ formatearFecha(t.completed_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No has completado tareas aún.</p>
    </div>

    <!-- Últimos canjes -->
    <div class="bloque">
      <h2 class="title">Últimos Canjes</h2>
      <table v-if="ultimosCanjes.length" class="tabla">
        <thead>
          <tr>
            <th>Recompensa</th>
            <th>Coste</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in ultimosCanjes" :key="c.id">
            <td>{{ c.reward_name }}</td>
            <td>{{ c.reward_cost }}</td>
            <td>{{ formatearFecha(c.redeemed_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No has canjeado recompensas aún.</p>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'; // usa el mismo import que tenías para api

export default {
  data() {
    return {
      estadisticas: {},
      ultimasTareas: [],
      ultimosCanjes: [],
    };
  },
  async mounted() {
    await this.cargarResumen();
  },
  methods: {
    async cargarResumen() {
      const res = await api.get('/students/summary', { params: { limit: 5 } });
      this.estadisticas = res.data.estadisticas;
      this.ultimasTareas = res.data.ultimasTareas;
      this.ultimosCanjes = res.data.ultimosCanjes;
    },
    formatearFecha(iso) {
      return new Date(iso).toLocaleString();
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
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
.tarjetas {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}
.tarjeta {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}
.bloque {
  margin-top: 1rem;
}
.tabla {
  width: 100%;
  border-collapse: collapse;
}
.tabla th,
.tabla td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}
</style>
