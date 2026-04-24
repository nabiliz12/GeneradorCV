<script setup lang="ts">
const props = defineProps<{
  nombre?: string
  apellido?: string
  profesion?: string
  email?: string
  telefono?: string
  direccion?: string
  codigoPostal?: string
  localidad?: string
  permisoConducir?: boolean
  foto?: string | null
  educacion?: { institucion: string; titulo: string; anioInicio: string; anioFin: string }[]
  certificaciones?: { certificacion: string; expedicion: string }[]
  experiencia?: { empresa: string; cargo: string; anioInicio: string; anioFin: string }[]
  idiomas?: { idioma: string; nivel: string }[]
}>()

function nivelADots(nivel: string): number {
  const map: Record<string, number> = {
    'Básico': 1,
    'Intermedio': 2,
    'Avanzado': 3,
    'Nativo': 5
  }
  return map[nivel] ?? 2
}

function nivelACefr(nivel: string): string {
  const map: Record<string, string> = {
    'Básico': 'A1 / A2',
    'Intermedio': 'B1 / B2',
    'Avanzado': 'C1',
    'Nativo': 'Nativo'
  }
  return map[nivel] ?? nivel
}
</script>

<template>
  <!-- Fondo gris igual que el body del HTML original -->
  <div class="cv-page-bg">
    <div class="europass">

      <!-- ══ HEADER ══ -->
      <header class="ep-header">
        <div class="ep-logo">
          <span class="ep-logo-eu">EU</span>
          <div class="ep-logo-text">
            <span class="ep-logo-title">Europass</span>
            <span class="ep-logo-subtitle">Curriculum Vitae</span>
          </div>
        </div>

        <img v-if="foto" :src="foto" class="ep-photo" alt="Foto de perfil" />
        <div v-else class="ep-photo-placeholder">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="15" r="8" fill="#b0bec5"/>
            <path d="M4 38c0-8.837 7.163-16 16-16s16 7.163 16 16" fill="#b0bec5"/>
          </svg>
        </div>
      </header>

      <!-- ══ NOMBRE ══ -->
      <div class="ep-name-bar">
        <h1 class="ep-fullname">
          {{ nombre }} <strong>{{ apellido }}</strong>
        </h1>
        <p class="ep-profesion">{{ profesion }}</p>
        <div class="ep-stars">
          <span class="ep-star">★</span><span class="ep-star">★</span><span class="ep-star">★</span>
          <span class="ep-star">★</span><span class="ep-star">★</span><span class="ep-star">★</span>
          <span class="ep-star">★</span><span class="ep-star">★</span><span class="ep-star">★</span>
          <span class="ep-star">★</span><span class="ep-star">★</span><span class="ep-star">★</span>
        </div>
      </div>

      <!-- ══ BODY ══ -->
      <div class="ep-body">

        <!-- ── SIDEBAR ── -->
        <aside class="ep-sidebar">

          <!-- INFORMACIÓN PERSONAL -->
          <section class="ep-section">
            <div class="ep-section-title">
              <span class="ep-section-icon">👤</span>
              Información personal
            </div>

            <div class="ep-info-row">
              <span class="ep-info-label">Dirección</span>
              <span class="ep-info-value">
                {{ direccion }}<br />
                {{ codigoPostal }} {{ localidad }}
              </span>
            </div>

            <div class="ep-info-row">
              <span class="ep-info-label">Teléfono</span>
              <span class="ep-info-value">{{ telefono }}</span>
            </div>

            <div class="ep-info-row">
              <span class="ep-info-label">Correo electrónico</span>
              <span class="ep-info-value ep-email">{{ email }}</span>
            </div>

            <div v-if="permisoConducir" class="ep-info-row">
              <span class="ep-info-label">Permiso de conducir</span>
              <span class="ep-info-value">B</span>
            </div>
          </section>

          <!-- IDIOMAS -->
          <section class="ep-section">
            <div class="ep-section-title">
              <span class="ep-section-icon">🌐</span>
              Idiomas
            </div>

            <div v-for="(lang, i) in idiomas" :key="i" class="ep-lang-row">
              <div class="ep-lang-name">{{ lang.idioma }}</div>
              <div class="ep-lang-cefr">{{ nivelACefr(lang.nivel) }}</div>
              <div class="ep-lang-dots">
                <span
                  v-for="d in 5"
                  :key="d"
                  class="ep-dot"
                  :class="{ filled: d <= nivelADots(lang.nivel) }"
                ></span>
              </div>
            </div>
          </section>

        </aside>

        <!-- ── MAIN ── -->
        <main class="ep-main">

          <!-- EXPERIENCIA LABORAL -->
          <section class="ep-section">
            <div class="ep-section-title">
              <span class="ep-section-icon">💼</span>
              Experiencia laboral
            </div>

            <div class="ep-timeline">
              <div v-for="(exp, i) in experiencia" :key="i" class="ep-timeline-item">
                <div class="ep-timeline-left">
                  <div class="ep-timeline-dot"></div>
                  <div class="ep-timeline-line"></div>
                </div>
                <div class="ep-timeline-content">
                  <div class="ep-entry-header">
                    <span class="ep-entry-title">{{ exp.cargo }}</span>
                    <span class="ep-entry-years">{{ exp.anioInicio }} — {{ exp.anioFin || 'Presente' }}</span>
                  </div>
                  <div class="ep-entry-subtitle">{{ exp.empresa }}</div>
                </div>
              </div>
            </div>
          </section>

          <!-- EDUCACIÓN Y FORMACIÓN -->
          <section class="ep-section">
            <div class="ep-section-title">
              <span class="ep-section-icon">🎓</span>
              Educación y formación
            </div>

            <div class="ep-timeline">
              <div v-for="(edu, i) in educacion" :key="'edu-' + i" class="ep-timeline-item">
                <div class="ep-timeline-left">
                  <div class="ep-timeline-dot"></div>
                  <div class="ep-timeline-line"></div>
                </div>
                <div class="ep-timeline-content">
                  <div class="ep-entry-header">
                    <span class="ep-entry-title">{{ edu.titulo }}</span>
                    <span class="ep-entry-years">{{ edu.anioInicio }} — {{ edu.anioFin }}</span>
                  </div>
                  <div class="ep-entry-subtitle">{{ edu.institucion }}</div>
                </div>
              </div>

              <div v-for="(cert, i) in certificaciones" :key="'cert-' + i" class="ep-timeline-item">
                <div class="ep-timeline-left">
                  <div class="ep-timeline-dot"></div>
                  <div class="ep-timeline-line"></div>
                </div>
                <div class="ep-timeline-content">
                  <div class="ep-entry-header">
                    <span class="ep-entry-title">{{ cert.certificacion }}</span>
                    <span class="ep-entry-years">{{ cert.expedicion }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </main>
      </div>

      <!-- ══ FOOTER ══ -->
      <footer class="ep-footer">
        <div class="ep-footer-logo">
          <span class="ep-footer-eu">EU</span>
          <span>© Unión Europea, 2002–2025 · europass.eu</span>
        </div>
        <span>Curriculum Vitae de {{ nombre }} {{ apellido }}</span>
      </footer>

    </div>
  </div>
</template>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── FONDO GRIS, hoja centrada, igual que el body del HTML original ── */
.cv-page-bg {
  background: #e8edf5;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 16px;
  font-family: 'Source Sans 3', Arial, sans-serif;
}

/* ── HOJA A4 ── */
.europass {
  width: 210mm;
  min-height: 297mm;
  background: #fff;
  box-shadow: 0 8px 48px rgba(0,30,100,0.18);
  display: flex;
  flex-direction: column;
  font-size: 9pt;
  color: #222;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

/* HEADER */
.ep-header {
  background: #003399;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px 0 20px;
}

.ep-logo { display: flex; align-items: center; gap: 10px; }

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
  flex-shrink: 0;
}

.ep-logo-text { display: flex; flex-direction: column; line-height: 1.15; }

.ep-logo-title {
  font-family: 'Source Serif 4', serif;
  font-size: 14pt;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.ep-logo-subtitle {
  font-size: 7.5pt;
  color: #aac4f0;
  text-transform: uppercase;
  letter-spacing: 1.8px;
}

.ep-photo {
  width: 70px;
  height: 88px;
  object-fit: cover;
  border: 2.5px solid rgba(255,255,255,0.8);
  display: block;
}

.ep-photo-placeholder {
  width: 70px;
  height: 88px;
  background: #1a3d7a;
  border: 2.5px solid rgba(255,255,255,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.ep-photo-placeholder svg { width: 42px; height: 42px; opacity: 0.5; }

/* NAME BAR */
.ep-name-bar {
  background: #003399;
  padding: 10px 24px 18px 20px;
}

.ep-fullname {
  font-family: 'Source Serif 4', serif;
  font-size: 22pt;
  font-weight: 400;
  color: #fff;
  letter-spacing: 0.2px;
  line-height: 1.1;
}

.ep-fullname strong { font-weight: 700; }

.ep-profesion {
  font-size: 8.5pt;
  color: #aac4f0;
  margin-top: 4px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.ep-stars { display: flex; gap: 4px; margin-top: 8px; }
.ep-star { color: #ffcc00; font-size: 8pt; }

/* BODY */
.ep-body { display: flex; flex: 1; }

/* SIDEBAR */
.ep-sidebar {
  width: 68mm;
  min-width: 68mm;
  background: #f4f7fc;
  border-right: 1.5px solid #dde4f0;
  padding: 22px 16px;
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* MAIN */
.ep-main {
  flex: 1;
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
}

/* SECTIONS */
.ep-section { margin-bottom: 20px; }

.ep-section-title {
  font-size: 7.5pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.4px;
  color: #003399;
  border-bottom: 1.5px solid #003399;
  padding-bottom: 4px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.ep-section-icon { font-size: 9pt; }

/* INFO ROWS */
.ep-info-row { display: flex; flex-direction: column; margin-bottom: 9px; }

.ep-info-label {
  font-size: 7pt;
  text-transform: uppercase;
  letter-spacing: 0.9px;
  color: #6b7fa3;
  margin-bottom: 1px;
}

.ep-info-value { font-size: 8.5pt; color: #222; line-height: 1.45; }
.ep-email { color: #003399; word-break: break-all; }

/* IDIOMAS */
.ep-lang-row { margin-bottom: 10px; }
.ep-lang-name { font-size: 8.5pt; font-weight: 600; color: #111; margin-bottom: 1px; }
.ep-lang-cefr { font-size: 7pt; color: #6b7fa3; margin-bottom: 3px; }
.ep-lang-dots { display: flex; gap: 3px; }

.ep-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1.5px solid #003399;
  background: transparent;
  display: inline-block;
}

.ep-dot.filled { background: #003399; }

/* TIMELINE */
.ep-timeline { position: relative; }

.ep-timeline-item {
  display: flex;
  gap: 12px;
  margin-bottom: 14px;
  position: relative;
}

.ep-timeline-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.ep-timeline-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #003399;
  margin-top: 3px;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.ep-timeline-line {
  width: 1.5px;
  background: #c5d3e8;
  flex: 1;
  margin-top: 2px;
}

.ep-timeline-item:last-child .ep-timeline-line { display: none; }

.ep-timeline-content { flex: 1; padding-bottom: 2px; }

.ep-entry-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 2px;
}

.ep-entry-title { font-size: 9.5pt; font-weight: 700; color: #111; line-height: 1.2; }

.ep-entry-years {
  font-size: 7.5pt;
  color: #003399;
  font-weight: 600;
  white-space: nowrap;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.ep-entry-subtitle { font-size: 8.5pt; color: #003399; font-weight: 600; margin-bottom: 3px; }
.ep-entry-desc { font-size: 8.5pt; color: #555; line-height: 1.55; }

/* FOOTER */
.ep-footer {
  border-top: 1px solid #dde4f0;
  background: #f4f7fc;
  padding: 7px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 6.5pt;
  color: #8a9bbb;
  letter-spacing: 0.4px;
}

.ep-footer-logo { display: flex; align-items: center; gap: 5px; }

.ep-footer-eu {
  background: #003399;
  color: #ffcc00;
  font-weight: 900;
  font-size: 6pt;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* PRINT */
@media print {
  .cv-page-bg { background: none; padding: 0; }
  .europass { box-shadow: none; width: 100%; min-height: 100vh; }
}
</style>
