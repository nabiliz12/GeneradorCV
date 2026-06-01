<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const id_cv = route.params.id_cv

function nivelADots(nivel: string): number {
  const map: Record<string, number> = { 'Básico': 1, 'Intermedio': 2, 'Avanzado': 3, 'Nativo': 5 }
  return map[nivel] ?? 2
}

function nivelACefr(nivel: string): string {
  const map: Record<string, string> = { 'Básico': 'A1 / A2', 'Intermedio': 'B1 / B2', 'Avanzado': 'C1', 'Nativo': 'Nativo' }
  return map[nivel] ?? nivel
}

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
const hayCambios = computed(() => JSON.stringify(cvData) !== snapshotInicial.value)

async function recogerDatos() {
  try {
    cargando.value = true
    const response = await fetch(`http://127.0.0.1:8001/api/recuperar_cv/${id_cv}`, {
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
  const elemento = document.querySelector('.europass') as HTMLElement
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
    await fetch(`http://127.0.0.1:8001/api/editar_cv/${id_cv}`, {
      method: 'POST',
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
  <div v-if="cargando" style="text-align:center; padding: 40px;">Cargando CV...</div>
  <div v-else-if="error" style="text-align:center; color:red; padding: 40px;">Error: {{ error }}</div>

  <div v-else class="cv-page-bg">

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

    <div class="europass">

      <header class="ep-header">
        <div class="ep-logo">
          <span class="ep-logo-eu">EU</span>
          <div class="ep-logo-text">
            <span class="ep-logo-title">Europass</span>
            <span class="ep-logo-subtitle">Curriculum Vitae</span>
          </div>
        </div>
        <img v-if="cvData.foto && cvData.foto_base64" :src="cvData.foto_base64" class="ep-photo" alt="Foto de perfil" />
  
      </header>

      <div class="ep-name-bar">
        <h1 class="ep-fullname">
          <span
            contenteditable="true"
            @blur="cvData.datosPersonales.nombre = ($event.target as HTMLElement).innerText.trim()"
          >{{ cvData.datosPersonales.nombre }}</span>
          <strong
            contenteditable="true"
            @blur="cvData.datosPersonales.apellido = ($event.target as HTMLElement).innerText.trim()"
          >{{ cvData.datosPersonales.apellido }}</strong>
        </h1>
        <div class="ep-stars"><span v-for="n in 12" :key="n" class="ep-star">★</span></div>
      </div>

      <div class="ep-body">

        <aside class="ep-sidebar">
          <section class="ep-section">
            <div class="ep-section-title"><span class="ep-section-icon">👤</span> Información personal</div>
            <div class="ep-info-row">
              <span class="ep-info-label">Dirección</span>
              <span class="ep-info-value">
                <span
                  contenteditable="true"
                  @blur="cvData.datosPersonales.direccion = ($event.target as HTMLElement).innerText.trim()"
                >{{ cvData.datosPersonales.direccion }}</span><br />
                <span
                  contenteditable="true"
                  @blur="cvData.datosPersonales.codigo_postal = ($event.target as HTMLElement).innerText.trim()"
                >{{ cvData.datosPersonales.codigo_postal }}</span>
                {{ ' ' }}
                <span
                  contenteditable="true"
                  @blur="cvData.datosPersonales.localidad = ($event.target as HTMLElement).innerText.trim()"
                >{{ cvData.datosPersonales.localidad }}</span>
              </span>
            </div>
            <div class="ep-info-row">
              <span class="ep-info-label">Teléfono</span>
              <span
                class="ep-info-value"
                contenteditable="true"
                @blur="cvData.datosPersonales.telefono = ($event.target as HTMLElement).innerText.trim()"
              >{{ cvData.datosPersonales.telefono }}</span>
            </div>
            <div class="ep-info-row">
              <span class="ep-info-label">Correo electrónico</span>
              <span
                class="ep-info-value ep-email"
                contenteditable="true"
                @blur="cvData.datosPersonales.email = ($event.target as HTMLElement).innerText.trim()"
              >{{ cvData.datosPersonales.email }}</span>
            </div>
            <div v-if="cvData.datosPersonales.permiso_conducir" class="ep-info-row">
              <span class="ep-info-label">Permiso de conducir</span>
              <span class="ep-info-value">B</span>
            </div>
          </section>

          <section class="ep-section">
            <div class="ep-section-title"><span class="ep-section-icon">🌐</span> Idiomas</div>
            <div v-for="(lang, i) in cvData.idiomas" :key="i" class="ep-lang-row">
              <div
                class="ep-lang-name"
                contenteditable="true"
                @blur="lang.nombre = ($event.target as HTMLElement).innerText.trim()"
              >{{ lang.nombre }}</div>
              <div class="ep-lang-cefr">{{ nivelACefr(lang.nivel) }}</div>
              <div class="ep-lang-dots">
                <span v-for="d in 5" :key="d" class="ep-dot" :class="{ filled: d <= nivelADots(lang.nivel) }"></span>
              </div>
            </div>
          </section>
        </aside>

        <main class="ep-main">

          <section v-if="cvData.descripcion" class="ep-section">
            <div class="ep-section-title"><span class="ep-section-icon">👤</span> Perfil profesional</div>
            <p
              class="ep-descripcion"
              contenteditable="true"
              @blur="cvData.descripcion = ($event.target as HTMLElement).innerText.trim()"
            >{{ cvData.descripcion }}</p>
          </section>

          <section class="ep-section">
            <div class="ep-section-title"><span class="ep-section-icon">💼</span> Experiencia laboral</div>
            <div class="ep-timeline">
              <div v-for="(exp, i) in cvData.experiencia" :key="i" class="ep-timeline-item">
                <div class="ep-timeline-left"><div class="ep-timeline-dot"></div><div class="ep-timeline-line"></div></div>
                <div class="ep-timeline-content">
                  <div class="ep-entry-header">
                    <span
                      class="ep-entry-title"
                      contenteditable="true"
                      @blur="exp.puesto = ($event.target as HTMLElement).innerText.trim()"
                    >{{ exp.puesto }}</span>
                    <span class="ep-entry-years">
                      <span
                        contenteditable="true"
                        @blur="exp.fecha_inicio = ($event.target as HTMLElement).innerText.trim()"
                      >{{ exp.fecha_inicio }}</span>
                      —
                      <span
                        contenteditable="true"
                        @blur="exp.fecha_fin = ($event.target as HTMLElement).innerText.trim()"
                      >{{ exp.fecha_fin || 'Presente' }}</span>
                    </span>
                  </div>
                  <div
                    class="ep-entry-subtitle"
                    contenteditable="true"
                    @blur="exp.empresa = ($event.target as HTMLElement).innerText.trim()"
                  >{{ exp.empresa }}</div>
                </div>
              </div>
            </div>
          </section>

          <section class="ep-section">
            <div class="ep-section-title"><span class="ep-section-icon">🎓</span> Educación y formación</div>
            <div class="ep-timeline">
              <div v-for="(edu, i) in cvData.educacion" :key="'edu-'+i" class="ep-timeline-item">
                <div class="ep-timeline-left"><div class="ep-timeline-dot"></div><div class="ep-timeline-line"></div></div>
                <div class="ep-timeline-content">
                  <div class="ep-entry-header">
                    <span
                      class="ep-entry-title"
                      contenteditable="true"
                      @blur="edu.titulo = ($event.target as HTMLElement).innerText.trim()"
                    >{{ edu.titulo }}</span>
                    <span class="ep-entry-years">
                      <span
                        contenteditable="true"
                        @blur="edu.anioInicio = ($event.target as HTMLElement).innerText.trim()"
                      >{{ edu.anioInicio }}</span>
                      —
                      <span
                        contenteditable="true"
                        @blur="edu.anioFin = ($event.target as HTMLElement).innerText.trim()"
                      >{{ edu.anioFin }}</span>
                    </span>
                  </div>
                  <div
                    class="ep-entry-subtitle"
                    contenteditable="true"
                    @blur="edu.institucion = ($event.target as HTMLElement).innerText.trim()"
                  >{{ edu.institucion }}</div>
                </div>
              </div>
              <div v-for="(cert, i) in cvData.certificaciones" :key="'cert-'+i" class="ep-timeline-item">
                <div class="ep-timeline-left"><div class="ep-timeline-dot"></div><div class="ep-timeline-line"></div></div>
                <div class="ep-timeline-content">
                  <div class="ep-entry-header">
                    <span
                      class="ep-entry-title"
                      contenteditable="true"
                      @blur="cert.certificacion = ($event.target as HTMLElement).innerText.trim()"
                    >{{ cert.certificacion }}</span>
                    <span
                      class="ep-entry-years"
                      contenteditable="true"
                      @blur="cert.expedicion = ($event.target as HTMLElement).innerText.trim()"
                    >{{ cert.expedicion }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </main>
      </div>

      <footer class="ep-footer">
        <div class="ep-footer-logo">
          <span class="ep-footer-eu">EU</span>
          <span>© Unión Europea, 2002–2025 · europass.eu</span>
        </div>
        <span>Curriculum Vitae de {{ cvData.datosPersonales.nombre }} {{ cvData.datosPersonales.apellido }}</span>
      </footer>

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
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.cv-page-bg { background: #e8edf5; min-height: 100vh; display: flex; justify-content: center; align-items: flex-start; padding: 40px 16px; font-family: 'Source Sans 3', Arial, sans-serif; }
.europass { width: 210mm; min-height: 297mm; background: #fff; box-shadow: 0 8px 48px rgba(0,30,100,0.18); display: flex; flex-direction: column; font-size: 9pt; color: #222; -webkit-print-color-adjust: exact; print-color-adjust: exact; }

.ep-header { background: #003399; display: flex; align-items: center; justify-content: space-between; padding: 14px 24px 0 20px; }
.ep-logo { display: flex; align-items: center; gap: 10px; }
.ep-logo-eu { background: #ffcc00; color: #003399; font-weight: 900; font-size: 13pt; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; letter-spacing: -0.5px; flex-shrink: 0; }
.ep-logo-text { display: flex; flex-direction: column; line-height: 1.15; }
.ep-logo-title { font-family: 'Source Serif 4', serif; font-size: 14pt; font-weight: 700; color: #fff; letter-spacing: 0.5px; }
.ep-logo-subtitle { font-size: 7.5pt; color: #aac4f0; text-transform: uppercase; letter-spacing: 1.8px; }
.ep-photo { width: 70px; height: 88px; object-fit: cover; border: 2.5px solid rgba(255,255,255,0.8); display: block; }
.ep-photo-placeholder { width: 70px; height: 88px; background: #1a3d7a; border: 2.5px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; }
.ep-photo-placeholder svg { width: 42px; height: 42px; opacity: 0.5; }

.ep-name-bar { background: #003399; padding: 10px 24px 18px 20px; }
.ep-fullname { font-family: 'Source Serif 4', serif; font-size: 22pt; font-weight: 400; color: #fff; letter-spacing: 0.2px; line-height: 1.1; display: flex; gap: 8px; flex-wrap: wrap; }
.ep-fullname strong { font-weight: 700; }
.ep-profesion { font-size: 8.5pt; color: #aac4f0; margin-top: 4px; text-transform: uppercase; letter-spacing: 1.5px; }
.ep-stars { display: flex; gap: 4px; margin-top: 8px; }
.ep-star { color: #ffcc00; font-size: 8pt; }

.ep-body { display: flex; flex: 1; }
.ep-sidebar { width: 68mm; min-width: 68mm; background: #f4f7fc; border-right: 1.5px solid #dde4f0; padding: 22px 16px; display: flex; flex-direction: column; }
.ep-main { flex: 1; padding: 22px 24px; display: flex; flex-direction: column; }
.ep-section { margin-bottom: 20px; }
.ep-section-title { font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 1.4px; color: #003399; border-bottom: 1.5px solid #003399; padding-bottom: 4px; margin-bottom: 12px; display: flex; align-items: center; gap: 5px; }
.ep-section-icon { font-size: 9pt; }
.ep-descripcion { font-size: 8.5pt; color: #555; line-height: 1.7; white-space: pre-line; }
.ep-info-row { display: flex; flex-direction: column; margin-bottom: 9px; }
.ep-info-label { font-size: 7pt; text-transform: uppercase; letter-spacing: 0.9px; color: #6b7fa3; margin-bottom: 1px; }
.ep-info-value { font-size: 8.5pt; color: #222; line-height: 1.45; }
.ep-email { color: #003399; word-break: break-all; }
.ep-lang-row { margin-bottom: 10px; }
.ep-lang-name { font-size: 8.5pt; font-weight: 600; color: #111; margin-bottom: 1px; }
.ep-lang-cefr { font-size: 7pt; color: #6b7fa3; margin-bottom: 3px; }
.ep-lang-dots { display: flex; gap: 3px; }
.ep-dot { width: 10px; height: 10px; border-radius: 50%; border: 1.5px solid #003399; background: transparent; display: inline-block; }
.ep-dot.filled { background: #003399; }
.ep-timeline { position: relative; }
.ep-timeline-item { display: flex; gap: 12px; margin-bottom: 14px; position: relative; }
.ep-timeline-left { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }
.ep-timeline-dot { width: 9px; height: 9px; border-radius: 50%; background: #003399; margin-top: 3px; flex-shrink: 0; position: relative; z-index: 1; }
.ep-timeline-line { width: 1.5px; background: #c5d3e8; flex: 1; margin-top: 2px; }
.ep-timeline-item:last-child .ep-timeline-line { display: none; }
.ep-timeline-content { flex: 1; padding-bottom: 2px; }
.ep-entry-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 2px; }
.ep-entry-title { font-size: 9.5pt; font-weight: 700; color: #111; line-height: 1.2; }
.ep-entry-years { font-size: 7.5pt; color: #003399; font-weight: 600; white-space: nowrap; letter-spacing: 0.3px; text-transform: uppercase; display: flex; align-items: center; gap: 3px; }
.ep-entry-subtitle { font-size: 8.5pt; color: #003399; font-weight: 600; margin-bottom: 3px; }
.ep-footer { border-top: 1px solid #dde4f0; background: #f4f7fc; padding: 7px 24px; display: flex; justify-content: space-between; align-items: center; font-size: 6.5pt; color: #8a9bbb; letter-spacing: 0.4px; }
.ep-footer-logo { display: flex; align-items: center; gap: 5px; }
.ep-footer-eu { background: #003399; color: #ffcc00; font-weight: 900; font-size: 6pt; width: 14px; height: 14px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

[contenteditable]:hover { background: rgba(0, 51, 153, 0.05); border-radius: 2px; }
[contenteditable]:focus { outline: none; background: rgba(0, 51, 153, 0.08); border-radius: 2px; }
.ep-name-bar [contenteditable]:hover { background: rgba(255,255,255,0.1); border-radius: 2px; }
.ep-name-bar [contenteditable]:focus { outline: none; background: rgba(255,255,255,0.15); border-radius: 2px; }

.match-badge { position: fixed; bottom: 28px; right: 28px; width: 64px; height: 64px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 9999; }
.match-rojo     { background: #e53935; }
.match-amarillo { background: #f9a825; }
.match-verde    { background: #2e7d32; }
.match-number { font-size: 16px; font-weight: 700; color: #fff; line-height: 1; }
.match-label  { font-size: 9px; color: rgba(255,255,255,0.85); font-weight: 500; letter-spacing: 0.5px; }

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
}
.btn-download { left: 28px; }
.btn-save     { left: 180px; }
.btn-save:disabled { opacity: 0.35; cursor: not-allowed; }

@media print {
  .cv-page-bg { background: none; padding: 0; }
  .europass { box-shadow: none; width: 100%; min-height: 100vh; }
  .match-badge, .btn-download, .btn-save { display: none; }
  [contenteditable]:hover, [contenteditable]:focus { background: none; }
}
</style>
