<template>
  <div class="contenedor">
    <h1>Ranking de Alumnos</h1>

    <div style="margin-bottom: 0.75rem">
      <button class="neutral" @click="refrescar">🔄 Refrescar</button>
    </div>

    <!-- Tabla Ranking -->
    <table class="tabla" v-if="ranking.length">
      <thead>
        <tr>
          <th>#</th>
          <th>Usuario</th>
          <th>Monedas</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="alumno in ranking" :key="alumno.username">
          <td>{{ alumno.position }}</td>
          <td>{{ alumno.username }}</td>
          <td>{{ alumno.coins }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay datos de ranking disponibles.</p>

    <!-- Últimas concesiones -->
    <h2 style="margin-top: 2rem">Últimas concesiones de monedas</h2>
    <table class="tabla" v-if="movimientos.length">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Usuario</th>
          <th>Monedas</th>
          <th>Origen</th>
          <th>Detalle</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(m, idx) in movimientos" :key="m.ref || idx">
          <td>{{ formatearFecha(m.timestamp) }}</td>
          <td>{{ m.username }}</td>
          <td>+{{ m.coins }}</td>
          <td>
            <span v-if="m.type === 'task'">Tarea aprobada</span>
            <span v-else>Asignación manual</span>
          </td>
          <td>{{ m.detail }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay movimientos recientes.</p>
  </div>
</template>

<script>
import api from '../../api';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      ranking: [],
      movimientos: [],
    };
  },
  mounted() {
    this.refrescar();
  },
  methods: {
    async refrescar() {
      await Promise.all([this.obtenerRanking(), this.obtenerMovimientos()]);
    },
    async obtenerRanking() {
      try {
        const res = await api.get('/students/ranking/all');
        this.ranking = res.data;
      } catch (error) {
        console.error('Error al obtener el ranking:', error);
        useToast().error('No se pudo obtener el ranking');
      }
    },
    async obtenerMovimientos() {
      try {
        const res = await api.get('/students/coin-events', {
          params: { limit: 10 },
        });
        this.movimientos = res.data;
      } catch (error) {
        console.error('Error al obtener movimientos:', error);
        useToast().error('No se pudieron cargar los últimos movimientos');
      }
    },
    formatearFecha(iso) {
      try {
        return new Date(iso).toLocaleString();
      } catch {
        return iso || '—';
      }
    },
  },
};
</script>

<style scoped>
.contenedor {
  padding: 2rem;
}
.tabla {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
}
.tabla th,
.tabla td {
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  text-align: left;
}
.tabla th {
  background-color: #f5f5f5;
}
.neutral {
  background: #f0f0f0;
  border: 1px solid #ddd;
  padding: 0.4rem 0.7rem;
  border-radius: 4px;
  cursor: pointer;
}
.neutral:hover {
  background: #e9e9e9;
}
</style>
