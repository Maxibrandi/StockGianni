<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
    <Navbar />

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6">

      <!-- Encabezado Principal y Acciones -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-3">
            <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
              Control de Inventario
            </h1>
            <span
              class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider"
              :class="esAdmin ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'"
            >
              {{ usuarioAutenticado?.rol || 'Usuario' }}
            </span>
          </div>
          <p class="text-xs sm:text-sm font-medium text-slate-500 mt-1">
            Gestión y consulta de prendas, talles y niveles de stock en tiempo real
          </p>
        </div>

        <div class="flex items-center gap-2.5">
          <router-link
            to="/pos"
            class="px-4 py-2.5 bg-white hover:bg-slate-100/80 text-slate-900 font-bold text-xs rounded-xl shadow-xs flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>Ir a Caja (POS)</span>
          </router-link>

          <button
            v-if="esAdmin"
            @click="mostrarModalCrear = true"
            class="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md shadow-indigo-600/10 flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Nueva Prenda</span>
          </button>
        </div>
      </div>

      <!-- Tarjetas de Métricas Rápidas (Solo Admin) -->
      <section v-if="esAdmin" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white p-6 rounded-2xl shadow-xs flex items-center justify-between">
          <div>
            <p class="text-xs font-black uppercase tracking-wider text-slate-900">Ganancia Real Hoy</p>
            <h3 class="text-2xl sm:text-3xl font-black text-slate-900 mt-1 tracking-tight">
              ${{ Number(gananciasDiarias || 0).toLocaleString('es-AR') }}
            </h3>
          </div>
          <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-black text-xl">
            💵
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-xs flex items-center justify-between">
          <div>
            <p class="text-xs font-black uppercase tracking-wider text-slate-900">Ganancia Real del Mes</p>
            <h3 class="text-2xl sm:text-3xl font-black text-slate-900 mt-1 tracking-tight">
              ${{ Number(gananciasMensuales || 0).toLocaleString('es-AR') }}
            </h3>
          </div>
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-black text-xl">
            📈
          </div>
        </div>
      </section>

      <!-- Barra de Búsqueda y Filtros -->
      <section class="bg-white p-5 rounded-2xl shadow-xs">
        <label for="search-barcode" class="block text-xs font-black text-slate-900 uppercase tracking-wider mb-2">
          Buscar por Código de Barras o Filtrar por Nombre / Categoría
        </label>
        <div class="flex flex-col sm:flex-row gap-3">
          <div class="relative flex-1">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              id="search-barcode"
              v-model="codigoBusqueda"
              @keyup.enter="buscarPorCodigo"
              type="text"
              placeholder="Pase el lector sobre el código o ingrese texto..."
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border-0 rounded-xl text-slate-900 font-medium text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
            />
          </div>
          <button
            @click="buscarPorCodigo"
            class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors cursor-pointer"
          >
            Buscar
          </button>
          <button
            v-if="filtroActivo"
            @click="limpiarFiltro"
            class="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition-colors cursor-pointer"
          >
            Limpiar Filtro
          </button>
        </div>
        <p v-if="mensajeBusqueda" class="text-xs font-semibold text-indigo-600 mt-2 flex items-center gap-1">
          <span>ℹ️</span> {{ mensajeBusqueda }}
        </p>
      </section>

      <!-- Cuadrícula: Alertas y Listado de Prendas -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Alertas Bajo Stock -->
        <div class="lg:col-span-1">
          <div class="bg-white p-5 rounded-2xl shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-2 border-b border-slate-100">
              <h2 class="text-base font-black text-slate-900 flex items-center gap-2">
                <span class="relative flex h-2.5 w-2.5">
                  <span v-if="alertasStock.length > 0" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5" :class="alertasStock.length > 0 ? 'bg-rose-500' : 'bg-emerald-500'"></span>
                </span>
                Stock Crítico ({{ alertasStock.length }})
              </h2>
            </div>

            <div v-if="alertasStock.length === 0" class="py-8 text-center text-slate-400 text-xs font-medium">
              <svg class="w-8 h-8 mx-auto text-emerald-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Sin alertas activas. Stock en nivel correcto.
            </div>

            <ul v-else class="divide-y divide-slate-100 max-h-[400px] overflow-y-auto pr-1 space-y-2">
              <li v-for="item in alertasStock" :key="item.id_stock_prenda" class="pt-2 first:pt-0">
                <div class="p-3 rounded-xl bg-rose-50/60 space-y-1">
                  <div class="flex justify-between items-center">
                    <span class="font-extrabold text-slate-900 text-xs">{{ item.prenda?.nombre || 'Prenda' }}</span>
                    <span class="bg-rose-100 text-rose-700 font-bold text-[10px] px-2 py-0.5 rounded-md uppercase">
                      Talle {{ item.talle }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-[11px] text-slate-500 font-medium">
                    <span>Stock: <strong class="text-rose-600 font-bold">{{ item.stock_actual }}</strong> (Mín: {{ item.stock_minimo }})</span>
                    <span class="font-mono text-slate-400">{{ item.codigo_barras }}</span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Tabla de Prendas -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-2xl shadow-xs overflow-hidden">
            <div class="p-4 bg-slate-50/50 flex justify-between items-center border-b border-slate-100">
              <h2 class="text-base font-black text-slate-900">Catálogo de Prendas ({{ prendasFiltradas.length }})</h2>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50/50 text-[11px] font-black uppercase tracking-wider text-slate-900 border-b border-slate-100">
                    <th class="py-3.5 px-4">ID</th>
                    <th class="py-3.5 px-4">Nombre / Categoría</th>
                    <th class="py-3.5 px-4">Tela</th>
                    <th class="py-3.5 px-4">Variantes (Talle / Stock)</th>
                    <th v-if="esAdmin" class="py-3.5 px-4 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 text-xs font-medium text-slate-700">
                  <tr v-for="prenda in prendasFiltradas" :key="prenda.id_prenda" class="hover:bg-slate-50/80 transition-colors">
                    <td class="py-3.5 px-4 font-bold text-slate-400">#{{ prenda.id_prenda }}</td>
                    <td class="py-3.5 px-4 font-extrabold text-slate-900">
                      {{ prenda.nombre }}
                      <span class="block text-[11px] font-medium text-slate-500">{{ prenda.categoria }}</span>
                    </td>
                    <td class="py-3.5 px-4 text-slate-600 font-semibold">{{ prenda.tipo_tela }}</td>
                    <td class="py-3.5 px-4">
                      <div class="flex flex-wrap gap-1.5">
                        <span
                          v-for="v in prenda.variantes"
                          :key="v.id_stock_prenda"
                          class="inline-flex items-center gap-1 rounded-lg px-2.5 py-1 text-[11px] font-bold"
                          :class="v.stock_actual <= v.stock_minimo ? 'bg-rose-50 text-rose-700' : 'bg-slate-100 text-slate-800'"
                        >
                          {{ v.talle }}: <strong class="text-slate-900">{{ v.stock_actual }}u.</strong> (${{ Number(v.precio_venta).toLocaleString('es-AR') }})
                        </span>
                      </div>
                    </td>
                    <td v-if="esAdmin" class="py-3.5 px-4 text-right">
                      <button
                        @click="descargarPDF(prenda.id_prenda)"
                        title="Imprimir etiquetas"
                        class="text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition-colors cursor-pointer inline-flex items-center gap-1"
                      >
                        🖨️ <span class="hidden sm:inline">PDF</span>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="prendasFiltradas.length === 0">
                    <td colspan="5" class="py-12 text-center text-slate-400 font-medium">
                      No se encontraron prendas registradas en el inventario.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

      <!-- Modal Crear Prenda -->
      <div v-if="mostrarModalCrear" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs">
        <div class="bg-white rounded-3xl shadow-2xl max-w-lg w-full overflow-hidden max-h-[90vh] flex flex-col">
          <div class="px-6 py-4 flex items-center justify-between bg-slate-50/50 border-b border-slate-100">
            <h3 class="text-base font-black text-slate-900">Registrar Nueva Prenda</h3>
            <button @click="mostrarModalCrear = false" class="text-slate-400 hover:text-slate-600 font-bold text-lg p-1">✕</button>
          </div>

          <form @submit.prevent="guardarPrenda" class="p-6 space-y-4 overflow-y-auto">
            <div>
              <label class="block text-xs font-black text-slate-900 uppercase tracking-wider mb-1">Nombre de la Prenda *</label>
              <input
                v-model="nuevaPrenda.nombre"
                type="text" required placeholder="Ej: Camisa Manga Larga"
                class="w-full px-3.5 py-2.5 bg-slate-50 border-0 rounded-xl text-slate-900 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-black text-slate-900 uppercase tracking-wider mb-1">Categoría *</label>
                <input
                  v-model="nuevaPrenda.categoria"
                  type="text" required placeholder="Ej: Camisas, Pantalones..."
                  class="w-full px-3.5 py-2.5 bg-slate-50 border-0 rounded-xl text-slate-900 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label class="block text-xs font-black text-slate-900 uppercase tracking-wider mb-1">Tipo de Tela *</label>
                <input
                  v-model="nuevaPrenda.tipo_tela"
                  type="text" required placeholder="Ej: Algodón, Denim..."
                  class="w-full px-3.5 py-2.5 bg-slate-50 border-0 rounded-xl text-slate-900 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="block text-xs font-black text-slate-900 uppercase tracking-wider">Talles, Precios y Cantidades</label>
                <button type="button" @click="agregarFilaVariante" class="text-xs font-bold text-indigo-600 hover:text-indigo-700 cursor-pointer">
                  + Agregar Talle
                </button>
              </div>

              <div class="space-y-2 max-h-[200px] overflow-y-auto pr-1">
                <div v-for="(v, idx) in nuevaPrenda.variantes" :key="idx" class="flex items-center gap-2 bg-slate-50 p-2 rounded-xl">
                  <input v-model="v.talle" type="text" placeholder="Talle" required class="w-16 px-2 py-1.5 bg-white border-0 rounded-lg text-xs font-bold text-slate-900" />
                  <input v-model.number="v.precio_venta" type="number" step="0.01" placeholder="Precio ($)" required class="w-24 px-2 py-1.5 bg-white border-0 rounded-lg text-xs font-bold text-slate-900" />
                  <input v-model.number="v.stock_actual" type="number" placeholder="Stock" required class="w-16 px-2 py-1.5 bg-white border-0 rounded-lg text-xs font-bold text-slate-900" />
                  <input v-model.number="v.stock_minimo" type="number" placeholder="Mínimo" required class="w-16 px-2 py-1.5 bg-white border-0 rounded-lg text-xs font-bold text-slate-900" />
                  <button type="button" @click="nuevaPrenda.variantes.splice(idx, 1)" class="text-rose-600 font-bold text-xs p-1 hover:bg-rose-50 rounded-md cursor-pointer">✕</button>
                </div>
              </div>
            </div>

            <div v-if="errorCrear" class="p-3 bg-rose-50 rounded-xl text-xs font-semibold text-rose-700 text-center">
              {{ errorCrear }}
            </div>

            <div class="pt-4 border-t border-slate-100 flex justify-end gap-2">
              <button type="button" @click="mostrarModalCrear = false" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors">
                Cancelar
              </button>
              <button type="submit" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-xs transition-colors cursor-pointer">
                Guardar Prenda
              </button>
            </div>
          </form>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/PrendasManager.vue'

const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const usuarioAutenticado = ref(null)
const esAdmin = computed(() => {
  const rol = (usuarioAutenticado.value?.rol || '').toLowerCase()
  return rol === 'admin' || rol === 'administrador'
})

const gananciasDiarias = ref(0)
const gananciasMensuales = ref(0)

const prendas = ref([])
const alertasStock = ref([])
const codigoBusqueda = ref('')
const mensajeBusqueda = ref('')
const filtroActivo = ref(false)
const mostrarModalCrear = ref(false)
const errorCrear = ref('')

const nuevaPrenda = ref({
  nombre: '',
  categoria: '',
  tipo_tela: '',
  variantes: [
    { talle: 'S', precio_venta: 15000, stock_actual: 10, stock_minimo: 3 },
    { talle: 'M', precio_venta: 15000, stock_actual: 10, stock_minimo: 3 }
  ]
})

const getAuthHeaders = () => {
  const token = usuarioAutenticado.value?.token
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  }
}

