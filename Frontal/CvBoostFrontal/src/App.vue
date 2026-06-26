<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'
import { useLangStore } from '@/store/langStore'

const router = useRouter()
const route = useRoute()
const langStore = useLangStore()

const estaLogueado = ref(false)
const nombreUsuario = ref('')

function actualizarEstadoSesion() {
  estaLogueado.value = !!localStorage.getItem('token')
  nombreUsuario.value = localStorage.getItem('nombre') || ''
}
onMounted(() => actualizarEstadoSesion())

watch(() => route.path, () => {
  actualizarEstadoSesion()
  mobileMenuAbierto.value = false
})

const menuAbierto = ref(false)
const mobileMenuAbierto = ref(false)

async function cerrarSesion() {
  localStorage.removeItem('token')
  localStorage.removeItem('nombre')
  localStorage.removeItem('email')
  estaLogueado.value = false
  menuAbierto.value = false
  mobileMenuAbierto.value = false
  router.push('/login')
}
</script>

<template>
  <div class="app-wrapper">

    <header class="navbar">
      <div class="logo-section" @click="$router.push('/')" style="cursor: pointer;">
        <img src="/logo.png" class="logo-img" />
        <span class="brand">Generador CV</span>
      </div>

      <!-- Desktop navigation -->
      <nav class="navigation">
        <RouterLink to="/">{{ langStore.t.nav_home }}</RouterLink>
        <RouterLink to="/forms/history">{{ langStore.t.nav_mycvs }}</RouterLink>
      </nav>

      <div class="navbar-right">
        <!-- Language toggle -->
        <div class="lang-toggle">
          <span :class="['lang-opt', { 'lang-active': langStore.lang === 'es' }]" @click="langStore.lang !== 'es' && langStore.toggleLang()">ES</span>
          <span :class="['lang-opt', { 'lang-active': langStore.lang === 'en' }]" @click="langStore.lang !== 'en' && langStore.toggleLang()">EN</span>
        </div>

        <!-- Desktop: sin sesión -->
        <div v-if="!estaLogueado" class="auth-buttons">
          <RouterLink to="/login" class="btn-ghost">{{ langStore.t.nav_login }}</RouterLink>
          <RouterLink to="/registro" class="btn-dark">{{ langStore.t.nav_register }}</RouterLink>
        </div>

        <!-- Desktop: con sesión -->
        <div v-if="estaLogueado" class="user-menu">
          <button class="avatar-btn" @click="menuAbierto = !menuAbierto" type="button">
            <div class="avatar-circle">{{ nombreUsuario[0]?.toUpperCase() }}</div>
            <span class="user-name">{{ nombreUsuario }}</span>
            <span class="chevron" :class="{ open: menuAbierto }">▾</span>
          </button>

          <div v-if="menuAbierto" class="dropdown">
            <div class="dropdown-item" @click="router.push('/forms/history'); menuAbierto = false">
              {{ langStore.t.nav_mycvs }}
            </div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item" @click="router.push('/ajustes'); menuAbierto = false">
              {{ langStore.t.nav_settings }}
            </div>
            <div class="dropdown-item danger" @click="cerrarSesion">
              {{ langStore.t.nav_logout }}
            </div>
          </div>

          <div v-if="menuAbierto" class="overlay" @click="menuAbierto = false"></div>
        </div>

        <!-- Mobile hamburger -->
        <button class="hamburger-btn" @click="mobileMenuAbierto = !mobileMenuAbierto" type="button" aria-label="Menu">
          <span class="hline" :class="{ 'hline-top-open': mobileMenuAbierto }"></span>
          <span class="hline hline-mid" :class="{ 'hline-mid-open': mobileMenuAbierto }"></span>
          <span class="hline" :class="{ 'hline-bot-open': mobileMenuAbierto }"></span>
        </button>
      </div>
    </header>

    <!-- Mobile menu panel -->
    <div class="mobile-menu" :class="{ 'mobile-menu-open': mobileMenuAbierto }">
      <RouterLink class="mobile-link" to="/" @click="mobileMenuAbierto = false">{{ langStore.t.nav_home }}</RouterLink>
      <RouterLink class="mobile-link" to="/forms/history" @click="mobileMenuAbierto = false">{{ langStore.t.nav_mycvs }}</RouterLink>

      <div class="mobile-divider"></div>

      <template v-if="!estaLogueado">
        <RouterLink class="mobile-link" to="/login" @click="mobileMenuAbierto = false">{{ langStore.t.nav_login }}</RouterLink>
        <RouterLink class="mobile-link mobile-link-dark" to="/registro" @click="mobileMenuAbierto = false">{{ langStore.t.nav_register }}</RouterLink>
      </template>

      <template v-if="estaLogueado">
        <div class="mobile-user-name">{{ nombreUsuario }}</div>
        <div class="mobile-link" @click="router.push('/ajustes'); mobileMenuAbierto = false">{{ langStore.t.nav_settings }}</div>
        <div class="mobile-link mobile-link-danger" @click="cerrarSesion">{{ langStore.t.nav_logout }}</div>
      </template>
    </div>

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

