<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore';

const store=useCvFormStore()
const meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
const aniosDisponibles = Array.from({ length: 101 }, (_, i) => String(new Date().getFullYear() - i))// array de los ultimos 100 años para los selects de fechas
function agregarEducacion() { store.formulario.educacion.push({ titulo: '', institucion: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false }) }
function eliminarEducacion(i: number) { store.formulario.educacion.splice(i, 1) }


</script>

<template>
      <div v-if="store.pagina === 2">
        <h1>Educación <span class="opcional-badge">Opcional</span></h1>
        <div class="chips-list">
          <div v-for="(edu, index) in store.formulario.educacion" :key="index" class="item-chip">
            <div class="chip-fields">
              <input v-model="edu.titulo" placeholder="Título obtenido" class="chip-input" />
              <input v-model="edu.institucion" placeholder="Institución" class="chip-input" />
              <div class="fecha-row">
                <span class="fecha-label">Inicio</span>
                <div class="fecha-selects">
                  <select v-model="edu.mesInicio" class="chip-select-sm"><option value="">Mes</option><option v-for="m in meses" :key="m" :value="m">{{ m }}</option></select>
                  <select v-model="edu.anioInicio" class="chip-select-sm"><option value="">Año</option><option v-for="a in aniosDisponibles" :key="a" :value="a">{{ a }}</option></select>
                </div>
              </div>
              <div class="fecha-row">
                <span class="fecha-label">Fin</span>
                <div class="fecha-selects">
                  <template v-if="!edu.actualidad">
                    <select v-model="edu.mesFin" class="chip-select-sm" :disabled="edu.actualidad"><option value="">Mes</option><option v-for="m in meses" :key="m" :value="m">{{ m }}</option></select>
                    <select v-model="edu.anioFin" class="chip-select-sm" :disabled="edu.actualidad"><option value="">Año</option><option v-for="a in aniosDisponibles" :key="a" :value="a">{{ a }}</option></select>
                  </template>
                  <label class="actualidad-check">
                    <input type="checkbox" v-model="edu.actualidad" @change="if(edu.actualidad){ edu.mesFin=''; edu.anioFin='' }" />
                    <span>Actualidad</span>
                  </label>
                </div>
              </div>
            </div>
            <button v-if="store.formulario.educacion.length > 1" @click=eliminarEducacion(index) type="button" class="chip-remove">✕</button>
          </div>
        </div>
        <button @click="agregarEducacion" type="button" class="btn-add">+ Agregar educación</button>
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
.chip-select-sm:disabled { background: #f3f4f6; color: #bbb; }
.actualidad-check { display: flex; align-items: center; gap: 5px; font-size: 12px; color: #555; cursor: pointer; white-space: nowrap; }
.actualidad-check input[type="checkbox"] { width: 14px; height: 14px; padding: 0; accent-color: #111; }
.chip-remove { flex-shrink: 0; width: 26px !important; height: 26px; border-radius: 50%; border: none; background: #f3f4f6; color: #999; font-size: 11px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; margin-top: 2px; }
.chip-remove:hover { background: #fee2e2; color: #b91c1c; }
.btn-add { background: transparent; color: #777; border: 1.5px dashed #ddd; padding: 8px 14px; border-radius: 10px; font-size: 13px; cursor: pointer; margin-top: 8px; width: 100%; }
.btn-add:hover { border-color: #111; color: #111; background: transparent; }
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
</style>
