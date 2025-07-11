import request from '../utils/request'

export default {
  getTasks() {
    return request.get('/tasks')
  },
  
  getTask(id) {
    return request.get(`/tasks/${id}`)
  },
  
  createTask(taskData) {
    return request.post('/tasks', taskData)
  },
  
  updateTask(id, taskData) {
    return request.put(`/tasks/${id}`, taskData)
  },
  
  deleteTask(id) {
    return request.delete(`/tasks/${id}`)
  }
}