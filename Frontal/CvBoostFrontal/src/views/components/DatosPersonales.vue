<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore'
import { useLangStore } from '@/store/langStore'

const store = useCvFormStore()
const langStore = useLangStore()

function estadoCampo(val: string): 'idle' | 'error' {
  if (!store.intentoAvanzar) return 'idle'
  return val.trim() ? 'idle' : 'error'
}

function claseCampo(estado: 'idle' | 'error') {
  if (estado === 'error') return 'field-error'
  return ''
}
</script>

<template>
  <div v-if="store.pagina === 1">
    <h1>{{ langStore.t.pd_title }}</h1>
    <div class="grid">
      <div class="row-2">
        <div class="field-wrap">
          <input v-model="store.formulario.datosPersonales.nombre" :placeholder="langStore.t.pd_name" :class="claseCampo(estadoCampo(store.formulario.datosPersonales.nombre))" />
          <span v-if="estadoCampo(store.formulario.datosPersonales.nombre) === 'error'" class="hint hint--error">{{ langStore.t.pd_required }}</span>
        </div>
        <div class="field-wrap">
          <input v-model="store.formulario.datosPersonales.apellido" :placeholder="langStore.t.pd_last" :class="claseCampo(estadoCampo(store.formulario.datosPersonales.apellido))" />
          <span v-if="estadoCampo(store.formulario.datosPersonales.apellido) === 'error'" class="hint hint--error">{{ langStore.t.pd_required }}</span>
        </div>
      </div>
      <div class="field-wrap">
        <input v-model="store.formulario.datosPersonales.email" :placeholder="langStore.t.pd_email" :class="claseCampo(estadoCampo(store.formulario.datosPersonales.email))"/>
        <span v-if="estadoCampo(store.formulario.datosPersonales.email) === 'error'" class="hint hint--error">{{ langStore.t.pd_required }}</span>
      </div>
      <div class="field-wrap">
        <input v-model="store.formulario.datosPersonales.telefono" :placeholder="langStore.t.pd_phone" :class="claseCampo(estadoCampo(store.formulario.datosPersonales.telefono))" />
        <span v-if="estadoCampo(store.formulario.datosPersonales.telefono) === 'error'" class="hint hint--error">{{ langStore.t.pd_required }}</span>
      </div>
      <div class="field-wrap">
        <input v-model="store.formulario.datosPersonales.direccion" :placeholder="langStore.t.pd_address" :class="claseCampo(estadoCampo(store.formulario.datosPersonales.direccion))" />
        <span v-if="estadoCampo(store.formulario.datosPersonales.direccion) === 'error'" class="hint hint--error">{{ langStore.t.pd_required }}</span>
      </div>
      <div class="row-2">
        <div class="field-wrap">
          <input v-model="store.formulario.datosPersonales.codigoPostal" :placeholder="langStore.t.pd_postal" :class="claseCampo(estadoCampo(store.formulario.datosPersonales.codigoPostal))" />
          <span v-if="estadoCampo(store.formulario.datosPersonales.codigoPostal) === 'error'" class="hint hint--error">{{ langStore.t.pd_required }}</span>
        </div>
        <div class="field-wrap">
          <input v-model="store.formulario.datosPersonales.localidad" :placeholder="langStore.t.pd_city" :class="claseCampo(estadoCampo(store.formulario.datosPersonales.localidad))" />
          <span v-if="estadoCampo(store.formulario.datosPersonales.localidad) === 'error'" class="hint hint--error">{{ langStore.t.pd_required }}</span>
        </div>
      </div>
      <div class="toggle-row">
        <div class="toggle-info">
          <div>
            <span class="toggle-label">{{ langStore.t.pd_license }}</span>
            <span class="toggle-sub">{{ langStore.t.pd_license_sub }}</span>
          </div>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" v-model="store.formulario.datosPersonales.permisoConducir" />
          <span class="toggle-track"><span class="toggle-thumb"></span></span>
        </label>
      </div>
    </div>
    <button @click="store.siguientePagina" type="button">{{ langStore.t.pd_next }}</button>
  </div>
</template>

<style>
h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; }
.grid { display: flex; flex-direction: column; gap: 12px; }
.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.field-wrap { display: flex; flex-direction: column; gap: 3px; }
.hint { font-size: 11.5px; font-weight: 500; padding-left: 2px; animation: hintIn 0.15s ease; }
.hint--error { color: #d97706; }
@keyframes hintIn { from { opacity: 0; transform: translateY(-2px); } to { opacity: 1; transform: translateY(0); } }

input {
  width: 100%; padding: 10px 12px; border: 1.5px solid #e7e7e7;
  border-radius: 10px; font-size: 14px; background: #fafafa;
  transition: border-color 0.2s, background 0.2s; outline: none;
  font-family: inherit; box-sizing: border-box;
}
input:focus { border-color: #111; background: white; }
input::placeholder { color: #aaa; }
.field-error { border-color: #f59e0b !important; background: #fffbeb !important; }
.field-ok { border-color: #4ade80 !important; background: #f0fdf4 !important; }

.toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border: 1px solid #e7e7e7; border-radius: 12px; background: #fafafa; }
.toggle-label { display: block; font-size: 14px; font-weight: 500; color: #111; }
.toggle-sub { display: block; font-size: 11px; color: #999; margin-top: 1px; }
.toggle-switch { position: relative; display: inline-flex; cursor: pointer; }
.toggle-switch input { position: absolute; opacity: 0; width: 0; height: 0; }
.toggle-track { width: 42px; height: 24px; background: #e0e0e0; border-radius: 999px; position: relative; transition: background 0.25s; display: block; }
.toggle-thumb { position: absolute; top: 3px; left: 3px; width: 18px; height: 18px; border-radius: 50%; background: white; box-shadow: 0 1px 4px rgba(0,0,0,0.2); transition: transform 0.25s; }
.toggle-switch input:checked + .toggle-track { background: #111; }
.toggle-switch input:checked + .toggle-track .toggle-thumb { transform: translateX(18px); }

button {
  border: none; background: #111; color: white; padding: 10px 14px;
  border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px;
  transition: 0.2s; width: 100%;
}
button:hover { transform: translateY(-1px); opacity: 0.9; }
</style>
