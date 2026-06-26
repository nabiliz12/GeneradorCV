<script setup lang="ts">
import { computed } from 'vue'
import { useCvFormStore } from '@/store/cvFormStore'
import { useLangStore } from '@/store/langStore'

const store = useCvFormStore()
const langStore = useLangStore()

const meses = computed(() => langStore.t.months)
const aniosDisponibles = Array.from({ length: 101 }, (_, i) => String(new Date().getFullYear() - i))

function agregarExperiencia() {
  store.formulario.experiencia.push({ cargo: '', empresa: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false })
}
function eliminarExperiencia(i: number) { store.formulario.experiencia.splice(i, 1) }
</script>

<template>
  <div v-if="store.pagina === 4">
    <h1>{{ langStore.t.exp_title }} <span class="opcional-badge">{{ langStore.t.edu_optional }}</span></h1>
    <div class="chips-list">
      <div v-for="(exp, index) in store.formulario.experiencia" :key="index" class="item-chip">
        <div class="chip-fields">
          <input v-model="exp.cargo" :placeholder="langStore.t.exp_role" class="chip-input" />
          <input v-model="exp.empresa" :placeholder="langStore.t.exp_company" class="chip-input" />
          <div class="fecha-row">
            <span class="fecha-label">{{ langStore.t.exp_start }}</span>
            <div class="fecha-selects">
              <select v-model="exp.mesInicio" class="chip-select-sm">
                <option value="">{{ langStore.t.edu_month }}</option>
                <option v-for="m in meses" :key="m" :value="m">{{ m }}</option>
              </select>
              <select v-model="exp.anioInicio" class="chip-select-sm">
                <option value="">{{ langStore.t.edu_year }}</option>
                <option v-for="a in aniosDisponibles" :key="a" :value="a">{{ a }}</option>
              </select>
            </div>
          </div>
          <div class="fecha-row">
            <span class="fecha-label">{{ langStore.t.exp_end }}</span>
            <div class="fecha-selects">
              <template v-if="!exp.actualidad">
                <select v-model="exp.mesFin" class="chip-select-sm">
                  <option value="">{{ langStore.t.edu_month }}</option>
                  <option v-for="m in meses" :key="m" :value="m">{{ m }}</option>
                </select>
                <select v-model="exp.anioFin" class="chip-select-sm">
                  <option value="">{{ langStore.t.edu_year }}</option>
                  <option v-for="a in aniosDisponibles" :key="a" :value="a">{{ a }}</option>
                </select>
              </template>
              <label class="actualidad-check">
                <input type="checkbox" v-model="exp.actualidad" @change="if(exp.actualidad){ exp.mesFin=''; exp.anioFin='' }" />
                <span>{{ langStore.t.exp_current }}</span>
              </label>
            </div>
          </div>
        </div>
        <button v-if="store.formulario.experiencia.length > 1" @click="eliminarExperiencia(index)" type="button" class="chip-remove">✕</button>
      </div>
    </div>
    <button @click="agregarExperiencia" type="button" class="btn-add">{{ langStore.t.exp_add }}</button>
    <div class="nav-buttons">
      <button @click="store.anteriorPagina" type="button" class="secondary">{{ langStore.t.exp_back }}</button>
      <button @click="store.siguientePagina" type="button">{{ langStore.t.exp_next }}</button>
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
button { border: none; background: #111; color: white; padding: 10px 14px; border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px; transition: 0.2s; width: 100%; }
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }
</style>
