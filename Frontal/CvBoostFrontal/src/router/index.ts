import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyForm from '@/views/MyForm.vue'
import PostFormulario from '@/views/PostFormulario.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/forms',
      name: 'forms',
      component:MyForm
    },
    {
      path: '/forms/descargarpdf',
      name: 'descargarpdf',
      component: PostFormulario
    }
  ],
})

export default router
