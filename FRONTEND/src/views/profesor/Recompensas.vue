<template>
  <div class="contenedor">
    <h1>Recompensas disponibles</h1>

    <div class="acciones">
      <button @click="mostrarCrearRecompensa = true">+ Crear nueva recompensa</button>
    </div>

    <table v-if="recompensas.length" class="tabla">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Descripción</th>
          <th>Coste</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="recompensa in recompensas" :key="recompensa.id">
          <td>{{ recompensa.name }}</td>
          <td>{{ recompensa.description }}</td>
          <td>{{ recompensa.cost }}</td>
          <td>
            <button class="editar" @click="abrirEditor(recompensa)">Editar</button>
            <button class="eliminar" @click="eliminarRecompensa(recompensa.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay recompensas registradas.</p>

    <!-- Modal: Crear Recompensa -->
    <div v-if="mostrarCrearRecompensa" class="modal">
      <h3>Crear nueva recompensa</h3>
      <form @submit.prevent="crearRecompensa" class="formulario">
        <div class="campo">
          <label for="nombre">Nombre</label>
          <input v-model="nuevaRecompensa.name" id="nombre" required />
        </div>

        <div class="campo">
          <label for="descripcion">Descripción</label>
          <textarea v-model="nuevaRecompensa.description" id="descripcion" required />
        </div>

        <div class="campo">
          <label for="coste">Coste en monedas</label>
          <input v-model.number="nuevaRecompensa.cost" id="coste" type="number" min="1" required />
        </div>

        <div class="acciones-form">
          <button type="submit">Crear</button>
          <button type="button" @click="mostrarCrearRecompensa = false">Cancelar</button>
        </div>
      </form>
    </div>

    <!-- Modal: Editar Recompensa -->
    <EditarRecompensa
      v-if="mostrarEditar"
      :recompensa="recompensaSeleccionada"
      @cerrar="cerrarEditor"
      @actualizada="actualizarEnLista"
    />
  </div>
</template>

<script>
import api from '../../api';
import { useToast } from 'vue-toastification';
import EditarRecompensa from '../../components/EditarRecompensa.vue';

export default {
  components: { EditarRecompensa },
  data() {
    return {
      recompensas: [],
      mostrarCrearRecompensa: false,
      mostrarEditar: false,
      recompensaSeleccionada: null,
      nuevaRecompensa: {
        name: '',
        description: '',
        cost: 1,
      },
    };
  },
  mounted() {
    this.obtenerRecompensas();
  },
  methods: {
    async obtenerRecompensas() {
      try {
        const res = await api.get('/rewards/list');
        this.recompensas = res.data;
      } catch (error) {
        console.error('Error al obtener recompensas:', error);
      }
    },
    async crearRecompensa() {
      try {
        await api.post('/rewards/create', this.nuevaRecompensa);
        this.toast.success('Recompensa creada con éxito');
        this.nuevaRecompensa = { name: '', description: '', cost: 1 };
        this.mostrarCrearRecompensa = false;
        this.obtenerRecompensas(); // recargar
      } catch (error) {
        console.error('Error al crear recompensa:', error);
        this.toast.error('No se pudo crear la recompensa');
      }
    },
    async eliminarRecompensa(id) {
      if (!confirm('¿Seguro que deseas eliminar esta recompensa?')) return;

      try {
        await api.delete(`/rewards/${id}`);
        this.toast.success('Recompensa eliminada');
        this.recompensas = this.recompensas.filter(r => r.id !== id);
      } catch (error) {
        console.error('Error al eliminar recompensa:', error);
        this.toast.error('No se pudo eliminar');
      }
    },
    abrirEditor(recompensa) {
      this.recompensaSeleccionada = recompensa;
      this.mostrarEditar = true;
    },
    cerrarEditor() {
      this.recompensaSeleccionada = null;
      this.mostrarEditar = false;
    },
    actualizarEnLista(recompensaEditada) {
      const index = this.recompensas.findIndex(r => r.id === recompensaEditada.id);
      if (index !== -1) this.recompensas.splice(index, 1, recompensaEditada);
    },
  },
  setup() {
    const toast = useToast();
    return { toast };
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
}

.tabla th {
  background-color: #f5f5f5;
}

.acciones,
.acciones-form {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
}

.editar {
  background: #3498db;
  color: white;
  padding: 0.3rem 0.7rem;
  border: none;
  border-radius: 4px;
}

.eliminar {
  background: #e74c3c;
  color: white;
  padding: 0.3rem 0.7rem;
  border: none;
  border-radius: 4px;
}

.modal {
  position: fixed;
  top: 15%;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  width: 400px;
  z-index: 1000;
}

.formulario {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.campo label {
  font-weight: bold;
}
</style>
