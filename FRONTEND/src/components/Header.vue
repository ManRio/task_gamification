<template>
  <header class="header">
    <img src="/logo.png" alt="Logo" class="logo" />
    <h1 class="titulo">Task Gamification</h1>
    <div class="acciones">
      <span class="usuario">{{ user.username }}</span>
      <button class="btn" @click="logout">Cerrar sesión</button>
    </div>
  </header>
</template>

<script>
import { useUserStore } from '../stores/userStore';

export default {
  setup() {
    const userStore = useUserStore();
    return {
      user: userStore.user,
      logout: userStore.logout,
    };
  },
};
</script>

<style scoped>
.header {
  height: 80px; /* más razonable que 150px; cámbialo si quieres */
  background: #2c3e50;
  color: #fff;
  display: grid; /* grid para centrar el título sin trucos */
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1rem;
  padding: 0 1.25rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.logo {
  height: 36px;
  display: block;
}

.titulo {
  margin: 0; /* 🔒 evita márgenes por defecto del h1 */
  text-align: center;
  font-size: 1.5rem; /* ~24px */
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
  opacity: 0.9;
  font-weight: 500;
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
