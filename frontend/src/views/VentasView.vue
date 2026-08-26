<template>
  <div class="min-h-screen bg-slate-300 p-4 font-sans text-black">
    <div class="max-w-7xl mx-auto space-y-4">

      <!-- Header y Navegación -->
      <header class="bg-white p-4 rounded-2xl shadow-md border-2 border-black flex flex-col sm:flex-row justify-between items-center gap-3">
        <div>
          <h1 class="text-2xl font-black text-black">Caja / Punto de Venta (POS)</h1>
          <p class="text-xs font-bold text-slate-700">Operador: {{ usuario?.nombre || usuario?.email || 'Vendedor' }} ({{ usuario?.rol }})</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <router-link
            v-if="esAdmin"
            to="/dashboard"
            class="px-4 py-2 bg-indigo-100 hover:bg-indigo-200 border-2 border-black rounded-xl font-black text-xs"
          >
            📊 Dashboard
          </router-link>
          <router-link
            to="/catalogo"
            class="px-4 py-2 bg-slate-200 hover:bg-slate-300 border-2 border-black rounded-xl font-black text-xs"
          >
            🏷️ Catálogo & Stock
          </router-link>
          <button
            @click="cerrarSesion"
            class="px-4 py-2 bg-slate-200 hover:bg-slate-300 border-2 border-black rounded-xl font-black text-xs"
          >
            Cerrar Sesión
          </button>
        </div>
      </header>

      <!-- Mensajes de Estado / Alertas -->
      <div v-if="mensajeExito" class="p-4 bg-emerald-100 border-2 border-emerald-800 rounded-xl text-emerald-950 font-black text-sm flex justify-between items-center">
        <span>✅ {{ mensajeExito }}</span>
        <button @click="mensajeExito = ''" class="text-emerald-950 font-bold">✕</button>
      </div>

      <div v-if="mensajeError" class="p-4 bg-red-100 border-2 border-red-800 rounded-xl text-red-950 font-black text-sm flex justify-between items-center">
        <span>❌ {{ mensajeError }}</span>
        <button @click="mensajeError = ''" class="text-red-950 font-bold">✕</button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Columna Izquierda: Escáner y Búsqueda -->
        <div class="lg:col-span-2 space-y-4">
          <!-- Entrada Escáner -->
          <div class="bg-white p-5 rounded-2xl shadow-md border-2 border-black space-y-2">
            <label class="block text-xs font-black uppercase tracking-wider">Escanear Código de Barras (Lector)</label>
            <div class="flex gap-2">
              <input
                ref="inputEscaner"
                v-model="codigoEscaneado"
                @keyup.enter="agregarAlCarritoPorCodigo"
                type="text"
                placeholder="Pase la lectora sobre el código o ingréselo..."
                autofocus
                class="w-full p-3 border-2 border-black rounded-xl font-black text-lg focus:ring-4 focus:ring-indigo-500 focus:outline-none"
              />
              <button
                @click="agregarAlCarritoPorCodigo"
                class="px-5 bg-indigo-800 hover:bg-indigo-900 text-white font-black text-sm rounded-xl border-2 border-black cursor-pointer"
              >
                Agregar
              </button>
            </div>
          </div>

          <!-- Selección Manual de Prendas -->
          <div class="bg-white p-4 rounded-2xl shadow-md border-2 border-black">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-black uppercase text-slate-700">O Seleccionar Prenda del Catálogo:</span>
              <button @click="mostrarSelectorManual = !mostrarSelectorManual" class="text-xs font-black text-indigo-900 underline">
                {{ mostrarSelectorManual ? 'Ocultar Catálogo Rápido' : 'Mostrar Catálogo Rápido' }}
              </button>
            </div>

            <div v-if="mostrarSelectorManual" class="space-y-3 pt-2 border-t-2 border-slate-200">
              <input
                v-model="filtroCatalogo"
                type="text"
                placeholder="Filtrar por nombre o tela..."
                class="w-full p-2 border-2 border-black rounded-lg text-xs font-black"
              />
              <div class="max-h-48 overflow-y-auto divide-y-2 divide-slate-100">
                <div
                  v-for="prenda in catalogoFiltrado"
                  :key="prenda.id_prenda"
                  class="py-2 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs font-black"
                >
                  <div>
                    <span>{{ prenda.nombre }} ({{ prenda.categoria }} - {{ prenda.tipo_tela }})</span>
                  </div>
                  <div class="flex flex-wrap gap-1.5">
                    <button
                      v-for="v in prenda.variantes"
                      :key="v.id_stock_prenda"
                      @click="agregarVarianteDirecta(prenda, v)"
                      :disabled="v.stock_actual <= 0"
                      class="px-2.5 py-1 rounded-lg border-2 border-black text-xs font-black disabled:opacity-40 disabled:cursor-not-allowed hover:bg-indigo-100"
                      :class="v.stock_actual <= v.stock_minimo ? 'bg-red-100' : 'bg-slate-100'"
                    >
                      {{ v.talle }} (${{ v.precio_venta }}) [{{ v.stock_actual }} u.]
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Items del Carrito -->
          <div class="bg-white rounded-2xl shadow-md border-2 border-black overflow-hidden">
            <div class="p-4 bg-slate-200 border-b-2 border-black font-black text-sm flex justify-between items-center">
              <span>Detalle de la Venta ({{ totalItemsEnCarrito }} unidades)</span>
              <button
                v-if="carrito.length > 0"
                @click="carrito = []"
                class="text-xs font-black text-red-700 hover:underline"
              >
                Vaciar Carrito
              </button>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left font-black text-sm">
                <thead>
                  <tr class="bg-slate-100 border-b-2 border-black text-xs uppercase">
                    <th class="p-3">Producto</th>
                    <th class="p-3">Precio</th>
                    <th class="p-3 text-center">Cant.</th>
                    <th class="p-3">Subtotal</th>
                    <th class="p-3 text-right">Acción</th>
                  </tr>
                </thead>
                <tbody class="divide-y-2 divide-slate-200">
                  <tr v-for="(item, idx) in carrito" :key="item.id_stock_prenda">
                    <td class="p-3">
                      {{ item.nombre }}
                      <span class="block text-xs text-slate-600 font-bold">Talle: {{ item.talle }} | Código: {{ item.codigo_barras }}</span>
                    </td>
                    <td class="p-3">${{ Number(item.precio).toLocaleString('es-AR') }}</td>
                    <td class="p-3 text-center">
                      <div class="inline-flex items-center gap-1 border-2 border-black rounded-lg p-0.5">
                        <button
                          @click="cambiarCantidad(item, -1)"
                          class="px-2 py-0.5 font-black hover:bg-slate-200 rounded text-xs"
                        >-</button>
                        <span class="px-2 font-black text-sm">{{ item.cantidad }}</span>
                        <button
                          @click="cambiarCantidad(item, 1)"
                          class="px-2 py-0.5 font-black hover:bg-slate-200 rounded text-xs"
                        >+</button>
                      </div>
                    </td>
                    <td class="p-3 font-black text-emerald-800">${{ (item.precio * item.cantidad).toLocaleString('es-AR') }}</td>
                    <td class="p-3 text-right">
                      <button @click="carrito.splice(idx, 1)" class="text-red-700 font-black hover:bg-red-100 p-1.5 rounded-lg border border-transparent hover:border-red-700">✕</button>
                    </td>
                  </tr>
                  <tr v-if="carrito.length === 0">
                    <td colspan="5" class="p-8 text-center text-slate-600 font-bold">
                      🛒 El carrito está vacío. Escanee un código de barras o seleccione una prenda arriba.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Columna Derecha: Resumen de Cobro -->
        <div class="lg:col-span-1">
          <div class="bg-white p-6 rounded-2xl shadow-md border-2 border-black space-y-6 sticky top-4">
            <h2 class="text-xl font-black border-b-2 border-black pb-2">Resumen de Cobro</h2>

            <div class="space-y-3">
              <div class="flex justify-between text-sm font-bold text-slate-700">
                <span>Líneas de productos:</span>
                <span>{{ carrito.length }}</span>
              </div>
              <div class="flex justify-between text-sm font-bold text-slate-700">
                <span>Total de prendas:</span>
                <span>{{ totalItemsEnCarrito }}</span>
              </div>
              <div class="pt-3 border-t-2 border-slate-200 flex justify-between items-center text-base font-black">
                <span>Total a Cobrar:</span>
                <span class="text-3xl font-black text-emerald-800">${{ totalVenta.toLocaleString('es-AR') }}</span>
              </div>
            </div>

            <button
              @click="procesarVenta"
              :disabled="carrito.length === 0 || procesando"
              class="w-full py-4 bg-emerald-700 hover:bg-emerald-800 text-white font-black text-lg rounded-xl border-2 border-black shadow-lg disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer transition-colors"
            >
              {{ procesando ? 'Procesando...' : 'Confirmar Venta' }}
            </button>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const inputEscaner = ref(null)
