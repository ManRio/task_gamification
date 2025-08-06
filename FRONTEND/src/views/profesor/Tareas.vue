<template>
  <div class="contenedor">
    <h1>Tareas asignadas</h1>

    <!-- Botón para abrir el formulario de creación -->
    <div class="acciones">
      <button @click="mostrarCrearTarea = true">+ Crear nueva tarea</button>
    </div>

    <!-- Tabla de tareas -->
    <table v-if="tareas.length" class="tabla">
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

    <!-- Modal: Crear Tarea -->
    <div v-if="mostrarCrearTarea" class="modal">
      <h3>Crear nueva tarea</h3>
      <form @submit.prevent="crearTarea" class="formulario-tarea">
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

        <div class="acciones-form">
          <button type="submit">Crear</button>
          <button type="button" @click="mostrarCrearTarea = false">
            Cancelar
          </button>
        </div>
      </form>
    </div>

    <!-- Modal: Editar Tarea -->
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
  components: {
    EditarTarea,
  },
  setup() {
    const toast = useToast(); // ⬅️ Inicializar

    return {
      toast,
    };
  },
  data() {
    return {
      tareas: [],
      mostrarCrearTarea: false,
      mostrarEditarTarea: false,
      tareaSeleccionada: null,
      nuevaTarea: {
        titulo: '',
        descripcion: '',
        monedas: 1,
      },
    };
  },
  mounted() {
    this.obtenerTareas();
  },
  methods: {
    async obtenerTareas() {
      try {
        const res = await api.get('/tasks/mine');
        this.tareas = res.data;
      } catch (error) {
        console.error('Error al obtener tareas:', error);
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

        await this.obtenerTareas(); // 👈 recarga la lista actualizada
        this.toast.success('Tarea creada correctamente');
      } catch (error) {
        console.error('Error al crear tarea:', error);
        this.toast.error('Error al crear tarea');
      }
    },
    async eliminarTarea(id) {
      if (!confirm('¿Estás seguro de que deseas eliminar esta tarea?')) return;

      try {
        await api.delete(`/tasks/${id}`);
        this.tareas = this.tareas.filter((t) => t.id !== id);
        this.toast.success('Tarea eliminada correctamente');
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
      if (index !== -1) {
        this.tareas.splice(index, 1, tareaActualizada);
      }
    },
  },
};
</script>

<style scoped>
.contenedor {
  padding: 2rem;
}

.acciones {
  margin-bottom: 1.5rem;
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
.eliminar {
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

.acciones-form {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
