import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyForm from '@/views/MyForm.vue'
import PostFormulario from '@/views/PostFormulario.vue'
import Login from '@/views/auth/Login.vue'
import Registro from '@/views/auth/Registro.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'homeview',
      component: HomeView,
    },
    {
      path: '/forms',
      name: 'forms',
      component:MyForm
    },
     {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/register',
      name: 'register',
      component: Registro,
    },
    {
      path: '/forms/descargarpdf',
      name: 'descargarpdf',
      component: PostFormulario
    }
  ],
})

export default router
