import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyForm from '@/views/MyForm.vue'
import Login from '@/views/auth/Login.vue'
import Registro from '@/views/auth/Registro.vue'
import HistorialFormularios from '@/views/HistorialFormularios.vue'
import VistaPreviaForm from '@/views/VistaPreviaForm.vue'
import Ajustes from '@/views/conSesion/ajustes.vue'

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
          path: '/login/ajustes',
          name: 'ajustes',
          component: Ajustes,
        },
    {
      path: '/registro',
      name: 'registro',
      component: Registro,
    },
    {
      path: '/forms/vista-previa/:id_cv',
      name: 'vistaprevia',
      component: VistaPreviaForm
    },
  ],
})

export default router
