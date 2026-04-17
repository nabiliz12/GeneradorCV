
<script setup lang="ts">
import cvEuropass from '@/assets/cv_europass_lc_es_spanish_1.jpg'
import cvNoPhoto from '@/assets/curriculum-vitae-sin-foto.jpg'
import router from '@/router'
import { reactive, ref } from 'vue'

const pagina = ref(1)
const ponerFoto = ref(false)

const form = reactive({
  nombre: '',
  apellido: '',
  direccion: '',
  profesion: '',
  codigoPostal: '',
  Localidad: '',
  email: '',
  telefono: '',
  experiencia: '',
  permisoConducir: false,
  idiomas: [{ idioma: '', nivel: '' }],
  certificaciones: [{ certificacion: '', anio: '' }],
})
// ideas: https://www.cvmaker.es/
async function submitForm() {
  console.log('Form submitted:', form)

  const response = await fetch('http://127.0.0.1:8001/api/form', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(form),
  })

  if (response.ok) {
    console.log('Form data successfully sent to the backend')
    router.push('/forms/vista-previa')
  } else {
    console.error('Failed to send form data to the backend')
  }
}

function siguientePagina() {
  pagina.value++
}

function anteriorPagina() {
  pagina.value--
}

function agregarIdioma() {
  form.idiomas.push({ idioma: '', nivel: '' })
}

function eliminarIdioma(index: number) {
  form.idiomas.splice(index, 1)
}

function agregarCertificacion() {
  form.certificaciones.push({ certificacion: '', anio: '' })
}

function eliminarCertificacion(index: number) {
  form.certificaciones.splice(index, 1)
}

const fileInput=ref<HTMLInputElement | null>(null)
function subirFoto() {
  fileInput.value?.click()
}

const fotoPerfil = ref<string | null>(null)

function onFileChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]

  if (!file) return

  const reader = new FileReader()

  reader.onload = () => {
    fotoPerfil.value = reader.result as string
  }

  reader.readAsDataURL(file)
}


function login() {
  router.push('/login')
}

function registrarse() {
  router.push('/register')
}
</script>

