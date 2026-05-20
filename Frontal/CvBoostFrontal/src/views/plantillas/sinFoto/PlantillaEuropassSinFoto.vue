
<script setup>
import { reactive } from 'vue'

const cv = reactive({
  nombre: 'Nombre Apellido',
  nationality: 'Española',
  dob: 'DD/MM/AAAA',
  gender: 'Femenino',
  phoneHome: '(+34) 000 000 000',
  phoneMobile: '(+34) 600 000 000',
  email: 'email@ejemplo.com',
  linkedin: 'www.linkedin.com/in/tu-perfil',
  address: 'Calle Ejemplo 1, 28001 Madrid (España)',

  aboutMe:
    '[Tu título profesional] con más de [X] años de experiencia en [sector/industria]. Habilidad demostrada para [competencia clave]. Orientado/a a resultados con capacidad para [otra fortaleza].',

  workExperience: [
    {
      title: 'Título del puesto',
      organization: 'Nombre de la organización',
      dates: 'MM/AAAA – Actualidad',
      address: 'Dirección, Ciudad, País',
      city: null,
      country: null,
      bullets: [
        '— Descripción de una responsabilidad o logro clave.',
        '— Otra responsabilidad o resultado destacado.',
      ],
    },
    {
      title: 'Título del puesto anterior',
      organization: 'Nombre de la organización',
      dates: 'MM/AAAA – MM/AAAA',
      address: null,
      city: 'Ciudad',
      country: 'País',
      bullets: [
        '— Descripción de una responsabilidad o logro clave.',
        '— Otra responsabilidad o resultado destacado.',
        '— Tercer punto relevante.',
      ],
    },
  ],

  education: [
    {
      title: 'Título académico – Nombre del programa o especialidad',
      institution: 'Nombre de la Universidad',
      dates: 'AAAA – AAAA',
      city: 'Ciudad',
      country: 'País',
      bullets: [],
    },
    {
      title: 'Otro título o certificado',
      institution: 'Centro educativo',
      dates: 'AAAA – AAAA',
      city: 'Ciudad',
      country: 'País',
      bullets: [],
    },
  ],

  languages: [
    {
      name: 'Inglés',
      listening: 'C1',
      reading: 'C1',
      spokenInteraction: 'B2',
      spokenProduction: 'B2',
      writing: 'C1',
    },
    {
      name: 'Francés',
      listening: 'B1',
      reading: 'B1',
      spokenInteraction: 'A2',
      spokenProduction: 'A2',
      writing: 'B1',
    },
  ],

  digitalSkills: 'Microsoft Office, Google Workspace, [herramienta específica], [otra herramienta].',

  additionalInfo: 'Permiso de conducir B. Disponibilidad para viajar. [Otras menciones relevantes].',
})
</script>


