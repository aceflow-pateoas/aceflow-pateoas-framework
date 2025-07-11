import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/tasks'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  const fetchTasks = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getTasks()
      // 后端返回的是 { tasks: [...], pagination: {...} }
      tasks.value = response.data.tasks || response.data
    } catch (err) {
      error.value = err.response?.data?.error || '获取任务失败'
    } finally {
      loading.value = false
    }
  }
  
  const createTask = async (taskData) => {
    console.log('Store createTask called with:', taskData)
    try {
      const response = await api.createTask(taskData)
      console.log('API response:', response.data)
      // 后端返回的是 { message: "...", task: {...} }
      const newTask = response.data.task || response.data
      tasks.value.push(newTask)
      console.log('Task added to store:', newTask)
      return newTask
    } catch (err) {
      console.error('Store createTask error:', err)
      console.error('Error response:', err.response?.data)
      throw err
    }
  }
  
  const updateTask = async (id, taskData) => {
    try {
      const response = await api.updateTask(id, taskData)
      // 后端返回的是 { message: "...", task: {...} }
      const updatedTask = response.data.task || response.data
      const index = tasks.value.findIndex(task => task.id === id)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }
      return updatedTask
    } catch (err) {
      throw err
    }
  }
  
  const deleteTask = async (id) => {
    try {
      await api.deleteTask(id)
      tasks.value = tasks.value.filter(task => task.id !== id)
    } catch (err) {
      throw err
    }
  }
  
  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask
  }
})