<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const cargando = ref(true)
const guardando = ref(false)
const guardandoPass = ref(false)
const eliminando = ref(false)

const nombre = ref('')
const apellidos = ref('')
const email = ref('')

const passActual = ref('')
const passNueva = ref('')
const passConfirm = ref('')

const toast = ref<{ msg: string; tipo: 'ok' | 'error' } | null>(null)
const modalEliminar = ref(false)

function mostrarToast(msg: string, tipo: 'ok' | 'error') {
  toast.value = { msg, tipo }
  setTimeout(() => toast.value = null, 3000)
}

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8001/api/usuario/perfil', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    if (!res.ok) { router.push('/login'); return }
    const data = await res.json()
    nombre.value = data.nombre
    apellidos.value = data.apellidos
    email.value = data.email
  } catch {
    mostrarToast('Error al cargar el perfil', 'error')
  } finally {
    cargando.value = false
  }
})

async function guardarPerfil() {
  guardando.value = true
  try {
    const res = await fetch('http://127.0.0.1:8001/api/usuario/perfil', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ nombre: nombre.value, apellidos: apellidos.value })
    })
    if (!res.ok) throw new Error()
    localStorage.setItem('nombre', nombre.value)
    mostrarToast('Datos actualizados correctamente', 'ok')
  } catch {
    mostrarToast('Error al guardar los datos', 'error')
  } finally {
    guardando.value = false
  }
}

async function cambiarContrasena() {
  if (passNueva.value !== passConfirm.value) {
    mostrarToast('Las contraseñas no coinciden', 'error'); return
  }
  if (passNueva.value.length < 6) {
    mostrarToast('La contraseña debe tener al menos 6 caracteres', 'error'); return
  }
  guardandoPass.value = true
  try {
    const res = await fetch('http://127.0.0.1:8001/api/usuario/contrasena', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        contrasena_actual: passActual.value,
        nueva_contrasena: passNueva.value
      })
    })
    const data = await res.json()
    if (!res.ok) { mostrarToast(data.detail || 'Error al cambiar contraseña', 'error'); return }
    passActual.value = ''
    passNueva.value = ''
    passConfirm.value = ''
    mostrarToast('Contraseña actualizada correctamente', 'ok')
  } catch {
    mostrarToast('Error de conexión', 'error')
  } finally {
    guardandoPass.value = false
  }
}

