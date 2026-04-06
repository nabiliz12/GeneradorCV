<script setup lang="ts">
import { reactive } from 'vue';

interface FormData {
  nombre: string
  email: string
  experiencia: string
}

const cv = reactive({
  name: "Nombre Apellido",
  email: "tuemail@email.com",
  phone: "600000000",
  address: "Ciudad, País",
  nationality: "Española",
  birthDate: "01/01/2000",

  experience: [
    {
      position:  "Desarrollador Frontend",
      company: "Empresa X",
      start: "2024",
      end: "Actualidad",
      description: "Desarrollo de aplicaciones web modernas"
    }
  ],

  education: [
    {
      title: "DAM - Desarrollo de Aplicaciones Multiplataforma",
      center: "Instituto X",
      start: "2023",
      end: "2025"
    }
  ],

  skills: ["Vue", "Angular", "Java", "HTML", "CSS"],

  languages: [
    { name: "Español", level: "Nativo" },
    { name: "Inglés", level: "Intermedio" }
  ]
})

async function descargarPdf() {
  const response = await fetch('http://127.0.0.1:8001/api/form/descargarpdf', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(cv)
  })

  const blob = await response.blob()
  const url = URL.createObjectURL(blob)

  const link = document.createElement('a')
  link.href = url
  link.download = 'cv-europass.pdf'
  link.click()

  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="cv-wrapper">

    <div class="cv">

      <!-- SIDEBAR -->
      <div class="sidebar">
        <h1>{{ cv.name }}</h1>

        <div class="block">
          <h3>Contacto</h3>
          <p>{{ cv.email }}</p>
          <p>{{ cv.phone }}</p>
          <p>{{ cv.address }}</p>
        </div>

        <div class="block">
          <h3>Información personal</h3>
          <p>Nacionalidad: {{ cv.nationality }}</p>
          <p>Fecha nacimiento: {{ cv.birthDate }}</p>
        </div>

        <div class="block">
          <h3>Idiomas</h3>
          <ul>
            <li v-for="(lang, i) in cv.languages" :key="i">
              {{ lang.name }} - {{ lang.level }}
            </li>
          </ul>
        </div>

        <div class="block">
          <h3>Competencias</h3>
          <ul>
            <li v-for="(skill, i) in cv.skills" :key="i">
              {{ skill }}
            </li>
          </ul>
        </div>
      </div>

      <!-- MAIN -->
      <div class="main">

        <div class="section">
          <h2>Experiencia laboral</h2>
          <div v-for="(job, i) in cv.experience" :key="i" class="item">
            <div class="row">
              <div class="date">{{ job.start }} - {{ job.end }}</div>
              <div>
                <strong>{{ job.position }}</strong>
                <p class="company">{{ job.company }}</p>
                <p>{{ job.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="section">
          <h2>Educación y formación</h2>
          <div v-for="(edu, i) in cv.education" :key="i" class="item">
            <div class="row">
              <div class="date">{{ edu.start }} - {{ edu.end }}</div>
              <div>
                <strong>{{ edu.title }}</strong>
                <p class="company">{{ edu.center }}</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- BOTÓN ABAJO DEL TODO -->
    <div class="download">
      <button @click="descargarPdf">Descargar PDF</button>
    </div>

  </div>
</template>

<style scoped>
.cv-wrapper {
  background: #f5f5f5;
  padding: 30px;
}

.cv {
  display: flex;
  max-width: 1000px;
  margin: auto;
  background: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

/* SIDEBAR */
.sidebar {
  width: 30%;
  background: #2f3e46;
  color: white;
  padding: 20px;
}

.sidebar h1 {
  font-size: 22px;
  margin-bottom: 20px;
}

.block {
  margin-bottom: 20px;
}

.block h3 {
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;
}

/* MAIN */
.main {
  width: 70%;
  padding: 20px;
}

.section {
  margin-bottom: 25px;
}

.section h2 {
  border-bottom: 2px solid #2f3e46;
  padding-bottom: 5px;
}

.row {
  display: flex;
  gap: 15px;
}

.date {
  min-width: 120px;
  font-weight: bold;
  color: #555;
}

.company {
  font-weight: bold;
  color: #2f3e46;
}

/* BOTÓN */
.download {
  text-align: center;
  margin-top: 20px;
}

button {
  background: #2f3e46;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}

button:hover {
  background: #1b262c;
}
</style>
