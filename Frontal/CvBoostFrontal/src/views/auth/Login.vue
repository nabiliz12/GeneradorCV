
<script setup lang="ts">

function verificarLogin() {


}

</script>



<template>

<div class="wrap">
<input type="text" placeholder="Correo electrónico"/>


<input type="password" placeholder="Contraseña"/>

<button @click="verificarLogin">Iniciar sesión</button>

</div>



</template>


<style scoped>
.wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
input {
  margin: 10px;
  padding: 10px;
  width: 200px;
}
button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
