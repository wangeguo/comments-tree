import axios from '@/services/axios'
import qs from 'qs'

export default {
  index () {
    return axios.get('/api/posts/')
  },

  get (id) {
    return axios.get(`/api/posts/${id}`)
  },

  create (post) {
    return axios.post('/api/posts/', qs.stringify(post))
  },

  update (post) {
    return axios.post(`/api/posts/${post.id}`, qs.stringify(post))
  },

  delete (id) {
    return axios.delete(`/api/posts/${id}`)
  },

  reply (parentId, post) {
    return axios.post(`/api/posts/${parentId}/replies/`, qs.stringify(post))
  }
}
