<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore';

const store=useCvFormStore()

function agregarIdioma() { store.formulario.idiomas.push({ idioma: '', nivel: '' }) }
function eliminarIdioma(i: number) { store.formulario.idiomas.splice(i, 1) }
</script>

<template>
     <div v-if="store.pagina === 5">
        <h1>Idiomas <span class="opcional-badge">Opcional</span></h1>
        <div class="chips-list">
          <div v-for="(idioma, index) in store.formulario.idiomas" :key="index" class="item-chip item-chip--row">
            <div class="field-wrap" style="flex:1">
              <input v-model="idioma.idioma" placeholder="Idioma" class="chip-input" />
            </div>
            <div class="field-wrap" style="flex:0 0 130px">
              <select v-model="idioma.nivel" class="chip-select">
                <option disabled value="">Nivel</option>
                <option>Básico</option><option>Intermedio</option><option>Avanzado</option><option>Nativo</option>
              </select>
            </div>
            <button @click="eliminarIdioma(index)" type="button" class="chip-remove">✕</button>
          </div>
        </div>
        <button @click="agregarIdioma" type="button" class="btn-add">+ Agregar idioma</button>
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
.item-chip--row { flex-direction: row; align-items: center; }
.field-wrap { display: flex; flex-direction: column; gap: 3px; }
.chip-input { width: 100%; padding: 7px 10px; border: 1.5px solid #e7e7e7; border-radius: 8px; font-size: 13px; background: white; outline: none; box-sizing: border-box; }
.chip-input:focus { border-color: #111; }
.chip-select { width: 100%; padding: 7px 8px; border: 1.5px solid #e7e7e7; border-radius: 8px; font-size: 13px; background: white; outline: none; box-sizing: border-box; }
.chip-remove { flex-shrink: 0; width: 26px !important; height: 26px; border-radius: 50%; border: none; background: #f3f4f6; color: #999; font-size: 11px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; }
.chip-remove:hover { background: #fee2e2; color: #b91c1c; }
.btn-add { background: transparent; color: #777; border: 1.5px dashed #ddd; padding: 8px 14px; border-radius: 10px; font-size: 13px; cursor: pointer; margin-top: 8px; width: 100%; }
.btn-add:hover { border-color: #111; color: #111; background: transparent; }
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
button { border: none; background: #111; color: white; padding: 10px 14px; border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px; transition: 0.2s; width: 100%; }
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }
</style>
