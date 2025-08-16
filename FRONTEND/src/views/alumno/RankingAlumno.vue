<template>
  <div class="contenedor">
    <h1>Ranking</h1>

    <h2>Mi posición</h2>
    <p v-if="miPosicion">
      #{{ miPosicion.position }} — {{ miPosicion.username }} ({{
        miPosicion.coins
      }}
      🪙)
    </p>
    <p v-else>No estás en el ranking todavía.</p>

    <h2 style="margin-top: 1.5rem">Ranking general</h2>
    <table v-if="ranking.length" class="tabla">
      <thead>
        <tr>
          <th>#</th>
          <th>Usuario</th>
          <th>Monedas</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in ranking" :key="r.username">
          <td>{{ r.position }}</td>
          <td>{{ r.username }}</td>
          <td>{{ r.coins }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay datos.</p>
  </div>
</template>

<script>
import api from '../../api';

export default {
  data() {
    return {
      miPosicion: null,
      ranking: [],
    };
  },
  mounted() {
    this.cargar();
  },
  methods: {
    async cargar() {
      const [resMe, resAll] = await Promise.all([
        api.get('/students/ranking/me'),
        api.get('/students/ranking'),
      ]);
      this.miPosicion = resMe.data;
      this.ranking = resAll.data;
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
}
.tabla th,
.tabla td {
  padding: 0.75rem;
  border: 1px solid #ccc;
}
</style>
