<template>
  <div class="alumnos">
    <h2>Gestión de alumnos</h2>

    <button @click="toggleFormulario" class="boton-toggle">
      {{ mostrarFormulario ? 'Cerrar formulario' : 'Crear nuevo alumno' }}
    </button>

    <!-- Formulario condicional -->
    <FormularioCrearAlumno
      v-if="mostrarFormulario"
      :alumnoEditar="alumnoEditando"
      @alumnoCreado="handleAlumnoCreado"
    />

    <!-- Filtros -->
    <div class="filtros">
      <input v-model="filtro.nombre" placeholder="Nombre" />
      <input v-model="filtro.apellidos" placeholder="Apellidos" />
      <input v-model="filtro.username" placeholder="Username" />
      <input v-model="filtro.curso" placeholder="Curso" />
    </div>

    <!-- Tabla -->
    <table>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Apellidos</th>
          <th>Username</th>
          <th>Email</th>
          <th>Curso</th>
          <th>Monedas</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="alumno in alumnosFiltrados" :key="alumno.id">
          <td>{{ alumno.first_name }}</td>
          <td>{{ alumno.last_name }}</td>
          <td>{{ alumno.username }}</td>
          <td>{{ alumno.email }}</td>
          <td>{{ alumno.course }}</td>
          <td>{{ alumno.coins }}</td>
          <td>
            <button @click="editarAlumno(alumno)">✏️</button>
            <button @click="borrarAlumno(alumno.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from '../../services/api';
import FormularioCrearAlumno from '../../components/FormularioCrearAlumno.vue';

const alumnos = ref([]);
const mostrarFormulario = ref(false);
const alumnoEditando = ref(null);

const filtro = ref({
  nombre: '',
  apellidos: '',
  username: '',
  curso: '',
});

const fetchAlumnos = async () => {
  try {
    const res = await axios.get('/students/all');
    alumnos.value = res.data;
  } catch (err) {
    console.error('Error al obtener alumnos:', err);
  }
};

const handleAlumnoCreado = () => {
  mostrarFormulario.value = false;
  alumnoEditando.value = null;
  fetchAlumnos();
};

const toggleFormulario = () => {
  if (mostrarFormulario.value && alumnoEditando.value) {
    alumnoEditando.value = null;
  }
  mostrarFormulario.value = !mostrarFormulario.value;
};

const editarAlumno = (alumno) => {
  alumnoEditando.value = { ...alumno };
  mostrarFormulario.value = true;
};

const borrarAlumno = async (id) => {
  if (!confirm('¿Seguro que quieres eliminar este alumno?')) return;
  try {
    await axios.delete(`/students/${id}`);
    fetchAlumnos();
  } catch (err) {
    console.error('Error al eliminar alumno:', err);
  }
};

const alumnosFiltrados = computed(() => {
  return alumnos.value.filter((alumno) => {
    const nombre = alumno.first_name?.toLowerCase() || '';
    const apellidos = alumno.last_name?.toLowerCase() || '';
    const username = alumno.username?.toLowerCase() || '';
    const curso = alumno.course?.toLowerCase() || '';

    return (
      nombre.includes(filtro.value.nombre?.toLowerCase() || '') &&
      apellidos.includes(filtro.value.apellidos?.toLowerCase() || '') &&
      username.includes(filtro.value.username?.toLowerCase() || '') &&
      curso.includes(filtro.value.curso?.toLowerCase() || '')
    );
  });
});

onMounted(() => {
  fetchAlumnos();
});
</script>

<style scoped>
.alumnos {
  max-width: 900px;
  margin: 2rem auto;
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

.filtros {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 1rem 0;
}

.filtros input {
  padding: 8px;
  flex: 1 1 200px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

th,
td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background-color: #f5f5f5;
}

button {
  margin-right: 5px;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
