<script setup lang="ts">
import router from '@/router'
import { reactive, ref, computed } from 'vue'

const pagina = ref(1) // para saber en que pagina estoy
const ponerFoto = ref(false) // para saber si el usuario quiere foto o no, así se la pasamos al backend y él decide si la incluye o no en el CV generado
const fileInput = ref<HTMLInputElement | null>(null) // referencia al input file para subir foto
const fotoPerfil = ref<string | null>(null) // para almacenar la foto de perfil en base64
const nuevaSkill = ref('')
const intentoAvanzar = ref(false) // que rellene lo que tenga que rellenar para poder pasar a la siguiente pagina
const totalPaginas = 9 // es el total de paginas
const progreso = computed(() => Math.round((pagina.value / totalPaginas) * 100)) //
const meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
const aniosDisponibles = Array.from({ length: 50 }, (_, i) => String(new Date().getFullYear() - i))// crea un array de los ultimos 50 años para los selects de fechas

const plantillaSeleccionada = ref<'europass' | 'minimalista' | 'moderna'>('europass')

const plantillas = [
  { id: 'europass',    label: 'Europass',    desc: 'Formato oficial europeo' },
  { id: 'minimalista', label: 'Minimalista', desc: 'Limpio y sencillo' },
  { id: 'moderna',     label: 'Moderna',     desc: 'Dark sidebar con acento verde' },
]

// ── CARGA IA ──
const cargando = ref(false)
const mensajesCarga = [
  'Analizando tu perfil...',
  'Redactando el perfil profesional...',
  'Ajustando el tono y estilo...',
  'Aplicando el formato final...',
  'Casi listo...'
]

const mensajeCargaActual = ref(mensajesCarga[0])
let intervaloMensajes: ReturnType<typeof setInterval> | null = null

const formulario = reactive({
  datosPersonales: {
    nombre: '', apellido: '', email: '', telefono: '',
    direccion: '', codigoPostal: '', localidad: '', permisoConducir: false
  },
  educacion: [{ titulo: '', institucion: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false }],
  certificaciones: [{ certificacion: '', mes: '', anio: '' }],
  experiencia: [{ cargo: '', empresa: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false }],
  idiomas: [{ idioma: '', nivel: '' }],
  skills: [] as string[],
  foto: false,
  ofertaDeTrabajo: { empresa: '', descripcion: '' },
})

function esValido(val: string) { return val.trim().length > 0 } // para los campos obligatorios de la primera pagina, si el campo tiene texto se considera ok, si no, error (si se ha intentado avanzar) o idle (si no se ha intentado avanzar aun)

function estadoCampo(val: string): 'idle' | 'error' | 'ok' { // devuelve el estado del campo para mostrar borde rojo o verde o ninguno
  if (!intentoAvanzar.value) return val.trim() ? 'ok' : 'idle'
  return val.trim() ? 'ok' : 'error'
}
function claseCampo(estado: 'idle' | 'error' | 'ok') { // devuelve la clase css segun el estado del campo
  if (estado === 'error') return 'field-error'
  if (estado === 'ok') return 'field-ok'
  return ''
}

function paginaEsValida(num: number): boolean {
  if (num === 1) {
    return esValido(formulario.datosPersonales.nombre) &&
      esValido(formulario.datosPersonales.apellido) &&
      esValido(formulario.datosPersonales.email) &&
      esValido(formulario.datosPersonales.telefono) &&
      esValido(formulario.datosPersonales.direccion) &&
      esValido(formulario.datosPersonales.codigoPostal) &&
      esValido(formulario.datosPersonales.localidad)
  }
  return true
}

