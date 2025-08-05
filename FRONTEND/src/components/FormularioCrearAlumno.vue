<template>
  <div class="formulario-crear-alumno">
    <h3>{{ alumnoEditar ? 'Editar alumno' : 'Crear nuevo alumno' }}</h3>
    <form @submit.prevent="alumnoEditar ? actualizarAlumno() : crearAlumno()">
      <div class="campo" v-for="(label, key) in campos" :key="key">
        <label>{{ label }}:</label>
        <input
          :type="
            key === 'email' ? 'email' : key === 'password' ? 'password' : 'text'
          "
          v-model="form[key]"
          :required="key !== 'password' || !alumnoEditar"
        />
      </div>
      <button type="submit">
        {{ alumnoEditar ? 'Actualizar' : 'Crear alumno' }}
      </button>
    </form>

    <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';
import axios from '../services/api';

const emit = defineEmits(['alumnoCreado', 'cancelarEdicion']);
const props = defineProps({
  alumnoEditar: Object,
});

const campos = {
  first_name: 'Nombre',
  last_name: 'Apellidos',
  email: 'Email',
  course: 'Curso',
  username: 'Username',
  password: 'Password',
};

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  course: '',
  username: '',
  password: '',
});

const mensaje = ref('');

watch(
  () => props.alumnoEditar,
  (nuevo) => {
    if (nuevo) {
      form.value = {
        ...nuevo,
        password: '',
      };
    } else {
      form.value = {
        first_name: '',
        last_name: '',
        email: '',
        course: '',
        username: '',
        password: '',
      };
    }
  },
  { immediate: true }
);

const crearAlumno = async () => {
  try {
    await axios.post('/students/create', form.value);
    mensaje.value = 'Alumno creado correctamente';
    emit('alumnoCreado');
  } catch (error) {
    console.error(error);
    mensaje.value = 'Error al crear el alumno';
  }
};

const actualizarAlumno = async () => {
  try {
    await axios.put(`/students/${props.alumnoEditar.id}`, form.value);
    mensaje.value = 'Alumno actualizado correctamente';
    emit('alumnoCreado'); // reutilizamos el mismo evento
  } catch (error) {
    console.error(error);
    mensaje.value = 'Error al actualizar el alumno';
  }
};
</script>

<style scoped>
.formulario-crear-alumno {
  max-width: 500px;
  margin-top: 1rem;
}

.campo {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  padding: 10px 16px;
  background-color: #1abc9c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.mensaje {
  margin-top: 1rem;
  font-weight: bold;
}
</style>