const agregarFilaVariante = () => {
  nuevaPrenda.value.variantes.push({ talle: '', precio_venta: 0, stock_actual: 0, stock_minimo: 0 })
}

const prendasFiltradas = computed(() => {
  if (!codigoBusqueda.value.trim() || !filtroActivo.value) {
    return prendas.value
  }
  const term = codigoBusqueda.value.trim().toLowerCase()
  return prendas.value.filter(p =>
    p.nombre.toLowerCase().includes(term) ||
    p.categoria.toLowerCase().includes(term) ||
    p.tipo_tela.toLowerCase().includes(term) ||
    p.variantes.some(v => v.codigo_barras?.toLowerCase().includes(term))
  )
})

const cargarDatos = async () => {
  try {
    const headers = getAuthHeaders()

    // 1. Cargar prendas
    const resPrendas = await fetch(`${API_URL}/prendas/`, { headers })
    if (resPrendas.ok) prendas.value = await resPrendas.json()

    // 2. Cargar alertas
    const resAlertas = await fetch(`${API_URL}/prendas/alertas/reposicion`, { headers })
    if (resAlertas.ok) alertasStock.value = await resAlertas.json()

    // 3. Cargar ganancias si es admin
    if (esAdmin.value) {
      const resGanancias = await fetch(`${API_URL}/reportes/resumen`, { headers })
      if (resGanancias.ok) {
        const datos = await resGanancias.json()
        gananciasDiarias.value = datos.ganancia_diaria
        gananciasMensuales.value = datos.ganancia_mensual
      }
    }
  } catch (error) {
    console.error("Error al conectar con el servidor:", error)
  }
}

