import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyForm from '@/views/MyForm.vue'
import DescargarFormulario from '@/views/DescargarFormulario.vue'
import Login from '@/views/auth/Login.vue'
import Registro from '@/views/auth/Registro.vue'
import HistorialFormularios from '@/views/HistorialFormularios.vue'

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
      path:'/forms/history',
      name:'history',
      component:HistorialFormularios
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
      component: DescargarFormulario
    }
  ],
})

export default router
