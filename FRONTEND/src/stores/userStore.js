import { defineStore } from 'pinia';
import axios from '../api'; // ya configurado con interceptor
import router from '../router';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isProfesor: (state) => state.user?.role === 'profesor',
    isAlumno: (state) => state.user?.role === 'alumno',
  },

  actions: {
    async login(username, password) {
      const res = await axios.post('/auth/login', { username, password });
      this.token = res.data.access_token;
      this.user = res.data.user;
      localStorage.setItem('token', this.token);
      localStorage.setItem('user', JSON.stringify(this.user));

      if (this.user.role === 'profesor') router.push('/profesor');
      else if (this.user.role === 'alumno') router.push('/alumno');
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/');
    },

    loadUserFromStorage() {
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        this.user = JSON.parse(savedUser);
      }
    },
  },
});
