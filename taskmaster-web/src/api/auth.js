import request from '../utils/request'

export default {
  login(credentials) {
    return request.post('/auth/login', credentials)
  },
  
  register(userData) {
    return request.post('/auth/register', userData)
  }
}