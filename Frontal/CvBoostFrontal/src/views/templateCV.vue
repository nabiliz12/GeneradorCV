<script setup lang="ts">

interface Idioma {
  idioma: string
  nivel: string
}

interface Certificacion {
  certificacion: string
  anio: string
}

interface CVData {
  nombre: string
  apellido: string
  direccion: string
  profesion: string
  codigoPostal: string
  Localidad: string
  email: string
  telefono: string
  experiencia: string
  permisoConducir: boolean
  idiomas: Idioma[]
  certificaciones: Certificacion[]
  fotoPerfil?: string | null
}

const props = defineProps<{
  data: CVData
}>()

// Nivel CEFR mapping para Europass
const nivelCEFR: Record<string, string> = {
  Básico: 'A1 / A2',
  Intermedio: 'B1 / B2',
  Avanzado: 'C1',
  Nativo: 'Nativo',
}

const nivelEstrellas: Record<string, number> = {
  Básico: 1,
  Intermedio: 2,
  Avanzado: 3,
  Nativo: 5,
}
</script>

<template>
  <div class="europass">

    <!-- CABECERA AZUL -->
    <header class="ep-header">
      <div class="ep-header-left">
        <div class="ep-logo">
          <span class="ep-logo-eu">EU</span>
          <div class="ep-logo-text">
            <span class="ep-logo-title">Europass</span>
            <span class="ep-logo-subtitle">Curriculum Vitae</span>
          </div>
        </div>
      </div>

      <div class="ep-header-right">
        <img
          v-if="data.fotoPerfil"
          :src="data.fotoPerfil"
          class="ep-photo"
          alt="Foto de perfil"
        />
        <div v-else class="ep-photo-placeholder">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="15" r="8" fill="#b0bec5"/>
            <path d="M4 38c0-8.837 7.163-16 16-16s16 7.163 16 16" fill="#b0bec5"/>
          </svg>
        </div>
      </div>
    </header>

    <!-- NOMBRE GRANDE -->
    <div class="ep-name-bar">
      <h1 class="ep-fullname">{{ data.nombre }} <strong>{{ data.apellido }}</strong></h1>
      <p class="ep-profesion">{{ data.profesion }}</p>
    </div>

    <div class="ep-body">

      <!-- COLUMNA IZQUIERDA -->
      <aside class="ep-sidebar">

        <!-- INFORMACIÓN PERSONAL -->
        <section class="ep-section">
          <div class="ep-section-title">
            <span class="ep-section-icon">👤</span>
            Información personal
          </div>

          <div class="ep-info-row" v-if="data.direccion">
            <span class="ep-info-label">Dirección</span>
            <span class="ep-info-value">
              {{ data.direccion }}<br />
              <span v-if="data.codigoPostal">{{ data.codigoPostal }} </span>
              {{ data.Localidad }}
            </span>
          </div>

          <div class="ep-info-row" v-if="data.telefono">
            <span class="ep-info-label">Teléfono</span>
            <span class="ep-info-value">{{ data.telefono }}</span>
          </div>

          <div class="ep-info-row" v-if="data.email">
            <span class="ep-info-label">Correo</span>
            <span class="ep-info-value ep-email">{{ data.email }}</span>
          </div>

          <div class="ep-info-row" v-if="data.permisoConducir">
            <span class="ep-info-label">Permiso conducir</span>
            <span class="ep-info-value">B</span>
          </div>
        </section>

        <!-- IDIOMAS -->
        <section class="ep-section" v-if="data.idiomas && data.idiomas.length">
          <div class="ep-section-title">
            <span class="ep-section-icon">🌐</span>
            Idiomas
          </div>

          <div
            v-for="(lang, idx) in data.idiomas"
            :key="idx"
            class="ep-lang-row"
          >
            <div class="ep-lang-name">{{ lang.idioma }}</div>
            <div class="ep-lang-level-label">{{ nivelCEFR[lang.nivel] || lang.nivel }}</div>
            <div class="ep-lang-dots">
              <span
                v-for="n in 5"
                :key="n"
                class="ep-dot"
                :class="{ 'ep-dot-filled': n <= (nivelEstrellas[lang.nivel] || 0) }"
              ></span>
            </div>
          </div>
        </section>

      </aside>

      <!-- COLUMNA DERECHA -->
      <main class="ep-main">

        <!-- EXPERIENCIA -->
        <section class="ep-section" v-if="data.experiencia || data.profesion">
          <div class="ep-section-title ep-section-title--main">
            <span class="ep-section-icon">💼</span>
            Experiencia laboral
          </div>

          <div class="ep-timeline-item">
            <div class="ep-timeline-dot"></div>
            <div class="ep-timeline-content">
              <div class="ep-job-title">{{ data.profesion }}</div>
              <div class="ep-job-desc" v-if="data.experiencia">
                {{ data.experiencia }}
              </div>
            </div>
          </div>
        </section>

        <!-- CERTIFICACIONES -->
        <section class="ep-section" v-if="data.certificaciones && data.certificaciones.length">
          <div class="ep-section-title ep-section-title--main">
            <span class="ep-section-icon">🎓</span>
            Educación y formación
          </div>

          <div
            v-for="(cert, idx) in data.certificaciones"
            :key="idx"
            class="ep-timeline-item"
          >
            <div class="ep-timeline-dot"></div>
            <div class="ep-timeline-content">
              <div class="ep-cert-year" v-if="cert.anio">{{ cert.anio }}</div>
              <div class="ep-cert-name">{{ cert.certificacion }}</div>
            </div>
          </div>
        </section>

      </main>
    </div>

    <!-- FOOTER EUROPASS -->
    <footer class="ep-footer">
      <span>© Unión Europea, 2002–{{ new Date().getFullYear() }}</span>
      <span>europass.eu</span>
    </footer>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ── BASE ── */
