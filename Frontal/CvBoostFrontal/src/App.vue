<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-wrapper">

    <!-- NAVBAR GLOBAL -->
    <header class="navbar">
      <div class="logo-section" @click="$router.push('/')" style="cursor: pointer;">
        <img src="@/assets/logo.png" class="logo-img" />
        <span class="brand">CV AI</span>
      </div>

      <nav class="navigation">
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/forms/history">Mis CVs</RouterLink>
      </nav>

      <div class="auth-buttons">
        <RouterLink to="/login" class="btn-ghost">Iniciar sesión</RouterLink>
        <RouterLink to="/register" class="btn-dark">Registrarse</RouterLink>
      </div>
    </header>

    <!-- CONTENIDO DINÁMICO -->
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

/* NAVBAR */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 70px;
  border-bottom: 1px solid #eee;
  background: white;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-img {
  height: 38px;
}

.brand {
  font-weight: 800;
  font-size: 20px;
}

.navigation {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
}

.navigation a {
  text-decoration: none;
  color: #666;
  padding: 6px 12px;
  border-radius: 8px;
}

.navigation a.router-link-exact-active {
  background: black;
  color: white;
}

/* AUTH */
.auth-buttons {
  display: flex;
  gap: 10px;
}

.btn-ghost {
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 8px;
  text-decoration: none;
  color: #111;
}

.btn-dark {
  background: #111;
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  text-decoration: none;
}

.content {
  flex: 1;
  width: 100%;
}
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background: #ffffff; /* 🔥 blanco puro */
}
</style>
