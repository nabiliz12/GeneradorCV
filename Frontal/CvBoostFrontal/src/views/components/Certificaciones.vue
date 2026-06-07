<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore';

const store=useCvFormStore()
const meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
const aniosDisponibles = Array.from({ length: 101 }, (_, i) => String(new Date().getFullYear() - i))// array de los ultimos 100 años para los selects de fechas
function agregarCertificacion() { store.formulario.certificaciones.push({ certificacion: '', mes: '', anio: '' }) }
function eliminarCertificacion(i: number) { store.formulario.certificaciones.splice(i, 1) }
</script>


<template>
        <div v-if="store.pagina === 3">
        <h1>Certificaciones <span class="opcional-badge">Opcional</span></h1>
        <div class="chips-list">
          <div v-for="(cert, index) in store.formulario.certificaciones" :key="index" class="item-chip">
            <div class="chip-fields">
              <input v-model="cert.certificacion" placeholder="Certificación" class="chip-input" />
              <div class="fecha-row">
                <span class="fecha-label">Expedición</span>
                <div class="fecha-selects">
                  <select v-model="cert.mes" class="chip-select-sm"><option value="">Mes</option><option v-for="m in meses" :key="m" :value="m">{{ m }}</option></select>
                  <select v-model="cert.anio" class="chip-select-sm"><option value="">Año</option><option v-for="a in aniosDisponibles" :key="a" :value="a">{{ a }}</option></select>
                </div>
              </div>
            </div>
            <button @click="eliminarCertificacion(index)" type="button" class="chip-remove">✕</button>
          </div>
        </div>
        <button @click="agregarCertificacion" type="button" class="btn-add">+ Agregar certificación</button>
        <div class="nav-buttons">
          <button @click="store.anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="store.siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

</template>


<style>

h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; display: flex; align-items: center; gap: 8px; }
.opcional-badge { font-size: 11px; font-weight: 500; background: #f3f4f6; color: #888; border-radius: 6px; padding: 2px 8px; }
.chips-list { display: flex; flex-direction: column; gap: 8px; }
.item-chip { display: flex; align-items: flex-start; gap: 8px; padding: 10px 12px; border: 1px solid #efefef; border-radius: 12px; background: #fafafa; }
.chip-fields { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.chip-input { width: 100%; padding: 7px 10px; border: 1.5px solid #e7e7e7; border-radius: 8px; font-size: 13px; background: white; outline: none; box-sizing: border-box; }
.chip-input:focus { border-color: #111; }
.fecha-row { display: flex; align-items: center; gap: 8px; }
.fecha-label { font-size: 11.5px; color: #888; font-weight: 500; white-space: nowrap; min-width: 38px; }
.fecha-selects { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.chip-select-sm { padding: 6px 8px; border: 1.5px solid #e7e7e7; border-radius: 8px; font-size: 12px; background: white; outline: none; cursor: pointer; width: auto; }
.chip-select-sm:focus { border-color: #111; }
.chip-remove { flex-shrink: 0; width: 26px !important; height: 26px; border-radius: 50%; border: none; background: #f3f4f6; color: #999; font-size: 11px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; margin-top: 2px; }
.chip-remove:hover { background: #fee2e2; color: #b91c1c; }
.btn-add { background: transparent; color: #777; border: 1.5px dashed #ddd; padding: 8px 14px; border-radius: 10px; font-size: 13px; cursor: pointer; margin-top: 8px; width: 100%; }
.btn-add:hover { border-color: #111; color: #111; background: transparent; }
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
button { border: none; background: #111; color: white; padding: 10px 14px; border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px; transition: 0.2s; width: 100%; }
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }
</style>
