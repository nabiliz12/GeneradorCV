<script></script>

<template>
  <div class="cv-page">
    <!-- Header -->
    <header class="cv-header">
      <h1 class="cv-name">{{ cv.name }}</h1>
      <div class="cv-contact">
        <span>{{ cv.phone }}</span>
        <span class="sep">|</span>
        <span>{{ cv.email }}</span>
        <span class="sep">|</span>
        <span>{{ cv.location }}</span>
        <span class="sep">|</span>
        <span>{{ cv.linkedin }}</span>
      </div>
    </header>

    <!-- Resumen -->
    <section class="cv-section">
      <h2 class="cv-section-title">RESUMEN</h2>
      <p class="cv-summary">{{ cv.resumen }}</p>
    </section>

    <!-- Experiencia Profesional -->
    <section class="cv-section">
      <h2 class="cv-section-title">EXPERIENCIA PROFESIONAL</h2>
      <div
        v-for="(exp, i) in cv.experiencia"
        :key="i"
        class="cv-entry"
      >
        <div class="cv-entry-header">
          <span class="cv-entry-title">{{ exp.puesto }}</span>
          <span class="cv-entry-date">{{ exp.fechas }}</span>
        </div>
        <div class="cv-entry-subtitle">{{ exp.empresa }} | {{ exp.ubicacion }}</div>
        <ul class="cv-bullets">
          <li v-for="(b, j) in exp.bullets" :key="j">{{ b }}</li>
        </ul>
      </div>
    </section>

    <!-- Educación -->
    <section class="cv-section">
      <h2 class="cv-section-title">EDUCACIÓN</h2>
      <div
        v-for="(edu, i) in cv.educacion"
        :key="i"
        class="cv-entry"
      >
        <div class="cv-entry-header">
          <span class="cv-entry-title">{{ edu.institucion }}</span>
          <span class="cv-entry-date">{{ edu.fecha }}</span>
        </div>
        <div class="cv-entry-subtitle">{{ edu.titulo }}</div>
      </div>
    </section>

    <!-- Habilidades -->
    <section class="cv-section">
      <h2 class="cv-section-title">HABILIDADES</h2>
      <p class="cv-skills-line" v-if="cv.habilidades.tecnicas">
        <strong>Habilidades técnicas</strong>: {{ cv.habilidades.tecnicas }}
      </p>
      <p class="cv-skills-line" v-if="cv.habilidades.blandas">
        <strong>Habilidades blandas</strong>: {{ cv.habilidades.blandas }}
      </p>
      <p class="cv-skills-line" v-if="cv.habilidades.idiomas">
        <strong>Idiomas</strong>: {{ cv.habilidades.idiomas }}
      </p>
    </section>

    <!-- Certificaciones -->
    <section class="cv-section">
      <h2 class="cv-section-title">CERTIFICACIONES (opcional)</h2>
      <div
        v-for="(cert, i) in cv.certificaciones"
        :key="i"
        class="cv-entry"
      >
        <div class="cv-entry-header">
          <span class="cv-entry-title">{{ cert.nombre }}</span>
          <span class="cv-entry-date">{{ cert.fecha }}</span>
        </div>
        <div class="cv-entry-subtitle" v-if="cert.entidad">{{ cert.entidad }}</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const cv = reactive({
  name: 'NOMBRE APELLIDO',
  phone: '000-000-0000',
  email: 'tuemail@gmail.com',
  location: 'Ciudad, País',
  linkedin: 'linkedin.com/in/usuario',

  resumen:
    '[Tu título profesional] con [X años] de experiencia en [Industria/Sector]. Conocido por [Fortaleza clave #1] y [Fortaleza clave #2]. Éxito demostrado en [Tarea o logro específico]. Experto en [Habilidad o Actividad], con una sólida formación en [Habilidad o Campo Relacionado].',

  experiencia: [
    {
      puesto: 'Tu título de trabajo más reciente',
      fechas: '9/2023 – Actualidad',
      empresa: 'Nombre de la empresa',
      ubicacion: 'Ubicación',
      bullets: [
        'Viñeta que describe una responsabilidad o logro clave.',
        'Viñeta que resalta una habilidad o proyecto en particular.',
        'Otro punto o logro relevante.',
      ],
    },
    {
      puesto: 'Título de trabajo anterior',
      fechas: '8/2020 – 9/2023',
      empresa: 'Nombre de la empresa',
      ubicacion: 'Ubicación',
      bullets: [
        'Viñeta que describe una responsabilidad o logro clave.',
        'Viñeta que resalta una habilidad o proyecto en particular.',
        'Otro punto o logro relevante.',
      ],
    },
    {
      puesto: 'Título de trabajo anterior',
      fechas: '9/2019 – 7/2020',
      empresa: 'Nombre de la empresa',
      ubicacion: 'Ubicación',
      bullets: [
        'Viñeta que describe una responsabilidad o logro clave.',
        'Viñeta que resalta una habilidad o proyecto en particular.',
        'Otro punto o logro relevante.',
      ],
    },
  ],

  educacion: [
    {
      institucion: 'Nombre de la Universidad, Ubicación',
      fecha: '5/2022',
      titulo: 'Licenciatura en [Especialidad]',
    },
    {
      institucion: 'Nombre de la Universidad, Ubicación',
      fecha: '5/2019',
      titulo: 'Licenciatura, Especialidad',
    },
  ],

  habilidades: {
    tecnicas: 'Microsoft Office, Adobe Photoshop, redacción técnica, análisis de datos.',
    blandas: 'comunicación, trabajo en equipo, resolución de problemas, adaptabilidad, gestión del tiempo.',
    idiomas: 'español (nivel A2), francés (nivel B1), inglés (lengua materna).',
  },

  certificaciones: [
    {
      nombre: 'Nombre de la certificación',
      fecha: '5/2023',
      entidad: 'Entidad emisora',
    },
  ],
})
</script>

