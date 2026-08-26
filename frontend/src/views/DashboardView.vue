<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
    <Navbar />

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-8">

      <!-- Encabezado con Bienvenida y Acciones Rápidas -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Panel de Control
          </h1>
          <p class="text-xs sm:text-sm font-medium text-slate-500 mt-1">
            Resumen ejecutivo del inventario y ventas en tiempo real
          </p>
        </div>

        <div class="flex items-center gap-2.5">
          <button
            @click="cargarDatosDashboard"
            :disabled="cargando"
            class="px-3.5 py-2 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs rounded-xl border border-slate-200 shadow-xs flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <svg class="w-3.5 h-3.5 text-slate-500" :class="{ 'animate-spin': cargando }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Actualizar</span>
          </button>

          <router-link
            to="/pos"
            class="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-md shadow-emerald-600/20 flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>Nueva Venta</span>
          </router-link>
        </div>
      </div>

      <!-- Tarjetas de Métricas Principales (KPIs) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">

        <!-- Ventas de Hoy -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Ventas Hoy</span>
            <div class="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-black">
              💵
            </div>
          </div>
          <p class="text-2xl sm:text-3xl font-black text-slate-900 mt-3 tracking-tight">
            ${{ Number(resumen.ganancia_diaria || 0).toLocaleString('es-AR') }}
          </p>
          <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-emerald-700 bg-emerald-50 w-fit px-2 py-0.5 rounded-md">
            <span>{{ resumen.cantidad_ventas_hoy || 0 }} transacciones hoy</span>
          </div>
        </div>

        <!-- Ventas del Mes -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Recaudación Mes</span>
            <div class="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-black">
              📈
            </div>
          </div>
          <p class="text-2xl sm:text-3xl font-black text-slate-900 mt-3 tracking-tight">
            ${{ Number(resumen.ganancia_mensual || 0).toLocaleString('es-AR') }}
          </p>
          <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-indigo-700 bg-indigo-50 w-fit px-2 py-0.5 rounded-md">
            <span>{{ resumen.cantidad_ventas_mes || 0 }} ventas acumuladas</span>
          </div>
        </div>

        <!-- Alertas de Reposición -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Stock Crítico</span>
            <div class="w-9 h-9 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center font-black">
              ⚠️
            </div>
          </div>
          <p class="text-2xl sm:text-3xl font-black text-slate-900 mt-3 tracking-tight" :class="alertasCount > 0 ? 'text-rose-600' : 'text-slate-900'">
            {{ alertasCount }}
          </p>
          <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold" :class="alertasCount > 0 ? 'text-rose-700 bg-rose-50' : 'text-slate-500 bg-slate-50'" class="w-fit px-2 py-0.5 rounded-md">
            <span>{{ alertasCount > 0 ? 'Requiere reposición urgente' : 'Inventario en nivel óptimo' }}</span>
          </div>
        </div>

        <!-- Catálogo Total -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden group">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Modelos Activos</span>
            <div class="w-9 h-9 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center font-black">
              🏷️
            </div>
          </div>
          <p class="text-2xl sm:text-3xl font-black text-slate-900 mt-3 tracking-tight">
            {{ totalPrendas }}
          </p>
          <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-slate-600 bg-slate-50 w-fit px-2 py-0.5 rounded-md">
            <span>Prendas en base de datos</span>
          </div>
        </div>

      </div>

      <!-- Cuadrícula: Top Productos y Alertas Detalladas -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Top Productos Más Vendidos -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h2 class="text-base font-extrabold text-slate-900 flex items-center gap-2">
                <span>🔥</span> Top 5 Productos Más Vendidos
              </h2>
              <p class="text-xs text-slate-500 font-medium">Mayor rotación durante el mes</p>
            </div>
            <router-link to="/catalogo" class="text-xs font-bold text-indigo-600 hover:text-indigo-700">Ver catálogo &rarr;</router-link>
          </div>

          <div v-if="!resumen.productos_top || resumen.productos_top.length === 0" class="py-8 text-center text-slate-400 text-sm font-medium">
            <svg class="w-10 h-10 mx-auto text-slate-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            No se registran ventas para el periodo actual.
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="(prod, idx) in resumen.productos_top"
              :key="idx"
              class="p-3 rounded-xl bg-slate-50 hover:bg-slate-100/80 border border-slate-100 flex items-center justify-between gap-3 transition-colors"
            >
              <div class="flex items-center gap-3">
                <span class="w-6 h-6 rounded-lg bg-indigo-100 text-indigo-700 font-black text-xs flex items-center justify-center">
                  {{ idx + 1 }}
                </span>
                <div>
                  <h4 class="text-xs sm:text-sm font-extrabold text-slate-900">{{ prod.nombre }}</h4>
                  <span class="text-[11px] font-bold text-slate-500">Talle: <strong class="text-slate-800">{{ prod.talle }}</strong></span>
                </div>
              </div>

              <div class="text-right">
                <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200/60">
                  {{ prod.cantidad_vendida }} un.
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Alertas de Stock Urgentes -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h2 class="text-base font-extrabold text-slate-900 flex items-center gap-2">
                <span>⚠️</span> Reposición Urgente de Stock
              </h2>
              <p class="text-xs text-slate-500 font-medium">Prendas con stock menor o igual al mínimo</p>
            </div>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full" :class="alertasCount > 0 ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'">
              {{ alertasCount }} faltantes
            </span>
          </div>

          <div v-if="alertas.length === 0" class="py-8 text-center text-slate-400 text-sm font-medium">
            <svg class="w-10 h-10 mx-auto text-emerald-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-emerald-700 font-bold">¡Inventario en excelente estado!</p>
            <p class="text-xs text-slate-400 mt-0.5">Todas las prendas tienen suficiente disponibilidad.</p>
          </div>

          <div v-else class="space-y-2.5 max-h-[300px] overflow-y-auto pr-1">
            <div
              v-for="item in alertas"
              :key="item.id_stock_prenda"
              class="p-3 rounded-xl bg-rose-50/50 border border-rose-100 flex items-center justify-between gap-3"
            >
              <div class="space-y-0.5">
                <div class="flex items-center gap-2">
                  <h4 class="text-xs sm:text-sm font-extrabold text-slate-900">{{ item.prenda?.nombre || 'Prenda' }}</h4>
                  <span class="text-[10px] font-black uppercase bg-white px-2 py-0.5 rounded border border-rose-200 text-rose-700">
                    Talle {{ item.talle }}
                  </span>
                </div>
                <div class="text-[11px] font-medium text-slate-600">
                  Stock actual: <strong class="text-rose-700 font-black">{{ item.stock_actual }}</strong> (Mínimo: {{ item.stock_minimo }}) &bull; <span class="font-mono text-slate-400">{{ item.codigo_barras }}</span>
                </div>
              </div>

              <button
                @click="descargarPDF(item.id_prenda)"
                title="Imprimir etiquetas con código de barras"
                class="px-2.5 py-1.5 bg-white hover:bg-slate-100 text-slate-700 text-xs font-bold rounded-lg border border-slate-200 shadow-2xs transition-colors shrink-0 cursor-pointer"
              >
                🖨️ PDF
              </button>
            </div>
          </div>
        </div>

      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/PrendasManager.vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const cargando = ref(false)
