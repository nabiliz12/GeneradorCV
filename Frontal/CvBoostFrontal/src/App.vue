<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-wrapper">
    <header class="navbar">
      <div class="logo-section">
        <img src="@/assets/logo.png" alt="logo" class="logo-img" />
        <span class="brand">CV Builder</span>
      </div>

      <nav class="navigation">
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/forms/history">Formularios</RouterLink>
      </nav>
    </header>

    <main class="content-full">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Reset radical para asegurar que nada nos robe espacio */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff; /* O el color que prefieras de fondo total */
}
</style>

<style scoped>
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

/* NAVBAR MODERNA PERO FULL WIDTH */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  height: 70px;
  background: #ffffff;
  border-bottom: 1px solid #eee;
  width: 100%;
  box-sizing: border-box;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-img {
  height: 40px;
  width: auto;
}

.brand {
  font-weight: 800;
  font-size: 22px;
  color: #1a1a1a;
}

/* NAVEGACIÓN */
.navigation {
  display: flex;
  gap: 15px;
}

.navigation a {
  text-decoration: none;
  color: #666;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
  transition: 0.2s;
}

.navigation a:hover {
  background: #f5f5f5;
  color: #000;
}

.navigation a.router-link-exact-active {
  background: #000;
  color: #fff;
}

/* AQUÍ ESTÁ EL TRUCO: TODO EL ANCHO */
.content-full {
  flex: 1;
  width: 100%;
  padding: 40px; /* Espacio interno para que el texto no toque el borde del monitor */
  box-sizing: border-box;
}

/* RESPONSIVE PARA MÓVILES */
@media (max-width: 768px) {
  .navbar {
    padding: 0 20px;
  }
  .content-full {
    padding: 20px;
  }
}
</style>
