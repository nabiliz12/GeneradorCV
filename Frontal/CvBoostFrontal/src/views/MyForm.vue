<script setup lang="ts">
import router from '@/router'
import { reactive, ref } from 'vue'

const pagina = ref(1)
const ponerFoto = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const fotoPerfil = ref<string | null>(null)
const nuevaSkill = ref('')

const form = reactive({
  datosPersonales: {
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    direccion: '',
    codigoPostal: '',
    localidad: '',
    permisoConducir: false
  },
  educacion: [{
    institucion: '',
    titulo: '',
    anioInicio: '',
    anioFin: ''
  }],
  certificaciones: [{ certificacion: '', expedicion: '' }],
  experiencia: [{ empresa: '', cargo: '', anioInicio: '', anioFin: '' }],
  idiomas: [{ idioma: '', nivel: '' }],
  skills: [] as string[],
  foto: false,
  ofertaDeTrabajo: {
    empresa: '',
    descripcion: ''
  }
})

async function enviarFormAlBack() {
  console.log('Form submitted:', form)
  const response = await fetch('http://127.0.0.1:8001/api/formulario', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form),
  })
  if (response.ok) {
    console.log('Form data successfully sent to the backend')
    router.push('/forms/vista-previa')
  } else {
    console.error('Failed to send form data to the backend')
  }
}

function siguientePagina() { pagina.value++ }
function anteriorPagina() { pagina.value-- }

function agregarEducacion() {
  form.educacion.push({ institucion: '', titulo: '', anioInicio: '', anioFin: '' })
}
function eliminarEducacion(index: number) { form.educacion.splice(index, 1) }

function agregarIdioma() { form.idiomas.push({ idioma: '', nivel: '' }) }
function eliminarIdioma(index: number) { form.idiomas.splice(index, 1) }

function agregarCertificacion() { form.certificaciones.push({ certificacion: '', expedicion: '' }) }
function eliminarCertificacion(index: number) { form.certificaciones.splice(index, 1) }

function agregarExperiencia() { form.experiencia.push({ empresa: '', cargo: '', anioInicio: '', anioFin: '' }) }
function eliminarExperiencia(index: number) { form.experiencia.splice(index, 1) }

function agregarSkill() {
  const skill = nuevaSkill.value.trim()
  if (skill && !form.skills.includes(skill)) {
    form.skills.push(skill)
  }
  nuevaSkill.value = ''
}

function agregarSkillConEnter(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    event.preventDefault()
    agregarSkill()
  }
}

function eliminarSkill(index: number) { form.skills.splice(index, 1) }

function subirFoto() { fileInput.value?.click() }

function onFileChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => { fotoPerfil.value = reader.result as string }
  reader.readAsDataURL(file)
}
</script>

