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
  foto: false as boolean,
  foto_base64: null as string | null,
  ofertaDeTrabajo: { empresa: '', descripcion: '' },
  descripcion: '',
  porcentaje: 0
})

const cargando = ref(true)
const error = ref<string | null>(null)
const snapshotInicial = ref('')
const haycambios = computed(() => JSON.stringify(cvData) !== snapshotInicial.value)

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
  console.log('CV DATA:', JSON.stringify(cvData, null, 2))
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

   <button @click="guardarCV" class="btn-save" :disabled="!haycambios" title="Guardar CV">
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
    <polyline points="17 21 17 13 7 13 7 21"/>
    <polyline points="7 3 7 8 15 8"/>
  </svg>
  Guardar
</button>

    <div class="cv">

      <header class="cv-header">
        <div class="cv-header-left">
      <h1 class="cv-name">
  <span
    contenteditable="true"
    @blur="cvData.datosPersonales.nombre = ($event.target as HTMLElement).innerText.trim()"
  >{{ cvData.datosPersonales.nombre }}</span>
  {{ ' ' }}
  <span
    class="cv-lastname"
    contenteditable="true"
    @blur="cvData.datosPersonales.apellido = ($event.target as HTMLElement).innerText.trim()"
  >{{ cvData.datosPersonales.apellido }}</span>
</h1>
          <div class="cv-contact-line">
            <span
              v-if="cvData.datosPersonales.email"
              contenteditable="true"
              @blur="cvData.datosPersonales.email = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.datosPersonales.email }}</span>
            <span class="cv-sep" v-if="cvData.datosPersonales.telefono">·</span>
            <span
              v-if="cvData.datosPersonales.telefono"
              contenteditable="true"
              @blur="cvData.datosPersonales.telefono = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.datosPersonales.telefono }}</span>
            <span class="cv-sep" v-if="cvData.datosPersonales.localidad">·</span>
            <span
              v-if="cvData.datosPersonales.localidad"
              contenteditable="true"
              @blur="cvData.datosPersonales.localidad = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.datosPersonales.localidad }}</span>
          </div>
          <div v-if="cvData.datosPersonales.permiso_conducir" class="cv-conducir">Permiso de conducir B</div>
        </div>