<style scoped>
/* ── Página ── */
.cv-page {
  width: 210mm;
  min-height: 297mm;
  margin: 0 auto;
  padding: 18mm 20mm;
  background: #ffffff;
  font-family: 'Calibri', 'Trebuchet MS', sans-serif;
  font-size: 10.5pt;
  color: #222222;
  box-sizing: border-box;
}

/* ── Cabecera ── */
.cv-header {
  text-align: center;
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 2px solid #2c4a6e;
}

.cv-name {
  font-size: 22pt;
  font-weight: 700;
  letter-spacing: 1px;
  color: #1a1a1a;
  margin: 0 0 4px 0;
  text-transform: uppercase;
}

.cv-contact {
  font-size: 9.5pt;
  color: #444;
}

.cv-contact .sep {
  margin: 0 6px;
  color: #888;
}

/* ── Secciones ── */
.cv-section {
  margin-top: 14px;
}

.cv-section-title {
  font-size: 10pt;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #2c4a6e;
  background-color: #dce6f0;
  padding: 3px 6px;
  margin: 0 0 8px 0;
  text-transform: uppercase;
}

/* ── Entradas (experiencia / educación / certs) ── */
.cv-entry {
  margin-bottom: 10px;
}

.cv-entry-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.cv-entry-title {
  font-weight: 600;
  font-size: 10.5pt;
  color: #1a1a1a;
}

.cv-entry-date {
  font-size: 10pt;
  color: #333;
  white-space: nowrap;
}

.cv-entry-subtitle {
  font-style: italic;
  font-size: 10pt;
  color: #444;
  margin-top: 1px;
  margin-bottom: 4px;
}

/* ── Bullets ── */
.cv-bullets {
  margin: 4px 0 0 18px;
  padding: 0;
  list-style: disc;
}

.cv-bullets li {
  margin-bottom: 2px;
  font-size: 10.5pt;
  line-height: 1.45;
}

/* ── Resumen ── */
.cv-summary {
  margin: 0;
  line-height: 1.5;
  text-align: justify;
  font-size: 10.5pt;
}

/* ── Habilidades ── */
.cv-skills-line {
  margin: 0 0 4px 0;
  font-size: 10.5pt;
  line-height: 1.5;
}

/* ── Print ── */
@media print {
  .cv-page {
    width: 210mm;
    padding: 15mm 18mm;
    box-shadow: none;
  }
}
</style>