<template>
  <div class="page">
    <div class="card">

      <!-- PAGE 1: Datos personales -->
      <div v-if="pagina === 1">
        <h1>Datos personales</h1>
        <div class="grid">
          <div class="row-2">
            <input v-model="form.datosPersonales.nombre" placeholder="Nombre" />
            <input v-model="form.datosPersonales.apellido" placeholder="Apellido" />
          </div>
          <input v-model="form.datosPersonales.email" placeholder="Email" />
          <input v-model="form.datosPersonales.telefono" placeholder="Teléfono" />
          <input v-model="form.datosPersonales.direccion" placeholder="Dirección" />
          <div class="row-2">
            <input v-model="form.datosPersonales.codigoPostal" placeholder="Código Postal" />
            <input v-model="form.datosPersonales.localidad" placeholder="Localidad" />
          </div>

          <!-- TOGGLE PERMISO CONDUCIR -->
          <div class="toggle-row">
            <div class="toggle-info">
              <span class="toggle-icon">🚗</span>
              <div>
                <span class="toggle-label">Permiso de conducir</span>
                <span class="toggle-sub">Incluir en el CV</span>
              </div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="form.datosPersonales.permisoConducir" />
              <span class="toggle-track">
                <span class="toggle-thumb"></span>
              </span>
            </label>
          </div>
        </div>
        <button @click="siguientePagina" type="button">Siguiente</button>
      </div>

      <!-- PAGE 2: Educación -->
      <div v-if="pagina === 2">
        <h1>Educación</h1>
        <div class="chips-list">
          <div v-for="(edu, index) in form.educacion" :key="index" class="item-chip">
            <div class="chip-fields">
              <input v-model="edu.institucion" placeholder="Institución" class="chip-input" />
              <input v-model="edu.titulo" placeholder="Título obtenido" class="chip-input" />
              <div class="chip-years">
                <input v-model="edu.anioInicio" placeholder="Inicio" class="chip-input-year" />
                <span class="year-sep">→</span>
                <input v-model="edu.anioFin" placeholder="Fin" class="chip-input-year" />
              </div>
            </div>
            <button
              v-if="form.educacion.length > 1"
              @click="eliminarEducacion(index)"
              type="button"
              class="chip-remove"
            >✕</button>
          </div>
        </div>
        <button @click="agregarEducacion" type="button" class="btn-add">+ Agregar educación</button>
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 3: Certificaciones -->
      <div v-if="pagina === 3">
        <h1>Certificaciones</h1>
        <div class="chips-list">
          <div v-for="(cert, index) in form.certificaciones" :key="index" class="item-chip">
            <div class="chip-fields">
              <input v-model="cert.certificacion" placeholder="Certificación" class="chip-input" />
              <input v-model="cert.expedicion" placeholder="Fecha de expedición" class="chip-input" />
            </div>
            <button @click="eliminarCertificacion(index)" type="button" class="chip-remove">✕</button>
          </div>
        </div>
        <button @click="agregarCertificacion" type="button" class="btn-add">+ Agregar certificación</button>
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 4: Experiencia -->
      <div v-if="pagina === 4">
        <h1>Experiencia</h1>
        <div class="chips-list">
          <div v-for="(exp, index) in form.experiencia" :key="index" class="item-chip">
            <div class="chip-fields">
              <input v-model="exp.empresa" placeholder="Empresa" class="chip-input" />
              <input v-model="exp.cargo" placeholder="Cargo" class="chip-input" />
              <div class="chip-years">
                <input v-model="exp.anioInicio" placeholder="Inicio" class="chip-input-year" />
                <span class="year-sep">→</span>
                <input v-model="exp.anioFin" placeholder="Fin" class="chip-input-year" />
              </div>
            </div>
            <button
              v-if="form.experiencia.length > 1"
              @click="eliminarExperiencia(index)"
              type="button"
              class="chip-remove"
            >✕</button>
          </div>
        </div>
        <button @click="agregarExperiencia" type="button" class="btn-add">+ Agregar experiencia</button>
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 5: Idiomas -->
      <div v-if="pagina === 5">
        <h1>Idiomas</h1>
        <div class="chips-list">
          <div v-for="(idioma, index) in form.idiomas" :key="index" class="item-chip item-chip--row">
            <input v-model="idioma.idioma" placeholder="Idioma" class="chip-input" />
            <select v-model="idioma.nivel" class="chip-select">
              <option disabled value="">Nivel</option>
              <option>Básico</option>
              <option>Intermedio</option>
              <option>Avanzado</option>
              <option>Nativo</option>
            </select>
            <button @click="eliminarIdioma(index)" type="button" class="chip-remove">✕</button>
          </div>
        </div>
        <button @click="agregarIdioma" type="button" class="btn-add">+ Agregar idioma</button>
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 6: Skills -->
      <div v-if="pagina === 6">
        <h1>Skills</h1>
        <h2>Añade tus habilidades técnicas o personales</h2>

        <!-- Tags visuales -->
        <div v-if="form.skills.length > 0" class="skills-tags">
          <span
            v-for="(skill, index) in form.skills"
            :key="index"
            class="skill-tag"
          >
            {{ skill }}
            <button @click="eliminarSkill(index)" type="button" class="skill-tag-remove">✕</button>
          </span>
        </div>

        <!-- Input para nueva skill -->
        <div class="skill-input-row">
          <input
            v-model="nuevaSkill"
            placeholder="Ej: JavaScript, Trabajo en equipo..."
            @keydown="agregarSkillConEnter"
          />
          <button @click="agregarSkill" type="button" class="btn-skill-add">+</button>
        </div>

        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 7: Oferta de trabajo -->
      <div v-if="pagina === 7">
        <h1>Oferta de trabajo</h1>
        <h2>Pega aquí la oferta a la que quieres aplicar para personalizar tu CV</h2>
        <div class="grid">
          <input v-model="form.ofertaDeTrabajo.empresa" placeholder="Empresa" />
          <div class="form-group">
            <label>Descripción de la oferta</label>
            <textarea
              v-model="form.ofertaDeTrabajo.descripcion"
              placeholder="Pega aquí el texto de la oferta de trabajo..."
              rows="6"
            ></textarea>
          </div>
        </div>
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 8: ¿Foto? -->
      <div v-if="pagina === 8">
        <h1>Plantilla</h1>
        <h2>¿Quieres añadir una foto de perfil?</h2>
        <div class="nav-buttons">
          <button type="button" @click="ponerFoto = true; siguientePagina()">Sí</button>
          <button type="button" class="secondary" @click="ponerFoto = false; enviarFormAlBack(); siguientePagina()">No</button>
        </div>
        <button @click="anteriorPagina" type="button" class="secondary" style="margin-top: 8px;">Atrás</button>
      </div>

      <!-- PAGE 9 CON FOTO -->
      <div v-if="pagina === 9 && ponerFoto">
        <h1>Foto de perfil</h1>
        <button @click="subirFoto" type="button" class="secondary">Subir foto</button>
        <input ref="fileInput" type="file" accept="image/*" style="display: none" @change="onFileChange" />
        <img v-if="fotoPerfil" :src="fotoPerfil" class="avatar" />
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="enviarFormAlBack()" type="button">Generar CV</button>
        </div>
      </div>

      <!-- PAGE 9 SIN FOTO -->
      <div v-if="pagina === 9 && !ponerFoto">
        <h1>Generando CV...</h1>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f7f7f8, #ffffff);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto;
  padding: 40px 16px;
}

