<template>
  <header class="header">
    <img src="/logo.png" alt="Logo" class="logo" />
    <h1 class="titulo">Task Gamification</h1>
    <div class="acciones">
      <!-- Click en el nombre abre el modal -->
      <button class="usuario" @click="abrirModalPerfil" title="Editar perfil">
        {{ user.username }}
      </button>
      <button class="btn" @click="logout">Cerrar sesión</button>
    </div>
  </header>

  <!-- MODAL: Editar perfil -->
  <Teleport to="body">
    <div v-if="mostrarPerfil" class="overlay" @click.self="cerrarModalPerfil">
      <div
        class="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="perfil-title"
      >
        <header class="modal__header">
          <h3 id="perfil-title">Editar perfil</h3>
          <button
            class="modal__close"
            aria-label="Cerrar"
            @click="cerrarModalPerfil"
          >
            ✕
          </button>
        </header>

        <form class="modal__body formulario" @submit.prevent="guardarPerfil">
          <!-- Nombre -->
          <div class="campo">
            <label for="first_name">Nombre</label>
            <input id="first_name" v-model.trim="form.first_name" required />
          </div>

          <!-- Apellidos -->
          <div class="campo">
            <label for="last_name">Apellidos</label>
            <input id="last_name" v-model.trim="form.last_name" required />
          </div>

          <!-- Email -->
          <div class="campo">
            <label for="email">Email</label>
            <input id="email" type="email" v-model.trim="form.email" required />
          </div>

          <!-- Curso (solo alumnos) -->
          <div v-if="user?.role === 'student'" class="campo">
            <label for="course">Curso</label>
            <input
              id="course"
              v-model.trim="form.course"
              placeholder="Ej.: 2ºB"
            />
          </div>

          <!-- (Opcional) Teléfono u otros datos -->
          <!--
          <div class="campo">
            <label for="phone">Teléfono</label>
            <input id="phone" v-model.trim="form.phone" />
          </div>
          -->

          <footer class="modal__footer">
            <button
              type="submit"
              class="btn btn--primary"
              :disabled="guardando"
            >
              {{ guardando ? 'Guardando…' : 'Guardar cambios' }}
            </button>
            <button
              type="button"
              class="btn btn--ghost"
              @click="cerrarModalPerfil"
              :disabled="guardando"
            >
              Cancelar
            </button>
          </footer>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { ref, watch, onBeforeUnmount } from 'vue';
import { useToast } from 'vue-toastification';
import { useUserStore } from '../stores/userStore';
import api from '../api'; // ajusta la ruta si tu helper está en otro path

export default {
  setup() {
    const toast = useToast();
    const userStore = useUserStore();
    const user = userStore.user; // asumes que es reactivo (pinia)

    // Modal
    const mostrarPerfil = ref(false);
    const guardando = ref(false);
    const _onEsc = ref(null);

    // Form
    const form = ref({
      first_name: '',
      last_name: '',
      email: '',
      course: '', // sólo aplicará si es alumno
      // phone: '', // ejemplo de campo extra
    });

    const hidratarForm = () => {
      form.value.first_name = user?.first_name || '';
      form.value.last_name = user?.last_name || '';
      form.value.email = user?.email || '';
      form.value.course = user?.course || '';
      // form.value.phone = user?.phone || '';
    };

    const abrirModalPerfil = () => {
      hidratarForm();
      mostrarPerfil.value = true;
    };

    const cerrarModalPerfil = () => {
      mostrarPerfil.value = false;
    };

    // Bloqueo de scroll + cerrar con ESC
    watch(mostrarPerfil, (open) => {
      document.body.style.overflow = open ? 'hidden' : '';
      if (open) {
        _onEsc.value = (e) =>
          e.key === 'Escape' && (mostrarPerfil.value = false);
        window.addEventListener('keydown', _onEsc.value);
      } else if (_onEsc.value) {
        window.removeEventListener('keydown', _onEsc.value);
        _onEsc.value = null;
      }
    });
    onBeforeUnmount(() => {
      if (_onEsc.value) window.removeEventListener('keydown', _onEsc.value);
      document.body.style.overflow = '';
    });

    const guardarPerfil = async () => {
      // payload mínimo común; el backend puede ignorar campos no aplicables al rol
      const payload = {
        first_name: form.value.first_name?.trim(),
        last_name: form.value.last_name?.trim(),
        email: form.value.email?.trim(),
        course:
          user?.role === 'student'
            ? (form.value.course || '').trim()
            : undefined,
        // phone: (form.value.phone || '').trim(),
      };

      guardando.value = true;
      try {
        // endpoint recomendado (ajusta a tu API): PUT /users/me
        const { data } = await api.put('/users/me', payload);

        // 1) Actualiza el store con la respuesta del backend si viene el user ya normalizado
        if (data?.user) {
          // si tienes un setter expuesto en el store, úsalo:
          // userStore.setUser(data.user)
          // si no, haz un merge sobre el objeto reactivo:
          Object.assign(user, data.user);
        } else {
          // fallback si tu backend no devuelve el usuario completo
          Object.assign(user, payload);
        }

        toast.success('Perfil actualizado');
        cerrarModalPerfil();
      } catch (err) {
        console.error('Error al guardar perfil:', err);
        const msg =
          err?.response?.data?.msg || 'No se pudo actualizar el perfil';
        toast.error(msg);
      } finally {
        guardando.value = false;
      }
    };

    const logout = userStore.logout;

    return {
      user,
      logout,
      // modal
      mostrarPerfil,
      abrirModalPerfil,
      cerrarModalPerfil,
      // form
      form,
      guardando,
      guardarPerfil,
    };
  },
};
</script>

<style scoped>
.header {
  height: 80px;
  background: #2c3e50;
  color: #fff;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1rem;
  padding: 0 1.25rem;
  position: sticky;
  top: 0;
  z-index: 10;
}
.logo {
  height: 75px;
  display: block;
}
.titulo {
  margin: 0;
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 0.3px;
  line-height: 1.2;
}
.acciones {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.usuario {
  background: transparent;
  border: 1px solid var(--c-border);
  color: #fff;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  cursor: pointer;
  opacity: 0.9;
  font-weight: 600;
}
.usuario:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.08);
}
.btn {
  background: #1abc9c;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.45rem 0.75rem;
  cursor: pointer;
}
.btn:hover {
  filter: brightness(1.05);
}
</style>
