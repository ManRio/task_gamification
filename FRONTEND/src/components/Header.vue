<template>
  <header class="app-header">
    <div class="logo-section">
      <img src="/logo.png" alt="TaskGamify logo" class="logo" />
      <span class="title">TaskGamify</span>
    </div>

    <div v-if="userStore.isAuthenticated" class="user-section">
      <span class="username">Hola, {{ userStore.user.username }}</span>
      <button @click="logout">Cerrar sesión</button>
    </div>
  </header>
</template>

<script setup>
import { useUserStore } from '../stores/userStore';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();

const logout = () => {
  userStore.logout();
  router.push('/');
};
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1e90ff;
  padding: 1rem 2rem;
  color: white;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo {
  height: 32px;
  width: 32px;
}

.title {
  font-size: 1.4rem;
  font-weight: 600;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  font-weight: 500;
}

button {
  background-color: white;
  color: #1e90ff;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  background-color: #f0f0f0;
}
</style>