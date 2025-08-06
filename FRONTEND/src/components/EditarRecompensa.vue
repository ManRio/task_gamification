<template>
  <div class="modal-overlay" @click.self="cerrar">
    <div class="modal">
      <h3>Editar recompensa</h3>
      <form @submit.prevent="guardarCambios" class="formulario">
        <div class="campo">
          <label for="nombre">Nombre</label>
          <input v-model="formData.name" id="nombre" required />
        </div>

        <div class="campo">
          <label for="descripcion">Descripción</label>
          <textarea v-model="formData.description" id="descripcion" required />
        </div>

        <div class="campo">
          <label for="cost">Coste (monedas)</label>
          <input
            v-model.number="formData.cost"
            id="cost"
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
  recompensa: Object,
});

const emit = defineEmits(['cerrar', 'actualizada']);
const toast = useToast();

const formData = reactive({
  name: '',
  description: '',
  cost: 1,
});

watch(
  () => props.recompensa,
  (nueva) => {
    if (nueva) {
      formData.name = nueva.name;
      formData.description = nueva.description;
      formData.cost = nueva.cost;
    }
  },
  { immediate: true }
);

function cerrar() {
  emit('cerrar');
}

async function guardarCambios() {
  try {
    const res = await api.put(`/rewards/${props.recompensa.id}`, {
      ...formData,
    });
    toast.success('Recompensa actualizada');
    emit('actualizada', res.data);
    cerrar();
  } catch (error) {
    console.error('Error al actualizar recompensa:', error);
    toast.error('Hubo un error al actualizar');
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

.formulario {
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
