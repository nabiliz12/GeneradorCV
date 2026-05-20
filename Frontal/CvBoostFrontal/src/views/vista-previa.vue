<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

onMounted(async () => {
  const id_cv = String(route.params.id_cv)
  const token = localStorage.getItem('token')

  const rutas: Record<string, string> = {
    europass:    `/forms/plantilla-europass/${id_cv}`,
    minimalista: `/forms/plantilla-minimalista/${id_cv}`,
    moderna:     `/forms/plantilla-moderna/${id_cv}`,
    'europass-sin-foto':    `/forms/plantilla-europass-sin-foto/${id_cv}`,
    'minimalista-sin-foto': `/forms/plantilla-minimalista-sin-foto/${id_cv}`,
  }

  try {
    const res = await fetch(`http://127.0.0.1:8001/api/recuperar_cv/${id_cv}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (!res.ok) { router.push('/forms/history'); return }

    const data = await res.json()
    const plantilla = data.plantilla

    if (!plantilla || !(plantilla in rutas)) { router.push('/forms/history'); return }

  router.replace(rutas[plantilla as string] as string)
  } catch {
    router.push('/forms/history')
  }
})
</script>

<template>
  <div style="display:flex;align-items:center;justify-content:center;min-height:100vh">
    <div class="spinner"></div>
  </div>
</template>

<style scoped>
.spinner {
  width: 28px; height: 28px;
  border-radius: 50%;
  border: 3px solid #f0f0f0;
  border-top-color: #111;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
