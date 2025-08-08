<template>
  <div class="contenedor">
    <h1>Recompensas disponibles</h1>

    <div class="acciones">
      <button class="neutral" @click="mostrarCrearRecompensa = true">
        + Crear nueva recompensa
      </button>
      <button class="neutral" @click="abrirAsignacion">
        💰 Asignar monedas
      </button>
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
            <button class="editar" @click="abrirEditor(recompensa)">
              Editar
            </button>
            <button class="eliminar" @click="eliminarRecompensa(recompensa.id)">
              Eliminar
            </button>
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
          <textarea
            v-model="nuevaRecompensa.description"
            id="descripcion"
            required
          />
        </div>

        <div class="campo">
          <label for="coste">Coste en monedas</label>
          <input
            v-model.number="nuevaRecompensa.cost"
            id="coste"
            type="number"
            min="1"
            required
          />
        </div>

        <div class="acciones-form">
          <button type="submit">Crear</button>
          <button type="button" @click="mostrarCrearRecompensa = false">
            Cancelar
          </button>
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

    <!-- Modal: Asignar Monedas -->
    <div v-if="mostrarAsignar" class="modal">
      <h3>Asignar monedas a un alumno</h3>

      <div v-if="cargandoAlumnos">Cargando alumnos…</div>
      <form v-else @submit.prevent="asignarMonedas" class="formulario">
        <div class="campo">
          <label for="alumno">Alumno</label>
          <select id="alumno" v-model.number="asignacion.student_id" required>
            <option disabled value="">Selecciona un alumno</option>
            <option v-for="a in alumnos" :key="a.id" :value="a.id">
              {{ a.first_name }} {{ a.last_name }} — {{ a.username }} ({{
                a.coins
              }}
              monedas)
            </option>
          </select>
        </div>

        <div class="campo">
          <label for="coins">Monedas</label>
          <input
            id="coins"
            type="number"
            min="1"
            v-model.number="asignacion.coins"
            required
          />
        </div>

        <div class="campo">
          <label for="reason">Motivo (opcional)</label>
          <textarea
            id="reason"
            v-model="asignacion.reason"
            placeholder="Ej.: comportamiento ejemplar, ayuda en clase…"
          />
        </div>

        <div class="acciones-form">
          <button type="submit" :disabled="asignando">
            {{ asignando ? 'Asignando…' : 'Asignar' }}
          </button>
          <button type="button" @click="cerrarAsignacion" :disabled="asignando">
            Cancelar
          </button>
        </div>
      </form>
    </div>
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
      nuevaRecompensa: { name: '', description: '', cost: 1 },

      // Asignación manual
      mostrarAsignar: false,
      alumnos: [],
      cargandoAlumnos: false,
      asignando: false,
      asignacion: { student_id: '', coins: 1, reason: '' },
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
        this.toast?.error?.('No se pudieron cargar las recompensas');
      }
    },
    async crearRecompensa() {
      try {
        await api.post('/rewards/create', this.nuevaRecompensa);
        this.toast.success('Recompensa creada con éxito');
        this.nuevaRecompensa = { name: '', description: '', cost: 1 };
        this.mostrarCrearRecompensa = false;
        this.obtenerRecompensas();
      } catch (error) {
        console.error('Error al crear recompensa:', error);
        this.toast.error(
          error?.response?.data?.msg || 'No se pudo crear la recompensa'
        );
      }
    },
    async eliminarRecompensa(id) {
      if (!confirm('¿Seguro que deseas eliminar esta recompensa?')) return;
      try {
        await api.delete(`/rewards/${id}`);
        this.toast.success('Recompensa eliminada');
        this.recompensas = this.recompensas.filter((r) => r.id !== id);
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
      const index = this.recompensas.findIndex(
        (r) => r.id === recompensaEditada.id
      );
      if (index !== -1) this.recompensas.splice(index, 1, recompensaEditada);
    },

    // ---- Asignación manual ----
    async abrirAsignacion() {
      this.mostrarAsignar = true;
      // carga perezosa
      if (!this.alumnos.length) {
        this.cargandoAlumnos = true;
        try {
          const res = await api.get('/students/all');
          this.alumnos = res.data;
        } catch (e) {
          console.error('Error al cargar alumnos:', e);
          this.toast.error('No se pudieron cargar los alumnos');
          this.mostrarAsignar = false;
        } finally {
          this.cargandoAlumnos = false;
        }
      }
    },
    cerrarAsignacion() {
      this.mostrarAsignar = false;
      this.asignacion = { student_id: '', coins: 1, reason: '' };
    },
    async asignarMonedas() {
      if (
        !this.asignacion.student_id ||
        !this.asignacion.coins ||
        this.asignacion.coins <= 0
      ) {
        this.toast.error('Selecciona un alumno y una cantidad válida');
        return;
      }
      this.asignando = true;
      try {
        const payload = {
          student_id: this.asignacion.student_id,
          coins: this.asignacion.coins,
          reason: (this.asignacion.reason || '').trim(),
        };
        const res = await api.post('/students/add-coins', payload);
        this.toast.success(`Asignadas ${payload.coins} monedas`);
        // actualizar saldo en el listado local de alumnos (si se está mostrando)
        const i = this.alumnos.findIndex((a) => a.id === payload.student_id);
        if (i !== -1 && res?.data?.new_balance != null) {
          this.alumnos[i] = { ...this.alumnos[i], coins: res.data.new_balance };
        }
        this.cerrarAsignacion();
      } catch (e) {
        console.error('Error al asignar monedas:', e);
        this.toast.error(e?.response?.data?.msg || 'No se pudo asignar');
      } finally {
        this.asignando = false;
      }
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
  align-items: center;
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
.neutral:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  top: 12%;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 420px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}
.formulario {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.campo label {
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.campo input,
.campo textarea,
.campo select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
</style>
