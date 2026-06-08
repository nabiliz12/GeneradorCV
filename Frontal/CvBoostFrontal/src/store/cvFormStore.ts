import { defineStore } from "pinia";
import { computed, reactive, ref } from "vue";

//Creas un store que tenga pagina, formulario, y todo lo compartido.
export const useCvFormStore=defineStore('cvForm',()=>{
  //paginas
  const pagina=ref(1)
  const totalPaginas = 10
  const progreso = computed(() => Math.round((pagina.value / totalPaginas) * 100))
  const intentoAvanzar=ref(false)
  const ponerFotoParaDialog = ref(false)

  const formulario = reactive({
  datosPersonales: {
    nombre: '', apellido: '', email: '', telefono: '',
    direccion: '', codigoPostal: '', localidad: '', permisoConducir: false
  },
  educacion: [{ titulo: '', institucion: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false }],
  certificaciones: [{ certificacion: '', mes: '', anio: '' }],
  experiencia: [{ cargo: '', empresa: '', mesInicio: '', anioInicio: '', mesFin: '', anioFin: '', actualidad: false }],
  idiomas: [{ idioma: '', nivel: '' }],
  skills: [] as string[],
  foto: false,
  foto_base64: null as string | null,
  ofertaDeTrabajo: { empresa: '', descripcion: '' },
})

function esValido(val: string) { return val.trim().length > 0 } // para los campos obligatorios de la primera pagina, si el campo tiene texto se considera ok, si no, error (si se ha intentado avanzar) o idle (si no se ha intentado avanzar aun)

function paginaEsValida(num: number): boolean {
  if (num === 1) {
    return esValido(formulario.datosPersonales.nombre) &&
      esValido(formulario.datosPersonales.apellido) &&
      esValido(formulario.datosPersonales.email) &&
      esValido(formulario.datosPersonales.telefono) &&
      esValido(formulario.datosPersonales.direccion) &&
      esValido(formulario.datosPersonales.codigoPostal) &&
      esValido(formulario.datosPersonales.localidad)
  }
  return true
}



  //educacion




  function siguientePagina(){
    intentoAvanzar.value = true

    if(!paginaEsValida(pagina.value))return
    intentoAvanzar.value=false

    pagina.value++
  }

  function anteriorPagina(){
    intentoAvanzar.value=false
    pagina.value--;
  }

  return {pagina,totalPaginas,progreso,intentoAvanzar,formulario,siguientePagina,anteriorPagina,ponerFotoParaDialog}

})
