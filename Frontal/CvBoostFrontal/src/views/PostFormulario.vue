<script setup lang="ts">


interface FormData {
  nombre: string
  email: string
  experiencia: string
}

const props = defineProps<{
  info: FormData
}>()


async function descargarPdf() {

  const form=props.info

  const response = await fetch('http://127.0.0.1:8001/api/form/descargarpdf', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(form)
  })

  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'formulario.pdf'
  link.click()
  URL.revokeObjectURL(url)
}

</script>

<template>
  <div>
    <h2>Información del formulario:</h2>
    <p><strong>Nombre:</strong> {{ info.nombre }}</p>
    <p><strong>Email:</strong> {{ info.email }}</p>
    <p><strong>Experiencia:</strong> {{ info.experiencia }}</p>
  </div>
  <button @click="descargarPdf">Descargar pdf</button>
</template>


/*
ReportLab (muy potente, PDF desde cero)
WeasyPrint (convierte HTML/CSS a PDF, útil si quieres diseño bonito)
FPDF / FPDF2 (simple, rápido para MVP)
*/
