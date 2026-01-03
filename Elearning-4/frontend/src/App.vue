<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

onMounted(() => {
  // Khôi phục session nếu có token
  if (localStorage.getItem('token')) {
    authStore.restoreSession();
  }
});
</script>