.europass {
  width: 210mm;
  min-height: 297mm;
  background: #fff;
  font-family: 'Source Sans 3', 'Arial', sans-serif;
  font-size: 9pt;
  color: #222;
  box-shadow: 0 4px 32px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
}

/* ── CABECERA AZUL EUROPASS ── */
.ep-header {
  background: #003399;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px 14px 20px;
}

.ep-header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.ep-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.ep-logo-eu {
  background: #ffcc00;
  color: #003399;
  font-weight: 900;
  font-size: 13pt;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: -0.5px;
}

.ep-logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.ep-logo-title {
  font-family: 'Source Serif 4', serif;
  font-size: 14pt;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.ep-logo-subtitle {
  font-size: 8pt;
  color: #aac4f0;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.ep-photo {
  width: 70px;
  height: 88px;
  object-fit: cover;
  border: 2px solid #fff;
}

.ep-photo-placeholder {
  width: 70px;
  height: 88px;
  background: #e8edf4;
  border: 2px solid #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ep-photo-placeholder svg {
  width: 44px;
  height: 44px;
}

/* ── BARRA DE NOMBRE ── */
.ep-name-bar {
  background: #003399;
  border-top: 1px solid #1a4fad;
  padding: 0 24px 16px 20px;
}

.ep-fullname {
  font-family: 'Source Serif 4', serif;
  font-size: 20pt;
  font-weight: 400;
  color: #fff;
  margin: 0 0 2px 0;
  letter-spacing: 0.2px;
}

.ep-fullname strong {
  font-weight: 700;
}

.ep-profesion {
  font-size: 9pt;
  color: #aac4f0;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1.2px;
}

/* ── BODY: SIDEBAR + MAIN ── */
.ep-body {
  display: flex;
  flex: 1;
}

/* ── SIDEBAR ── */
.ep-sidebar {
  width: 68mm;
  background: #f4f7fc;
  border-right: 1px solid #dde4f0;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* ── MAIN ── */
.ep-main {
  flex: 1;
  padding: 20px 22px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* ── SECTIONS ── */
.ep-section {
  margin-bottom: 18px;
}

.ep-section-title {
  font-size: 8.5pt;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: #003399;
  border-bottom: 1.5px solid #003399;
  padding-bottom: 4px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ep-section-title--main {
  color: #003399;
  border-bottom-color: #003399;
}

.ep-section-icon {
  font-size: 10pt;
}

/* ── INFO ROWS (sidebar) ── */
.ep-info-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 7px;
}

.ep-info-label {
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: #6b7fa3;
  margin-bottom: 1px;
}

.ep-info-value {
  font-size: 8.5pt;
  color: #222;
  line-height: 1.4;
}

.ep-email {
  color: #003399;
  word-break: break-all;
}

/* ── IDIOMAS ── */
.ep-lang-row {
  margin-bottom: 8px;
}

.ep-lang-name {
  font-size: 8.5pt;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 1px;
}

.ep-lang-level-label {
  font-size: 7.5pt;
  color: #6b7fa3;
  margin-bottom: 3px;
}

.ep-lang-dots {
  display: flex;
  gap: 3px;
}

.ep-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1.5px solid #003399;
  background: transparent;
  display: inline-block;
}

.ep-dot-filled {
  background: #003399;
}

/* ── TIMELINE (main) ── */
.ep-timeline-item {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  position: relative;
}

.ep-timeline-dot {
  width: 8px;
  height: 8px;
  min-width: 8px;
  border-radius: 50%;
  background: #003399;
  margin-top: 4px;
  position: relative;
}

.ep-timeline-dot::after {
  content: '';
  position: absolute;
  top: 8px;
  left: 3px;
  width: 1.5px;
  height: 100vh;
  background: #c5d3e8;
  z-index: 0;
}

.ep-timeline-item:last-child .ep-timeline-dot::after {
  display: none;
}

.ep-timeline-content {
  flex: 1;
}

.ep-job-title {
  font-size: 9.5pt;
  font-weight: 600;
  color: #111;
  margin-bottom: 3px;
}

.ep-job-desc {
  font-size: 8.5pt;
  color: #444;
  line-height: 1.5;
  white-space: pre-wrap;
}

.ep-cert-year {
  font-size: 7.5pt;
  font-weight: 600;
  color: #003399;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 1px;
}

.ep-cert-name {
  font-size: 8.5pt;
  color: #222;
}

/* ── FOOTER ── */
.ep-footer {
  border-top: 1px solid #dde4f0;
  background: #f4f7fc;
  padding: 6px 24px;
  display: flex;
  justify-content: space-between;
  font-size: 7pt;
  color: #8a9bbb;
  letter-spacing: 0.5px;
}
</style>