<img v-if="cvData.foto && cvData.foto_base64" :src="cvData.foto_base64" class="cv-avatar" alt="Foto" />
      </header>

      <div class="cv-rule"></div>

      <section v-if="cvData.descripcion" class="cv-descripcion-section">
        <h2 class="cv-descripcion-title">Perfil profesional</h2>
        <p
          class="cv-descripcion-text"
          contenteditable="true"
          @blur="cvData.descripcion = ($event.target as HTMLElement).innerText.trim()"
        >{{ cvData.descripcion }}</p>
        <div class="cv-rule cv-rule-sm"></div>
      </section>

      <div class="cv-body">
        <div class="cv-col-left">

          <section v-if="cvData.experiencia?.length" class="cv-section">
            <h2 class="cv-section-title">Experiencia</h2>
            <div v-for="(exp, i) in cvData.experiencia" :key="i" class="cv-entry">
              <div class="cv-entry-head">
                <strong
                  contenteditable="true"
                  @blur="exp.puesto = ($event.target as HTMLElement).innerText.trim()"
                >{{ exp.puesto }}</strong>
                <span class="cv-entry-date">
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
                class="cv-entry-org"
                contenteditable="true"
                @blur="exp.empresa = ($event.target as HTMLElement).innerText.trim()"
              >{{ exp.empresa }}</div>
            </div>
          </section>

          <section v-if="cvData.educacion?.length || cvData.certificaciones?.length" class="cv-section">
            <h2 class="cv-section-title">Formación</h2>
            <div v-for="(edu, i) in cvData.educacion" :key="'e'+i" class="cv-entry">
              <div class="cv-entry-head">
                <strong
                  contenteditable="true"
                  @blur="edu.titulo = ($event.target as HTMLElement).innerText.trim()"
                >{{ edu.titulo }}</strong>
                <span class="cv-entry-date">
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
                class="cv-entry-org"
                contenteditable="true"
                @blur="edu.institucion = ($event.target as HTMLElement).innerText.trim()"
              >{{ edu.institucion }}</div>
            </div>
            <div v-for="(cert, i) in cvData.certificaciones" :key="'c'+i" class="cv-entry">
              <div class="cv-entry-head">
                <strong
                  contenteditable="true"
                  @blur="cert.certificacion = ($event.target as HTMLElement).innerText.trim()"
                >{{ cert.certificacion }}</strong>
                <span
                  class="cv-entry-date"
                  contenteditable="true"
                  @blur="cert.expedicion = ($event.target as HTMLElement).innerText.trim()"
                >{{ cert.expedicion }}</span>
              </div>
            </div>
          </section>

        </div>

        <div class="cv-col-right">

          <section v-if="cvData.idiomas?.length" class="cv-section">
            <h2 class="cv-section-title">Idiomas</h2>
            <div v-for="(lang, i) in cvData.idiomas" :key="i" class="cv-lang-row">
              <span
                class="cv-lang-name"
                contenteditable="true"
                @blur="lang.nombre = ($event.target as HTMLElement).innerText.trim()"
              >{{ lang.nombre }}</span>
              <span
                class="cv-lang-nivel"
                contenteditable="true"
                @blur="lang.nivel = ($event.target as HTMLElement).innerText.trim()"
              >{{ lang.nivel }}</span>
            </div>
          </section>

          <section v-if="cvData.skills?.length" class="cv-section">
            <h2 class="cv-section-title">Skills</h2>
            <ul class="cv-skill-list">
              <li
                v-for="(skill, i) in cvData.skills"
                :key="i"
                contenteditable="true"
                @blur="cvData.skills[i] = ($event.target as HTMLElement).innerText.trim()"
              >{{ skill }}</li>
            </ul>
          </section>

          <section class="cv-section">
            <h2 class="cv-section-title">Contacto</h2>
            <div class="cv-contact-block">
              <div
                v-if="cvData.datosPersonales.direccion"
                contenteditable="true"
                @blur="cvData.datosPersonales.direccion = ($event.target as HTMLElement).innerText.trim()"
              >{{ cvData.datosPersonales.direccion }}</div>
              <div>
                <span
                  contenteditable="true"
                  @blur="cvData.datosPersonales.codigo_postal = ($event.target as HTMLElement).innerText.trim()"
                >{{ cvData.datosPersonales.codigo_postal }}</span>
                {{ ' ' }}
                <span
                  contenteditable="true"
                  @blur="cvData.datosPersonales.localidad = ($event.target as HTMLElement).innerText.trim()"
                >{{ cvData.datosPersonales.localidad }}</span>
              </div>
            </div>
          </section>

        </div>
      </div>
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.cv-bg { background: #f2f2f0; min-height: 100vh; display: flex; justify-content: center; align-items: flex-start; padding: 48px 16px; font-family: 'Lato', sans-serif; }
.cv { width: 210mm; min-height: 297mm; background: #fff; padding: 44px 48px; box-shadow: 0 4px 40px rgba(0,0,0,0.08); color: #1a1a1a; }

.cv-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; }
.cv-header-left { flex: 1; }
.cv-name { font-family: 'Playfair Display', serif; font-size: 36pt; font-weight: 400; line-height: 1.05; color: #111; letter-spacing: -0.5px; display: flex; gap: 8px; flex-wrap: wrap; }
.cv-lastname { font-weight: 400; }
.cv-title { font-size: 10pt; font-weight: 300; color: #888; text-transform: uppercase; letter-spacing: 3px; margin-top: 6px; }
.cv-contact-line { font-size: 8.5pt; color: #555; margin-top: 10px; display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }
.cv-sep { color: #bbb; }
.cv-conducir { font-size: 8pt; color: #888; margin-top: 4px; }
.cv-avatar { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid #eee; flex-shrink: 0; margin-top: 4px; }
.cv-rule { height: 1px; background: #1a1a1a; margin: 24px 0; }
.cv-rule-sm { margin: 20px 0 0 0; }

.cv-descripcion-section { margin-bottom: 0; }
.cv-descripcion-title { font-family: 'Playfair Display', serif; font-size: 10pt; font-weight: 700; color: #111; text-transform: uppercase; letter-spacing: 2.5px; margin-bottom: 8px; }
.cv-descripcion-text { font-size: 9pt; color: #555; line-height: 1.7; font-weight: 300; white-space: pre-line; }

.cv-body { display: grid; grid-template-columns: 1fr 200px; gap: 40px; margin-top: 24px; }
.cv-section { margin-bottom: 28px; }
.cv-section-title { font-family: 'Playfair Display', serif; font-size: 10pt; font-weight: 700; color: #111; text-transform: uppercase; letter-spacing: 2.5px; border-bottom: 1px solid #111; padding-bottom: 6px; margin-bottom: 14px; }
.cv-entry { margin-bottom: 14px; }
.cv-entry-head { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }
.cv-entry-head strong { font-size: 9.5pt; font-weight: 700; color: #111; }
.cv-entry-date { font-size: 7.5pt; font-weight: 300; color: #999; white-space: nowrap; }
.cv-entry-org { font-size: 8.5pt; font-weight: 300; color: #666; margin-top: 2px; font-style: italic; }
.cv-lang-row { display: flex; justify-content: space-between; font-size: 8.5pt; color: #333; padding: 4px 0; border-bottom: 1px solid #f0f0f0; }
.cv-lang-name { font-weight: 700; }
.cv-lang-nivel { color: #888; font-weight: 300; }
.cv-skill-list { list-style: none; padding: 0; }
.cv-skill-list li { font-size: 8.5pt; color: #444; padding: 3px 0; border-bottom: 1px solid #f0f0f0; font-weight: 300; }
.cv-skill-list li::before { content: '— '; color: #bbb; }
.cv-contact-block { font-size: 8.5pt; color: #555; line-height: 1.7; font-weight: 300; }

.match-badge { position: fixed; bottom: 28px; right: 28px; width: 64px; height: 64px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 9999; }
.match-rojo     { background: #e53935; }
.match-amarillo { background: #f9a825; }
.match-verde    { background: #2e7d32; }
.match-number { font-size: 16px; font-weight: 700; color: #fff; line-height: 1; font-family: 'Lato', sans-serif; }
.match-label  { font-size: 9px; color: rgba(255,255,255,0.85); font-weight: 500; letter-spacing: 0.5px; font-family: 'Lato', sans-serif; }

.btn-download,
.btn-save {
  position: fixed;
  bottom: 28px;
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
.btn-download { left: 28px; }
.btn-save     { left: 180px; }
.btn-save:disabled { opacity: 0.35; cursor: not-allowed; }
@media print {
  .cv-bg { background: none; padding: 0; }
  .cv { box-shadow: none; padding: 20px; width: 100%; }
  .match-badge { display: none; }
}
</style>
