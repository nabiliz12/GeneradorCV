<script setup lang="ts">
import router from '@/router';
import { useCvFormStore } from '@/store/cvFormStore';
import { ref } from 'vue';
const store=useCvFormStore()

const plantillaSeleccionada = ref<'europass' | 'minimalista' | 'moderna'>('europass')

const plantillas = [
  { id: 'europass',    label: 'Europass',    desc: 'Formato oficial europeo' },
  { id: 'minimalista', label: 'Minimalista', desc: 'Limpio y sencillo' },
  { id: 'moderna',     label: 'Moderna',     desc: 'Dark sidebar con acento verde' },
]

async function guardarCV() {

  //peticion http
  try {
    const response = await fetch('http://127.0.0.1:8001/api/cv', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
      body: JSON.stringify({
        ...store.formulario,
        plantilla: plantillaSeleccionada.value,      }),
    })

    if (!response.ok) {
      const err = await response.json()
      console.error('Error del backend:', JSON.stringify(err, null, 2))
      return
    }

    const data = await response.json()
    if (!data.id_cv) { console.error('Backend no devolvió id_cv:', data); return }

    const rutas: Record<'europass' | 'minimalista' | 'moderna', string> = {
      europass:    `/forms/plantilla-europass/${data.id_cv}`,
      minimalista: `/forms/plantilla-minimalista/${data.id_cv}`,
      moderna:     `/forms/plantilla-moderna/${data.id_cv}`,
    }
    router.push(rutas[plantillaSeleccionada.value])
  } finally {

  }
}


</script>