.card {
  width: 100%;
  max-width: 480px;
  background: white;
  padding: 28px;
  border-radius: 16px;
  border: 1px solid #eee;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; }
h2 { font-size: 14px; font-weight: 500; color: #555; margin-bottom: 16px; }

.grid { display: flex; flex-direction: column; gap: 12px; }

.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

input, select, textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e7e7e7;
  border-radius: 10px;
  font-size: 14px;
  background: #fafafa;
  transition: all 0.2s ease;
  outline: none;
  font-family: inherit;
  box-sizing: border-box;
}

textarea { resize: vertical; min-height: 100px; }
input:focus, select:focus, textarea:focus { border-color: #111; background: white; }
input::placeholder, textarea::placeholder { color: #aaa; }

.form-group { display: flex; flex-direction: column; gap: 6px; }
label { font-size: 12px; color: #666; }

/* ── TOGGLE ──────────────────────────────── */
.toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border: 1px solid #e7e7e7;
  border-radius: 12px;
  background: #fafafa;
  transition: border-color 0.2s;
}
.toggle-row:hover { border-color: #ccc; }

.toggle-info { display: flex; align-items: center; gap: 10px; }
.toggle-icon { font-size: 18px; }
.toggle-label { display: block; font-size: 14px; font-weight: 500; color: #111; }
.toggle-sub { display: block; font-size: 11px; color: #999; margin-top: 1px; }

.toggle-switch { position: relative; display: inline-flex; cursor: pointer; }
.toggle-switch input { position: absolute; opacity: 0; width: 0; height: 0; }

.toggle-track {
  width: 42px;
  height: 24px;
  background: #e0e0e0;
  border-radius: 999px;
  position: relative;
  transition: background 0.25s ease;
  display: block;
}
.toggle-thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  transition: transform 0.25s ease;
}
.toggle-switch input:checked + .toggle-track { background: #111; }
.toggle-switch input:checked + .toggle-track .toggle-thumb { transform: translateX(18px); }

/* ── CHIPS LIST ──────────────────────────── */
.chips-list { display: flex; flex-direction: column; gap: 8px; }

.item-chip {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 12px;
  border: 1px solid #efefef;
  border-radius: 12px;
  background: #fafafa;
  transition: border-color 0.2s;
}
.item-chip:hover { border-color: #ddd; }

/* Variante fila (idiomas) */
.item-chip--row {
  flex-direction: row;
  align-items: center;
}
.item-chip--row .chip-input { flex: 1; }
.item-chip--row .chip-select { flex: 0 0 130px; }

.chip-fields { flex: 1; display: flex; flex-direction: column; gap: 6px; }

.chip-input {
  width: 100%;
  padding: 7px 10px;
  border: 1px solid #e7e7e7;
  border-radius: 8px;
  font-size: 13px;
  background: white;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
.chip-input:focus { border-color: #111; }

.chip-years { display: flex; align-items: center; gap: 6px; }

.chip-input-year {
  flex: 1;
  padding: 7px 8px;
  border: 1px solid #e7e7e7;
  border-radius: 8px;
  font-size: 13px;
  background: white;
  outline: none;
  box-sizing: border-box;
  text-align: center;
  transition: border-color 0.2s;
}
.chip-input-year:focus { border-color: #111; }

.year-sep { font-size: 12px; color: #bbb; flex-shrink: 0; }

.chip-select {
  padding: 7px 8px;
  border: 1px solid #e7e7e7;
  border-radius: 8px;
  font-size: 13px;
  background: white;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.chip-select:focus { border-color: #111; }

/* Botón X */
.chip-remove {
  flex-shrink: 0;
  width: 26px !important;
  height: 26px;
  border-radius: 50%;
  border: none;
  background: #f3f4f6;
  color: #999;
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-top: 2px;
  transition: background 0.2s, color 0.2s;
}
.chip-remove:hover {
  background: #fee2e2;
  color: #b91c1c;
  transform: none;
  opacity: 1;
}

/* ── BTN AÑADIR ──────────────────────────── */
.btn-add {
  background: transparent;
  color: #777;
  border: 1.5px dashed #ddd;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 13px;
  cursor: pointer;
  margin-top: 8px;
  width: 100%;
  transition: border-color 0.2s, color 0.2s;
}
.btn-add:hover {
  border-color: #111;
  color: #111;
  background: transparent;
  transform: none;
  opacity: 1;
}

/* ── SKILLS ──────────────────────────────── */
.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px 5px 12px;
  background: #f3f4f6;
  border: 1px solid #e7e7e7;
  border-radius: 999px;
  font-size: 13px;
  color: #111;
  animation: fadeIn 0.2s ease;
}

.skill-tag-remove {
  width: 16px !important;
  height: 16px;
  border-radius: 50%;
  border: none;
  background: #ddd;
  color: #666;
  font-size: 9px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-top: 0;
  transition: background 0.2s, color 0.2s;
  flex-shrink: 0;
}
.skill-tag-remove:hover {
  background: #fee2e2;
  color: #b91c1c;
  transform: none;
  opacity: 1;
}

.skill-input-row {
  display: flex;
  gap: 8px;
  align-items: center;
}
.skill-input-row input {
  flex: 1;
}

.btn-skill-add {
  flex-shrink: 0;
  width: 38px !important;
  height: 38px;
  border-radius: 10px;
  border: none;
  background: #111;
  color: white;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-top: 0;
  transition: opacity 0.2s;
}
.btn-skill-add:hover {
  transform: translateY(-1px);
  opacity: 0.85;
}

/* ── NAVEGACIÓN ──────────────────────────── */
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }

button {
  border: none;
  background: #111;
  color: white;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 12px;
  transition: 0.2s;
  width: 100%;
}
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }

.avatar {
  width: 90px;
  height: 90px;
  border-radius: 14px;
  object-fit: cover;
  margin-top: 12px;
  border: 1px solid #eee;
  display: block;
}

.card > div { animation: fadeIn 0.25s ease; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