const resumen = ref({
  ganancia_diaria: 0,
  ganancia_mensual: 0,
  cantidad_ventas_hoy: 0,
  cantidad_ventas_mes: 0,
  productos_top: []
})
const alertas = ref([])
const alertasCount = ref(0)
const totalPrendas = ref(0)

const getAuthHeaders = () => {
  const user = JSON.parse(localStorage.getItem('usuario_stock') || '{}')
  return {
    'Content-Type': 'application/json',
    ...(user.token ? { 'Authorization': `Bearer ${user.token}` } : {})
  }
}

const descargarPDF = (idPrenda) => {
  window.open(`${API_URL}/prendas/${idPrenda}/pdf-codigos`, '_blank')
}

const cargarDatosDashboard = async () => {
  cargando.value = true
  const headers = getAuthHeaders()

  try {
    // 1. Cargar resumen financiero
    const resResumen = await fetch(`${API_URL}/reportes/resumen`, { headers })
    if (resResumen.ok) {
      resumen.value = await resResumen.json()
    }

    // 2. Cargar alertas
    const resAlertas = await fetch(`${API_URL}/prendas/alertas/reposicion`, { headers })
    if (resAlertas.ok) {
      alertas.value = await resAlertas.json()
      alertasCount.value = alertas.value.length
    }

    // 3. Cargar total de prendas
    const resPrendas = await fetch(`${API_URL}/prendas/`, { headers })
    if (resPrendas.ok) {
      const prendasData = await resPrendas.json()
      totalPrendas.value = prendasData.length
    }
  } catch (e) {
    console.error("Error al cargar datos del dashboard:", e)
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  cargarDatosDashboard()
})
</script>