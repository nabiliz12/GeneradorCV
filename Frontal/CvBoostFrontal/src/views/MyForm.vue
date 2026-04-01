<script setup lang="ts">
import router from '@/router'
import { reactive } from 'vue'
import PostFormulario from './DescargarFormulario.vue'

const form=reactive({
  nombre:'',
  email:'',
  experiencia:''
})
// ideas: https://www.cvmaker.es/
async function submitForm() {
  console.log('Form submitted:', form)

  const response = await fetch('http://127.0.0.1:8001/api/form', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(form)
  })

  if (response.ok) {
    console.log('Form data successfully sent to the backend')
  } else {
    console.error('Failed to send form data to the backend')
  }

  router.push('/forms/descargarpdf')


}

function login() {
  router.push('/login')
}

function registrarse() {
  router.push('/register')
}
</script>

<template>

  <div>
    <button @click="login">Iniciar sesión</button>
    <button @click="registrarse">Registrarse</button>
  </div>


  <div>

  <form @submit.prevent="submitForm">
    <div>
      <label for="nombre">Name:</label>
      <input v-model="form.nombre" placeholder="Introduce tu nombre" />
    </div>

    <div>
      <label for="email">Email:</label>
      <input v-model="form.email" placeholder="Introduce tu email" />
    </div>

    <div>
      <label for="experiencia">Experiencia:</label>
      <textarea v-model="form.experiencia" placeholder="Describe tu experiencia"></textarea>
    </div>

    <div>

      <button type="submit">Enviar</button>
    </div>

  </form>


    </div>

</template>

<style scoped>
form div {
  margin-bottom: 8px;
}
</style>
