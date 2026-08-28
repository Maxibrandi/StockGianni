<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
    <Navbar />

    <!-- Toast de notificación -->
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-2"
    >
      <div
        v-if="toast.visible"
        class="fixed bottom-5 right-5 z-50 flex items-center gap-3 px-4 py-3.5 rounded-2xl shadow-xl text-sm font-semibold max-w-sm"
        :class="toast.type === 'success' ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'"
        role="alert"
        aria-live="polite"
      >
        <svg v-if="toast.type === 'success'" class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <svg v-else class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </transition>

    <div class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">

        <!-- Columna Izquierda: Escáner y Catálogo -->
        <div class="lg:col-span-2 space-y-4">

          <!-- Encabezado POS -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Punto de Venta</h1>
              <p class="text-xs sm:text-sm font-medium text-slate-500 mt-0.5">
                Operador: <strong class="text-slate-700">{{ usuario?.nombre || usuario?.email || 'Vendedor' }}</strong>
                <span class="ml-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold uppercase" :class="esAdmin ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'">
                  {{ usuario?.rol || 'vendedor' }}
                </span>
              </p>
            </div>
          </div>

          <!-- Escáner de Código de Barras -->
          <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs space-y-3">
            <label for="scanner-input" class="block text-xs font-bold text-slate-500 uppercase tracking-wider">
              Escanear Código de Barras
            </label>
            <div class="flex gap-2.5">
              <div class="relative flex-1">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <!-- Ícono escáner -->
                  <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h1M4 10h1M4 14h1M4 18h1M8 4v16M12 4v16M16 4v16M20 6h-1M20 10h-1M20 14h-1M20 18h-1" />
                  </svg>
                </div>
                <input
                  id="scanner-input"
                  ref="inputEscaner"
                  v-model="codigoEscaneado"
                  @keyup.enter="agregarAlCarritoPorCodigo"
                  type="text"
                  placeholder="Pase la lectora o ingrese el código..."
                  autofocus
                  class="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl font-semibold text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all placeholder:text-slate-400"
                />
              </div>
              <button
                @click="agregarAlCarritoPorCodigo"
                :disabled="!codigoEscaneado.trim() || buscandoCodigo"
                class="px-5 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl border border-indigo-700 shadow-sm transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shrink-0"
              >
                <svg v-if="buscandoCodigo" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>{{ buscandoCodigo ? 'Buscando...' : 'Agregar' }}</span>
              </button>
            </div>
          </div>

          <!-- Selección Manual del Catálogo -->
          <div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
            <button
              @click="mostrarSelectorManual = !mostrarSelectorManual"
              class="w-full flex items-center justify-between p-4 text-sm font-bold text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <span class="flex items-center gap-2">
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                Seleccionar del Catálogo
              </span>
              <svg
                class="w-4 h-4 text-slate-400 transition-transform duration-200"
                :class="mostrarSelectorManual ? 'rotate-180' : ''"
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="opacity-0 -translate-y-2"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 -translate-y-2"
            >
              <div v-if="mostrarSelectorManual" class="border-t border-slate-100 p-4 space-y-3">
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                  <input
                    v-model="filtroCatalogo"
                    type="text"
                    placeholder="Filtrar por nombre, categoría o tela..."
                    class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all placeholder:text-slate-400"
                  />
                </div>

                <!-- Skeleton catálogo -->
                <div v-if="cargandoCatalogo" class="space-y-2">
                  <div v-for="i in 4" :key="i" class="py-3 flex items-center gap-3">
                    <div class="flex-1 h-3.5 bg-slate-100 rounded animate-pulse"></div>
                    <div class="flex gap-1.5">
                      <div class="w-16 h-7 bg-slate-100 rounded-lg animate-pulse"></div>
                      <div class="w-16 h-7 bg-slate-100 rounded-lg animate-pulse"></div>
                    </div>
                  </div>
                </div>

                <div v-else-if="catalogoFiltrado.length === 0" class="py-6 text-center text-xs text-slate-400 font-medium">
                  No se encontraron prendas que coincidan con la búsqueda.
                </div>

                <div v-else class="max-h-52 overflow-y-auto divide-y divide-slate-100 -mx-1 px-1">
                  <div
                    v-for="prenda in catalogoFiltrado"
                    :key="prenda.id_prenda"
                    class="py-2.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
                  >
                    <div class="min-w-0">
                      <span class="text-xs font-bold text-slate-900 truncate block">{{ prenda.nombre }}</span>
                      <span class="text-[10px] text-slate-500 font-medium">{{ prenda.categoria }} · {{ prenda.tipo_tela }}</span>
                    </div>
                    <div class="flex flex-wrap gap-1.5 shrink-0">
                      <button
                        v-for="v in prenda.variantes"
                        :key="v.id_stock_prenda"
                        @click="agregarVarianteDirecta(prenda, v)"
                        :disabled="v.stock_actual <= 0"
                        class="px-2.5 py-1 rounded-lg border text-xs font-bold transition-colors cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                        :class="v.stock_actual <= 0 ? 'bg-slate-50 border-slate-200 text-slate-400' : v.stock_actual <= v.stock_minimo ? 'bg-amber-50 border-amber-200 text-amber-700 hover:bg-amber-100' : 'bg-slate-100 border-slate-200 text-slate-700 hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-700'"
                        :title="v.stock_actual <= 0 ? 'Sin stock' : `${v.stock_actual} unidades disponibles`"
                      >
                        {{ v.talle }} · ${{ Number(v.precio_venta).toLocaleString('es-AR') }}
                        <span class="ml-1 opacity-60">[{{ v.stock_actual }}]</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- Carrito / Detalle de Venta -->
          <div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
            <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
              <h2 class="text-sm font-black text-slate-900 flex items-center gap-2">
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Detalle de Venta
                <span class="text-slate-400 font-semibold text-xs">({{ totalItemsEnCarrito }} {{ totalItemsEnCarrito === 1 ? 'prenda' : 'prendas' }})</span>
              </h2>
              <button
                v-if="carrito.length > 0"
                @click="carrito = []"
                class="text-xs font-bold text-rose-600 hover:text-rose-700 hover:bg-rose-50 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
              >
                Vaciar carrito
              </button>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead>
                  <tr class="text-[11px] font-black uppercase tracking-wider text-slate-400 border-b border-slate-100 bg-slate-50/50">
                    <th class="py-3 px-4">Producto</th>
                    <th class="py-3 px-4 hidden sm:table-cell">Precio</th>
                    <th class="py-3 px-4 text-center">Cant.</th>
                    <th class="py-3 px-4 text-right">Subtotal</th>
                    <th class="py-3 px-4 w-10"></th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(item, idx) in carrito" :key="item.id_stock_prenda" class="hover:bg-slate-50/50 transition-colors">
                    <td class="py-3 px-4">
                      <span class="text-sm font-bold text-slate-900 block">{{ item.nombre }}</span>
                      <span class="text-[11px] text-slate-500 font-medium">
                        Talle {{ item.talle }} &bull; <span class="font-mono">{{ item.codigo_barras }}</span>
                      </span>
                    </td>
                    <td class="py-3 px-4 text-xs font-semibold text-slate-700 hidden sm:table-cell">
                      ${{ Number(item.precio).toLocaleString('es-AR') }}
                    </td>
                    <td class="py-3 px-4">
                      <div class="flex items-center justify-center">
                        <div class="inline-flex items-center border border-slate-200 rounded-lg overflow-hidden bg-white shadow-xs">
                          <button
                            @click="cambiarCantidad(item, -1)"
                            class="px-2.5 py-1.5 text-slate-600 hover:bg-slate-100 font-bold text-sm transition-colors cursor-pointer"
                            aria-label="Restar"
                          >−</button>
                          <span class="px-3 py-1.5 font-black text-sm text-slate-900 border-x border-slate-200 min-w-[32px] text-center">{{ item.cantidad }}</span>
                          <button
                            @click="cambiarCantidad(item, 1)"
                            class="px-2.5 py-1.5 text-slate-600 hover:bg-slate-100 font-bold text-sm transition-colors cursor-pointer"
                            aria-label="Sumar"
                          >+</button>
                        </div>
                      </div>
                    </td>
                    <td class="py-3 px-4 text-right">
                      <span class="text-sm font-black text-emerald-700">
                        ${{ (item.precio * item.cantidad).toLocaleString('es-AR') }}
                      </span>
                    </td>
                    <td class="py-3 px-4 text-right">
                      <button
                        @click="carrito.splice(idx, 1)"
                        class="text-slate-400 hover:text-rose-600 hover:bg-rose-50 p-1.5 rounded-lg transition-colors cursor-pointer"
                        aria-label="Eliminar del carrito"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="carrito.length === 0">
                    <td colspan="5" class="py-12 text-center">
                      <svg class="w-10 h-10 mx-auto text-slate-300 mb-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                      <p class="text-sm text-slate-400 font-medium">El carrito está vacío.</p>
                      <p class="text-xs text-slate-400 mt-1">Escanee un código o seleccione una prenda del catálogo.</p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- Columna Derecha: Resumen y Cobro -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-6 space-y-5 sticky top-24">
            <h2 class="text-lg font-black text-slate-900 flex items-center gap-2">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Resumen de Cobro
            </h2>

            <!-- Detalle de importes -->
            <div class="space-y-2.5 text-sm">
              <div class="flex justify-between text-slate-600 font-medium">
                <span>Líneas de productos</span>
                <span class="font-bold text-slate-900">{{ carrito.length }}</span>
              </div>
              <div class="flex justify-between text-slate-600 font-medium">
                <span>Total de prendas</span>
                <span class="font-bold text-slate-900">{{ totalItemsEnCarrito }}</span>
              </div>
              <div class="border-t border-dashed border-slate-200 pt-2.5 flex justify-between items-end">
                <span class="font-bold text-slate-700">Total a cobrar</span>
                <span class="text-3xl font-black text-emerald-700 tracking-tight">
                  ${{ totalVenta.toLocaleString('es-AR') }}
                </span>
              </div>
            </div>

            <!-- Mensaje de error inline -->
            <div v-if="mensajeError" class="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs font-semibold text-rose-700 flex items-start gap-2">
              <svg class="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ mensajeError }}</span>
            </div>

            <!-- Botón Confirmar Venta -->
            <button
              @click="procesarVenta"
              :disabled="carrito.length === 0 || procesando"
              class="w-full py-4 bg-emerald-600 hover:bg-emerald-700 text-white font-black text-base rounded-xl shadow-lg shadow-emerald-600/20 transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2.5"
            >
              <svg v-if="procesando" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ procesando ? 'Procesando venta...' : 'Confirmar Venta' }}
            </button>

            <!-- Nota de ayuda -->
            <p v-if="carrito.length === 0" class="text-xs text-slate-400 text-center font-medium">
              Agregue prendas al carrito para habilitar el cobro.
            </p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/PrendasManager.vue'

