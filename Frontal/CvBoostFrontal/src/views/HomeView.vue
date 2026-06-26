<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useLangStore } from '@/store/langStore'

const router = useRouter()
const langStore = useLangStore()

function irAlFormulario() {
  if (!localStorage.getItem('token')) {
    router.push('/login')
  } else {
    router.push('/forms')
  }
}
</script>

<template>
  <section class="hero">
    <h1>
      {{ langStore.t.hero_title_1 }} <span>{{ langStore.t.hero_title_2 }}</span> {{ langStore.t.hero_title_3 }}
    </h1>
    <p>{{ langStore.t.hero_sub }}</p>
    <button class="btn-modern" @click="irAlFormulario">
      {{ langStore.t.hero_btn }}
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
  background: #ffffff;
}

.hero h1 {
  font-size: 46px !important;
  font-weight: 800 !important;
  color: #111 !important;
  max-width: 800px;
  line-height: 1.1 !important;
  display: block !important;
  margin-bottom: 0 !important;
}

.hero h1 span {
  background: linear-gradient(90deg, #000, #666);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero p {
  font-size: 17px;
  color: #666;
  margin-top: 16px;
  max-width: 600px;
}

.btn-modern {
  width: auto !important;
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

@media (max-width: 640px) {
  .hero { padding: 60px 20px; }
  .hero h1 { font-size: 32px !important; }
  .hero p { font-size: 15px; }
}
</style>
