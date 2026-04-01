<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

function irAlFormulario() {
  console.log('Redirigiendo al formulario...');
  router.push('/forms');
}
</script>

<template>
  <div class="hero-section">
    <button class="btn-modern" @click="irAlFormulario">
      <span>Comenzar Gratis</span>
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon">
        <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
</template>

<style scoped>
/* Contenedor para centrarlo o darle aire */
.hero-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.btn-modern {
  /* Estructura */
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 32px;

  /* Colores y Bordes */
  background: #111827; /* Negro azulado profundo */
  color: #ffffff;
  border: none;
  border-radius: 12px;

  /* Tipografía */
  font-size: 18px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  letter-spacing: -0.2px;
  cursor: pointer;

  /* Animaciones y Sombras */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* EFECTO HOVER (Pasar el ratón) */
.btn-modern:hover {
  background: #1f2937;
  transform: translateY(-2px); /* Sube un poquito */
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  gap: 18px; /* El icono se separa un poco más al hacer hover */
}

/* EFECTO ACTIVE (Al hacer clic) */
.btn-modern:active {
  transform: translateY(0); /* Se hunde de nuevo */
  background: #000000;
}

/* EL ICONO (Flecha) */
.icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.btn-modern:hover .icon {
  transform: translateX(4px); /* La flecha se mueve a la derecha */
}

/* Adaptación móvil rápida */
@media (max-width: 768px) {
  .btn-modern {
    width: 100%;
    justify-content: center;
    padding: 14px 24px;
    font-size: 16px;
  }
}
</style>