const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const inputEscaner = ref(null)
const codigoEscaneado = ref('')
const carrito = ref([])
const catalogoPrendas = ref([])
const filtroCatalogo = ref('')
const mostrarSelectorManual = ref(false)
const procesando = ref(false)
const buscandoCodigo = ref(false)
const cargandoCatalogo = ref(false)
const mensajeError = ref('')

const toast = reactive({ visible: false, message: '', type: 'success' })
let toastTimer = null

const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.message = message
  toast.type = type
  toast.visible = true
  toastTimer = setTimeout(() => { toast.visible = false }, 4000)
}

const usuario = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('usuario_stock') || '{}')
  } catch (e) {
    return {}
  }
})

const esAdmin = computed(() => {
  const rol = (usuario.value?.rol || '').toLowerCase()
  return rol === 'admin' || rol === 'administrador'
})

const getAuthHeaders = () => {
  const token = usuario.value?.token
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  }
}

const totalVenta = computed(() => {
  return carrito.value.reduce((acc, item) => acc + (Number(item.precio) * item.cantidad), 0)
})

const totalItemsEnCarrito = computed(() => {
  return carrito.value.reduce((acc, item) => acc + item.cantidad, 0)
})

const catalogoFiltrado = computed(() => {
  if (!filtroCatalogo.value.trim()) return catalogoPrendas.value
  const term = filtroCatalogo.value.trim().toLowerCase()
  return catalogoPrendas.value.filter(p =>
    p.nombre.toLowerCase().includes(term) ||
    p.tipo_tela.toLowerCase().includes(term) ||
    p.categoria.toLowerCase().includes(term)
  )
})