/* ── Navbar ── */
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

/* ── Navbar right ── */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* ── Language toggle ── */
.lang-toggle {
  display: flex;
  align-items: center;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 3px;
  gap: 2px;
}
.lang-opt {
  font-size: 12px;
  font-weight: 600;
  color: #999;
  cursor: pointer;
  padding: 3px 8px;
  border-radius: 6px;
  user-select: none;
  transition: color 0.15s, background 0.15s;
  line-height: 1.4;
}
.lang-opt:hover { color: #555; }
.lang-active {
  background: white;
  color: #111;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* ── Auth buttons ── */
.auth-buttons { display: flex; gap: 10px; }
.btn-ghost { border: 1px solid #ddd; padding: 6px 12px; border-radius: 8px; text-decoration: none; color: #111; font-size: 14px; }
.btn-dark { background: #111; color: white; padding: 6px 12px; border-radius: 8px; text-decoration: none; font-size: 14px; }

/* ── User menu ── */
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
  width: 28px; height: 28px; border-radius: 50%;
  background: #111; color: white;
  font-size: 13px; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
}

.user-name { font-size: 13px; font-weight: 500; color: #111; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.chevron { font-size: 11px; color: #999; transition: transform 0.2s; display: inline-block; }
.chevron.open { transform: rotate(180deg); }

.dropdown {
  position: absolute; top: calc(100% + 8px); right: 0;
  background: white; border: 1px solid #eee;
  border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  min-width: 180px; overflow: hidden;
  animation: fadeIn 0.15s ease; z-index: 200;
}

.dropdown-item { padding: 10px 16px; font-size: 13px; color: #111; cursor: pointer; transition: background 0.15s; user-select: none; }
.dropdown-item:hover { background: #f7f7f8; }
.dropdown-item.danger { color: #b91c1c; }
.dropdown-item.danger:hover { background: #fef2f2; }
.dropdown-divider { height: 1px; background: #f0f0f0; margin: 4px 0; }

.overlay { position: fixed; inset: 0; z-index: 99; }

/* ── Hamburger ── */
.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 36px; height: 36px;
  background: none; border: none; cursor: pointer;
  border-radius: 8px; padding: 6px;
  transition: background 0.15s;
}
.hamburger-btn:hover { background: #f3f4f6; }

.hline {
  display: block; width: 20px; height: 2px;
  background: #111; border-radius: 2px;
  transition: transform 0.25s, opacity 0.25s;
  transform-origin: center;
}
.hline-top-open { transform: translateY(7px) rotate(45deg); }
.hline-mid-open { opacity: 0; transform: scaleX(0); }
.hline-bot-open { transform: translateY(-7px) rotate(-45deg); }

/* ── Mobile menu panel ── */
.mobile-menu {
  display: none;
  flex-direction: column;
  background: white;
  border-bottom: 1px solid #eee;
  padding: 0 20px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.25s ease, padding 0.25s ease;
  position: sticky;
  top: 70px;
  z-index: 98;
}
.mobile-menu-open {
  max-height: 400px;
  padding: 12px 20px 20px;
}

.mobile-link {
  display: block;
  padding: 11px 4px;
  font-size: 15px;
  font-weight: 500;
  color: #111;
  text-decoration: none;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: color 0.15s;
}
.mobile-link:last-child { border-bottom: none; }
.mobile-link:hover { color: #555; }
.mobile-link.router-link-exact-active { color: #111; font-weight: 700; }

.mobile-link-dark {
  margin-top: 6px;
  background: #111; color: white;
  border-radius: 10px; padding: 11px 16px;
  text-align: center; border-bottom: none;
}
.mobile-link-dark:hover { color: white; opacity: 0.85; }

.mobile-link-danger { color: #b91c1c; border-bottom: none; }
.mobile-link-danger:hover { color: #991b1b; }

.mobile-divider { height: 1px; background: #eee; margin: 4px 0; }

.mobile-user-name {
  font-size: 13px; color: #888; padding: 8px 4px 4px;
  font-weight: 500;
}

/* ── Main content ── */
.content { flex: 1; width: 100%; }

/* ── Animations ── */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .navbar { padding: 0 16px; }
  .brand { font-size: 16px; }
  .navigation { display: none; }
  .auth-buttons { display: none; }
  .user-menu { display: none; }
  .hamburger-btn { display: flex; }
  .mobile-menu { display: flex; }
}
</style>