<template>
<div v-if="store.pagina === 9">
        <h1>Elige tu plantilla</h1>
        <h2>{{ store.ponerFotoParaDialog ? 'Vista con foto de perfil' : 'Vista sin foto de perfil' }}</h2>

        <div class="plantillas-grid">
          <button
            v-for="p in plantillas"
            :key="p.id"
            type="button"
            class="plantilla-card"
            :class="{ selected: plantillaSeleccionada === p.id }"
            @click="plantillaSeleccionada = (p.id as any)"
          >
            <div class="plantilla-preview">
              <svg viewBox="0 0 120 160" xmlns="http://www.w3.org/2000/svg">

                <!-- ── EUROPASS ── -->
                <template v-if="p.id === 'europass'">
                  <rect width="120" height="160" fill="#f4f7fc"/>
                  <rect width="120" height="32" fill="#003399"/>
                  <rect x="8" y="8" width="16" height="16" rx="8" fill="#ffcc00"/>
                  <rect x="28" y="10" width="30" height="5" rx="2" fill="white" opacity="0.9"/>
                  <rect x="28" y="18" width="20" height="3" rx="1" fill="#aac4f0"/>
                  <template v-if="store.ponerFotoParaDialog">
                    <rect x="88" y="4" width="26" height="24" rx="1" fill="#1a3d7a"/>
                    <circle cx="101" cy="12" r="5" fill="#b0bec5"/>
                    <path d="M91 28 q10-8 20 0" fill="#b0bec5"/>
                  </template>

                  <rect x="8" y="36" width="60" height="8" fill="#003399" opacity="0.15"/>
                  <rect x="8" y="48" width="45" height="4" rx="1" fill="#003399" opacity="0.5"/>
                  <rect x="8" y="56" width="30" height="3" rx="1" fill="#aac4f0"/>
                  <rect x="0" y="68" width="42" height="92" fill="#f0f4fa"/>
                  <rect x="42" y="68" width="1" height="92" fill="#dde4f0"/>
                  <rect x="6" y="76" width="30" height="2" rx="1" fill="#003399" opacity="0.6"/>
                  <rect x="6" y="82" width="22" height="2" rx="1" fill="#aaa"/>
                  <rect x="6" y="88" width="26" height="2" rx="1" fill="#aaa"/>
                  <rect x="6" y="94" width="18" height="2" rx="1" fill="#aaa"/>
                  <circle cx="8" cy="104" r="2" fill="#003399" opacity="0.5"/>
                  <circle cx="13" cy="104" r="2" fill="#003399" opacity="0.5"/>
                  <circle cx="18" cy="104" r="2" fill="#003399"/>
                  <circle cx="23" cy="104" r="2" fill="#003399"/>
                  <circle cx="28" cy="104" r="2" fill="#003399"/>
                  <rect x="48" y="76" width="40" height="2" rx="1" fill="#003399" opacity="0.7"/>
                  <circle cx="52" cy="86" r="3" fill="#003399"/>
                  <rect x="58" y="84" width="30" height="2" rx="1" fill="#333"/>
                  <rect x="58" y="89" width="22" height="2" rx="1" fill="#aaa"/>
                  <circle cx="52" cy="98" r="3" fill="#003399"/>
                  <rect x="58" y="96" width="26" height="2" rx="1" fill="#333"/>
                  <rect x="58" y="101" width="18" height="2" rx="1" fill="#aaa"/>
                  <rect x="0" y="148" width="120" height="12" fill="#f0f4fa"/>
                  <rect x="6" y="152" width="50" height="2" rx="1" fill="#aaa"/>
                </template>

                <!-- ── MINIMALISTA ── -->
                <template v-if="p.id === 'minimalista'">
                  <rect width="120" height="160" fill="white"/>
                  <rect x="8" y="12" width="55" height="8" rx="1" fill="#111" opacity="0.85"/>
                  <rect x="8" y="24" width="40" height="6" rx="1" fill="#111"/>
                  <rect x="8" y="34" width="35" height="2" rx="1" fill="#999"/>
                  <rect x="8" y="40" width="70" height="2" rx="1" fill="#ccc"/>
                  <template v-if="store.ponerFotoParaDialog">
                    <circle cx="100" cy="22" r="14" fill="#e0e0e0"/>
                    <circle cx="100" cy="17" r="5" fill="#b0bec5"/>
                    <path d="M86 36 q14-10 28 0" fill="#b0bec5"/>
                  </template>

                  <rect x="8" y="50" width="104" height="1" fill="#111"/>
                  <rect x="8" y="58" width="40" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="8" y="64" width="55" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="69" width="35" height="2" rx="1" fill="#aaa"/>
                  <rect x="8" y="77" width="50" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="82" width="30" height="2" rx="1" fill="#aaa"/>
                  <rect x="8" y="90" width="40" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="8" y="96" width="52" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="101" width="38" height="2" rx="1" fill="#aaa"/>
                  <rect x="8" y="109" width="48" height="2" rx="1" fill="#333"/>
                  <rect x="8" y="114" width="28" height="2" rx="1" fill="#aaa"/>
                  <rect x="76" y="58" width="36" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="76" y="65" width="28" height="2" rx="1" fill="#555"/>
                  <rect x="76" y="70" width="22" height="1" rx="0.5" fill="#eee"/>
                  <rect x="76" y="75" width="24" height="2" rx="1" fill="#555"/>
                  <rect x="76" y="80" width="22" height="1" rx="0.5" fill="#eee"/>
                  <rect x="76" y="90" width="36" height="2" rx="1" fill="#111" opacity="0.7"/>
                  <rect x="76" y="97" width="26" height="2" rx="1" fill="#555"/>
                  <rect x="76" y="102" width="22" height="1" rx="0.5" fill="#eee"/>
                  <rect x="76" y="107" width="30" height="2" rx="1" fill="#555"/>
                </template>

                <!-- ── MODERNA ── -->
                <template v-if="p.id === 'moderna'">
                  <rect width="120" height="160" fill="white"/>
                  <rect width="44" height="160" fill="#1b2333"/>
                  <template v-if="store.ponerFotoParaDialog">
                    <circle cx="22" cy="24" r="14" fill="#2a3547"/>
                    <circle cx="22" cy="24" r="14" fill="none" stroke="#00c896" stroke-width="2"/>
                    <circle cx="22" cy="20" r="5" fill="#3d4a5c"/>
                    <path d="M10 38 q12-8 24 0" fill="#3d4a5c"/>
                  </template>

                  <rect x="6" y="46" width="24" height="2" rx="1" fill="#00c896" opacity="0.8"/>
                  <rect x="6" y="52" width="32" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.6"/>
                  <rect x="6" y="57" width="28" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.6"/>
                  <rect x="6" y="62" width="30" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.6"/>
                  <rect x="6" y="72" width="20" height="2" rx="1" fill="#00c896" opacity="0.8"/>
                  <rect x="6" y="78" width="32" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.5"/>
                  <rect x="6" y="82" width="20" height="2" rx="1" fill="#00c896" opacity="0.4"/>
                  <rect x="6" y="88" width="32" height="1.5" rx="0.5" fill="#c8d6e5" opacity="0.5"/>
                  <rect x="6" y="92" width="24" height="2" rx="1" fill="#00c896" opacity="0.4"/>
                  <rect x="6" y="102" width="18" height="2" rx="1" fill="#00c896" opacity="0.8"/>
                  <rect x="6" y="108" width="14" height="5" rx="2" fill="#00c896" opacity="0.15" stroke="#00c896" stroke-width="0.5"/>
                  <rect x="22" y="108" width="16" height="5" rx="2" fill="#00c896" opacity="0.15" stroke="#00c896" stroke-width="0.5"/>
                  <rect x="6" y="116" width="18" height="5" rx="2" fill="#00c896" opacity="0.15" stroke="#00c896" stroke-width="0.5"/>
                  <rect x="50" y="14" width="50" height="6" rx="1" fill="#111" opacity="0.8"/>
                  <rect x="50" y="24" width="35" height="2" rx="1" fill="#888"/>
                  <rect x="50" y="30" width="20" height="2" rx="1" fill="#00c896"/>
                  <rect x="50" y="40" width="45" height="2" rx="1" fill="#333" opacity="0.7"/>
                  <rect x="50" y="45" width="60" height="0.5" fill="#eee"/>
                  <circle cx="53" cy="54" r="2.5" fill="#00c896"/>
                  <rect x="58" y="52" width="32" height="2" rx="1" fill="#111"/>
                  <rect x="58" y="57" width="22" height="2" rx="1" fill="#00c896" opacity="0.7"/>
                  <circle cx="53" cy="68" r="2.5" fill="#00c896"/>
                  <rect x="58" y="66" width="28" height="2" rx="1" fill="#111"/>
                  <rect x="58" y="71" width="18" height="2" rx="1" fill="#00c896" opacity="0.7"/>
                  <rect x="50" y="84" width="45" height="2" rx="1" fill="#333" opacity="0.7"/>
                  <rect x="50" y="89" width="60" height="0.5" fill="#eee"/>
                  <circle cx="53" cy="98" r="2.5" fill="#00c896"/>
                  <rect x="58" y="96" width="30" height="2" rx="1" fill="#111"/>
                  <rect x="58" y="101" width="20" height="2" rx="1" fill="#00c896" opacity="0.7"/>
                </template>

              </svg>
            </div>

            <div class="plantilla-check" v-if="plantillaSeleccionada === p.id">✓</div>

            <div class="plantilla-info">
              <span class="plantilla-name">{{ p.label }}</span>
              <span class="plantilla-desc">{{ p.desc }}</span>
            </div>
          </button>
        </div>

        <div class="nav-buttons" style="margin-top: 20px;">
          <button @click="store.anteriorPagina()" type="button" class="secondary">Atrás</button>
          <button @click="guardarCV()" type="button">Generar CV</button>
        </div>
      </div>