const cargarCatalogo = async () => {
  cargandoCatalogo.value = true
  try {
    const res = await fetch(`${API_URL}/prendas/`, { headers: getAuthHeaders() })
    if (res.ok) {
      catalogoPrendas.value = await res.json()
    }
  } catch (e) {
    console.error('Error al cargar catálogo:', e)
  } finally {
    cargandoCatalogo.value = false
  }
}

const agregarVarianteDirecta = (prenda, variante) => {
  mensajeError.value = ''

  const itemExistente = carrito.value.find(i => i.id_stock_prenda === variante.id_stock_prenda)

  if (itemExistente) {
    if (itemExistente.cantidad + 1 > variante.stock_actual) {
      mensajeError.value = `Stock máximo alcanzado para ${prenda.nombre} (Talle: ${variante.talle}). Disponibles: ${variante.stock_actual}`
      return
    }
    itemExistente.cantidad += 1
  } else {
    carrito.value.push({
      id_stock_prenda: variante.id_stock_prenda,
      nombre: prenda.nombre,
      talle: variante.talle,
      precio: Number(variante.precio_venta || 0),
      codigo_barras: variante.codigo_barras,
      stock_actual: variante.stock_actual,
      cantidad: 1
    })
  }
}

const cambiarCantidad = (item, delta) => {
  mensajeError.value = ''
  if (delta > 0 && item.cantidad + delta > item.stock_actual) {
    mensajeError.value = `Sin más stock disponible para ${item.nombre} (Talle ${item.talle}). Máximo: ${item.stock_actual}`
    return
  }
  item.cantidad += delta
  if (item.cantidad <= 0) {
    const idx = carrito.value.findIndex(i => i.id_stock_prenda === item.id_stock_prenda)
    if (idx !== -1) carrito.value.splice(idx, 1)
  }
}

