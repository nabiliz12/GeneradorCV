<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function irAlFormulario() {
  router.push('/login')
}
</script>

<template>
  <section class="hero">

    <h1>
      Convierte cualquier <span>oferta de trabajo</span> en tu CV perfecto
    </h1>

    <p>
      Pega una oferta de empleo y nuestra IA crea un CV optimizado para esa posición.
    </p>

    <button class="btn-modern" @click="irAlFormulario">
      Comenzar gratis
    </button>



  </section>
</template>

<style scoped>
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 110px 20px;
  background: #ffffff; /* 🔥 importante */
}

h1 {
  font-size: 46px;
  font-weight: 800;
  color: #111;
  max-width: 800px;
  line-height: 1.1;
}

h1 span {
  background: linear-gradient(90deg, #000, #666);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

p {
  font-size: 17px;
  color: #666;
  margin-top: 16px;
  max-width: 600px;
}

.btn-modern {
  margin-top: 30px;
  background: #111;
  color: white;
  border: none;
  padding: 14px 22px;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
}

.btn-modern:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  transition: 0.2s;
}

.mini-text {
  margin-top: 14px;
  font-size: 13px;
  color: #888;
}
</style>
