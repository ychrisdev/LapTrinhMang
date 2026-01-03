<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4">
        <router-link to="/blogs" class="text-gray-600">← Quay lại</router-link>
      </div>
    </nav>
    
    <div class="container mx-auto px-4 py-8 max-w-2xl">
      <h2 class="text-3xl font-bold mb-6">Tạo Blog mới</h2>
      
      <form @submit.prevent="handleSubmit" class="card">
        <div class="mb-4">
          <label class="block mb-2">Tiêu đề *</label>
          <input v-model="form.title" type="text" class="input" required>
        </div>
        
        <div class="mb-4">
          <label class="block mb-2">Nội dung *</label>
          <textarea 
            v-model="form.content" 
            class="input" 
            rows="10" 
            required
          ></textarea>
        </div>
        
        <div class="mb-6">
          <label class="block mb-2">Hình ảnh</label>
          <input 
            type="file" 
            @change="handleFileChange" 
            accept="image/*"
            class="input"
          >
        </div>
        
        <button type="submit" class="btn btn-primary w-full">Tạo Blog</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from '@/api/axios';

const router = useRouter();

const form = ref({
  title: '',
  content: ''
});

const imageFile = ref(null);

const handleFileChange = (e) => {
  imageFile.value = e.target.files[0];
};

const handleSubmit = async () => {
  try {
    const formData = new FormData();
    formData.append('title', form.value.title);
    formData.append('content', form.value.content);
    if (imageFile.value) {
      formData.append('image', imageFile.value);
    }
    
    await axios.post('/blogs', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    alert('Tạo blog thành công!');
    router.push('/blogs');
  } catch (error) {
    alert('Tạo blog thất bại!');
  }
};
</script>