<template>
  <div class="layout">
    <Header />
    <div class="content">
      <!-- La diferencia es el prop del Sidebar -->
      <Sidebar role="alumno" />
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
  position: relative;
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: #fff;
  z-index: 0;
}

/* 👉 mismo fondo translúcido que en profesor */
.main-content::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('/logonegro.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  opacity: 0.09;
  pointer-events: none;
  z-index: -1;
}
</style>
