<template>
  <div class="contenedor">
    <h1>Ranking de Alumnos</h1>

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
  </div>
</template>

<script>
import api from '../../api';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      ranking: [],
    };
  },
  mounted() {
    this.obtenerRanking();
  },
  methods: {
    async obtenerRanking() {
      try {
        const res = await api.get('/students/ranking/all');
        this.ranking = res.data;
      } catch (error) {
        console.error('Error al obtener el ranking:', error);
        useToast().error('No se pudo obtener el ranking');
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
</style>
