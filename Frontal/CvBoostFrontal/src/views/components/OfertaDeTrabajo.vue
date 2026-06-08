<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore';

const store=useCvFormStore()

</script>

<template>
     <div v-if="store.pagina === 7">
        <h1>Oferta de trabajo <span class="opcional-badge">Opcional</span></h1>
        <h2>Pega aquí la oferta a la que quieres aplicar para personalizar tu CV</h2>
        <div class="grid">
          <div class="field-wrap">
            <input v-model="store.formulario.ofertaDeTrabajo.empresa" placeholder="Empresa" />
          </div>
          <div class="form-group">
            <label>Descripción de la oferta</label>
            <textarea v-model="store.formulario.ofertaDeTrabajo.descripcion" placeholder="Pega aquí el texto de la oferta de trabajo..." rows="6"></textarea>
          </div>
        </div>
        <div class="nav-buttons">
          <button @click="store.anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="store.siguientePagina" type="button">Siguiente</button>
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
