<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLangStore } from '@/store/langStore'

const router = useRouter()
const langStore = useLangStore()

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
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/perfil`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    if (!res.ok) { router.push('/login'); return }
    const data = await res.json()
    nombre.value = data.nombre
    apellidos.value = data.apellidos
    email.value = data.email
  } catch {
    mostrarToast(langStore.t.settings_toast_profile_err, 'error')
  } finally {
    cargando.value = false
  }
})

async function guardarPerfil() {
  guardando.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/actualizar_perfil`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ nombre: nombre.value, apellidos: apellidos.value })
    })
    if (!res.ok) throw new Error()
    localStorage.setItem('nombre', nombre.value)
    mostrarToast(langStore.t.settings_toast_saved, 'ok')
  } catch {
    mostrarToast(langStore.t.settings_toast_save_err, 'error')
  } finally {
    guardando.value = false
  }
}

async function cambiarContrasena() {
  if (passNueva.value !== passConfirm.value) {
    mostrarToast(langStore.t.settings_toast_pass_nomatch, 'error'); return
  }
  if (passNueva.value.length < 3) {
    mostrarToast(langStore.t.settings_toast_pass_short, 'error'); return
  }
  guardandoPass.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/cambiar_contraseña`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ contrasena_actual: passActual.value, nueva_contrasena: passNueva.value })
    })
    const data = await res.json()
    if (!res.ok) { mostrarToast(data.detail || langStore.t.settings_toast_pass_err, 'error'); return }
    passActual.value = ''
    passNueva.value = ''
    passConfirm.value = ''
    mostrarToast(langStore.t.settings_toast_pass_changed, 'ok')
  } catch {
    mostrarToast(langStore.t.settings_toast_conn, 'error')
  } finally {
    guardandoPass.value = false
  }
}

async function eliminarCuenta() {
  eliminando.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/usuario`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    if (!res.ok) throw new Error()
    localStorage.clear()
    router.push('/')
  } catch {
    mostrarToast(langStore.t.settings_toast_delete_err, 'error')
    eliminando.value = false
    modalEliminar.value = false
  }
}
</script>

<template>
  <div class="page">

    <div v-if="toast" class="toast" :class="toast.tipo">{{ toast.msg }}</div>

    <div v-if="modalEliminar" class="modal-overlay" @click.self="modalEliminar = false">
      <div class="modal">
        <h2>{{ langStore.t.settings_modal_title }}</h2>
        <p>{{ langStore.t.settings_modal_text }}</p>
        <div class="modal-buttons">
          <button class="secondary" @click="modalEliminar = false" type="button">{{ langStore.t.settings_modal_cancel }}</button>
          <button class="danger" @click="eliminarCuenta" :disabled="eliminando" type="button">
            {{ eliminando ? langStore.t.settings_modal_deleting : langStore.t.settings_modal_confirm }}
          </button>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="page-header">
        <button class="btn-back" @click="router.back()" type="button">{{ langStore.t.settings_back }}</button>
        <h1>{{ langStore.t.settings_title }}</h1>
      </div>

      <div v-if="cargando" class="cargando">
        <div class="spinner"></div>
        <span>{{ langStore.t.settings_loading }}</span>
      </div>

      <div v-else class="card">

        <div class="section">
          <h2>{{ langStore.t.settings_personal_title }}</h2>
          <p class="section-desc">{{ langStore.t.settings_personal_desc }}</p>
          <div class="fields">
            <div class="row-2">
              <div class="field-wrap">
                <label>{{ langStore.t.settings_name }}</label>
                <input v-model="nombre" :placeholder="langStore.t.settings_name_placeholder" />
              </div>
              <div class="field-wrap">
                <label>{{ langStore.t.settings_last }}</label>
                <input v-model="apellidos" :placeholder="langStore.t.settings_last_placeholder" />
              </div>
            </div>
            <div class="field-wrap">
              <label>{{ langStore.t.settings_email }}</label>
              <input :value="email" disabled class="input-disabled" />
              <span class="field-hint">{{ langStore.t.settings_email_hint }}</span>
            </div>
          </div>
          <div class="section-footer">
            <button @click="guardarPerfil" :disabled="guardando" type="button">
              {{ guardando ? langStore.t.settings_saving : langStore.t.settings_save }}
            </button>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section">
          <h2>{{ langStore.t.settings_pass_title }}</h2>
          <p class="section-desc">{{ langStore.t.settings_pass_desc }}</p>
          <div class="fields">
            <div class="field-wrap">
              <label>{{ langStore.t.settings_pass_current }}</label>
              <input v-model="passActual" type="password" placeholder="••••••••" />
            </div>
            <div class="row-2">
              <div class="field-wrap">
                <label>{{ langStore.t.settings_pass_new }}</label>
                <input v-model="passNueva" type="password" placeholder="••••••••" />
              </div>
              <div class="field-wrap">
                <label>{{ langStore.t.settings_pass_repeat }}</label>
                <input v-model="passConfirm" type="password" placeholder="••••••••" />
              </div>
            </div>
          </div>
          <div class="section-footer">
            <button @click="cambiarContrasena" :disabled="guardandoPass" type="button">
              {{ guardandoPass ? langStore.t.settings_pass_changing : langStore.t.settings_pass_change }}
            </button>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section">
          <div class="danger-row">
            <div>
              <span class="danger-desc">{{ langStore.t.settings_delete_desc }}</span>
            </div>
            <button class="btn-danger" @click="modalEliminar = true" type="button">
              {{ langStore.t.settings_delete_btn }}
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

.page-header { display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }

h1 { font-size: 18px; font-weight: 600; color: #111; margin: 0; }

.btn-back {
  background: #f3f4f6; color: #111; border: none;
  border-radius: 8px; padding: 7px 12px; font-size: 13px;
  cursor: pointer; transition: background 0.2s; width: auto; margin: 0;
}
.btn-back:hover { background: #e5e7eb; }

.card {
  background: white; border: 1px solid #eee;
  border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); overflow: hidden;
}

.divider { height: 1px; background: #f0f0f0; }

.section { padding: 24px; }

.section h2 { font-size: 14px; font-weight: 600; color: #111; margin: 0 0 3px 0; }
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

.danger-row {
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  padding: 14px 16px; background: #fff5f5;
  border: 1px solid #fee2e2; border-radius: 10px;
  flex-wrap: wrap;
}
.danger-desc { display: block; font-size: 12px; color: #999; }
.btn-danger {
  background: #b91c1c; color: white; border: none;
  border-radius: 8px; padding: 8px 14px; font-size: 13px;
  cursor: pointer; white-space: nowrap; flex-shrink: 0;
  transition: 0.2s; width: auto; margin: 0;
}
.btn-danger:hover { opacity: 0.85; }

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

.toast {
  position: fixed; bottom: 24px; right: 24px;
  padding: 12px 18px; border-radius: 10px;
  font-size: 13px; font-weight: 500;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  z-index: 9999; animation: slideUp 0.2s ease;
}
.toast.ok { background: #111; color: white; }
.toast.error { background: #b91c1c; color: white; }

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

@media (max-width: 480px) {
  .row-2 { grid-template-columns: 1fr; }
  .danger-row { flex-direction: column; align-items: flex-start; }
}
</style>
