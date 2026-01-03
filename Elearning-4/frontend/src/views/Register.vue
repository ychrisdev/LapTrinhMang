<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-96">
      <!-- Header - Ngang hàng với tiêu đề căn giữa -->
      <div class="relative mb-6">
        <router-link to="/" class="absolute left-0 top-1/2 -translate-y-1/2 text-gray-500 text-sm hover:text-gray-700">
          ←
        </router-link>
        <h2 class="text-2xl font-bold text-center">Đăng ký</h2>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label class="block mb-2 text-sm">Tên</label>
          <input v-model="form.name" type="text" class="input" required>
        </div>
        
        <div class="mb-4">
          <label class="block mb-2 text-sm">Email</label>
          <input v-model="form.email" type="email" class="input" required>
        </div>
        
        <div class="mb-6">
          <label class="block mb-2 text-sm">Password</label>
          <input v-model="form.password" type="password" class="input" required>
        </div>
        
        <button type="submit" class="btn btn-primary w-full">Đăng ký</button>
      </form>
      
      <p class="mt-4 text-center text-sm">
        Đã có tài khoản? 
        <router-link to="/login" class="text-blue-500">Đăng nhập</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  name: '',
  email: '',
  password: ''
});

const handleSubmit = async () => {
  try {
    await authStore.register(form.value);
    alert('Đăng ký thành công! Vui lòng đăng nhập.');
    router.push('/login');
  } catch (error) {
    alert(error.response?.data?.message || 'Đăng ký thất bại');
  }
};
</script>