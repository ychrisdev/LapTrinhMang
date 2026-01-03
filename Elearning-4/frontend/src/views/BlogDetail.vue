<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4">
        <router-link to="/blogs" class="text-gray-600 hover:text-gray-900">
          ← Quay lại danh sách
        </router-link>
      </div>
    </nav>
    
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-4 py-8 text-center">
      <p class="text-gray-500">Đang tải...</p>
    </div>
    
    <!-- Blog Content -->
    <div v-else-if="blog" class="container mx-auto px-4 py-8 max-w-4xl">
      <article class="card">
        <!-- Title -->
        <h1 class="text-4xl font-bold mb-4">{{ blog.title }}</h1>
        
        <!-- Meta Info -->
        <div class="flex items-center gap-4 text-sm text-gray-500 mb-6 pb-6 border-b">
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            {{ blog.author_name }}
          </span>
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ formatDate(blog.created_at) }}
          </span>
          <span v-if="blog.updated_at !== blog.created_at" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Cập nhật: {{ formatDate(blog.updated_at) }}
          </span>
        </div>
        
        <!-- Image -->
        <div v-if="blog.image" class="mb-6">
          <img 
            :src="getImageUrl(blog.image)" 
            :alt="blog.title"
            class="w-full h-auto rounded-lg shadow-md"
          >
        </div>
        
        <!-- Content -->
        <div class="prose max-w-none mb-8">
          <p class="text-gray-700 text-lg leading-relaxed whitespace-pre-wrap">{{ blog.content }}</p>
        </div>
        
        <!-- Actions (if owner) -->
        <div v-if="authStore.user?.id === blog.user_id" class="flex gap-3 pt-6 border-t">
          <router-link 
            :to="`/blogs/${blog.id}/edit`" 
            class="btn btn-secondary"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Chỉnh sửa
          </router-link>
          <button 
            @click="deleteBlog" 
            class="btn btn-danger"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Xóa
          </button>
        </div>
      </article>
    </div>
    
    <!-- Error State -->
    <div v-else class="container mx-auto px-4 py-8 text-center">
      <p class="text-red-500">Không tìm thấy blog!</p>
      <router-link to="/blogs" class="btn btn-primary mt-4">
        Về danh sách
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import axios from '@/api/axios';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const blog = ref(null);
const loading = ref(true);

const loadBlog = async () => {
  try {
    loading.value = true;
    const { data } = await axios.get(`/blogs/${route.params.id}`);
    blog.value = data.data;
  } catch (error) {
    console.error(error);
    blog.value = null;
  } finally {
    loading.value = false;
  }
};

const deleteBlog = async () => {
  if (!confirm('Bạn có chắc chắn muốn xóa blog này?')) return;
  
  try {
    await axios.delete(`/blogs/${route.params.id}`);
    alert('Xóa blog thành công!');
    router.push('/blogs');
  } catch (error) {
    alert('Xóa blog thất bại!');
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getImageUrl = (imagePath) => {
  // Xử lý URL hình ảnh từ backend
  if (!imagePath) return '';
  
  // Nếu đã là URL đầy đủ thì return luôn
  if (imagePath.startsWith('http')) return imagePath;
  
  // Xóa /api khỏi URL vì uploads không nằm trong /api
  const baseURL = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:3000';
  return `${baseURL}/uploads/${imagePath}`;
};

onMounted(loadBlog);
</script>