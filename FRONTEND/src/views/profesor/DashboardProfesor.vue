<template>
  <div class="dashboard">
    <h1>Resumen General</h1>

    <!-- Tarjetas estadísticas -->
    <div class="tarjetas">
      <div class="tarjeta" v-for="(valor, clave) in estadisticas" :key="clave">
        <h3>{{ clave.replaceAll('_', ' ').toUpperCase() }}</h3>
        <p>{{ valor }}</p>
      </div>
    </div>

    <!-- Podio de alumnos -->
    <div class="podio">
      <h2>Top 3 alumnos</h2>
      <ol>
        <li v-for="(alumno, i) in topAlumnos" :key="alumno.username">
          <span>{{ ['🥇', '🥈', '🥉'][i] }}</span>
          {{ alumno.username }} - {{ alumno.coins }} monedas
        </li>
      </ol>
    </div>

    <!-- Gráfico de monedas -->
    <div class="grafico">
      <h2>Distribución de monedas</h2>
      <BarChart :chartData="chartData" />
    </div>

    <!-- Historial de canjes -->
    <div class="historial">
      <h2>Historial de Canjes</h2>
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
import BarChart from '../../components/BarChart.vue';

export default {
  components: { BarChart },
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

      if (this.rankingData.length > 0) {
        this.chartData = {
          labels: this.rankingData.map((a) => a.username),
          datasets: [
            {
              label: 'Monedas',
              backgroundColor: '#42A5F5',
              data: this.rankingData.map((a) => a.coins),
            },
          ],
        };
      } else {
        this.chartData = null;
      }
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
</style>