<template>
  <div class="page">

    <!-- UNA SOLA CARD PARA TODO -->
    <div class="card">

      <!-- PAGE 1 -->
      <div v-if="pagina === 1">
        <h1>Datos personales</h1>

        <div class="grid">
          <input v-model="form.nombre" placeholder="Nombre" />
          <input v-model="form.apellido" placeholder="Apellido" />
          <input v-model="form.email" placeholder="Email" />
          <input v-model="form.telefono" placeholder="Teléfono" />
          <input v-model="form.direccion" placeholder="Dirección" />
          <input v-model="form.codigoPostal" placeholder="Código Postal" />
          <input v-model="form.Localidad" placeholder="Localidad" />
        </div>

        <button @click="siguientePagina" type="button">Siguiente</button>
      </div>

      <!-- PAGE 2 -->
      <div v-if="pagina === 2">
        <h1>Certificaciones</h1>

        <div class="grid">
          <div
            v-for="(certificacion, index) in form.certificaciones"
            :key="index"
            class="form-group"
          >
            <input v-model="certificacion.certificacion" placeholder="Certificación" />
            <input v-model="certificacion.anio" placeholder="Año" />
            <button @click="eliminarCertificacion(index)" type="button">Eliminar</button>
          </div>
        </div>

        <button @click="agregarCertificacion" type="button">Agregar Certificación</button>

        <button @click="anteriorPagina" type="button">Atrás</button>
        <button @click="siguientePagina" type="button">Siguiente</button>
      </div>

      <!-- PAGE 3 -->
      <div v-if="pagina === 3">
        <h1>Experiencia</h1>

        <input v-model="form.profesion" placeholder="Profesión" />

        <button @click="anteriorPagina" type="button">Atrás</button>
        <button @click="siguientePagina" type="button">Siguiente</button>
      </div>

      <!-- PAGE 4 -->
      <div v-if="pagina === 4">
        <h1>Idiomas</h1>

        <div class="grid">
          <div v-for="(idioma, index) in form.idiomas" :key="index" class="form-group">
            <input v-model="idioma.idioma" placeholder="Idioma" />

            <div class="form-group">
              <label>Nivel</label>
              <select v-model="idioma.nivel">
                <option disabled value="">Elige una opción</option>
                <option>Básico</option>
                <option>Intermedio</option>
                <option>Avanzado</option>
                <option>Nativo</option>
              </select>
            </div>

            <button @click="eliminarIdioma(index)" type="button">Eliminar</button>
          </div>
        </div>

        <button @click="agregarIdioma" type="button">Agregar Idioma</button>

        <button @click="anteriorPagina" type="button">Atrás</button>
        <button @click="siguientePagina" type="button">Siguiente</button>
      </div>

      <!-- PAGE 5 -->
      <div v-if="pagina === 5">
        <h1>Plantilla</h1>

        <h2>¿Quieres poner foto?</h2>

        <button type="button" @click="ponerFoto = true; siguientePagina()">
          Sí
        </button>

        <button type="button" @click="ponerFoto = false; siguientePagina()">
          No
        </button>

        <button @click="anteriorPagina" type="button">Atrás</button>
      </div>

      <!-- PAGE 6 CON FOTO -->
      <div v-if="pagina === 6 && ponerFoto">
        <h1>Plantilla con foto</h1>

        <button @click="subirFoto" type="button">Subir foto</button>

        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          style="display: none"
          @change="onFileChange"
        />

        <img v-if="fotoPerfil" :src="fotoPerfil" class="avatar" />

        <button @click="anteriorPagina" type="button">Atrás</button>
        <button @click="submitForm()">Generar CV</button>

      </div>

      <!-- PAGE 6 SIN FOTO escoger plantilla -->
      <div v-if="pagina === 6 && !ponerFoto">
        <h1>Generando cv...</h1>



        <!-- <button @click="submitForm()" type="button">Generar CV</button> -->
      </div>



    </div>
  </div>
</template>


<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f7f7f8, #ffffff);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto;
  padding: 40px 16px;
}

.card {
  width: 100%;
  max-width: 460px;
  background: white;
  padding: 28px;
  border-radius: 16px;
  border: 1px solid #eee;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

/* TITULO */
h1 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 22px;
  color: #111;
  text-align: left;
}

h2 {
  font-size: 14px;
  font-weight: 500;
  color: #555;
  margin-bottom: 16px;
}

/* GRID */
.grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* INPUTS BONITOS */
input,
select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e7e7e7;
  border-radius: 10px;
  font-size: 14px;
  background: #fafafa;
  transition: all 0.2s ease;
  outline: none;
}

input:focus,
select:focus {
  border-color: #111;
  background: white;
}

/* PLACEHOLDER */
input::placeholder {
  color: #aaa;
}

/* FORM GROUP */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* LABELS */
label {
  font-size: 12px;
  color: #666;
}

/* BOTONES */
button {
  border: none;
  background: #111;
  color: white;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 12px;
  transition: 0.2s;
}

button:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

/* BOTÓN SECUNDARIO */
button.secondary {
  background: #f3f4f6;
  color: #111;
}

/* TOP BAR */
.top-bar {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 10px;
}

/* BOTONES LOGIN */
.btn-primary {
  background: #111;
  color: white;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 13px;
}

.btn-secondary {
  background: white;
  border: 1px solid #e5e5e5;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 13px;
  color: #111;
}

/* AVATAR */
.avatar {
  width: 90px;
  height: 90px;
  border-radius: 14px;
  object-fit: cover;
  margin-top: 12px;
  border: 1px solid #eee;
}

/* animación suave de páginas */
.card > div {
  animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
