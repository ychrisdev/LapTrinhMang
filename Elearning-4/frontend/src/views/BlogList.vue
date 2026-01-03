<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="text-2xl font-bold text-blue-600">Blog System</router-link>
        <div class="space-x-4">
          <router-link v-if="authStore.isLoggedIn" to="/blogs/create" class="btn btn-primary">
            Tạo Blog
          </router-link>
          <button v-if="authStore.isLoggedIn" @click="logout" class="btn btn-secondary">
            Logout
          </button>
          <router-link v-else to="/login" class="btn btn-primary">Login</router-link>
        </div>
      </div>
    </nav>
    
    <div class="container mx-auto px-4 py-8">
      <h2 class="text-3xl font-bold mb-6">Danh sách Blogs</h2>
      
      <!-- Search & Sort -->
      <div class="flex gap-2 mb-6">
        <input 
          v-model="search" 
          type="text" 
          placeholder="Tìm kiếm..." 
          class="input flex-1"
          @keyup.enter="loadBlogs"
        >
        <select v-model="sort" @change="loadBlogs" class="input w-40">
          <option value="created_at">Mới nhất</option>
          <option value="title">Tiêu đề</option>
        </select>
        <button @click="loadBlogs" class="btn btn-primary">Tìm</button>
      </div>
      
      <!-- Blog List -->
      <div v-if="blogs.length > 0" class="grid gap-4">
        <div 
          v-for="blog in blogs" 
          :key="blog.id" 
          class="card hover:shadow-lg transition-shadow"
        >
          <div class="flex gap-4">
            <!-- Thumbnail -->
            <div v-if="blog.image" class="flex-shrink-0">
              <img 
                :src="getImageUrl(blog.image)" 
                :alt="blog.title"
                class="w-48 h-32 object-cover rounded-lg"
                @error="handleImageError"
              >
            </div>
            
            <!-- Content -->
            <div class="flex-1">
              <h3 class="font-bold text-xl mb-2">{{ blog.title }}</h3>
              <p class="text-gray-600 mb-2">{{ blog.content.substring(0, 150) }}...</p>
              <div class="flex justify-between items-center text-sm text-gray-500 mb-4">
                <span>By {{ blog.author_name }}</span>
                <span>{{ formatDate(blog.created_at) }}</span>
              </div>
              <div class="flex gap-2">
                <router-link 
                  :to="`/blogs/${blog.id}`" 
                  class="btn btn-primary"
                >
                  Xem chi tiết
                </router-link>
                <template v-if="authStore.user?.id === blog.user_id">
                  <router-link 
                    :to="`/blogs/${blog.id}/edit`" 
                    class="btn btn-secondary"
                  >
                    Sửa
                  </router-link>
                  <button 
                    @click="deleteBlog(blog.id)" 
                    class="btn btn-danger"
                  >
                    Xóa
                  </button>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-8 text-gray-500">
        Không có blog nào
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import axios from '@/api/axios';

const router = useRouter();
const authStore = useAuthStore();

const blogs = ref([]);
const search = ref('');
const sort = ref('created_at');

const loadBlogs = async () => {
  try {
    const { data } = await axios.get('/blogs', {
      params: { search: search.value, sort: sort.value }
    });
    blogs.value = data.data;
  } catch (error) {
    console.error(error);
  }
};

const deleteBlog = async (id) => {
  if (!confirm('Bạn có chắc muốn xóa blog này?')) return;
  
  try {
    await axios.delete(`/blogs/${id}`);
    alert('Xóa thành công!');
    loadBlogs();
  } catch (error) {
    alert('Xóa thất bại!');
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('vi-VN');
};

const getImageUrl = (imagePath) => {
  if (!imagePath) return '';
  if (imagePath.startsWith('http')) return imagePath;
  
  const baseURL = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:3000';
  return `${baseURL}/uploads/${imagePath}`;
};

const handleImageError = (e) => {
  console.error('Lỗi load hình:', e.target.src);
  e.target.style.display = 'none';
};

const logout = () => {
  authStore.logout();
  router.push('/');
};

onMounted(loadBlogs);
</script> 