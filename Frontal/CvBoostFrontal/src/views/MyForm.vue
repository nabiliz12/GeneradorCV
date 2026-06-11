<script setup lang="ts">
import DatosPersonales from './components/DatosPersonales.vue'
import Educacion from './components/Educacion.vue'
import { useCvFormStore } from '@/store/cvFormStore.ts'
import Certificaciones from './components/Certificaciones.vue'
import Experiencia from './components/Experiencia.vue'
import Idiomas from './components/Idiomas.vue'
import Skills from './components/Skills.vue'
import OfertaDeTrabajo from './components/OfertaDeTrabajo.vue'
import FotoDePerfil from './components/FotoDePerfil.vue'
import ElegirPlantilla from './components/ElegirPlantilla.vue'
import { onUnmounted } from 'vue'

const store=useCvFormStore()
onUnmounted(() => store.resetear())

</script>

<template>
  <div class="page">
    <div class="card">


      <!-- BARRA DE PROGRESO -->
      <div class="progress-wrap">
        <div class="progress-header">
          <span class="progress-step">Paso {{ store.pagina }} de {{ store.totalPaginas }}</span>
          <span class="progress-pct">{{ store.progreso }}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: store.progreso + '%' }"></div>
        </div>
      </div>

      <!-- PAGE 1: Datos personales -->
      <DatosPersonales></DatosPersonales>


      <!-- PAGE 2: Educación -->
      <Educacion></Educacion>


      <!-- PAGE 3: Certificaciones -->
      <Certificaciones></Certificaciones>

      <!-- PAGE 4: Experiencia -->
      <Experiencia></Experiencia>

      <!-- PAGE 5: Idiomas -->
      <Idiomas></Idiomas>


      <!-- PAGE 6: Skills -->
      <Skills></Skills>

      <!-- PAGE 7: Oferta de trabajo -->
      <OfertaDeTrabajo></OfertaDeTrabajo>

      <!-- PAGE 8: Foto de perfil -->
     <FotoDePerfil></FotoDePerfil>

      <!-- PAGE 9: Elegir plantilla -->
     <ElegirPlantilla></ElegirPlantilla>

    </div>
  </div>
</template>

<style scoped>
:deep(.grid) { display: flex; flex-direction: column; gap: 12px; }
:deep(.field-wrap) { display: flex; flex-direction: column; gap: 3px; }
:deep(.row-2) { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

.page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(180deg, #f7f7f8, #ffffff);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto;
  padding: 40px 16px;
}
.card {
  width: 100%; max-width: 480px; background: white;
  padding: 28px; border-radius: 16px; border: 1px solid #eee;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.progress-wrap { margin-bottom: 24px; }
.progress-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.progress-step { font-size: 12px; color: #999; font-weight: 500; }
.progress-pct { font-size: 12px; color: #111; font-weight: 600; }
.progress-track { width: 100%; height: 4px; background: #f0f0f0; border-radius: 999px; overflow: hidden; }
.progress-fill { height: 100%; background: #111; border-radius: 999px; transition: width 0.35s ease; }
.card > div { animation: fadeIn 0.25s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
</style>