async function guardarCV() {
  cargando.value = true
  mensajeCargaActual.value = mensajesCarga[0]
  let i = 0
  intervaloMensajes = setInterval(() => {
    i = (i + 1) % mensajesCarga.length
    mensajeCargaActual.value = mensajesCarga[i]
  }, 2000)

  //peticion http
  try {
    const response = await fetch('http://127.0.0.1:8001/api/cv', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
      body: JSON.stringify({
        ...formulario,
        plantilla: plantillaSeleccionada.value,
        foto: ponerFoto.value === true,
        foto_base64: ponerFoto.value ? fotoPerfil.value : null,
      }),
    })

    if (!response.ok) {
      const err = await response.json()
      console.error('Error del backend:', JSON.stringify(err, null, 2))
      return
    }

    const data = await response.json()
    if (!data.id_cv) { console.error('Backend no devolvió id_cv:', data); return }

    const rutas: Record<'europass' | 'minimalista' | 'moderna', string> = {
      europass:    `/forms/plantilla-europass/${data.id_cv}`,
      minimalista: `/forms/plantilla-minimalista/${data.id_cv}`,
      moderna:     `/forms/plantilla-moderna/${data.id_cv}`,
    }
    router.push(rutas[plantillaSeleccionada.value])
  } finally {
    if (intervaloMensajes) clearInterval(intervaloMensajes)
    cargando.value = false
  }
}

function siguientePagina() {
  intentoAvanzar.value = true
  if (!paginaEsValida(pagina.value)) return
  intentoAvanzar.value = false
  pagina.value++
}
function anteriorPagina() { intentoAvanzar.value = false; pagina.value-- }

function agregarEducacion() { formulario.educacion.push({ titulo: '', institucion: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false }) }
function eliminarEducacion(i: number) { formulario.educacion.splice(i, 1) }
function agregarIdioma() { formulario.idiomas.push({ idioma: '', nivel: '' }) }
function eliminarIdioma(i: number) { formulario.idiomas.splice(i, 1) }
function agregarCertificacion() { formulario.certificaciones.push({ certificacion: '', mes: '', anio: '' }) }
function eliminarCertificacion(i: number) { formulario.certificaciones.splice(i, 1) }
function agregarExperiencia() { formulario.experiencia.push({ cargo: '', empresa: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false }) }
function eliminarExperiencia(i: number) { formulario.experiencia.splice(i, 1) }

