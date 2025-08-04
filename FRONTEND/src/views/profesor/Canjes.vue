<template>
  <div class="layout">
    <Sidebar />
    <div class="main-content">
      <Header />
      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../../components/Sidebar.vue';
import Header from '../../components/Header.vue';
</script>

<style scoped>
.layout {
  display: flex;
}

.main-content {
  margin-left: 220px;
  width: 100%;
}
main {
  padding: 2rem;
}
</style>
