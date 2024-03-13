import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Admin from '../views/Admin.vue'
import Manager from '../views/Manager.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/admin',
      name: 'admin',
      component:Admin
    },
    ,
    {
      path: '/manager',
      name: 'manager',
      component:Manager
    }
  ]
})

export default router
