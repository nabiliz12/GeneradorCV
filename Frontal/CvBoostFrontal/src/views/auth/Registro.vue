<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'

const nombre = ref('')
const apellidos = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const cargando = ref(false)

async function registrarse() {
  error.value = ''
  if (password.value !== passwordConfirm.value) { error.value = 'Las contraseñas no coinciden'; return }
  cargando.value = true
  try {
const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/registro`, {
        method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre: nombre.value, apellidos: apellidos.value, email: email.value, contrasena: password.value })
    })
    if (!res.ok) { error.value = (await res.json()).detail || 'Error al registrarse'; return }
    router.push('/login')
  } catch { error.value = 'Error de conexión' }
  finally { cargando.value = false }


}
</script>

<template>
  <div class="page">
    <div class="card">
      <h1>Crear cuenta</h1>
      <div class="grid">
        <div class="row-2">
          <input v-model="nombre" placeholder="Nombre" />
          <input v-model="apellidos" placeholder="Apellidos" />
        </div>
        <input v-model="email" type="email" placeholder="Correo electrónico" />
        <input v-model="password" type="password" placeholder="Contraseña" />
        <input v-model="passwordConfirm" type="password" placeholder="Repetir contraseña" />
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
      <button @click="registrarse" :disabled="cargando" type="button">
        {{ cargando ? 'Registrando...' : 'Crear cuenta' }}
      </button>
      <p class="link-text">¿Ya tienes cuenta? <a @click="router.push('/login')">Inicia sesión</a></p>
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
  max-width: 480px;
  background: white;
  padding: 28px;
  border-radius: 16px;
  border: 1px solid #eee;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  animation: fadeIn 0.25s ease;
}
h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; }
.grid { display: flex; flex-direction: column; gap: 12px; }
.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e7e7e7;
  border-radius: 10px;
  font-size: 14px;
  background: #fafafa;
  transition: all 0.2s ease;
  outline: none;
  font-family: inherit;
  box-sizing: border-box;
}
input:focus { border-color: #111; background: white; }
input::placeholder { color: #aaa; }
.error-msg {
  font-size: 13px;
  color: #b91c1c;
  margin-top: 10px;
  padding: 8px 12px;
  background: #fef2f2;
  border-radius: 8px;
  border: 1px solid #fee2e2;
}
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
  width: 100%;
}
button:hover:not(:disabled) { transform: translateY(-1px); opacity: 0.9; }
button:disabled { opacity: 0.5; cursor: not-allowed; }
.link-text { text-align: center; font-size: 13px; color: #777; margin-top: 16px; }
.link-text a { color: #111; font-weight: 600; cursor: pointer; text-decoration: underline; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>

