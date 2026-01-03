<template>
  <div class="min-h-screen bg-gray-50">
    <!-- NAVBAR -->
    <nav class="bg-white border-b">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        
        <!-- Logo -->
        <h1 class="text-2xl font-semibold text-blue-600">
          Blog System
        </h1>

        <!-- Navigation -->
        <div class="flex items-center gap-6">
          <!-- Blogs -->
          <router-link
            to="/blogs"
            class="px-4 py-2 rounded border border-gray-300 text-gray-700 hover:bg-gray-100"
          >
            Blogs
          </router-link>

          <!-- Login / Logout -->
          <router-link
            v-if="!authStore.isLoggedIn"
            to="/login"
            class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
          >
            Login
          </router-link>

          <button
            v-else
            @click="logout"
            class="px-4 py-2 rounded border border-red-500 text-red-500 hover:bg-red-50"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>

    <!-- CONTENT -->
    <div class="container mx-auto px-6 py-20 text-center">
      <h2 class="text-4xl font-bold mb-4">
        Chào mừng đến Blog System
      </h2>

      <p class="text-gray-600 mb-10">
        Nền tảng blog đơn giản và hiệu quả
      </p>

      <router-link
        to="/blogs"
        class="inline-block px-10 py-4 text-lg rounded bg-blue-600 text-white hover:bg-blue-700"
      >
        Xem tất cả Blogs
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/')
}
</script>
