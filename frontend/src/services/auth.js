import axios from '@/services/axios'
import qs from 'qs'

export default {
  register (credentials) {
    return axios.post('/api/auth/register', qs.stringify(credentials))
  },

  login (credentials) {
    return axios.post('/api/auth/login', qs.stringify(credentials))
  }
}