const codigoEscaneado = ref('')
const carrito = ref([])
const catalogoPrendas = ref([])
const filtroCatalogo = ref('')
const mostrarSelectorManual = ref(false)
const procesando = ref(false)
const mensajeExito = ref('')
const mensajeError = ref('')

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

const cerrarSesion = () => {
  localStorage.removeItem('usuario_stock')
  router.push('/')
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
  try {
    const res = await fetch(`${API_URL}/prendas/`, { headers: getAuthHeaders() })
    if (res.ok) {
      catalogoPrendas.value = await res.json()
    }
  } catch (e) {
    console.error("Error al cargar catálogo:", e)
  }
}

const agregarVarianteDirecta = (prenda, variante) => {
  mensajeError.value = ''
  mensajeExito.value = ''

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
    mensajeError.value = `Stock insuficiente. Disponibles: ${item.stock_actual}`
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
  mensajeExito.value = ''

  try {
    const res = await fetch(`${API_URL}/prendas/buscar/codigo?codigo=${encodeURIComponent(code)}`, {
      headers: getAuthHeaders()
    })

    if (res.ok) {
      const prenda = await res.json()
      // Encontrar la variante exacta escaneada
      const variante = prenda.variantes.find(v => v.codigo_barras === code) || prenda.variantes[0]

      if (!variante) {
        mensajeError.value = "No se encontraron talles disponibles para esta prenda."
        return
      }

      if (variante.stock_actual <= 0) {
        mensajeError.value = `Sin stock para ${prenda.nombre} (Talle ${variante.talle}).`
        return
      }

      agregarVarianteDirecta(prenda, variante)
    } else {
      mensajeError.value = `Código de barras "${code}" no registrado en el inventario.`
    }
  } catch (e) {
    console.error(e)
    mensajeError.value = "Error de conexión al buscar código de barras."
  } finally {
    codigoEscaneado.value = ''
    if (inputEscaner.value) inputEscaner.value.focus()
  }
}

const procesarVenta = async () => {
  if (carrito.value.length === 0) return

  mensajeError.value = ''
  mensajeExito.value = ''
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
      mensajeExito.value = `Venta #${ventaRegistrada.id_venta} registrada con éxito por $${Number(ventaRegistrada.total).toLocaleString('es-AR')}.`
      carrito.value = []
      await cargarCatalogo()
    } else {
      const err = await res.json().catch(() => ({}))
      mensajeError.value = err.detail || "Error al procesar la venta. Verifique disponibilidad de stock."
    }
  } catch (e) {
    console.error("Error al registrar venta:", e)
    mensajeError.value = "Error de conexión con el servidor."
  } finally {
    procesando.value = false
  }
}

onMounted(() => {
  cargarCatalogo()
})
</script>