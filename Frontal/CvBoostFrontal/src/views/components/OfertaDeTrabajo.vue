<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore'
import { useLangStore } from '@/store/langStore'

const store = useCvFormStore()
const langStore = useLangStore()
</script>

<template>
  <div v-if="store.pagina === 7">
    <h1>{{ langStore.t.offer_title }} <span class="opcional-badge">{{ langStore.t.edu_optional }}</span></h1>
    <h2>{{ langStore.t.offer_sub }}</h2>
    <div class="grid">
      <div class="field-wrap">
        <input v-model="store.formulario.ofertaDeTrabajo.empresa" :placeholder="langStore.t.offer_company" />
      </div>
      <div class="form-group">
        <label>{{ langStore.t.offer_desc_label }}</label>
        <textarea v-model="store.formulario.ofertaDeTrabajo.descripcion" :placeholder="langStore.t.offer_desc_placeholder" rows="6"></textarea>
      </div>
    </div>
    <div class="nav-buttons">
      <button @click="store.anteriorPagina" type="button" class="secondary">{{ langStore.t.offer_back }}</button>
      <button @click="store.siguientePagina" type="button">{{ langStore.t.offer_next }}</button>
    </div>
  </div>
</template>

<style>
h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; display: flex; align-items: center; gap: 8px; }
h2 { font-size: 14px; font-weight: 500; color: #555; margin-bottom: 16px; }
.opcional-badge { font-size: 11px; font-weight: 500; background: #f3f4f6; color: #888; border-radius: 6px; padding: 2px 8px; }
.grid { display: flex; flex-direction: column; gap: 12px; }
.field-wrap { display: flex; flex-direction: column; gap: 3px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
label { font-size: 12px; color: #666; }
input, textarea { width: 100%; padding: 10px 12px; border: 1.5px solid #e7e7e7; border-radius: 10px; font-size: 14px; background: #fafafa; transition: border-color 0.2s, background 0.2s; outline: none; font-family: inherit; box-sizing: border-box; }
textarea { resize: vertical; min-height: 100px; }
input:focus, textarea:focus { border-color: #111; background: white; }
input::placeholder, textarea::placeholder { color: #aaa; }
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
button { border: none; background: #111; color: white; padding: 10px 14px; border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px; transition: 0.2s; width: 100%; }
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }
</style>