</template>


<style>
h1 { font-size: 18px; font-weight: 600; margin-bottom: 22px; color: #111; display: flex; align-items: center; gap: 8px; }
h2 { font-size: 14px; font-weight: 500; color: #555; margin-bottom: 16px; }
.plantillas-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.plantilla-card { position: relative; display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 10px 8px 12px; border: 2px solid #e7e7e7; border-radius: 14px; background: #fafafa; cursor: pointer; transition: border-color 0.2s, box-shadow 0.2s, background 0.2s; width: 100%; margin: 0; }
.plantilla-card:hover { border-color: #999; background: white; transform: none; opacity: 1; }
.plantilla-card.selected { border-color: #111; background: white; box-shadow: 0 0 0 3px rgba(0,0,0,0.06); }
.plantilla-preview { width: 100%; aspect-ratio: 3/4; overflow: hidden; border-radius: 6px; border: 1px solid #eee; background: white; }
.plantilla-preview svg { width: 100%; height: 100%; display: block; }
.plantilla-check { position: absolute; top: 8px; right: 8px; width: 20px; height: 20px; border-radius: 50%; background: #111; color: white; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.plantilla-info { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.plantilla-name { font-size: 12px; font-weight: 700; color: #111; }
.plantilla-desc { font-size: 10px; color: #999; text-align: center; line-height: 1.3; }
.nav-buttons { display: flex; gap: 10px; margin-top: 16px; }
.nav-buttons button { flex: 1; margin-top: 0; }
button { border: none; background: #111; color: white; padding: 10px 14px; border-radius: 10px; font-size: 14px; cursor: pointer; margin-top: 12px; transition: 0.2s; width: 100%; }
button:hover { transform: translateY(-1px); opacity: 0.9; }
button.secondary { background: #f3f4f6; color: #111; }
</style>
