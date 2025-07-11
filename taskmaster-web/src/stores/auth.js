import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)
  
  const isAuthenticated = computed(() => !!token.value)
  
  const login = async (credentials) => {
    try {
      const response = await api.login(credentials)
      token.value = response.data.token
      user.value = { id: response.data.userId, email: credentials.email }
      localStorage.setItem('token', token.value)
      return response.data
    } catch (error) {
      throw error
    }
  }
  
  const register = async (userData) => {
    try {
      const response = await api.register(userData)
      return response.data
    } catch (error) {
      throw error
    }
  }
  
  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }
  
  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout
  }
})