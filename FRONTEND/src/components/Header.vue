<template>
  <header class="header">
    <img src="/logo.png" alt="Logo" class="logo" />
    <h1 class="titulo">Task Gamification</h1>
    <div class="acciones">
      <span>{{ user.username }}</span>
      <button @click="logout">Cerrar sesión</button>
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
  height: 60px;
  background: #34495e;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.logo {
  height: 40px;
}

.acciones {
  display: flex;
  gap: 1rem;
  align-items: center;
}
</style>
