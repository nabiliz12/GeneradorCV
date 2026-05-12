import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyForm from '@/views/MyForm.vue'
import Login from '@/views/auth/Login.vue'
import Registro from '@/views/auth/Registro.vue'
import HistorialFormularios from '@/views/HistorialFormularios.vue'
import Ajustes from '@/views/conSesion/Ajustes.vue'
import PlantillaEuropass from '@/views/plantillas/PlantillaEuropass.vue'
import PlantillaMinimalista from '@/views/plantillas/PlantillaMinimalista.vue'
import PlantillaModerna from '@/views/plantillas/PlantillaModerna.vue'

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
      path: '/forms/plantilla-europass/:id_cv',
      name: 'plantillaEuropass',
      component: PlantillaEuropass
    },
    {
      path: '/forms/plantilla-minimalista/:id_cv',
      name: 'plantillaMinimalista',
      component: PlantillaMinimalista
    },
    {
    path: '/forms/plantilla-moderna/:id_cv',
    name: 'plantillaModerna',
    component: PlantillaModerna
  }  ],
})

export default router