function agregarSkill() {
  const s = nuevaSkill.value.trim()
  if (s && !formulario.skills.includes(s)) formulario.skills.push(s)
  nuevaSkill.value = ''
}
function agregarSkillConEnter(e: KeyboardEvent) {
  if (e.key === 'Enter') { e.preventDefault(); agregarSkill() }
}
function eliminarSkill(i: number) { formulario.skills.splice(i, 1) }
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

      <!-- OVERLAY DE CARGA IA -->
      <div v-if="cargando" class="loading-overlay">
        <div class="loading-card">
          <div class="loading-spinner"></div>
          <div class="loading-texts">
            <p class="loading-title">Generando tu CV</p>
            <p class="loading-subtitle">{{ mensajeCargaActual }}</p>
          </div>
        </div>
      </div>

      <!-- BARRA DE PROGRESO -->
      <div class="progress-wrap">
        <div class="progress-header">
          <span class="progress-step">Paso {{ pagina }} de {{ totalPaginas }}</span>
          <span class="progress-pct">{{ progreso }}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: progreso + '%' }"></div>
        </div>
      </div>

      <!-- PAGE 1: Datos personales -->
      <div v-if="pagina === 1">
        <h1>Datos personales</h1>
        <div class="grid">
          <div class="row-2">
            <div class="field-wrap">
              <input v-model="formulario.datosPersonales.nombre" placeholder="Nombre" :class="claseCampo(estadoCampo(formulario.datosPersonales.nombre))" />
              <span v-if="estadoCampo(formulario.datosPersonales.nombre) === 'error'" class="hint hint--error">Obligatorio</span>
            </div>
            <div class="field-wrap">
              <input v-model="formulario.datosPersonales.apellido" placeholder="Apellido" :class="claseCampo(estadoCampo(formulario.datosPersonales.apellido))" />
              <span v-if="estadoCampo(formulario.datosPersonales.apellido) === 'error'" class="hint hint--error">Obligatorio</span>
            </div>
          </div>
          <div class="field-wrap">
            <input v-model="formulario.datosPersonales.email" placeholder="Email" />
          </div>
          <div class="field-wrap">
            <input v-model="formulario.datosPersonales.telefono" placeholder="Teléfono" :class="claseCampo(estadoCampo(formulario.datosPersonales.telefono))" />
            <span v-if="estadoCampo(formulario.datosPersonales.telefono) === 'error'" class="hint hint--error">Obligatorio</span>
          </div>
          <div class="field-wrap">
            <input v-model="formulario.datosPersonales.direccion" placeholder="Dirección" :class="claseCampo(estadoCampo(formulario.datosPersonales.direccion))" />
            <span v-if="estadoCampo(formulario.datosPersonales.direccion) === 'error'" class="hint hint--error">Obligatorio</span>
          </div>
          <div class="row-2">
            <div class="field-wrap">
              <input v-model="formulario.datosPersonales.codigoPostal" placeholder="Código Postal" :class="claseCampo(estadoCampo(formulario.datosPersonales.codigoPostal))" />
              <span v-if="estadoCampo(formulario.datosPersonales.codigoPostal) === 'error'" class="hint hint--error">Obligatorio</span>
            </div>
            <div class="field-wrap">
              <input v-model="formulario.datosPersonales.localidad" placeholder="Localidad" :class="claseCampo(estadoCampo(formulario.datosPersonales.localidad))" />
              <span v-if="estadoCampo(formulario.datosPersonales.localidad) === 'error'" class="hint hint--error">Obligatorio</span>
            </div>
          </div>
          <div class="toggle-row">
            <div class="toggle-info">
              <div>
                <span class="toggle-label">Permiso de conducir</span>
                <span class="toggle-sub">Incluir en el CV</span>
              </div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="formulario.datosPersonales.permisoConducir" />
              <span class="toggle-track"><span class="toggle-thumb"></span></span>
            </label>
          </div>
        </div>
        <button @click="siguientePagina" type="button">Siguiente</button>
      </div>

      <!-- PAGE 2: Educación -->
      <div v-if="pagina === 2">
        <h1>Educación <span class="opcional-badge">Opcional</span></h1>
        <div class="chips-list">
          <div v-for="(edu, index) in formulario.educacion" :key="index" class="item-chip">
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
            <button v-if="formulario.educacion.length > 1" @click="eliminarEducacion(index)" type="button" class="chip-remove">✕</button>
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
        <h1>Certificaciones <span class="opcional-badge">Opcional</span></h1>
        <div class="chips-list">
          <div v-for="(cert, index) in formulario.certificaciones" :key="index" class="item-chip">
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
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 4: Experiencia -->
      <div v-if="pagina === 4">
        <h1>Experiencia <span class="opcional-badge">Opcional</span></h1>
        <div class="chips-list">
          <div v-for="(exp, index) in formulario.experiencia" :key="index" class="item-chip">
            <div class="chip-fields">
              <input v-model="exp.cargo" placeholder="Cargo" class="chip-input" />
              <input v-model="exp.empresa" placeholder="Empresa" class="chip-input" />
              <div class="fecha-row">
                <span class="fecha-label">Inicio</span>
                <div class="fecha-selects">
                  <select v-model="exp.mesInicio" class="chip-select-sm"><option value="">Mes</option><option v-for="m in meses" :key="m" :value="m">{{ m }}</option></select>
                  <select v-model="exp.anioInicio" class="chip-select-sm"><option value="">Año</option><option v-for="a in aniosDisponibles" :key="a" :value="a">{{ a }}</option></select>
                </div>
              </div>
              <div class="fecha-row">
                <span class="fecha-label">Fin</span>
                <div class="fecha-selects">
                  <template v-if="!exp.actualidad">
                    <select v-model="exp.mesFin" class="chip-select-sm"><option value="">Mes</option><option v-for="m in meses" :key="m" :value="m">{{ m }}</option></select>
                    <select v-model="exp.anioFin" class="chip-select-sm"><option value="">Año</option><option v-for="a in aniosDisponibles" :key="a" :value="a">{{ a }}</option></select>
                  </template>
                  <label class="actualidad-check">
                    <input type="checkbox" v-model="exp.actualidad" @change="if(exp.actualidad){ exp.mesFin=''; exp.anioFin='' }" />
                    <span>Actualidad</span>
                  </label>
                </div>
              </div>
            </div>
            <button v-if="formulario.experiencia.length > 1" @click="eliminarExperiencia(index)" type="button" class="chip-remove">✕</button>
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
        <h1>Idiomas <span class="opcional-badge">Opcional</span></h1>
        <div class="chips-list">
          <div v-for="(idioma, index) in formulario.idiomas" :key="index" class="item-chip item-chip--row">
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
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 6: Skills -->
      <div v-if="pagina === 6">
        <h1>Skills <span class="opcional-badge">Opcional</span></h1>
        <h2>Añade tus habilidades técnicas o personales</h2>
        <div v-if="formulario.skills.length > 0" class="skills-tags">
          <span v-for="(skill, index) in formulario.skills" :key="index" class="skill-tag">
            {{ skill }}
            <button @click="eliminarSkill(index)" type="button" class="skill-tag-remove">✕</button>
          </span>
        </div>
        <div class="skill-input-row">
          <input v-model="nuevaSkill" placeholder="Ej: JavaScript, Trabajo en equipo..." @keydown="agregarSkillConEnter" />
          <button @click="agregarSkill" type="button" class="btn-skill-add">+</button>
        </div>
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 7: Oferta de trabajo -->
      <div v-if="pagina === 7">
        <h1>Oferta de trabajo <span class="opcional-badge">Opcional</span></h1>
        <h2>Pega aquí la oferta a la que quieres aplicar para personalizar tu CV</h2>
        <div class="grid">
          <div class="field-wrap">
            <input v-model="formulario.ofertaDeTrabajo.empresa" placeholder="Empresa" />
          </div>
          <div class="form-group">
            <label>Descripción de la oferta</label>
            <textarea v-model="formulario.ofertaDeTrabajo.descripcion" placeholder="Pega aquí el texto de la oferta de trabajo..." rows="6"></textarea>
          </div>
        </div>
        <div class="nav-buttons">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 8: Foto de perfil -->
      <div v-if="pagina === 8">
        <h1>Foto de perfil</h1>
        <h2>¿Quieres añadir una foto a tu CV?</h2>
        <div class="foto-opciones">
          <button type="button" class="foto-opcion" :class="{ selected: ponerFoto }" @click="ponerFoto = true">
            <span class="foto-opcion-label">Sí, añadir foto</span>
          </button>
          <button type="button" class="foto-opcion" :class="{ selected: !ponerFoto }" @click="ponerFoto = false">
            <span class="foto-opcion-label">Sin foto</span>
          </button>
        </div>
        <div v-if="ponerFoto" class="foto-upload-area">
          <button @click="subirFoto" type="button" class="secondary">Subir foto</button>
          <input ref="fileInput" type="file" accept="image/*" style="display: none" @change="onFileChange" />
          <img v-if="fotoPerfil" :src="fotoPerfil" class="avatar" />
        </div>
        <div class="nav-buttons" style="margin-top: 16px;">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="siguientePagina" type="button">Siguiente</button>
        </div>
      </div>

      <!-- PAGE 9: Elegir plantilla -->
      <div v-if="pagina === 9">
        <h1>Elige tu plantilla</h1>
        <h2>{{ ponerFoto ? 'Vista con foto de perfil' : 'Vista sin foto de perfil' }}</h2>

        <div class="plantillas-grid">
          <button
            v-for="p in plantillas"
            :key="p.id"
            type="button"
            class="plantilla-card"
            :class="{ selected: plantillaSeleccionada === p.id }"
            @click="plantillaSeleccionada = (p.id as any)"
          >
            <div class="plantilla-preview">
              <svg viewBox="0 0 120 160" xmlns="http://www.w3.org/2000/svg">

                <!-- ── EUROPASS ── -->
                <template v-if="p.id === 'europass'">
                  <rect width="120" height="160" fill="#f4f7fc"/>
                  <rect width="120" height="32" fill="#003399"/>
                  <rect x="8" y="8" width="16" height="16" rx="8" fill="#ffcc00"/>
                  <rect x="28" y="10" width="30" height="5" rx="2" fill="white" opacity="0.9"/>
                  <rect x="28" y="18" width="20" height="3" rx="1" fill="#aac4f0"/>
                  <template v-if="ponerFoto">
                    <rect x="88" y="4" width="26" height="24" rx="1" fill="#1a3d7a"/>
                    <circle cx="101" cy="12" r="5" fill="#b0bec5"/>
                    <path d="M91 28 q10-8 20 0" fill="#b0bec5"/>
                  </template>
             
                  <rect x="8" y="36" width="60" height="8" fill="#003399" opacity="0.15"/>
                  <rect x="8" y="48" width="45" height="4" rx="1" fill="#003399" opacity="0.5"/>
                  <rect x="8" y="56" width="30" height="3" rx="1" fill="#aac4f0"/>
                  <rect x="0" y="68" width="42" height="92" fill="#f0f4fa"/>
                  <rect x="42" y="68" width="1" height="92" fill="#dde4f0"/>
                  <rect x="6" y="76" width="30" height="2" rx="1" fill="#003399" opacity="0.6"/>
                  <rect x="6" y="82" width="22" height="2" rx="1" fill="#aaa"/>
                  <rect x="6" y="88" width="26" height="2" rx="1" fill="#aaa"/>
                  <rect x="6" y="94" width="18" height="2" rx="1" fill="#aaa"/>
                  <circle cx="8" cy="104" r="2" fill="#003399" opacity="0.5"/>
                  <circle cx="13" cy="104" r="2" fill="#003399" opacity="0.5"/>
                  <circle cx="18" cy="104" r="2" fill="#003399"/>
                  <circle cx="23" cy="104" r="2" fill="#003399"/>
                  <circle cx="28" cy="104" r="2" fill="#003399"/>
                  <rect x="48" y="76" width="40" height="2" rx="1" fill="#003399" opacity="0.7"/>
                  <circle cx="52" cy="86" r="3" fill="#003399"/>
                  <rect x="58" y="84" width="30" height="2" rx="1" fill="#333"/>
                  <rect x="58" y="89" width="22" height="2" rx="1" fill="#aaa"/>
                  <circle cx="52" cy="98" r="3" fill="#003399"/>
                  <rect x="58" y="96" width="26" height="2" rx="1" fill="#333"/>
                  <rect x="58" y="101" width="18" height="2" rx="1" fill="#aaa"/>
                  <rect x="0" y="148" width="120" height="12" fill="#f0f4fa"/>
                  <rect x="6" y="152" width="50" height="2" rx="1" fill="#aaa"/>
                </template>

                <!-- ── MINIMALISTA ── -->
                <template v-if="p.id === 'minimalista'">
                  <rect width="120" height="160" fill="white"/>
                  <rect x="8" y="12" width="55" height="8" rx="1" fill="#111" opacity="0.85"/>
                  <rect x="8" y="24" width="40" height="6" rx="1" fill="#111"/>
                  <rect x="8" y="34" width="35" height="2" rx="1" fill="#999"/>
                  <rect x="8" y="40" width="70" height="2" rx="1" fill="#ccc"/>
                  <template v-if="ponerFoto">
                    <circle cx="100" cy="22" r="14" fill="#e0e0e0"/>
                    <circle cx="100" cy="17" r="5" fill="#b0bec5"/>
                    <path d="M86 36 q14-10 28 0" fill="#b0bec5"/>
                  </template>

                  <rect x="8" y="50" width="104" height="1" fill="#111"/>
                  <rect x="8" y="58" width="40" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="8" y="64" width="55" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="69" width="35" height="2" rx="1" fill="#aaa"/>
                  <rect x="8" y="77" width="50" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="82" width="30" height="2" rx="1" fill="#aaa"/>
                  <rect x="8" y="90" width="40" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="8" y="96" width="52" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="101" width="38" height="2" rx="1" fill="#aaa"/>
                  <rect x="8" y="109" width="48" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="114" width="28" height="2" rx="1" fill="#aaa"/>
                  <rect x="76" y="58" width="36" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="76" y="65" width="28" height="2" rx="1" fill="#555"/>
                  <rect x="76" y="70" width="22" height="1" rx="0.5" fill="#eee"/>
                  <rect x="76" y="75" width="24" height="2" rx="1" fill="#555"/>
                  <rect x="76" y="80" width="22" height="1" rx="0.5" fill="#eee"/>
                  <rect x="76" y="90" width="36" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="76" y="97" width="26" height="2" rx="1" fill="#555"/>
                  <rect x="76" y="102" width="22" height="1" rx="0.5" fill="#eee"/>
                  <rect x="76" y="107" width="30" height="2" rx="1" fill="#555"/>
                </template>

                <!-- ── MODERNA ── -->
                <template v-if="p.id === 'moderna'">
                  <rect width="120" height="160" fill="white"/>
                  <rect width="44" height="160" fill="#1b2333"/>
                  <template v-if="ponerFoto">
                    <circle cx="22" cy="24" r="14" fill="#2a3547"/>
                    <circle cx="22" cy="24" r="14" fill="none" stroke="#00c896" stroke-width="2"/>
                    <circle cx="22" cy="20" r="5" fill="#3d4a5c"/>
                    <path d="M10 38 q12-8 24 0" fill="#3d4a5c"/>
                  </template>

                  <rect x="6" y="46" width="24" height="2" rx="1" fill="#00c896" opacity="0.8"/>
                  <rect x="6" y="52" width="32" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.6"/>
                  <rect x="6" y="57" width="28" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.6"/>
                  <rect x="6" y="62" width="30" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.6"/>
                  <rect x="6" y="72" width="20" height="2" rx="1" fill="#00c896" opacity="0.8"/>
                  <rect x="6" y="78" width="32" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.5"/>
                  <rect x="6" y="82" width="20" height="2" rx="1" fill="#00c896" opacity="0.4"/>
                  <rect x="6" y="88" width="32" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.5"/>
                  <rect x="6" y="92" width="24" height="2" rx="1" fill="#00c896" opacity="0.4"/>
                  <rect x="6" y="102" width="18" height="2" rx="1" fill="#00c896" opacity="0.8"/>
                  <rect x="6" y="108" width="14" height="5" rx="2" fill="#00c896" opacity="0.15" stroke="#00c896" stroke-width="0.5"/>
                  <rect x="22" y="108" width="16" height="5" rx="2" fill="#00c896" opacity="0.15" stroke="#00c896" stroke-width="0.5"/>
                  <rect x="6" y="116" width="18" height="5" rx="2" fill="#00c896" opacity="0.15" stroke="#00c896" stroke-width="0.5"/>
                  <rect x="50" y="14" width="50" height="6" rx="1" fill="#111" opacity="0.8"/>
                  <rect x="50" y="24" width="35" height="2" rx="1" fill="#888"/>
                  <rect x="50" y="30" width="20" height="2" rx="1" fill="#00c896"/>
                  <rect x="50" y="40" width="45" height="2" rx="1" fill="#333" opacity="0.7"/>
                  <rect x="50" y="45" width="60" height="0.5" fill="#eee"/>
                  <circle cx="53" cy="54" r="2.5" fill="#00c896"/>
                  <rect x="58" y="52" width="32" height="2" rx="1" fill="#111"/>
                  <rect x="58" y="57" width="22" height="2" rx="1" fill="#00c896" opacity="0.7"/>
                  <circle cx="53" cy="68" r="2.5" fill="#00c896"/>
                  <rect x="58" y="66" width="28" height="2" rx="1" fill="#111"/>
                  <rect x="58" y="71" width="18" height="2" rx="1" fill="#00c896" opacity="0.7"/>
                  <rect x="50" y="84" width="45" height="2" rx="1" fill="#333" opacity="0.7"/>
                  <rect x="50" y="89" width="60" height="0.5" fill="#eee"/>
                  <circle cx="53" cy="98" r="2.5" fill="#00c896"/>
                  <rect x="58" y="96" width="30" height="2" rx="1" fill="#111"/>
                  <rect x="58" y="101" width="20" height="2" rx="1" fill="#00c896" opacity="0.7"/>
                </template>

              </svg>
            </div>

            <div class="plantilla-check" v-if="plantillaSeleccionada === p.id">✓</div>

            <div class="plantilla-info">
              <span class="plantilla-name">{{ p.label }}</span>
              <span class="plantilla-desc">{{ p.desc }}</span>
            </div>
          </button>
        </div>

        <div class="nav-buttons" style="margin-top: 20px;">
          <button @click="anteriorPagina" type="button" class="secondary">Atrás</button>
          <button @click="guardarCV()" type="button">Generar CV</button>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(180deg, #f7f7f8, #ffffff);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto;
  padding: 40px 16px;
}
.card {
  width: 100%; max-width: 480px; background: white;
  padding: 28px; border-radius: 16px; border: 1px solid #eee;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; display: flex; align-items: center; gap: 8px; }
h2 { font-size: 14px; font-weight: 500; color: #555; margin-bottom: 16px; }

.opcional-badge { font-size: 11px; font-weight: 500; background: #f3f4f6; color: #888; border-radius: 6px; padding: 2px 8px; }
.grid { display: flex; flex-direction: column; gap: 12px; }
.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.field-wrap { display: flex; flex-direction: column; gap: 3px; }
.hint { font-size: 11.5px; font-weight: 500; padding-left: 2px; animation: hintIn 0.15s ease; }
.hint--error { color: #d97706; }
.hint--ok { color: #16a34a; }
@keyframes hintIn { from { opacity: 0; transform: translateY(-2px); } to { opacity: 1; transform: translateY(0); } }

input, select, textarea {
  width: 100%; padding: 10px 12px; border: 1.5px solid #e7e7e7;
  border-radius: 10px; font-size: 14px; background: #fafafa;
  transition: border-color 0.2s, background 0.2s; outline: none;
  font-family: inherit; box-sizing: border-box;
}
textarea { resize: vertical; min-height: 100px; }
input:focus, select:focus, textarea:focus { border-color: #111; background: white; }
input::placeholder, textarea::placeholder { color: #aaa; }
.field-error { border-color: #f59e0b !important; background: #fffbeb !important; }
.field-ok { border-color: #4ade80 !important; background: #f0fdf4 !important; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
label { font-size: 12px; color: #666; }

.toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border: 1px solid #e7e7e7; border-radius: 12px; background: #fafafa; }
.toggle-info { display: flex; align-items: center; gap: 10px; }
.toggle-icon { font-size: 18px; }
.toggle-label { display: block; font-size: 14px; font-weight: 500; color: #111; }
.toggle-sub { display: block; font-size: 11px; color: #999; margin-top: 1px; }
.toggle-switch { position: relative; display: inline-flex; cursor: pointer; }
.toggle-switch input { position: absolute; opacity: 0; width: 0; height: 0; }
.toggle-track { width: 42px; height: 24px; background: #e0e0e0; border-radius: 999px; position: relative; transition: background 0.25s; display: block; }
.toggle-thumb { position: absolute; top: 3px; left: 3px; width: 18px; height: 18px; border-radius: 50%; background: white; box-shadow: 0 1px 4px rgba(0,0,0,0.2); transition: transform 0.25s; }
.toggle-switch input:checked + .toggle-track { background: #111; }
.toggle-switch input:checked + .toggle-track .toggle-thumb { transform: translateX(18px); }

.chips-list { display: flex; flex-direction: column; gap: 8px; }
.item-chip { display: flex; align-items: flex-start; gap: 8px; padding: 10px 12px; border: 1px solid #efefef; border-radius: 12px; background: #fafafa; }
.item-chip--row { flex-direction: row; align-items: flex-start; }
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
.chip-select { width: 100%; padding: 7px 8px; border: 1.5px solid #e7e7e7; border-radius: 8px; font-size: 13px; background: white; outline: none; box-sizing: border-box; }
.chip-remove { flex-shrink: 0; width: 26px !important; height: 26px; border-radius: 50%; border: none; background: #f3f4f6; color: #999; font-size: 11px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; margin-top: 2px; }
.chip-remove:hover { background: #fee2e2; color: #b91c1c; transform: none; opacity: 1; }
.btn-add { background: transparent; color: #777; border: 1.5px dashed #ddd; padding: 8px 14px; border-radius: 10px; font-size: 13px; cursor: pointer; margin-top: 8px; width: 100%; }
.btn-add:hover { border-color: #111; color: #111; background: transparent; transform: none; opacity: 1; }

.skills-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.skill-tag { display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px 5px 12px; background: #f3f4f6; border: 1px solid #e7e7e7; border-radius: 999px; font-size: 13px; color: #111; }
.skill-tag-remove { width: 16px !important; height: 16px; border-radius: 50%; border: none; background: #ddd; color: #666; font-size: 9px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; }
.skill-input-row { display: flex; gap: 8px; align-items: center; }
.skill-input-row input { flex: 1; }
.btn-skill-add { flex-shrink: 0; width: 38px !important; height: 38px; border-radius: 10px; border: none; background: #111; color: white; font-size: 20px; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; margin-top: 0; }

/* PROGRESO */
.progress-wrap { margin-bottom: 24px; }
.progress-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.progress-step { font-size: 12px; color: #999; font-weight: 500; }
.progress-pct { font-size: 12px; color: #111; font-weight: 600; }
.progress-track { width: 100%; height: 4px; background: #f0f0f0; border-radius: 999px; overflow: hidden; }
.progress-fill { height: 100%; background: #111; border-radius: 999px; transition: width 0.35s ease; }

/* NAV */
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
button {
  border: none; background: #111; color: white; padding: 10px 14px;
  border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px;
  transition: 0.2s; width: 100%;
}
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }

/* SELECTOR DE PLANTILLA */
.plantillas-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.plantilla-card {
  position: relative; display: flex; flex-direction: column; align-items: center;
  gap: 8px; padding: 10px 8px 12px; border: 2px solid #e7e7e7;
  border-radius: 14px; background: #fafafa; cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  width: 100%; margin: 0;
}
.plantilla-card:hover { border-color: #999; background: white; transform: none; opacity: 1; }
.plantilla-card.selected { border-color: #111; background: white; box-shadow: 0 0 0 3px rgba(0,0,0,0.06); }
.plantilla-preview { width: 100%; aspect-ratio: 3/4; overflow: hidden; border-radius: 6px; border: 1px solid #eee; background: white; }
.plantilla-preview svg { width: 100%; height: 100%; display: block; }
.plantilla-check {
  position: absolute; top: 8px; right: 8px;
  width: 20px; height: 20px; border-radius: 50%;
  background: #111; color: white; font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.plantilla-info { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.plantilla-name { font-size: 12px; font-weight: 700; color: #111; }
.plantilla-desc { font-size: 10px; color: #999; text-align: center; line-height: 1.3; }

/* FOTO */
.foto-opciones { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
.foto-opcion {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 16px 10px; border: 2px solid #e7e7e7; border-radius: 14px;
  background: #fafafa; cursor: pointer; transition: all 0.2s;
  margin: 0; width: 100%;
}
.foto-opcion:hover { border-color: #999; background: white; transform: none; opacity: 1; }
.foto-opcion.selected { border-color: #111; background: white; box-shadow: 0 0 0 3px rgba(0,0,0,0.06); }
.foto-opcion-icon { font-size: 22px; }
.foto-opcion-label { font-size: 13px; font-weight: 600; color: #111; }
.foto-upload-area { display: flex; flex-direction: column; align-items: flex-start; gap: 10px; padding: 14px; border: 1px dashed #ddd; border-radius: 12px; background: #fafafa; }
.avatar { width: 80px; height: 80px; border-radius: 12px; object-fit: cover; border: 1px solid #eee; display: block; }

/* PAGE TRANSITIONS */
.card > div { animation: fadeIn 0.25s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

/* ── LOADING OVERLAY ── */
.loading-overlay {
  position: fixed; inset: 0; z-index: 999;
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center;
}
.loading-card {
  display: flex; flex-direction: column; align-items: center; gap: 16px;
  padding: 36px 48px; background: white;
  border-radius: 16px; border: 1px solid #e7e7e7;
  box-shadow: 0 8px 24px rgba(0,0,0,0.07);
}
.loading-spinner {
  width: 36px; height: 36px; border-radius: 50%;
  border: 3px solid #f0f0f0;
  border-top-color: #111;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-texts { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.loading-title { font-size: 15px; font-weight: 600; color: #111; margin: 0; }
.loading-subtitle { font-size: 13px; color: #999; margin: 0; }
</style>
