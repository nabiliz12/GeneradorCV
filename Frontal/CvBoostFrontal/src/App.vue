<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { RouterLink, RouterView, useRouter,useRoute  } from 'vue-router'

const router = useRouter()
const route = useRoute()
const estaLogueado = ref(false)
const nombreUsuario = ref('')

function actualizarEstadoSesion() {
  estaLogueado.value = !!localStorage.getItem('token')
  nombreUsuario.value = localStorage.getItem('nombre') || ''
}
onMounted(() => {
  actualizarEstadoSesion()
})
// Se re-ejecuta en cada cambio de ruta

watch(() => route.path, () => {
  actualizarEstadoSesion()
})

const menuAbierto = ref(false)

async function cerrarSesion() {

  localStorage.removeItem('token')
  localStorage.removeItem('nombre')
  localStorage.removeItem('email')
  estaLogueado.value = false
  menuAbierto.value = false
  router.push('/login')
}
</script>

<template>
  <div class="app-wrapper">

    <header class="navbar">
      <div class="logo-section" @click="$router.push('/')" style="cursor: pointer;">
        <img src="/logo.png" class="logo-img" />
        <span class="brand">Crea CV</span>
      </div>

      <nav class="navigation">
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/forms/history">Mis CVs</RouterLink>
      </nav>

      <!-- SIN SESIÓN -->

      <div v-if="!estaLogueado" class="auth-buttons">
        <RouterLink to="/login" class="btn-ghost">Iniciar sesión</RouterLink>
        <RouterLink to="/registro" class="btn-dark">Registrarse</RouterLink>
      </div>

      <!-- CON SESIÓN -->
      <div v-if="estaLogueado" class="user-menu">
        <button class="avatar-btn" @click="menuAbierto = !menuAbierto" type="button">
          <div class="avatar-circle">{{ nombreUsuario[0]?.toUpperCase() }}</div>
          <span class="user-name">{{ nombreUsuario }}</span>
          <span class="chevron" :class="{ open: menuAbierto }">▾</span>
        </button>

        <div v-if="menuAbierto" class="dropdown">
          <div class="dropdown-item" @click="router.push('/forms/history'); menuAbierto = false">
            Mis CVs
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item" @click="router.push('/ajustes'); menuAbierto = false">
            Ajustes
          </div>
          <div class="dropdown-item danger" @click="cerrarSesion">
            Cerrar sesión
          </div>
        </div>

        <div v-if="menuAbierto" class="overlay" @click="menuAbierto = false"></div>
      </div>
    </header>

    <main class="content">
      <RouterView />
    </main>

  </div>
</template>

<style scoped>
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 70px;
  border-bottom: 1px solid #eee;
  background: white;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-section { display: flex; align-items: center; gap: 10px; }
.logo-img { height: 38px; }
.brand { font-weight: 800; font-size: 20px; color: #111; }

.navigation {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
}
.navigation a { text-decoration: none; color: #666; padding: 6px 12px; border-radius: 8px; }
.navigation a.router-link-exact-active { background: black; color: white; }

.auth-buttons { display: flex; gap: 10px; }
.btn-ghost { border: 1px solid #ddd; padding: 6px 12px; border-radius: 8px; text-decoration: none; color: #111; }
.btn-dark { background: #111; color: white; padding: 6px 12px; border-radius: 8px; text-decoration: none; }

/* ── MENÚ USUARIO ── */
.user-menu { position: relative; }

.avatar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: 1px solid #e7e7e7;
  border-radius: 999px;
  padding: 5px 12px 5px 6px;
  cursor: pointer;
  transition: border-color 0.2s;
  font-family: inherit;
}
.avatar-btn:hover { border-color: #bbb; }

.avatar-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #111;
  color: white;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name { font-size: 13px; font-weight: 500; color: #111; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.chevron { font-size: 11px; color: #999; transition: transform 0.2s; display: inline-block; }
.chevron.open { transform: rotate(180deg); }

.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border: 1px solid #eee;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  min-width: 180px;
  overflow: hidden;
  animation: fadeIn 0.15s ease;
  z-index: 200;
}

.dropdown-item { padding: 10px 16px; font-size: 13px; color: #111; cursor: pointer; transition: background 0.15s; user-select: none; }
.dropdown-item:hover { background: #f7f7f8; }
.dropdown-item.danger { color: #b91c1c; }
.dropdown-item.danger:hover { background: #fef2f2; }
.dropdown-divider { height: 1px; background: #f0f0f0; margin: 4px 0; }

.overlay { position: fixed; inset: 0; z-index: 99; }

.content { flex: 1; width: 100%; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
