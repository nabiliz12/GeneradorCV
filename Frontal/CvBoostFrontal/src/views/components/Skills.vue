<script setup lang="ts">
import { useCvFormStore } from '@/store/cvFormStore';
import { ref } from 'vue';

const store=useCvFormStore()

const nuevaSkill = ref('')

function agregarSkill() {
  const s = nuevaSkill.value.trim()
  if (s && !store.formulario.skills.includes(s)) store.formulario.skills.push(s)
  nuevaSkill.value = ''
}

function agregarSkillConEnter(e: KeyboardEvent) {
  if (e.key === 'Enter') { e.preventDefault(); agregarSkill() }
}


function eliminarSkill(i: number) { store.formulario.skills.splice(i, 1) }

</script>


<template>
<div v-if="store.pagina === 6">
        <h1>Skills <span class="opcional-badge">Opcional</span></h1>
        <h2>Añade tus habilidades técnicas o personales</h2>
        <div v-if="store.formulario.skills.length > 0" class="skills-tags">
          <span v-for="(skill, index) in store.formulario.skills" :key="index" class="skill-tag">
            {{ skill }}
            <button @click="eliminarSkill(index)" type="button" class="skill-tag-remove">✕</button>
          </span>
        </div>
        <div class="skill-input-row">
          <input v-model="nuevaSkill" placeholder="Ej: JavaScript, Trabajo en equipo..." @keydown="agregarSkillConEnter" />
          <button @click="agregarSkill" type="button" class="btn-skill-add">+</button>
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
.skills-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.skill-tag { display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px 5px 12px; background: #f3f4f6; border: 1px solid #e7e7e7; border-radius: 999px; font-size: 13px; color: #111; }
.skill-tag-remove { width: 16px !important; height: 16px; border-radius: 50%; border: none; background: #ddd; color: #666; font-size: 9px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; }
.skill-input-row { display: flex; gap: 8px; align-items: center; }
.skill-input-row input { flex: 1; width: 100%; padding: 10px 12px; border: 1.5px solid #e7e7e7; border-radius: 10px; font-size: 14px; background: #fafafa; outline: none; box-sizing: border-box; }
.skill-input-row input:focus { border-color: #111; background: white; }
.btn-skill-add { flex-shrink: 0; width: 38px !important; height: 38px; border-radius: 10px; border: none; background: #111; color: white; font-size: 20px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; margin-top: 0; }
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
button { border: none; background: #111; color: white; padding: 10px 14px; border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px; transition: 0.2s; width: 100%; }
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }

</style>
