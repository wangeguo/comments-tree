import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/pages/post/PostList')
    },

    // Auth
    {
      path: '/auth/register',
      name: 'Register',
      component: () => import('@/pages/auth/Register')
    },
    {
      path: '/auth/login',
      name: 'Login',
      component: () => import('@/pages/auth/Login')
    },

    // Post
    {
      path: '/create',
      name: 'CreatePost',
      component: () => import('@/pages/post/CreatePost')
    },
    {
      path: '/update/:id',
      name: 'UpdatePost',
      component: () => import('@/pages/post/UpdatePost')
    },
    {
      path: '/reply/:id',
      name: 'ReplyPost',
      component: () => import('@/pages/post/ReplyPost')
    }
  ]
})
