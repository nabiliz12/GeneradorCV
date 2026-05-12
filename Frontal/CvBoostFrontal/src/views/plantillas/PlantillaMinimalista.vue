<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const id_cv = route.params.id_cv

const cvData = ref<any>(null)
const cargando = ref(true)
const error = ref<string | null>(null)

async function recogerDatos() {
  try {
    cargando.value = true
    const response = await fetch(`http://127.0.0.1:8001/api/recuperar_cv/${id_cv}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
    })
    if (!response.ok) throw new Error(`Error ${response.status}`)
    cvData.value = await response.json()
    console.log('CV DATA:', JSON.stringify(cvData.value, null, 2))
  } catch (e: any) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}

onMounted(() => recogerDatos())
</script>

<template>
  <div v-if="cargando" style="text-align:center;padding:40px;font-family:sans-serif">Cargando CV...</div>
  <div v-else-if="error" style="text-align:center;color:red;padding:40px;font-family:sans-serif">Error: {{ error }}</div>

  <div v-else-if="cvData" class="cv-bg">
    <div class="cv">

      <!-- CABECERA -->
      <header class="cv-header">
        <div class="cv-header-left">
          <h1 class="cv-name">
            {{ cvData.datosPersonales?.nombre }}<br />
            <span class="cv-lastname">{{ cvData.datosPersonales?.apellido }}</span>
          </h1>
          <p v-if="cvData.datosPersonales?.profesion" class="cv-title">{{ cvData.datosPersonales.profesion }}</p>
          <div class="cv-contact-line">
            <span v-if="cvData.datosPersonales?.email">{{ cvData.datosPersonales.email }}</span>
            <span class="cv-sep" v-if="cvData.datosPersonales?.telefono">·</span>
            <span v-if="cvData.datosPersonales?.telefono">{{ cvData.datosPersonales.telefono }}</span>
            <span class="cv-sep" v-if="cvData.datosPersonales?.localidad">·</span>
            <span v-if="cvData.datosPersonales?.localidad">{{ cvData.datosPersonales.localidad }}</span>
          </div>
          <div v-if="cvData.datosPersonales?.permiso_conducir" class="cv-conducir">🚗 Permiso de conducir B</div>
        </div>
        <img v-if="cvData.foto_base64" :src="cvData.foto_base64" class="cv-avatar" alt="Foto" />
      </header>

      <div class="cv-rule"></div>

      <!-- ✅ DESCRIPCIÓN / PERFIL PROFESIONAL (ancho completo) -->
      <section v-if="cvData.descripcion" class="cv-descripcion-section">
        <h2 class="cv-descripcion-title">Perfil profesional</h2>
        <p class="cv-descripcion-text">{{ cvData.descripcion }}</p>
        <div class="cv-rule cv-rule-sm"></div>
      </section>

      <!-- CUERPO: 2 columnas -->
      <div class="cv-body">

        <!-- COLUMNA IZQUIERDA -->
        <div class="cv-col-left">

          <section v-if="cvData.experiencia?.length" class="cv-section">
            <h2 class="cv-section-title">Experiencia</h2>
            <div v-for="(exp, i) in cvData.experiencia" :key="i" class="cv-entry">
              <div class="cv-entry-head">
                <strong>{{ exp.puesto || exp.cargo }}</strong>
                <span class="cv-entry-date">
                  {{ exp.mesInicio || exp.fecha_inicio || '' }} {{ exp.anioInicio }} —
                  {{ exp.actualidad ? 'Actualidad' : ((exp.mesFin || exp.fecha_fin || '') + ' ' + (exp.anioFin || '')) }}
                </span>
              </div>
              <div class="cv-entry-org">{{ exp.empresa }}</div>
            </div>
          </section>

          <section v-if="cvData.educacion?.length || cvData.certificaciones?.length" class="cv-section">
            <h2 class="cv-section-title">Formación</h2>
            <div v-for="(edu, i) in cvData.educacion" :key="'e'+i" class="cv-entry">
              <div class="cv-entry-head">
                <strong>{{ edu.titulo }}</strong>
                <span class="cv-entry-date">{{ edu.anioInicio }} — {{ edu.actualidad ? 'Actualidad' : edu.anioFin }}</span>
              </div>
              <div class="cv-entry-org">{{ edu.institucion }}</div>
            </div>
            <div v-for="(cert, i) in cvData.certificaciones" :key="'c'+i" class="cv-entry">
              <div class="cv-entry-head">
                <strong>{{ cert.certificacion }}</strong>
                <span class="cv-entry-date">{{ cert.mes }} {{ cert.anio }}</span>
              </div>
            </div>
          </section>

        </div>

        <!-- COLUMNA DERECHA -->
        <div class="cv-col-right">

          <section v-if="cvData.idiomas?.length" class="cv-section">
            <h2 class="cv-section-title">Idiomas</h2>
            <div v-for="(lang, i) in cvData.idiomas" :key="i" class="cv-lang-row">
              <span class="cv-lang-name">{{ lang.nombre || lang.idioma }}</span>
              <span class="cv-lang-nivel">{{ lang.nivel }}</span>
            </div>
          </section>

          <section v-if="cvData.skills?.length" class="cv-section">
            <h2 class="cv-section-title">Skills</h2>
            <ul class="cv-skill-list">
              <li v-for="(skill, i) in cvData.skills" :key="i">{{ skill }}</li>
            </ul>
          </section>

          <section class="cv-section">
            <h2 class="cv-section-title">Contacto</h2>
            <div class="cv-contact-block">
              <div v-if="cvData.datosPersonales?.direccion">{{ cvData.datosPersonales.direccion }}</div>
              <div>{{ cvData.datosPersonales?.codigo_postal }} {{ cvData.datosPersonales?.localidad }}</div>
            </div>
          </section>

        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.cv-bg {
  background: #f2f2f0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 48px 16px;
  font-family: 'Lato', sans-serif;
}

.cv {
  width: 210mm;
  min-height: 297mm;
  background: #fff;
  padding: 44px 48px;
  box-shadow: 0 4px 40px rgba(0,0,0,0.08);
  color: #1a1a1a;
}

.cv-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}
.cv-header-left { flex: 1; }

.cv-name {
  font-family: 'Playfair Display', serif;
  font-size: 36pt;
  font-weight: 400;
  line-height: 1.05;
  color: #111;
  letter-spacing: -0.5px;
}
.cv-lastname { font-weight: 700; }

.cv-title {
  font-size: 10pt;
  font-weight: 300;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin-top: 6px;
}

.cv-contact-line {
  font-size: 8.5pt;
  color: #555;
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
}
.cv-sep { color: #bbb; }
.cv-conducir { font-size: 8pt; color: #888; margin-top: 4px; }

.cv-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #eee;
  flex-shrink: 0;
  margin-top: 4px;
}

.cv-rule {
  height: 1px;
  background: #1a1a1a;
  margin: 24px 0;
}
.cv-rule-sm { margin: 20px 0 0 0; }

/* ✅ DESCRIPCIÓN */
.cv-descripcion-section { margin-bottom: 0; }
.cv-descripcion-title {
  font-family: 'Playfair Display', serif;
  font-size: 10pt;
  font-weight: 700;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  margin-bottom: 8px;
}
.cv-descripcion-text {
  font-size: 9pt;
  color: #555;
  line-height: 1.7;
  font-weight: 300;
  white-space: pre-line;
}

.cv-body {
  display: grid;
  grid-template-columns: 1fr 200px;
  gap: 40px;
  margin-top: 24px;
}

.cv-section { margin-bottom: 28px; }

.cv-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 10pt;
  font-weight: 700;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  border-bottom: 1px solid #111;
  padding-bottom: 6px;
  margin-bottom: 14px;
}

.cv-entry { margin-bottom: 14px; }
.cv-entry-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 8px;
}
.cv-entry-head strong { font-size: 9.5pt; font-weight: 700; color: #111; }
.cv-entry-date { font-size: 7.5pt; font-weight: 300; color: #999; white-space: nowrap; }
.cv-entry-org { font-size: 8.5pt; font-weight: 300; color: #666; margin-top: 2px; font-style: italic; }

.cv-lang-row {
  display: flex;
  justify-content: space-between;
  font-size: 8.5pt;
  color: #333;
  padding: 4px 0;
  border-bottom: 1px solid #f0f0f0;
}
.cv-lang-name { font-weight: 700; }
.cv-lang-nivel { color: #888; font-weight: 300; }

.cv-skill-list { list-style: none; padding: 0; }
.cv-skill-list li {
  font-size: 8.5pt;
  color: #444;
  padding: 3px 0;
  border-bottom: 1px solid #f0f0f0;
  font-weight: 300;
}
.cv-skill-list li::before { content: '— '; color: #bbb; }

.cv-contact-block { font-size: 8.5pt; color: #555; line-height: 1.7; font-weight: 300; }

@media print {
  .cv-bg { background: none; padding: 0; }
  .cv { box-shadow: none; padding: 20px; width: 100%; }
}
</style>
