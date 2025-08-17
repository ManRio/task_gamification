<template>
  <div class="contenedor">
    <h1 class="principal_title">Tareas asignadas</h1>

    <!-- Acciones -->
    <div class="acciones">
      <button class="secundario" @click="mostrarCrearTarea = true">
        ➕ Crear nueva tarea
      </button>
      <button
        class="secundario"
        @click="refrescarTodo"
        :disabled="cargandoPendientes || cargandoTareas"
      >
        🔄 Refrescar
      </button>
    </div>

    <!-- BLOQUE: Pendientes de aprobación -->
    <section class="bloque">
      <h2 class="title">Pendientes de aprobación</h2>

      <div v-if="cargandoPendientes">Cargando pendientes…</div>
      <table v-else-if="pendientes.length" class="tabla">
        <thead>
          <tr>
            <th>Alumno</th>
            <th>Tarea</th>
            <th>Monedas</th>
            <th>Entregada</th>
            <th style="width: 180px">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in pendientes" :key="p.completion_id">
            <td>{{ p.student_username }} (ID: {{ p.student_id }})</td>
            <td>{{ p.task_title }}</td>
            <td>{{ p.task_reward }}</td>
            <td>{{ formatearFecha(p.completed_at) }}</td>
            <td>
              <button
                class="secundario aprobar"
                :disabled="accionandoId === p.completion_id"
                @click="aprobarEntrega(p)"
              >
                ✅ Aprobar
              </button>
              <button
                class="secundario rechazar"
                :disabled="accionandoId === p.completion_id"
                @click="rechazarEntrega(p)"
              >
                ❌ Rechazar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay entregas pendientes.</p>
    </section>

    <!-- BLOQUE: Tareas del profesor -->
    <section class="bloque">
      <h2 class="title">Tareas creadas por mi</h2>

      <div v-if="cargandoTareas">Cargando tareas…</div>
      <table v-else-if="tareas.length" class="tabla">
        <thead>
          <tr>
            <th>Título</th>
            <th>Descripción</th>
            <th>Monedas</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tarea in tareas" :key="tarea.id">
            <td>{{ tarea.title }}</td>
            <td>{{ tarea.description }}</td>
            <td>{{ tarea.reward }}</td>
            <td>
              <button class="editar" @click="abrirEditor(tarea)">Editar</button>
              <button class="eliminar" @click="eliminarTarea(tarea.id)">
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-else>No hay tareas aún.</p>
    </section>

    <!-- MODAL: Crear Tarea -->
    <Teleport to="body">
      <div
        v-if="mostrarCrearTarea"
        class="overlay"
        @click.self="mostrarCrearTarea = false"
      >
        <div
          class="modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="crear-tarea-title"
        >
          <header class="modal__header">
            <h3 id="crear-tarea-title">Crear nueva tarea</h3>
            <button
              class="modal__close"
              aria-label="Cerrar"
              @click="mostrarCrearTarea = false"
            >
              ✕
            </button>
          </header>

          <form
            @submit.prevent="crearTarea"
            class="modal__body formulario-tarea"
          >
            <div class="campo">
              <label for="titulo">Título</label>
              <input v-model="nuevaTarea.titulo" id="titulo" required />
            </div>

            <div class="campo">
              <label for="descripcion">Descripción</label>
              <textarea
                v-model="nuevaTarea.descripcion"
                id="descripcion"
                required
              ></textarea>
            </div>

            <div class="campo">
              <label for="monedas">Monedas</label>
              <input
                v-model.number="nuevaTarea.monedas"
                id="monedas"
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
                @click="mostrarCrearTarea = false"
              >
                Cancelar
              </button>
            </footer>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Modal: Editar Tarea (componente propio) -->
    <EditarTarea
      v-if="mostrarEditarTarea"
      :tarea="tareaSeleccionada"
      :visible="mostrarEditarTarea"
      @cerrar="cerrarEditor"
      @actualizada="actualizarTareaEnLista"
    />
  </div>
</template>

<script>
import api from '../../api';
import EditarTarea from '../../components/EditarTarea.vue';
import { useToast } from 'vue-toastification';