<template>
  <div class="cv-page">

    <!-- Logo Europass -->
    <div class="ep-logo">
      <div class="ep-flag">
        <svg viewBox="0 0 60 40" xmlns="http://www.w3.org/2000/svg" width="52" height="36">
          <rect width="60" height="40" fill="#003399"/>
          <g transform="translate(30,20)">
            <circle v-for="(star, i) in 12" :key="i"
              :cx="Math.round(Math.sin((i * 30) * Math.PI / 180) * 11)"
              :cy="Math.round(-Math.cos((i * 30) * Math.PI / 180) * 11)"
              r="2" fill="#FFCC00"/>
          </g>
        </svg>
      </div>
      <span class="ep-wordmark">europass</span>
    </div>

    <!-- Nombre -->
    <h1 class="ep-name">{{ cv.nombre }}</h1>

    <!-- Info personal línea 1 -->
    <div class="ep-personal-row">
      <span><strong>Nationality:</strong> {{ cv.nationality }}</span>
      <span><strong>Date of birth:</strong> {{ cv.dob }}</span>
      <span><strong>Gender:</strong> {{ cv.gender }}</span>
      <span>🏠 <strong>Phone number:</strong> {{ cv.phoneHome }}</span>
    </div>
    <!-- Info personal línea 2 -->
    <div class="ep-personal-row">
      <span>📞 <strong>Phone number:</strong> {{ cv.phoneMobile }}</span>
      <span>✉️ <strong>Email address:</strong>
        <a :href="'mailto:' + cv.email">{{ cv.email }}</a>
      </span>
    </div>
    <!-- LinkedIn -->
    <div class="ep-personal-row">
      <span>
        <svg class="ep-icon" viewBox="0 0 24 24" fill="#0077B5"><path d="M19 0H5C2.24 0 0 2.24 0 5v14c0 2.76 2.24 5 5 5h14c2.76 0 5-2.24 5-5V5c0-2.76-2.24-5-5-5zM8 19H5V9h3v10zM6.5 7.73C5.53 7.73 4.75 6.95 4.75 6S5.53 4.27 6.5 4.27 8.25 5.05 8.25 6 7.47 7.73 6.5 7.73zM20 19h-3v-5.6c0-1.34-.03-3.07-1.87-3.07-1.87 0-2.16 1.46-2.16 2.97V19h-3V9h2.88v1.36h.04c.4-.76 1.38-1.56 2.84-1.56 3.04 0 3.6 2 3.6 4.59V19z"/></svg>
        <strong>LinkedIn:</strong>
        <a :href="cv.linkedin" target="_blank">{{ cv.linkedin }}</a>
      </span>
    </div>
    <!-- Home address -->
    <div class="ep-personal-row">
      <span>📍 <strong>Home:</strong> {{ cv.address }}</span>
    </div>

    <!-- ABOUT ME -->
    <section class="ep-section">
      <h2 class="ep-section-title">ABOUT ME</h2>
      <p class="ep-text">{{ cv.aboutMe }}</p>
    </section>

    <!-- WORK EXPERIENCE -->
    <section class="ep-section">
      <h2 class="ep-section-title">WORK EXPERIENCE</h2>
      <div v-for="(job, i) in cv.workExperience" :key="i" class="ep-entry">
        <div class="ep-job-title">{{ job.title }}</div>
        <div class="ep-job-org">
          <em>{{ job.organization }}</em>
          <span class="ep-dates"> [ {{ job.dates }} ]</span>
        </div>
        <div class="ep-job-address" v-if="job.address">
          <strong>Address:</strong> {{ job.address }}
        </div>
        <div class="ep-job-city" v-if="job.city">
          <strong>City:</strong> {{ job.city }}
        </div>
        <div class="ep-job-country" v-if="job.country">
          <strong>Country:</strong> {{ job.country }}
        </div>
        <ul class="ep-bullets">
          <li v-for="(b, j) in job.bullets" :key="j">{{ b }}</li>
        </ul>
      </div>
    </section>

    <!-- EDUCATION AND TRAINING -->
    <section class="ep-section">
      <h2 class="ep-section-title">EDUCATION AND TRAINING</h2>
      <div v-for="(edu, i) in cv.education" :key="i" class="ep-entry">
        <div class="ep-job-title">{{ edu.title }}</div>
        <div class="ep-job-org">
          <em>{{ edu.institution }}</em>
          <span class="ep-dates"> [ {{ edu.dates }} ]</span>
        </div>
        <div class="ep-job-city" v-if="edu.city">
          <strong>City:</strong> {{ edu.city }}
        </div>
        <div class="ep-job-country" v-if="edu.country">
          <strong>Country:</strong> {{ edu.country }}
        </div>
        <ul class="ep-bullets" v-if="edu.bullets && edu.bullets.length">
          <li v-for="(b, j) in edu.bullets" :key="j">{{ b }}</li>
        </ul>
      </div>
    </section>

    <!-- LANGUAGE SKILLS -->
    <section class="ep-section" v-if="cv.languages && cv.languages.length">
      <h2 class="ep-section-title">LANGUAGE SKILLS</h2>
      <table class="ep-lang-table">
        <thead>
          <tr>
            <th></th>
            <th colspan="2">UNDERSTANDING</th>
            <th colspan="2">SPEAKING</th>
            <th>WRITING</th>
          </tr>
          <tr class="ep-lang-subheader">
            <th></th>
            <th>Listening</th>
            <th>Reading</th>
            <th>Spoken interaction</th>
            <th>Spoken production</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(lang, i) in cv.languages" :key="i">
            <td class="ep-lang-name">{{ lang.name }}</td>
            <td>{{ lang.listening }}</td>
            <td>{{ lang.reading }}</td>
            <td>{{ lang.spokenInteraction }}</td>
            <td>{{ lang.spokenProduction }}</td>
            <td>{{ lang.writing }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- DIGITAL SKILLS -->
    <section class="ep-section" v-if="cv.digitalSkills">
      <h2 class="ep-section-title">DIGITAL SKILLS</h2>
      <p class="ep-text">{{ cv.digitalSkills }}</p>
    </section>

    <!-- ADDITIONAL INFO -->
    <section class="ep-section" v-if="cv.additionalInfo">
      <h2 class="ep-section-title">ADDITIONAL INFORMATION</h2>
      <p class="ep-text">{{ cv.additionalInfo }}</p>
    </section>

    <!-- Footer verde -->
    <div class="ep-footer-bar"></div>
  </div>
</template>

<style scoped>
/* ── Página ── */
.cv-page {
  width: 210mm;
  min-height: 297mm;
  margin: 0 auto;
  padding: 14mm 18mm 20mm;
  background: #ffffff;
  font-family: 'Arial', 'Helvetica Neue', sans-serif;
  font-size: 9.5pt;
  color: #1a1a1a;
  box-sizing: border-box;
  position: relative;
  border-left: 8px solid #00857a;
}

/* ── Logo Europass ── */
.ep-logo {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-bottom: 14px;
}

.ep-flag svg {
  display: block;
}

.ep-wordmark {
  font-size: 22pt;
  font-weight: 300;
  color: #00857a;
  letter-spacing: 1px;
}

/* ── Nombre ── */
.ep-name {
  font-size: 16pt;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

/* ── Datos personales ── */
.ep-personal-row {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  font-size: 9pt;
  margin-bottom: 3px;
  align-items: center;
}

.ep-personal-row a {
  color: #0051a5;
  text-decoration: none;
}

.ep-personal-row a:hover {
  text-decoration: underline;
}

.ep-icon {
  width: 12px;
  height: 12px;
  vertical-align: middle;
  margin-right: 3px;
}

/* ── Secciones ── */
.ep-section {
  margin-top: 16px;
}

.ep-section-title {
  font-size: 9.5pt;
  font-weight: 700;
  text-transform: uppercase;
  color: #1a1a1a;
  border-bottom: 1.5px solid #00857a;
  padding-bottom: 2px;
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
}

/* ── Entradas de experiencia / educación ── */
.ep-entry {
  margin-bottom: 12px;
}

.ep-job-title {
  font-weight: 700;
  font-size: 10pt;
  margin-bottom: 1px;
}

.ep-job-org {
  font-size: 9.5pt;
  margin-bottom: 2px;
}

.ep-job-org em {
  font-style: italic;
  font-weight: 600;
}

.ep-dates {
  font-style: normal;
  font-weight: 400;
  color: #333;
}

.ep-job-address,
.ep-job-city,
.ep-job-country {
  font-size: 9.5pt;
  margin-bottom: 1px;
}

/* ── Bullets (guiones) ── */
.ep-bullets {
  list-style: none;
  padding: 0;
  margin: 4px 0 0 0;
}

.ep-bullets li {
  margin-bottom: 3px;
  line-height: 1.45;
  font-size: 9.5pt;
}

/* ── Texto libre ── */
.ep-text {
  margin: 0;
  line-height: 1.5;
  font-size: 9.5pt;
}

/* ── Tabla de idiomas ── */
.ep-lang-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9pt;
  margin-top: 4px;
}

.ep-lang-table th {
  background: #e8f5f4;
  color: #1a1a1a;
  font-weight: 700;
  border: 1px solid #bbb;
  padding: 4px 6px;
  text-align: center;
  font-size: 8.5pt;
}

.ep-lang-subheader th {
  background: #f4fafa;
  font-weight: 600;
}

.ep-lang-table td {
  border: 1px solid #bbb;
  padding: 4px 6px;
  text-align: center;
}

.ep-lang-name {
  text-align: left !important;
  font-weight: 600;
}

/* ── Barra verde inferior ── */
.ep-footer-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 10px;
  background: #00857a;
}

/* ── Print ── */
@media print {
  .cv-page {
    width: 210mm;
    padding: 12mm 16mm 18mm;
    box-shadow: none;
  }
  .ep-footer-bar {
    position: fixed;
  }
}
</style>
