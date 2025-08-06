<template>
  <div class="layout">
    <Header />
    <div class="content">
      <Sidebar />
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue';
import Header from '../components/Header.vue';
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.content {
  display: flex;
  flex: 1;
}

.main-content {
  position: relative; /* 🔑 Necesario para que ::before se posicione dentro */
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: rgb(255, 255, 255);
  z-index: 0;
}

/* Fondo con transparencia sin afectar contenido */
.main-content::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('/logonegro.png'); /* Ruta relativa desde /public */
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  opacity: 0.09; /* Ajusta la transparencia aquí */
  pointer-events: none;
  z-index: -1; /* Asegura que esté debajo del contenido */
}
</style>
