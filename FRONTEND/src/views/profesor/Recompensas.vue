<template>
  <div class="contenedor">
    <h1 class="principal_title">Recompensas disponibles</h1>

    <div class="acciones">
      <button class="boton-toggle" @click="mostrarCrearRecompensa = true">
        ➕ Crear nueva recompensa
      </button>
      <button class="boton-toggle" @click="abrirAsignacion">
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

    <!-- MODAL: Crear Recompensa -->
    <Teleport to="body">
      <div
        v-if="mostrarCrearRecompensa"
        class="overlay"
        @click.self="mostrarCrearRecompensa = false"
      >
        <div
          class="modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
        >
          <header class="modal__header">
            <h3 id="modal-title">Crear nueva recompensa</h3>
            <button
              class="modal__close"
              @click="mostrarCrearRecompensa = false"
              aria-label="Cerrar"
            >
              ✕
            </button>
          </header>

          <form
            @submit.prevent="crearRecompensa"
            class="modal__body formulario"
          >
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

            <footer class="modal__footer">
              <button type="submit" class="btn btn--primary">Crear</button>
              <button
                type="button"
                class="btn btn--ghost"
                @click="mostrarCrearRecompensa = false"
              >
                Cancelar
              </button>
            </footer>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- MODAL: Editar Recompensa (componente propio) -->
    <EditarRecompensa
      v-if="mostrarEditar"
      :recompensa="recompensaSeleccionada"
      @cerrar="cerrarEditor"
      @actualizada="actualizarEnLista"
    />

    <!-- MODAL: Asignar Monedas -->
    <Teleport to="body">
      <div v-if="mostrarAsignar" class="overlay" @click.self="cerrarAsignacion">
        <div
          class="modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="asignar-title"
        >
          <header class="modal__header">
            <h3 id="asignar-title">Asignar monedas a un alumno</h3>
            <button
              class="modal__close"
              aria-label="Cerrar"
              @click="cerrarAsignacion"
            >
              ✕
            </button>
          </header>

          <form
            v-if="!cargandoAlumnos"
            @submit.prevent="asignarMonedas"
            class="modal__body formulario"
          >
            <div class="campo">
              <label for="alumno">Alumno</label>
              <select
                id="alumno"
                v-model.number="asignacion.student_id"
                required
              >
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

            <footer class="modal__footer">
              <button
                type="submit"
                class="btn btn--primary"
                :disabled="asignando"
              >
                {{ asignando ? 'Asignando…' : 'Asignar' }}
              </button>
              <button
                type="button"
                class="btn btn--ghost"
                @click="cerrarAsignacion"
                :disabled="asignando"
              >
                Cancelar
              </button>
            </footer>
          </form>

          <div v-else class="modal__body">Cargando alumnos…</div>
        </div>
      </div>
    </Teleport>
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
      // modales
      mostrarCrearRecompensa: false,
      mostrarAsignar: false,
      // editor
      mostrarEditar: false,
      recompensaSeleccionada: null,
      nuevaRecompensa: { name: '', description: '', cost: 1 },
      // asignación manual
      alumnos: [],
      cargandoAlumnos: false,
      asignando: false,
      asignacion: { student_id: '', coins: 1, reason: '' },
      // handlers para limpiar eventos
      _onEscCrear: null,
      _onEscAsignar: null,
    };
  },

  watch: {
    mostrarCrearRecompensa(open) {
      this._toggleBodyAndEsc(open, 'crear');
    },
    mostrarAsignar(open) {
      this._toggleBodyAndEsc(open, 'asignar');
    },
  },

  mounted() {
    this.obtenerRecompensas();
  },

  beforeUnmount() {
    if (this._onEscCrear)
      window.removeEventListener('keydown', this._onEscCrear);
    if (this._onEscAsignar)
      window.removeEventListener('keydown', this._onEscAsignar);
    document.body.style.overflow = '';
  },

  methods: {
    _toggleBodyAndEsc(open, cual) {
      document.body.style.overflow = open ? 'hidden' : '';
      const handler = (e) => {
        if (e.key === 'Escape') {
          if (cual === 'crear') this.mostrarCrearRecompensa = false;
          else this.mostrarAsignar = false;
        }
      };
      const key = cual === 'crear' ? '_onEscCrear' : '_onEscAsignar';
      if (open) {
        window.addEventListener('keydown', handler);
        this[key] = handler;
      } else if (this[key]) {
        window.removeEventListener('keydown', this[key]);
        this[key] = null;
      }
    },

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
      const i = this.recompensas.findIndex(
        (r) => r.id === recompensaEditada.id
      );
      if (i !== -1) this.recompensas.splice(i, 1, recompensaEditada);
    },

    async abrirAsignacion() {
      this.mostrarAsignar = true;
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
.boton-toggle {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background-color: #1abc9c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
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
</style>
