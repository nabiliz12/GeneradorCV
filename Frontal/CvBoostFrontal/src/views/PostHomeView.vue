<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

function irAlFormulario() {
  console.log('Redirigiendo al formulario...');
  router.push('/forms');
}

</script>

<template>


  <div>
  <button @click="irAlFormulario">Comenzar Gratis</button>
  </div>
</template>