export default {
  components: { EditarTarea },
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      tareas: [],
      cargandoTareas: false,
      pendientes: [],
      cargandoPendientes: false,
      accionandoId: null,

      mostrarCrearTarea: false,
      mostrarEditarTarea: false,
      tareaSeleccionada: null,

      nuevaTarea: { titulo: '', descripcion: '', monedas: 1 },

      _onEscCrear: null,
    };
  },
  watch: {
    mostrarCrearTarea(open) {
      document.body.style.overflow = open ? 'hidden' : '';
      const handler = (e) =>
        e.key === 'Escape' && (this.mostrarCrearTarea = false);
      if (open) {
        window.addEventListener('keydown', handler);
        this._onEscCrear = handler;
      } else if (this._onEscCrear) {
        window.removeEventListener('keydown', this._onEscCrear);
        this._onEscCrear = null;
      }
    },
  },
  beforeUnmount() {
    if (this._onEscCrear)
      window.removeEventListener('keydown', this._onEscCrear);
    document.body.style.overflow = '';
  },
  mounted() {
    this.refrescarTodo();
  },
  methods: {
    async refrescarTodo() {
      await Promise.all([this.obtenerTareas(), this.obtenerPendientes()]);
    },

    // -------- PENDIENTES --------
    async obtenerPendientes() {
      this.cargandoPendientes = true;
      try {
        const res = await api.get('/tasks/pending_approval');
        this.pendientes = res.data;
      } catch (error) {
        console.error('Error al obtener pendientes:', error);
        this.toast.error('No se pudieron cargar las pendientes');
      } finally {
        this.cargandoPendientes = false;
      }
    },

    async aprobarEntrega(p) {
      if (this.accionandoId) return;
      this.accionandoId = p.completion_id;

      const backup = [...this.pendientes];
      this.pendientes = this.pendientes.filter(
        (x) => x.completion_id !== p.completion_id
      );

      try {
        await api.post(`/tasks/validate/${p.completion_id}`);
        this.toast.success(
          `Aprobada: "${p.task_title}" (+${p.task_reward} monedas)`
        );
      } catch (error) {
        console.error('Error al aprobar:', error);
        this.toast.error('No se pudo aprobar. Reintentando cargar.');
        this.pendientes = backup;
      } finally {
        this.accionandoId = null;
      }
    },

    async rechazarEntrega(p) {
      if (this.accionandoId) return;
      if (
        !confirm(
          `¿Rechazar la entrega de "${p.task_title}" de ${p.student_username}?`
        )
      )
        return;

      this.accionandoId = p.completion_id;

      const backup = [...this.pendientes];
      this.pendientes = this.pendientes.filter(
        (x) => x.completion_id !== p.completion_id
      );

      try {
        await api.post(`/tasks/reject/${p.completion_id}`);
        this.toast.info(`Rechazada: "${p.task_title}"`);
      } catch (error) {
        console.error('Error al rechazar:', error);
        this.toast.error('No se pudo rechazar. Reintentando cargar.');
        this.pendientes = backup;
      } finally {
        this.accionandoId = null;
      }
    },

    formatearFecha(iso) {
      if (!iso) return '—';
      try {
        return new Date(iso).toLocaleString();
      } catch {
        return iso;
      }
    },

    // -------- MIS TAREAS --------
    async obtenerTareas() {
      this.cargandoTareas = true;
      try {
        const res = await api.get('/tasks/mine');
        this.tareas = res.data;
      } catch (error) {
        console.error('Error al obtener tareas:', error);
        this.toast.error('No se pudieron cargar tus tareas');
      } finally {
        this.cargandoTareas = false;
      }
    },

    async crearTarea() {
      try {
        await api.post('/tasks/create', {
          title: this.nuevaTarea.titulo,
          description: this.nuevaTarea.descripcion,
          reward: this.nuevaTarea.monedas,
        });
        this.nuevaTarea = { titulo: '', descripcion: '', monedas: 1 };
        this.mostrarCrearTarea = false;
        await this.obtenerTareas();
        this.toast.success('Tarea creada correctamente');
      } catch (error) {
        console.error('Error al crear tarea:', error);
        this.toast.error(error?.response?.data?.msg || 'Error al crear tarea');
      }
    },

    async eliminarTarea(id) {
      if (!confirm('¿Eliminar esta tarea?')) return;
      try {
        await api.delete(`/tasks/${id}`);
        this.tareas = this.tareas.filter((t) => t.id !== id);
        this.toast.success('Tarea eliminada');
      } catch (error) {
        console.error('Error al eliminar tarea:', error);
        this.toast.error('Error al eliminar la tarea');
      }
    },

    abrirEditor(tarea) {
      this.tareaSeleccionada = tarea;
      this.mostrarEditarTarea = true;
    },
    cerrarEditor() {
      this.mostrarEditarTarea = false;
      this.tareaSeleccionada = null;
    },
    actualizarTareaEnLista(tareaActualizada) {
      const index = this.tareas.findIndex((t) => t.id === tareaActualizada.id);
      if (index !== -1) this.tareas.splice(index, 1, tareaActualizada);
    },
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
.acciones {
  margin-bottom: 1.5rem;
  display: flex;
  gap: 0.5rem;
}
.secundario {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background-color: #1abc9c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.bloque {
  margin-top: 2rem;
}
.tabla {
  width: 100%;
  border-collapse: collapse;
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
.editar,
.eliminar,
.aprobar,
.rechazar {
  margin-right: 0.5rem;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.editar {
  background-color: #3498db;
  color: white;
}
.eliminar {
  background-color: #e74c3c;
  color: white;
}
.aprobar {
  background-color: #27ae60;
  color: white;
}
.rechazar {
  background-color: #8e44ad;
  color: white;
}
.formulario-tarea {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.campo {
  display: flex;
  flex-direction: column;
}
.campo label {
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.campo input,
.campo textarea {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
</style>
