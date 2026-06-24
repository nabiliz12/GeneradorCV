<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const id_cv = route.params.id_cv

const cvData = reactive({
  datosPersonales: {
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    direccion: '',
    codigo_postal: '',
    localidad: '',
    permiso_conducir: false
  },
  educacion: [] as { institucion: string; titulo: string; anioInicio: string; anioFin: string }[],
  certificaciones: [] as { certificacion: string; expedicion: string }[],
  experiencia: [] as { empresa: string; puesto: string; fecha_inicio: string; fecha_fin: string; descripcion: string }[],
  idiomas: [] as { nombre: string; nivel: string }[],
  skills: [] as string[],
  foto: false as boolean ,
  foto_base64: null as string | null,
  ofertaDeTrabajo: { empresa: '', descripcion: '' },
  descripcion: '',
  porcentaje: 0
})

const cargando = ref(true)
const error = ref<string | null>(null)

const snapshotInicial = ref('')
const hayCambios = computed(() => JSON.stringify(cvData) !== snapshotInicial.value)

function nivelPct(nivel: string): number {
  const map: Record<string, number> = { 'Básico': 25, 'Intermedio': 55, 'Avanzado': 80, 'Nativo': 100 }
  return map[nivel] ?? 50
}

async function recogerDatos() {
  try {
    cargando.value = true
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/recuperar_cv/${id_cv}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
    })
    if (!response.ok) throw new Error(`Error ${response.status}`)
    Object.assign(cvData, await response.json())
    snapshotInicial.value = JSON.stringify(cvData)
  } catch (e: any) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}

onMounted(() => recogerDatos())

async function descargarCV() {
  const html2pdf = (await import('html2pdf.js')).default
  const elemento = document.querySelector('.cv') as HTMLElement
  html2pdf()
    .set({
      margin: 0,
      filename: `cv_de_${cvData.datosPersonales.nombre}_${cvData.datosPersonales.apellido}.pdf`,
      image: { type: 'jpeg', quality: 1 },
      html2canvas: { scale: 1.5, useCORS: true },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    })
    .from(elemento)
    .save()
}

