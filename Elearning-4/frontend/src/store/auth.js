import { defineStore } from 'pinia';
import axios from '../api/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    async register(userData) {
      const { data } = await axios.post('/auth/register', userData);
      return data;
    },
    
    async login(credentials) {
      const { data } = await axios.post('/auth/login', credentials);
      this.token = data.data.token;
      this.user = data.data.user;
      localStorage.setItem('token', data.data.token);
    },
    
    async restoreSession() {
      try {
        const { data } = await axios.get('/auth/profile');
        this.user = data.data;
      } catch (error) {
        this.logout();
      }
    },
    
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
    }
  }
});