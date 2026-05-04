<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'

const email = ref('')
const contrasena = ref('')
const error = ref('')
const cargando = ref(false)

async function verificarLogin() {
  error.value = ''
  cargando.value = true
  try {
    const res = await fetch('http://127.0.0.1:8001/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, contrasena: contrasena.value })
    })
    if (!res.ok) { error.value = (await res.json()).detail || 'Credenciales incorrectas'; return }
    const data = await res.json()
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('nombre', data.nombre)
    router.push('/forms')
  } catch { error.value = 'Error de conexión' }
  finally { cargando.value = false }
}
</script>

<template>
  <div class="page">
    <div class="card">
      <h1>Iniciar sesión</h1>
      <div class="grid">
        <input v-model="email" type="email" placeholder="Correo electrónico" />
        <input v-model="contrasena" type="password" placeholder="Contraseña" />
      </div>
      <p v-if="error" class="error-msg">{{ error }}</p>
      <button @click="verificarLogin" :disabled="cargando" type="button">
        {{ cargando ? 'Entrando...' : 'Entrar' }}
      </button>
      <p class="link-text">¿No tienes cuenta? <a @click="router.push('/registro')">Regístrate</a></p>
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
