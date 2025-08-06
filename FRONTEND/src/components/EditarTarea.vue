<template>
  <div class="modal-overlay" @click.self="cerrar">
    <div class="modal">
      <h3>Editar tarea</h3>
      <form @submit.prevent="guardarCambios" class="formulario-tarea">
        <div class="campo">
          <label for="titulo">Título</label>
          <input v-model="formData.title" id="titulo" required />
        </div>

        <div class="campo">
          <label for="descripcion">Descripción</label>
          <textarea v-model="formData.description" id="descripcion" required />
        </div>

        <div class="campo">
          <label for="monedas">Monedas</label>
          <input
            v-model.number="formData.reward"
            id="monedas"
            type="number"
            min="1"
            required
          />
        </div>

        <div class="acciones">
          <button type="submit">Guardar</button>
          <button type="button" @click="cerrar">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue';
import api from '../api';
import { useToast } from 'vue-toastification';

const props = defineProps({
  tarea: Object, // tarea original que se pasa como prop
  visible: Boolean, // control de visibilidad del modal
});

const emit = defineEmits(['cerrar', 'actualizada']);

const toast = useToast();

const formData = reactive({
  title: '',
  description: '',
  reward: 1,
});

watch(
  () => props.tarea,
  (nueva) => {
    if (nueva) {
      formData.title = nueva.title;
      formData.description = nueva.description;
      formData.reward = nueva.reward;
    }
  },
  { immediate: true }
);

function cerrar() {
  emit('cerrar');
}

async function guardarCambios() {
  try {
    const res = await api.put(`/tasks/${props.tarea.id}`, { ...formData });
    toast.success('Tarea actualizada');
    emit('actualizada', res.data); // enviamos la tarea actualizada al padre
    cerrar();
  } catch (error) {
    console.error('Error al actualizar tarea:', error);
    toast.error('Hubo un error al actualizar la tarea');
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
}

.formulario-tarea {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.campo label {
  font-weight: bold;
}

.campo input,
.campo textarea {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.acciones {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
