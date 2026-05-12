<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface CvResumen {
  id_cv: number
  titulo: string
  fecha_creacion: string
  empresa_oferta: string | null
}

const cvs = ref<CvResumen[]>([])
const cargando = ref(true)
const error = ref<string | null>(null)
const eliminando = ref<number | null>(null)

async function cargarHistorial() {
  try {
    cargando.value = true
    const token = localStorage.getItem('token')
    const res = await fetch('http://127.0.0.1:8001/api/historial', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) throw new Error(`Error ${res.status}`)
    const data = await res.json()
    cvs.value = data.cvs
  } catch (e: any) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}

async function eliminarCv(id_cv: number) {
  if (!confirm('¿Seguro que quieres eliminar este CV?')) return
  eliminando.value = id_cv
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(`http://127.0.0.1:8001/api/historial/eliminar/${id_cv}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) throw new Error(`Error ${res.status}`)
    cvs.value = cvs.value.filter(c => c.id_cv !== id_cv)
  } catch (e: any) {
    alert('No se pudo eliminar: ' + e.message)
  } finally {
    eliminando.value = null
  }
}

function verCv(id_cv: number) {
  router.push(`/forms/vista-previa/${id_cv}`)
}

function formatFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function irAlFormulario() {
  if (!localStorage.getItem('token')) {
   return router.push('/login')
  } else {
   return router.push('/forms')
  }
}

onMounted(() => cargarHistorial())
</script>

<template>
  <div class="page">
    <div class="card">
      <div class="header">
        <h1>Mis CVs</h1>
        <button class="btn-new" @click="irAlFormulario">+ Nuevo CV</button>
      </div>

      <!-- Estado: cargando -->
      <div v-if="cargando" class="estado-centro">
        <div class="spinner"></div>
        <span>Cargando historial...</span>
      </div>

      <!-- Estado: error -->
      <div v-else-if="error" class="estado-centro estado-error">
        <span>no se han encontrado CVs</span>
        <button class="btn-retry" @click="cargarHistorial">Reintentar</button>
      </div>

      <!-- Estado: vacío -->
      <div v-else-if="cvs.length === 0" class="estado-centro estado-vacio">
        <span class="vacio-icon">📄</span>
        <p>Todavía no has generado ningún CV.</p>
        <button @click="router.push('/forms/formulario')">Crear mi primer CV</button>
      </div>

      <!-- Lista de CVs -->
      <div v-else class="lista">
        <div
          v-for="cv in cvs"
          :key="cv.id_cv"
          class="cv-item"
          @click="verCv(cv.id_cv)"
        >
          <div class="cv-item-left">
            <span class="cv-icon">📋</span>
            <div class="cv-info">
              <span class="cv-titulo">{{ cv.titulo }}</span>
              <div class="cv-meta">
                <span v-if="cv.empresa_oferta" class="cv-empresa">{{ cv.empresa_oferta }}</span>
                <span class="cv-fecha">{{ formatFecha(cv.fecha_creacion) }}</span>
              </div>
            </div>
          </div>

          <div class="cv-item-actions" @click.stop>
            <button
              class="btn-eliminar"
              :disabled="eliminando === cv.id_cv"
              @click="eliminarCv(cv.id_cv)"
              title="Eliminar"
            >
              {{ eliminando === cv.id_cv ? '...' : '🗑' }}
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: linear-gradient(180deg, #f7f7f8, #ffffff);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto;
  padding: 40px 16px;
}

.card {
  width: 100%;
  max-width: 520px;
  background: white;
  padding: 28px;
  border-radius: 16px;
  border: 1px solid #eee;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}

h1 { font-size: 18px; font-weight: 600; color: #111; }

.btn-new {
  background: #111; color: white;
  border: none; border-radius: 10px;
  padding: 8px 14px; font-size: 13px;
  cursor: pointer; width: auto; margin: 0;
  transition: 0.2s;
}
.btn-new:hover { opacity: 0.85; transform: translateY(-1px); }

/* ── Estados ── */
.estado-centro {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 0;
  color: #888;
  font-size: 14px;
}

.estado-error { color: #b91c1c; }

.estado-vacio .vacio-icon { font-size: 36px; }
.estado-vacio p { color: #999; font-size: 14px; }
.estado-vacio button {
  background: #111; color: white;
  border: none; border-radius: 10px;
  padding: 9px 16px; font-size: 13px;
  cursor: pointer; width: auto; margin: 0;
  transition: 0.2s;
}

.btn-retry {
  background: #fee2e2; color: #b91c1c;
  border: none; border-radius: 8px;
  padding: 7px 14px; font-size: 13px;
  cursor: pointer; width: auto; margin: 0;
}

/* ── Spinner ── */
.spinner {
  width: 22px; height: 22px;
  border: 2.5px solid #e7e7e7;
  border-top-color: #111;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Lista ── */
.lista { display: flex; flex-direction: column; gap: 8px; }

.cv-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border: 1px solid #efefef;
  border-radius: 12px;
  background: #fafafa;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
  animation: fadeIn 0.2s ease;
}
.cv-item:hover { border-color: #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }

.cv-item-left { display: flex; align-items: center; gap: 12px; flex: 1; min-width: 0; }

.cv-icon { font-size: 20px; flex-shrink: 0; }

.cv-info { display: flex; flex-direction: column; gap: 3px; min-width: 0; }

.cv-titulo {
  font-size: 14px; font-weight: 600; color: #111;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.cv-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

.cv-empresa {
  font-size: 12px; color: #003399; font-weight: 500;
  background: #eef2ff; border-radius: 6px;
  padding: 1px 7px;
}

.cv-fecha { font-size: 11.5px; color: #aaa; }

/* ── Botones de acción ── */
.cv-item-actions { display: flex; gap: 6px; flex-shrink: 0; }

.btn-ver, .btn-eliminar {
  width: 32px; height: 32px;
  border-radius: 8px; border: none;
  font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  padding: 0; margin: 0; transition: background 0.2s;
}
.btn-ver { background: #f3f4f6; }
.btn-ver:hover { background: #e0e7ff; }
.btn-eliminar { background: #f3f4f6; }
.btn-eliminar:hover { background: #fee2e2; }
.btn-eliminar:disabled { opacity: 0.5; cursor: not-allowed; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