async function eliminarCuenta() {
  eliminando.value = true
  try {
    const res = await fetch('http://127.0.0.1:8001/api/usuario', {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    if (!res.ok) throw new Error()
    localStorage.clear()
    router.push('/')
  } catch {
    mostrarToast('Error al eliminar la cuenta', 'error')
    eliminando.value = false
    modalEliminar.value = false
  }
}
</script>

<template>
  <div class="page">

    <!-- Toast -->
    <div v-if="toast" class="toast" :class="toast.tipo">{{ toast.msg }}</div>

    <!-- Modal eliminar cuenta -->
    <div v-if="modalEliminar" class="modal-overlay" @click.self="modalEliminar = false">
      <div class="modal">
        <h2>¿Eliminar cuenta?</h2>
        <p>Esta acción es irreversible. Se eliminarán tu cuenta y todos tus CVs permanentemente.</p>
        <div class="modal-buttons">
          <button class="secondary" @click="modalEliminar = false" type="button">Cancelar</button>
          <button class="danger" @click="eliminarCuenta" :disabled="eliminando" type="button">
            {{ eliminando ? 'Eliminando...' : 'Sí, eliminar' }}
          </button>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="page-header">
        <button class="btn-back" @click="router.back()" type="button">← Volver</button>
        <h1>Ajustes</h1>
      </div>

      <div v-if="cargando" class="cargando">
        <div class="spinner"></div>
        <span>Cargando...</span>
      </div>

      <div v-else class="card">

        <!-- Datos personales -->
        <div class="section">
          <h2>Datos personales</h2>
          <p class="section-desc">Actualiza tu nombre y apellidos</p>
          <div class="fields">
            <div class="row-2">
              <div class="field-wrap">
                <label>Nombre</label>
                <input v-model="nombre" placeholder="Tu nombre" />
              </div>
              <div class="field-wrap">
                <label>Apellidos</label>
                <input v-model="apellidos" placeholder="Tus apellidos" />
              </div>
            </div>
            <div class="field-wrap">
              <label>Email</label>
              <input :value="email" disabled class="input-disabled" />
              <span class="field-hint">El email no se puede cambiar</span>
            </div>
          </div>
          <div class="section-footer">
            <button @click="guardarPerfil" :disabled="guardando" type="button">
              {{ guardando ? 'Guardando...' : 'Guardar cambios' }}
            </button>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Contraseña -->
        <div class="section">
          <h2>Contraseña</h2>
          <p class="section-desc">Cambia tu contraseña de acceso</p>
          <div class="fields">
            <div class="field-wrap">
              <label>Contraseña actual</label>
              <input v-model="passActual" type="password" placeholder="••••••••" />
            </div>
            <div class="row-2">
              <div class="field-wrap">
                <label>Nueva contraseña</label>
                <input v-model="passNueva" type="password" placeholder="••••••••" />
              </div>
              <div class="field-wrap">
                <label>Repetir contraseña</label>
                <input v-model="passConfirm" type="password" placeholder="••••••••" />
              </div>
            </div>
          </div>
          <div class="section-footer">
            <button @click="cambiarContrasena" :disabled="guardandoPass" type="button">
              {{ guardandoPass ? 'Cambiando...' : 'Cambiar contraseña' }}
            </button>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Zona de peligro -->
        <div class="section">
          <div class="danger-row">
            <div>
              <span class="danger-desc">Se eliminarán tu cuenta y todos tus CVs permanentemente</span>
            </div>
            <button class="btn-danger" @click="modalEliminar = true" type="button">
              Eliminar cuenta
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
  background: linear-gradient(180deg, #f7f7f8, #ffffff);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto;
  padding: 40px 16px;
}

.container { max-width: 520px; margin: 0 auto; }

.page-header {
  display: flex; align-items: center; gap: 14px; margin-bottom: 24px;
}

h1 { font-size: 18px; font-weight: 600; color: #111; margin: 0; }

.btn-back {
  background: #f3f4f6; color: #111; border: none;
  border-radius: 8px; padding: 7px 12px; font-size: 13px;
  cursor: pointer; transition: background 0.2s; width: auto; margin: 0;
}
.btn-back:hover { background: #e5e7eb; }

/* ── Card única ── */
.card {
  background: white;
  border: 1px solid #eee;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  overflow: hidden;
}

.divider { height: 1px; background: #f0f0f0; }

/* ── Secciones dentro de la card ── */
.section { padding: 24px; }

.section h2 {
  font-size: 14px; font-weight: 600; color: #111;
  margin: 0 0 3px 0;
}
.section-desc { font-size: 12px; color: #999; margin: 0 0 18px 0; }

.fields { display: flex; flex-direction: column; gap: 12px; }
.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.field-wrap { display: flex; flex-direction: column; gap: 5px; }

label { font-size: 12px; font-weight: 500; color: #555; }
.field-hint { font-size: 11px; color: #bbb; }

input {
  width: 100%; padding: 9px 12px;
  border: 1.5px solid #e7e7e7; border-radius: 10px;
  font-size: 14px; background: #fafafa;
  transition: border-color 0.2s, background 0.2s;
  outline: none; font-family: inherit; box-sizing: border-box;
}
input:focus { border-color: #111; background: white; }
input::placeholder { color: #bbb; }
.input-disabled { background: #f3f4f6 !important; color: #aaa; cursor: not-allowed; }

.section-footer { margin-top: 18px; display: flex; justify-content: flex-end; }

button {
  background: #111; color: white; border: none;
  border-radius: 10px; padding: 9px 18px; font-size: 13px;
  font-weight: 500; cursor: pointer; transition: 0.2s;
  width: auto; margin: 0;
}
button:hover:not(:disabled) { opacity: 0.85; transform: translateY(-1px); }
button:disabled { opacity: 0.5; cursor: not-allowed; }
button.secondary { background: #f3f4f6; color: #111; }

/* ── Zona peligro ── */
.danger-row {
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  padding: 14px 16px; background: #fff5f5;
  border: 1px solid #fee2e2; border-radius: 10px;
}
.danger-title { display: block; font-size: 13px; font-weight: 600; color: #b91c1c; margin-bottom: 3px; }
.danger-desc { display: block; font-size: 12px; color: #999; }
.btn-danger {
  background: #b91c1c; color: white; border: none;
  border-radius: 8px; padding: 8px 14px; font-size: 13px;
  cursor: pointer; white-space: nowrap; flex-shrink: 0;
  transition: 0.2s; width: auto; margin: 0;
}
.btn-danger:hover { opacity: 0.85; }

/* ── Modal ── */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 999; padding: 16px; animation: fadeIn 0.15s ease;
}
.modal {
  background: white; border-radius: 16px; padding: 28px;
  max-width: 360px; width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  animation: slideUp 0.2s ease;
}
.modal h2 { font-size: 15px; font-weight: 700; color: #111; margin: 0 0 10px 0; }
.modal p { font-size: 13px; color: #666; line-height: 1.6; margin: 0 0 20px 0; }
.modal-buttons { display: flex; gap: 10px; justify-content: flex-end; }
button.danger { background: #b91c1c; color: white; }
button.danger:hover:not(:disabled) { opacity: 0.85; }

/* ── Toast ── */
.toast {
  position: fixed; bottom: 24px; right: 24px;
  padding: 12px 18px; border-radius: 10px;
  font-size: 13px; font-weight: 500;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  z-index: 9999; animation: slideUp 0.2s ease;
}
.toast.ok { background: #111; color: white; }
.toast.error { background: #b91c1c; color: white; }

/* ── Spinner ── */
.cargando {
  display: flex; flex-direction: column; align-items: center;
  gap: 12px; padding: 60px 0; color: #999; font-size: 14px;
}
.spinner {
  width: 22px; height: 22px;
  border: 2.5px solid #e7e7e7; border-top-color: #111;
  border-radius: 50%; animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
