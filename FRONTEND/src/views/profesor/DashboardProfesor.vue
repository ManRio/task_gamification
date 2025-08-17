<template>
  <div class="dashboard">
    <h1 class="principal_title">Resumen General</h1>

    <!-- Tarjetas estadísticas -->
    <div class="tarjetas">
      <div class="tarjeta" v-for="(valor, clave) in estadisticas" :key="clave">
        <h3>{{ clave.replaceAll('_', ' ').toUpperCase() }}</h3>
        <p>{{ valor }}</p>
      </div>
    </div>

    <!-- Podio de alumnos -->
    <div class="podio">
      <h2 class="title">Top 3 alumnos</h2>
      <ol>
        <li v-for="(alumno, i) in topAlumnos" :key="alumno.username">
          <span>{{ ['🥇', '🥈', '🥉'][i] }}</span>
          {{ alumno.username }} - {{ alumno.coins }} monedas
        </li>
      </ol>
    </div>

    <!-- Distribución de monedas en tabla -->
    <div class="grafico">
      <h2 class="title">Distribución de monedas</h2>
      <table class="tabla-monedas">
        <thead>
          <tr>
            <th>#</th>
            <th>Alumno</th>
            <th>Monedas</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(alumno, i) in rankingData"
            :key="alumno.username"
            :class="{ top1: i === 0 }"
          >
            <td>{{ i + 1 }}</td>
            <td>{{ alumno.username }}</td>
            <td>{{ alumno.coins }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Historial de canjes -->
    <div class="historial">
      <h2 class="title">Historial de Canjes</h2>
      <table>
        <thead>
          <tr>
            <th>Alumno</th>
            <th>Recompensa</th>
            <th>Coste</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="canje in canjes" :key="canje.id">
            <td>{{ canje.student_name }}</td>
            <td>{{ canje.reward_name }}</td>
            <td>{{ canje.reward_cost }} monedas</td>
            <td>{{ new Date(canje.redeemed_at).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../../api';

export default {
  data() {
    return {
      estadisticas: {},
      topAlumnos: [],
      rankingData: [],
      canjes: [],
      chartData: null,
    };
  },
  async mounted() {
    try {
      await this.obtenerEstadisticas();
      await this.obtenerRanking();
      await this.obtenerCanjes();
    } catch (err) {
      console.error('Error al montar dashboard:', err);
    }
  },
  methods: {
    async obtenerEstadisticas() {
      const res = await api.get('/students/stats/global');
      this.estadisticas = res.data;
    },
    async obtenerRanking() {
      const res = await api.get('/students/ranking/all');
      const alumnos = res.data;
      this.topAlumnos = alumnos.slice(0, 3);
      this.rankingData = alumnos.slice(0, 10);
    },
    async obtenerCanjes() {
      const res = await api.get('/rewards/history/all');
      this.canjes = res.data;
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
  grid-template-rows: auto auto;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
.tarjeta {
  background: #d4edda;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  transition: ease 0.3s;
}
.tarjeta:hover {
  background: #c3e6cb;
  transform: scale(1.02);
}
.podio ol {
  list-style: none;
  padding: 0;
}
.podio li {
  background: #ecf0f1;
  padding: 0.5rem 1rem;
  margin: 0.3rem 0;
  border-radius: 6px;
}
.historial table {
  width: 100%;
  border-collapse: collapse;
}
.historial th,
.historial td {
  border: 1px solid #ccc;
  padding: 0.5rem;
}
.tabla-monedas {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.tabla-monedas th,
.tabla-monedas td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: center;
}
.tabla-monedas tr.top1 {
  background-color: #d4edda;
  font-weight: bold;
}
</style>
