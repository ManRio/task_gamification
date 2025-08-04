<template>
  <div>
    <router-view />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import Header from './components/Header.vue';

const route = useRoute();

// Ocultamos el header en la landing (/)
const showHeader = computed(() => route.path !== '/');
</script>
