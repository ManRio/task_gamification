<template>
  <div class="contenedor">
    <h1>Historial de Canjes</h1>

    <table v-if="canjes.length" class="tabla">
      <thead>
        <tr>
          <th>Alumno</th>
          <th>Recompensa</th>
          <th>Coste</th>
          <th>Fecha</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="canje in canjes" :key="canje.id">
          <td>{{ canje.student_name }}</td>
          <td>{{ canje.reward_name }}</td>
          <td>{{ canje.reward_cost }} 🪙</td>
          <td>{{ formatearFecha(canje.redeemed_at) }}</td>
          <td>
            <button class="eliminar" @click="eliminarCanje(canje.id)">
              Eliminar
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>No hay canjes registrados aún.</p>
  </div>
</template>

<script>
import api from '../../api';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      canjes: [],
    };
  },
  mounted() {
    this.obtenerCanjes();
  },
  methods: {
    async obtenerCanjes() {
      try {
        const res = await api.get('/rewards/history/all');
        this.canjes = res.data;
      } catch (error) {
        console.error('Error al obtener canjes:', error);
      }
    },
    async eliminarCanje(id) {
      if (
        !confirm('¿Eliminar este canje? Se devolverán las monedas al alumno.')
      )
        return;

      try {
        await api.delete(`/rewards/delete-redemption/${id}`);
        this.canjes = this.canjes.filter((c) => c.id !== id);
        this.$toast.success('Canje eliminado y monedas devueltas');
      } catch (error) {
        console.error('Error al eliminar canje:', error);
        this.$toast.error('No se pudo eliminar el canje');
      }
    },
    formatearFecha(fechaIso) {
      return new Date(fechaIso).toLocaleString('es-ES');
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
  margin-top: 1rem;
}

.tabla th,
.tabla td {
  padding: 0.75rem;
  border: 1px solid #ccc;
  text-align: left;
}

.tabla th {
  background-color: #f5f5f5;
}

.eliminar {
  background-color: #e74c3c;
  color: white;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
