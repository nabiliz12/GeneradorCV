import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyForm from '@/views/MyForm.vue'
import Login from '@/views/auth/Login.vue'
import Registro from '@/views/auth/Registro.vue'
import HistorialFormularios from '@/views/HistorialFormularios.vue'
import VistaPreviaForm from '@/views/VistaPreviaForm.vue'

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
      path: '/forms/vista-previa',
      name: 'vistaprevia',
      component: VistaPreviaForm
    }
  ],
})

export default router