const agregarAlCarritoPorCodigo = async () => {
  const code = codigoEscaneado.value.trim()
  if (!code) return

  mensajeError.value = ''
  buscandoCodigo.value = true

  try {
    const res = await fetch(`${API_URL}/prendas/buscar/codigo?codigo=${encodeURIComponent(code)}`, {
      headers: getAuthHeaders()
    })

    if (res.ok) {
      const prenda = await res.json()
      const variante = prenda.variantes.find(v => v.codigo_barras === code) || prenda.variantes[0]

      if (!variante) {
        mensajeError.value = 'No se encontraron talles disponibles para esta prenda.'
        return
      }

      if (variante.stock_actual <= 0) {
        mensajeError.value = `Sin stock para ${prenda.nombre} (Talle ${variante.talle}).`
        return
      }

      agregarVarianteDirecta(prenda, variante)
    } else {
      mensajeError.value = `Código "${code}" no registrado en el inventario.`
    }
  } catch (e) {
    console.error(e)
    mensajeError.value = 'Error de conexión al buscar el código de barras.'
  } finally {
    buscandoCodigo.value = false
    codigoEscaneado.value = ''
    if (inputEscaner.value) inputEscaner.value.focus()
  }
}

const procesarVenta = async () => {
  if (carrito.value.length === 0) return

  mensajeError.value = ''
  procesando.value = true

  try {
    const payload = {
      productos: carrito.value.map(i => ({
        id_stock_prenda: i.id_stock_prenda,
        cantidad: i.cantidad
      }))
    }

    const res = await fetch(`${API_URL}/ventas/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      const ventaRegistrada = await res.json()
      showToast(`✅ Venta #${ventaRegistrada.id_venta} registrada por $${Number(ventaRegistrada.total).toLocaleString('es-AR')}`, 'success')
      carrito.value = []
      await cargarCatalogo()
    } else {
      const err = await res.json().catch(() => ({}))
      mensajeError.value = err.detail || 'Error al procesar la venta. Verifique disponibilidad de stock.'
    }
  } catch (e) {
    console.error('Error al registrar venta:', e)
    mensajeError.value = 'Error de conexión con el servidor.'
  } finally {
    procesando.value = false
  }
}

onMounted(() => {
  cargarCatalogo()
})
</script>