async function guardarCV() {
  try {
    await fetch(`${import.meta.env.VITE_API_URL}/api/editar_cv/${id_cv}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
      body: JSON.stringify(cvData)
    })
    snapshotInicial.value = JSON.stringify(cvData)
  } catch (e: any) {
    alert('Error al guardar: ' + e.message)
  }
}
</script>

<template>
  <div v-if="cargando" style="text-align:center;padding:40px;font-family:sans-serif">Cargando CV...</div>
  <div v-else-if="error" style="text-align:center;color:red;padding:40px;font-family:sans-serif">Error: {{ error }}</div>

  <div v-else-if="cvData" class="cv-bg">

    <button @click="descargarCV()" class="btn-download" title="Descargar CV">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      Descargar CV
    </button>

    <button @click="guardarCV" class="btn-save" :disabled="!hayCambios" title="Guardar CV">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
        <polyline points="17 21 17 13 7 13 7 21"/>
        <polyline points="7 3 7 8 15 8"/>
      </svg>
      Guardar
    </button>

    <div class="cv">
      <aside class="sidebar">
        <div class="sb-photo-wrap" v-if="cvData.foto">
          <img
            v-if="cvData.foto && cvData.foto_base64"
            :src="cvData.foto_base64"
            class="sb-photo"
            alt="Foto de perfil"
          />
        </div>

        <div class="sb-nombre">
          <span
            class="sb-nombre-first"
            contenteditable="true"
            @blur="cvData.datosPersonales.nombre = ($event.target as HTMLElement).innerText.trim()"
          >{{ cvData.datosPersonales?.nombre }}</span>
          <span
            class="sb-nombre-last"
            contenteditable="true"
            @blur="cvData.datosPersonales.apellido = ($event.target as HTMLElement).innerText.trim()"
          >{{ cvData.datosPersonales?.apellido }}</span>
        </div>

        <section class="sb-section">
          <h3 class="sb-section-title">Contacto</h3>
          <div class="sb-item">
            <span class="sb-icon">✉</span>
            <span
              contenteditable="true"
              @blur="cvData.datosPersonales.email = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.datosPersonales?.email }}</span>
          </div>
          <div class="sb-item">
            <span class="sb-icon">📱</span>
            <span
              contenteditable="true"
              @blur="cvData.datosPersonales.telefono = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.datosPersonales?.telefono }}</span>
          </div>
            <div class="sb-item">
              <span class="sb-icon">📍</span>
              <span>
                <span
                  contenteditable="true"
                  @blur="cvData.datosPersonales.direccion = ($event.target as HTMLElement).innerText.trim()"
                >{{ cvData.datosPersonales?.direccion }}</span>,
                <span
                  contenteditable="true"
                  @blur="cvData.datosPersonales.localidad = ($event.target as HTMLElement).innerText.trim()"
                >{{ cvData.datosPersonales?.localidad }}</span>
              </span>
            </div>
          <div v-if="cvData.datosPersonales?.permiso_conducir" class="sb-item">
            <span class="sb-icon">🚗</span><span>Permiso B</span>
          </div>
        </section>

        <section v-if="cvData.idiomas?.length" class="sb-section">
          <h3 class="sb-section-title">Idiomas</h3>
          <div v-for="(lang, i) in cvData.idiomas" :key="i" class="sb-lang">
            <div class="sb-lang-header">
              <span
                contenteditable="true"
                @blur="lang.nombre = ($event.target as HTMLElement).innerText.trim()"
              >{{ lang.nombre }}</span>
              <span class="sb-lang-nivel">{{ lang.nivel }}</span>
            </div>
            <div class="sb-lang-bar"><div class="sb-lang-fill" :style="{ width: nivelPct(lang.nivel) + '%' }"></div></div>
          </div>
        </section>

        <section v-if="cvData.skills?.length" class="sb-section">
          <h3 class="sb-section-title">Skills</h3>
          <div class="sb-skills">
            <span
              v-for="(skill, i) in cvData.skills"
              :key="i"
              class="sb-skill"
              contenteditable="true"
              @blur="cvData.skills[i] = ($event.target as HTMLElement).innerText.trim()"
            >{{ skill }}</span>
          </div>
        </section>
      </aside>

      <main class="main">
        <header class="main-header">
          <h1 class="main-name">
            <span
              contenteditable="true"
              @blur="cvData.datosPersonales.nombre = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.datosPersonales?.nombre }}</span>
            <span
              contenteditable="true"
              @blur="cvData.datosPersonales.apellido = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.datosPersonales?.apellido }}</span>
          </h1>
          <div class="main-accent-bar"></div>
        </header>

        <section v-if="cvData.descripcion" class="main-section">
          <h2 class="main-section-title"><span class="main-section-icon">👤</span> Sobre mí</h2>
          <p
            class="main-descripcion"
            contenteditable="true"
            @blur="cvData.descripcion = ($event.target as HTMLElement).innerText.trim()"
          >{{ cvData.descripcion }}</p>
        </section>

        <section v-if="cvData.experiencia?.length" class="main-section">
          <h2 class="main-section-title"><span class="main-section-icon">💼</span> Experiencia laboral</h2>
          <div v-for="(exp, i) in cvData.experiencia" :key="i" class="main-entry">
            <div class="main-entry-dot"></div>
            <div class="main-entry-content">
              <div class="main-entry-top">
                <strong
                  class="main-entry-role"
                  contenteditable="true"
                  @blur="exp.puesto = ($event.target as HTMLElement).innerText.trim()"
                >{{ exp.puesto }}</strong>
                <span class="main-entry-badge">
                  <span
                    contenteditable="true"
                    @blur="exp.fecha_inicio = ($event.target as HTMLElement).innerText.trim()"
                  >{{ exp.fecha_inicio }}</span>
                  —
                  <span
                    contenteditable="true"
                    @blur="exp.fecha_fin = ($event.target as HTMLElement).innerText.trim()"
                  >{{ exp.fecha_fin || 'Actualidad' }}</span>
                </span>
              </div>
              <div
                class="main-entry-company"
                contenteditable="true"
                @blur="exp.empresa = ($event.target as HTMLElement).innerText.trim()"
              >{{ exp.empresa }}</div>
            </div>
          </div>
        </section>

        <section v-if="cvData.educacion?.length || cvData.certificaciones?.length" class="main-section">
          <h2 class="main-section-title"><span class="main-section-icon">🎓</span> Formación académica</h2>
          <div v-for="(edu, i) in cvData.educacion" :key="'e'+i" class="main-entry">
            <div class="main-entry-dot"></div>
            <div class="main-entry-content">
              <div class="main-entry-top">
                <strong
                  class="main-entry-role"
                  contenteditable="true"
                  @blur="edu.titulo = ($event.target as HTMLElement).innerText.trim()"
                >{{ edu.titulo }}</strong>
                <span class="main-entry-badge">
                  <span
                    contenteditable="true"
                    @blur="edu.anioInicio = ($event.target as HTMLElement).innerText.trim()"
                  >{{ edu.anioInicio }}</span>
                  —
                  <span
                    contenteditable="true"
                    @blur="edu.anioFin = ($event.target as HTMLElement).innerText.trim()"
                  >{{ edu.anioFin || 'Actualidad' }}</span>
                </span>
              </div>
              <div
                class="main-entry-company"
                contenteditable="true"
                @blur="edu.institucion = ($event.target as HTMLElement).innerText.trim()"
              >{{ edu.institucion }}</div>
            </div>
          </div>
          <div v-for="(cert, i) in cvData.certificaciones" :key="'c'+i" class="main-entry">
            <div class="main-entry-dot"></div>
            <div class="main-entry-content">
              <div class="main-entry-top">
                <strong
                  class="main-entry-role"
                  contenteditable="true"
                  @blur="cert.certificacion = ($event.target as HTMLElement).innerText.trim()"
                >{{ cert.certificacion }}</strong>
                <span
                  class="main-entry-badge"
                  contenteditable="true"
                  @blur="cert.expedicion = ($event.target as HTMLElement).innerText.trim()"
                >{{ cert.expedicion }}</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>

    <div v-if="Number(cvData.porcentaje) > 0" class="match-badge" :class="{
      'match-rojo':     Number(cvData.porcentaje) < 30,
      'match-amarillo': Number(cvData.porcentaje) >= 30 && Number(cvData.porcentaje) < 70,
      'match-verde':    Number(cvData.porcentaje) >= 70
    }">
      <span class="match-number">{{ Number(cvData.porcentaje) }}%</span>
      <span class="match-label">match</span>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.cv-bg { background: #d8dee8; min-height: 100vh; display: flex; justify-content: center; align-items: flex-start; padding: 48px 16px; font-family: 'DM Sans', sans-serif; }
.cv { width: 210mm; min-height: 297mm; background: #fff; display: grid; grid-template-columns: 70mm 1fr; box-shadow: 0 16px 64px rgba(0,0,0,0.22); overflow: hidden; }

.sidebar { background: #1b2333; display: flex; flex-direction: column; }
.sb-photo-wrap { background: #232d40; padding: 28px 28px 20px; display: flex; justify-content: center; }
.sb-photo { width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #00c896; }
.sb-photo-placeholder { width: 100px; height: 100px; border-radius: 50%; background: #1b2333; border: 3px solid #00c896; display: flex; align-items: center; justify-content: center; }
.sb-photo-placeholder svg { width: 60px; height: 60px; }
.sb-nombre { padding: 14px 22px 0; display: flex; flex-direction: column; line-height: 1.2; }
.sb-nombre-first { font-size: 9pt; font-weight: 300; color: #c8d6e5; letter-spacing: 1px; }
.sb-nombre-last { font-size: 13pt; font-weight: 700; color: #fff; letter-spacing: 0.5px; }
.sb-section { padding: 16px 22px; border-bottom: 1px solid rgba(255,255,255,0.06); }
.sb-section:last-child { border-bottom: none; }
.sb-section-title { font-size: 7pt; font-weight: 700; text-transform: uppercase; letter-spacing: 2.5px; color: #00c896; margin-bottom: 12px; }
.sb-item { display: flex; align-items: flex-start; gap: 8px; font-size: 7.5pt; color: #c8d6e5; margin-bottom: 8px; line-height: 1.45; }
.sb-icon { font-size: 8pt; flex-shrink: 0; margin-top: 1px; }
.sb-lang { margin-bottom: 10px; }
.sb-lang-header { display: flex; justify-content: space-between; font-size: 8pt; color: #c8d6e5; margin-bottom: 4px; }
.sb-lang-nivel { color: #6b7fa3; font-size: 7pt; }
.sb-lang-bar { height: 3px; background: rgba(255,255,255,0.1); border-radius: 999px; overflow: hidden; }
.sb-lang-fill { height: 100%; background: #00c896; border-radius: 999px; }
.sb-skills { display: flex; flex-wrap: wrap; gap: 5px; }
.sb-skill { font-size: 7pt; background: rgba(0,200,150,0.15); color: #00c896; border: 1px solid rgba(0,200,150,0.3); border-radius: 4px; padding: 3px 8px; letter-spacing: 0.3px; }

.main { padding: 36px 32px; background: #fff; }
.main-header { margin-bottom: 28px; }
.main-name { font-size: 22pt; font-weight: 300; color: #111; line-height: 1.1; letter-spacing: -0.5px; display: flex; gap: 8px; flex-wrap: wrap; }
.main-name span:last-child { font-weight: 700; }
.main-title { font-size: 9pt; color: #888; font-weight: 400; text-transform: uppercase; letter-spacing: 2px; margin-top: 5px; }
.main-accent-bar { height: 3px; width: 48px; background: #00c896; border-radius: 999px; margin-top: 14px; }
.main-section { margin-bottom: 26px; }
.main-section-title { font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: #111; margin-bottom: 16px; display: flex; align-items: center; gap: 6px; padding-bottom: 6px; border-bottom: 2px solid #f0f0f0; }
.main-section-icon { font-size: 9pt; }
.main-descripcion { font-size: 8.5pt; color: #555; line-height: 1.7; white-space: pre-line; }
.main-entry { display: flex; gap: 14px; margin-bottom: 16px; align-items: flex-start; }
.main-entry-dot { width: 8px; height: 8px; border-radius: 50%; background: #00c896; margin-top: 4px; flex-shrink: 0; }
.main-entry-content { flex: 1; }
.main-entry-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 3px; }
.main-entry-role { font-size: 9.5pt; font-weight: 700; color: #111; line-height: 1.2; }
.main-entry-badge { font-size: 7pt; background: #f4f4f4; color: #666; border-radius: 20px; padding: 2px 8px; white-space: nowrap; font-weight: 500; flex-shrink: 0; margin-top: 2px; display: flex; align-items: center; gap: 3px; }
.main-entry-company { font-size: 8.5pt; color: #00c896; font-weight: 500; }

/* Feedback visual al editar */
[contenteditable]:focus { outline: none; background: rgba(0, 200, 150, 0.07); border-radius: 3px; }
[contenteditable]:hover  { background: rgba(0, 200, 150, 0.04); border-radius: 3px; }

.match-badge { position: fixed; bottom: 28px; right: 28px; width: 64px; height: 64px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 9999; }
.match-rojo     { background: #e53935; }
.match-amarillo { background: #f9a825; }
.match-verde    { background: #2e7d32; }
.match-number { font-size: 16px; font-weight: 700; color: #fff; line-height: 1; font-family: 'DM Sans', sans-serif; }
.match-label  { font-size: 9px; color: rgba(255,255,255,0.85); font-weight: 500; letter-spacing: 0.5px; font-family: 'DM Sans', sans-serif; }

.btn-download,
.btn-save {
  position: fixed;
  bottom: 28px;
  left: 180px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #111;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  transition: opacity 0.2s, transform 0.2s;
  z-index: 9999;
  width: auto !important;
  margin-top: 0 !important;
}
.btn-save:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.btn-download { left: 28px;  padding: 10px 18px; }
.btn-save     { left: 180px; padding: 10px 18px; }

@media print {
  .cv-bg { background: none; padding: 0; }
  .cv { box-shadow: none; width: 100%; min-height: 100vh; }
  .match-badge, .btn-download, .btn-save { display: none; }
}
</style>
