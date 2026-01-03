<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4">
        <router-link :to="`/blogs/${route.params.id}`" class="text-gray-600 hover:text-gray-900">
          ← Quay lại
        </router-link>
      </div>
    </nav>
    
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-4 py-8 text-center">
      <p class="text-gray-500">Đang tải...</p>
    </div>
    
    <!-- Edit Form -->
    <div v-else-if="blog" class="container mx-auto px-4 py-8 max-w-2xl">
      <h2 class="text-3xl font-bold mb-6">Chỉnh sửa Blog</h2>
      
      <form @submit.prevent="handleSubmit" class="card">
        <!-- Title -->
        <div class="mb-4">
          <label class="block mb-2 font-medium text-gray-700">
            Tiêu đề *
          </label>
          <input 
            v-model="form.title" 
            type="text" 
            class="input" 
            placeholder="Nhập tiêu đề blog..."
            required
          >
        </div>
        
        <!-- Content -->
        <div class="mb-4">
          <label class="block mb-2 font-medium text-gray-700">
            Nội dung *
          </label>
          <textarea 
            v-model="form.content" 
            class="input" 
            rows="12" 
            placeholder="Viết nội dung blog của bạn..."
            required
          ></textarea>
          <p class="text-sm text-gray-500 mt-1">
            {{ form.content.length }} ký tự
          </p>
        </div>
        
        <!-- Current Image -->
        <div v-if="blog.image" class="mb-4">
          <label class="block mb-2 font-medium text-gray-700">
            Hình ảnh hiện tại
          </label>
          <div class="relative inline-block">
            <img 
              :src="getImageUrl(blog.image)" 
              alt="Current image"
              class="w-48 h-32 object-cover rounded-lg border"
            >
            <button
              type="button"
              @click="removeCurrentImage"
              class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- New Image Upload -->
        <div class="mb-6">
          <label class="block mb-2 font-medium text-gray-700">
            {{ blog.image ? 'Thay đổi hình ảnh' : 'Thêm hình ảnh' }}
          </label>
          <input 
            type="file" 
            @change="handleFileChange" 
            accept="image/*"
            class="input"
            ref="fileInput"
          >
          <p class="text-sm text-gray-500 mt-1">
            Chấp nhận: JPG, PNG, GIF (tối đa 5MB)
          </p>
          
          <!-- Preview new image -->
          <div v-if="imagePreview" class="mt-3">
            <p class="text-sm text-gray-600 mb-2">Xem trước hình mới:</p>
            <img 
              :src="imagePreview" 
              alt="Preview"
              class="w-48 h-32 object-cover rounded-lg border"
            >
          </div>
        </div>
        
        <!-- Submit Buttons -->
        <div class="flex gap-3">
          <button 
            type="submit" 
            class="btn btn-primary flex-1"
            :disabled="submitting"
          >
            <svg v-if="submitting" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ submitting ? 'Đang lưu...' : 'Cập nhật Blog' }}
          </button>
          <button 
            type="button"
            @click="router.push(`/blogs/${route.params.id}`)"
            class="btn btn-secondary"
          >
            Hủy
          </button>
        </div>
      </form>
    </div>
    
    <!-- Error State -->
    <div v-else class="container mx-auto px-4 py-8 text-center">
      <p class="text-red-500">Không tìm thấy blog hoặc bạn không có quyền chỉnh sửa!</p>
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
const submitting = ref(false);
const imageFile = ref(null);
const imagePreview = ref(null);
const fileInput = ref(null);
const removeImage = ref(false);

const form = ref({
  title: '',
  content: ''
});

const loadBlog = async () => {
  try {
    loading.value = true;
    const { data } = await axios.get(`/blogs/${route.params.id}`);
    
    // Check if user is the owner
    if (data.data.user_id !== authStore.user?.id) {
      blog.value = null;
      return;
    }
    
    blog.value = data.data;
    form.value = {
      title: data.data.title,
      content: data.data.content
    };
  } catch (error) {
    console.error(error);
    blog.value = null;
  } finally {
    loading.value = false;
  }
};

const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('Kích thước file không được vượt quá 5MB!');
      if (fileInput.value) fileInput.value.value = '';
      return;
    }
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Vui lòng chỉ chọn file hình ảnh!');
      if (fileInput.value) fileInput.value.value = '';
      return;
    }
    
    imageFile.value = file;
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    imageFile.value = null;
    imagePreview.value = null;
  }
};

const removeCurrentImage = () => {
  if (confirm('Bạn có chắc muốn xóa hình ảnh hiện tại?')) {
    removeImage.value = true;
    blog.value.image = null;
  }
};

const handleSubmit = async () => {
  try {
    submitting.value = true;
    
    const formData = new FormData();
    formData.append('title', form.value.title);
    formData.append('content', form.value.content);
    
    if (imageFile.value) {
      formData.append('image', imageFile.value);
    }
    
    if (removeImage.value) {
      formData.append('removeImage', 'true');
    }
    
    await axios.put(`/blogs/${route.params.id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    alert('Cập nhật blog thành công!');
    router.push(`/blogs/${route.params.id}`);
  } catch (error) {
    console.error(error);
    alert(error.response?.data?.message || 'Cập nhật blog thất bại!');
  } finally {
    submitting.value = false;
  }
};

const getImageUrl = (imagePath) => {
  if (!imagePath) return '';
  if (imagePath.startsWith('http')) return imagePath;
  
  const baseURL = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:3000';
  return `${baseURL}/uploads/${imagePath}`;
};

onMounted(() => {
  if (!authStore.isLoggedIn) {
    router.push('/login');
  } else {
    loadBlog();
  }
});
</script>