const guardarPrenda = async () => {
  errorCrear.value = ''
  try {
    const response = await fetch(`${API_URL}/prendas/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(nuevaPrenda.value)
    })

    if (response.ok) {
      mostrarModalCrear.value = false
      nuevaPrenda.value = {
        nombre: '',
        categoria: '',
        tipo_tela: '',
        variantes: [{ talle: 'S', precio_venta: 15000, stock_actual: 10, stock_minimo: 3 }]
      }
      await cargarDatos()
    } else {
      const err = await response.json().catch(() => ({}))
      errorCrear.value = err.detail || 'Error al guardar la prenda. Verifique los datos.'
    }
  } catch (error) {
    console.error("Error guardando prenda:", error)
    errorCrear.value = 'Error de conexión con el servidor.'
  }
}

const buscarPorCodigo = async () => {
  const query = codigoBusqueda.value.trim()
  if (!query) {
    filtroActivo.value = false
    mensajeBusqueda.value = ''
    return
  }

  filtroActivo.value = true
  try {
    const res = await fetch(`${API_URL}/prendas/buscar/codigo?codigo=${encodeURIComponent(query)}`, {
      headers: getAuthHeaders()
    })
    if (res.ok) {
      const prenda = await res.json()
      mensajeBusqueda.value = `Encontrado: ${prenda.nombre} (${prenda.categoria})`
      if (!prendas.value.some(p => p.id_prenda === prenda.id_prenda)) {
        prendas.value.unshift(prenda)
      }
    } else {
      mensajeBusqueda.value = `Filtrando por: "${query}"`
    }
  } catch (e) {
    mensajeBusqueda.value = `Filtrando por: "${query}"`
  }
}

const limpiarFiltro = () => {
  codigoBusqueda.value = ''
  mensajeBusqueda.value = ''
  filtroActivo.value = false
}

const descargarPDF = (idPrenda) => {
  window.open(`${API_URL}/prendas/${idPrenda}/pdf-codigos`, '_blank')
}

onMounted(() => {
  const sesionGuardada = localStorage.getItem('usuario_stock')
  if (sesionGuardada) {
    usuarioAutenticado.value = JSON.parse(sesionGuardada)
  }
  cargarDatos()
})
</script>