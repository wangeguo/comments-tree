import axios from 'axios'

// axios.interceptors.response.use(
//   res => {
//     if (!res.data.success) {
//       return Promise.reject(res.data.message)
//     }
//
//     return res.data
//   },
//   error => {
//     return Promise.reject(error)
//   })

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
export default axios
