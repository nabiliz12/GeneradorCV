<script setup lang="ts">
import { reactive, ref } from 'vue'

const text = ref('')

const form=reactive({
  name:'',
  email:'',
  experiencia:''
})

function submitForm() {
  console.log('Form submitted:', form)
}

</script>

<template>
  <form>
    <div>
      <label for="name">Name:</label>
      <input v-model="form.name" placeholder="Introduce tu nombre" />
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
      <button type="submit" @click.prevent="submitForm">Enviar</button>
    </div>
  </form>
</template>

<style scoped>
form div {
  margin-bottom: 8px;
}
</style>
