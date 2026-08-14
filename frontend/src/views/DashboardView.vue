<template>
  <div class="min-h-screen bg-slate-300 p-6 font-sans text-black space-y-6">
    <header class="bg-white p-6 rounded-2xl shadow-md border-2 border-black flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-black">Panel de Control (Dashboard)</h1>
        <p class="text-sm font-bold text-slate-700">Métricas generales de la tienda</p>
      </div>
      <div class="flex gap-2">
        <router-link to="/catalogo" class="px-4 py-2 bg-indigo-800 text-white font-black rounded-xl border-2 border-black">
          Ir al Catálogo
        </router-link>
        <router-link to="/pos" class="px-4 py-2 bg-emerald-700 text-white font-black rounded-xl border-2 border-black">
          Ir a Caja (POS)
        </router-link>
      </div>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-2xl border-2 border-black shadow-md">
        <h3 class="text-lg font-black uppercase">Ventas de Hoy</h3>
        <p class="text-4xl font-black text-emerald-800 mt-2">${{ gananciasDiarias.toLocaleString('es-AR') }}</p>
      </div>
      <div class="bg-white p-6 rounded-2xl border-2 border-black shadow-md">
        <h3 class="text-lg font-black uppercase">Ventas del Mes</h3>
        <p class="text-4xl font-black text-indigo-900 mt-2">${{ gananciasMensuales.toLocaleString('es-AR') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_URL = 'http://localhost:8000/api/v1'
const gananciasDiarias = ref(0)
const gananciasMensuales = ref(0)

onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/ventas/reporte-ganancias`)
    if (res.ok) {
      const data = await res.json()
      gananciasDiarias.value = data.ganancia_diaria
      gananciasMensuales.value = data.ganancia_mensual
    }
  } catch (e) {
    console.error("Error al obtener ganancias:", e)
  }
})
</script>