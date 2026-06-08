<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore';
import { ref } from 'vue';

const store=useCvFormStore()
const fileInput = ref<HTMLInputElement | null>(null) // referencia al input file para subir foto
const fotoPerfil = ref<string | null>(null) // para almacenar la foto de perfil en base64


function subirFoto() {
   fileInput.value?.click()
}

function onFileChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => { fotoPerfil.value = reader.result as string }
  reader.readAsDataURL(file)
  reader.onload = () =>{
  fotoPerfil.value = reader.result as string
  store.formulario.foto_base64 = reader.result as string
  }
}

</script>

<template>
    <div v-if="store.pagina === 8">
        <h1>Foto de perfil</h1>
        <h2>¿Quieres añadir una foto a tu CV?</h2>
        <div class="foto-opciones">
          <button type="button" class="foto-opcion" :class="{ selected: store.ponerFotoParaDialog }" @click="store.ponerFotoParaDialog = true ; store.formulario.foto = true">
            <span class="foto-opcion-label">Sí, añadir foto</span>
          </button>
          <button type="button" class="foto-opcion" :class="{ selected: !store.ponerFotoParaDialog }" @click="store.ponerFotoParaDialog = false; store.formulario.foto = false; store.formulario.foto_base64 = null;">
            <span class="foto-opcion-label">Sin foto</span>
          </button>
        </div>
        <div v-if="store.ponerFotoParaDialog" class="foto-upload-area">
          <button @click="subirFoto" type="button" class="secondary">Subir foto</button>
          <input ref="fileInput" type="file" accept="image/*" style="display: none" @change="onFileChange" />
          <img v-if="fotoPerfil" :src="fotoPerfil" class="avatar" />
        </div>
        <div class="nav-buttons" style="margin-top: 16px;">
          <button @click="store.anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="store.siguientePagina" type="button">Siguiente</button>
        </div>
      </div>


</template>


<style>
h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; display: flex; align-items: center; gap: 8px; }
h2 { font-size: 14px; font-weight: 500; color: #555; margin-bottom: 16px; }
.foto-opciones { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
.foto-opcion { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 16px 10px; border: 2px solid #e7e7e7; border-radius: 14px; background: #fafafa; cursor: pointer; transition: all 0.2s; margin: 0; width: 100%; }
.foto-opcion:hover { border-color: #999; background: white; transform: none; opacity: 1; }
.foto-opcion.selected { border-color: #111; background: white; box-shadow: 0 0 0 3px rgba(0,0,0,0.06); }
.foto-opcion-label { font-size: 13px; font-weight: 600; color: #111; }
.foto-upload-area { display: flex; flex-direction: column; align-items: flex-start; gap: 10px; padding: 14px; border: 1px dashed #ddd; border-radius: 12px; background: #fafafa; }
.avatar { width: 80px; height: 80px; border-radius: 12px; object-fit: cover; border: 1px solid #eee; display: block; }
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
button { border: none; background: #111; color: white; padding: 10px 14px; border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px; transition: 0.2s; width: 100%; }
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }
</style>
