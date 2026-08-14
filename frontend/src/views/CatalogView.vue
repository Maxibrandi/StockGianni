<template>
  <!-- Contenedor general con fondo neutro claro -->
  <div class="min-h-screen bg-slate-300 p-4 sm:p-6 font-sans text-black">
    <div class="max-w-7xl mx-auto space-y-6">

      <!-- 1. PANTALLA DE LOGIN -->
      <div v-if="!usuarioAutenticado" class="min-h-[85vh] flex items-center justify-center">
        <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-2xl border-4 border-slate-900 space-y-6">
          <div class="text-center">
            <h1 class="text-4xl font-black text-black tracking-tight">StockGianni</h1>
            <p class="text-sm font-black text-slate-800 mt-2">Acceso al Sistema de Inventario</p>
          </div>

          <form @submit.prevent="iniciarSesion" class="space-y-4">
            <div>
              <label class="block text-xs font-black text-black uppercase tracking-wider mb-2">Perfil / Rol</label>
              <select
                v-model="formularioLogin.rol"
                class="block w-full rounded-xl border-2 border-black p-3 text-black font-black bg-white focus:ring-4 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="vendedor">Vendedor (Solo Consultas)</option>
                <option value="admin">Administrador (Control Total)</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-black text-black uppercase tracking-wider mb-2">Contraseña</label>
              <input
                v-model="formularioLogin.password"
                type="password"
                placeholder="••••••••"
                required
                class="block w-full rounded-xl border-2 border-black p-3 text-black font-black focus:ring-4 focus:ring-indigo-500 focus:outline-none"
              />
              <p class="text-xs font-bold text-slate-900 mt-2">
                Claves Demo: Admin: <code class="bg-slate-200 text-black px-1.5 py-0.5 rounded border border-black">admin123</code> | Vendedor: <code class="bg-slate-200 text-black px-1.5 py-0.5 rounded border border-black">ventas123</code>
              </p>
            </div>

            <div v-if="errorLogin" class="p-3 bg-red-200 border-2 border-red-700 rounded-xl text-xs font-black text-red-950 text-center">
              {{ errorLogin }}
            </div>

            <button
              type="submit"
              class="w-full rounded-xl bg-indigo-800 hover:bg-indigo-900 py-3.5 text-sm font-black text-white shadow-lg transition-colors cursor-pointer border-2 border-black"
            >
              Ingresar
            </button>
          </form>
        </div>
      </div>

      <!-- 2. PANEL PRINCIPAL -->
      <template v-else>
        <!-- Header -->
        <header class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-white p-6 rounded-2xl shadow-md border-2 border-black">
          <div>
            <div class="flex items-center gap-3">
              <h1 class="text-3xl font-black text-black">Control de Inventario</h1>
              <span
                class="px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider border-2"
                :class="usuarioAutenticado.rol === 'admin' ? 'bg-purple-200 text-purple-950 border-purple-800' : 'bg-blue-200 text-blue-950 border-blue-800'"
              >
                {{ usuarioAutenticado.rol }}
              </span>
            </div>
            <p class="text-sm font-extrabold text-black mt-1">Gestión de productos y ventas en tiempo real.</p>
          </div>

          <div class="flex items-center gap-3">
            <button
              v-if="usuarioAutenticado.rol === 'admin'"
              @click="mostrarModalCrear = true"
              class="inline-flex items-center justify-center rounded-xl bg-indigo-800 px-5 py-3 text-sm font-black text-white shadow-md hover:bg-indigo-900 transition-colors border-2 border-black cursor-pointer"
            >
              + Nueva Prenda
            </button>

            <button
              @click="cerrarSesion"
              class="rounded-xl bg-slate-200 hover:bg-slate-300 px-4 py-3 text-xs font-black text-black transition-colors border-2 border-black cursor-pointer"
            >
              Cerrar Sesión
            </button>
          </div>
        </header>

        <!-- GANANCIAS REALES DESDE LA BASE DE DATOS (ADMIN) -->
        <section v-if="usuarioAutenticado.rol === 'admin'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-white p-6 rounded-2xl shadow-md border-2 border-black flex items-center justify-between">
            <div>
              <p class="text-xs font-black uppercase tracking-wider text-black">Ganancia Real Hoy</p>
              <h3 class="text-3xl font-black text-emerald-800 mt-1">${{ gananciasDiarias.toLocaleString('es-AR') }}</h3>
            </div>
            <div class="p-3 bg-emerald-200 border-2 border-emerald-800 rounded-xl text-black font-black text-2xl">
              💵
            </div>
          </div>

          <div class="bg-white p-6 rounded-2xl shadow-md border-2 border-black flex items-center justify-between">
            <div>
              <p class="text-xs font-black uppercase tracking-wider text-black">Ganancia Real del Mes</p>
              <h3 class="text-3xl font-black text-indigo-900 mt-1">${{ gananciasMensuales.toLocaleString('es-AR') }}</h3>
            </div>
            <div class="p-3 bg-indigo-200 border-2 border-indigo-800 rounded-xl text-black font-black text-2xl">
              📈
            </div>
          </div>
        </section>

        <!-- Barra de Búsqueda Lector -->
        <section class="bg-white p-5 rounded-2xl shadow-md border-2 border-black">
          <label for="search-barcode" class="block text-xs font-black text-black uppercase tracking-wider mb-2">
            Escanear Código de Barras (Lector)
          </label>
          <input
            id="search-barcode"
            v-model="codigoBusqueda"
            @keyup.enter="buscarPorCodigo"
            type="text"
            placeholder="Pase la lectora sobre la etiqueta..."
            class="block w-full max-w-md rounded-xl border-2 border-black py-3 px-4 text-black font-black placeholder:text-slate-500 focus:ring-4 focus:ring-indigo-500 focus:outline-none"
          />
        </section>

        <!-- Grid: Alertas y Listado -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

          <!-- Alertas Bajo Stock -->
          <div class="lg:col-span-1">
            <div class="bg-white p-5 rounded-2xl shadow-md border-2 border-black">
              <h2 class="text-base font-black text-black flex items-center gap-2 mb-4">
                <span class="flex h-3.5 w-3.5 rounded-full bg-red-600 border border-black"></span>
                Alertas de Bajo Stock
              </h2>

              <p v-if="alertasStock.length === 0" class="text-xs font-black text-black">
                Sin alertas activas. Stock en nivel correcto.
              </p>

              <ul v-else class="divide-y-2 divide-black max-h-[380px] overflow-y-auto">
                <li v-for="item in alertasStock" :key="item.id_stock_prenda" class="py-3">
                  <div class="flex justify-between items-center">
                    <span class="font-black text-black text-sm">{{ item.prenda?.nombre || 'Prenda' }}</span>
                    <span class="bg-red-200 text-red-950 font-black text-xs px-2 py-1 rounded-lg border border-red-800">
                      Talle: {{ item.talle }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-xs mt-1 text-black font-black">
                    <span>Stock: <strong class="text-red-700 font-black">{{ item.stock_actual }}</strong> (Mín: {{ item.stock_minimo }})</span>
                    <span class="font-mono text-slate-800">{{ item.codigo_barras }}</span>
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tabla de Prendas -->
          <div class="lg:col-span-2">
            <div class="bg-white rounded-2xl shadow-md border-2 border-black overflow-hidden">
              <div class="p-4 border-b-2 border-black bg-slate-200">
                <h2 class="text-base font-black text-black">Catálogo de Prendas</h2>
              </div>

              <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr class="bg-slate-300 border-b-2 border-black text-xs font-black uppercase text-black">
                      <th class="py-3 px-4">ID</th>
                      <th class="py-3 px-4">Nombre</th>
                      <th class="py-3 px-4">Variantes (Talle / Stock)</th>
                      <th v-if="usuarioAutenticado.rol === 'admin'" class="py-3 px-4 text-right">Acciones</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y-2 divide-slate-300 text-sm font-black text-black">
                    <tr v-for="prenda in prendas" :key="prenda.id_prenda" class="hover:bg-slate-100">
                      <td class="py-3 px-4 font-black text-black">#{{ prenda.id_prenda }}</td>
                      <td class="py-3 px-4 font-black text-black">{{ prenda.nombre }}</td>
                      <td class="py-3 px-4">
                        <div class="flex flex-wrap gap-2">
                          <span
                            v-for="v in prenda.variantes"
                            :key="v.id_stock_prenda"
                            class="inline-flex items-center gap-1 rounded-lg px-2.5 py-1 text-xs font-black border-2"
                            :class="v.stock_actual <= v.stock_minimo ? 'bg-red-200 text-red-950 border-red-800' : 'bg-slate-200 text-black border-black'"
                          >
                            {{ v.talle }}: {{ v.stock_actual }} u. (${{ v.precio_venta }})
                          </span>
                        </div>
                      </td>
                      <td v-if="usuarioAutenticado.rol === 'admin'" class="py-3 px-4 text-right">
                        <button
                          @click="descargarPDF(prenda.id_prenda)"
                          class="text-xs font-black text-black hover:bg-indigo-200 bg-indigo-100 border-2 border-black px-3 py-1.5 rounded-xl transition-colors cursor-pointer"
                        >
                          Imprimir PDF
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </div>

        <!-- MODAL CREAR PRENDA -->
        <div v-if="mostrarModalCrear" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-xs">
          <div class="bg-white rounded-2xl shadow-2xl border-4 border-black max-w-lg w-full overflow-hidden">
            <div class="px-6 py-4 bg-slate-200 border-b-2 border-black flex items-center justify-between">
              <h3 class="text-base font-black text-black">Registrar Nueva Prenda</h3>
              <button @click="mostrarModalCrear = false" class="text-black font-black text-xl hover:text-slate-700">✕</button>
            </div>

            <form @submit.prevent="guardarPrenda" class="p-6 space-y-4">
              <div>
                <label class="block text-xs font-black text-black uppercase mb-1">Nombre de la Prenda</label>
                <input
                  v-model="nuevaPrenda.nombre"
                  type="text" required placeholder="Ej: Camisa Manga Larga"
                  class="block w-full rounded-xl border-2 border-black p-2.5 text-black font-black focus:ring-4 focus:ring-indigo-500 focus:outline-none"
                />
              </div>

              <div>
                <div class="flex items-center justify-between mb-2">
                  <label class="block text-xs font-black text-black uppercase">Talles y Cantidades</label>
                  <button type="button" @click="agregarFilaVariante" class="text-xs font-black text-indigo-900 cursor-pointer">
                    + Agregar Talle
                  </button>
                </div>

                <div class="space-y-2 max-h-[180px] overflow-y-auto">
                  <div v-for="(v, idx) in nuevaPrenda.variantes" :key="idx" class="flex items-center gap-2 bg-slate-100 p-2 rounded-xl border-2 border-black">
                    <input v-model="v.talle" type="text" placeholder="Talle" required class="w-16 rounded-lg border-2 border-black p-1 text-xs font-black text-black" />
                    <input v-model.number="v.precio_venta" type="number" step="0.01" placeholder="Precio ($)" required class="w-24 rounded-lg border-2 border-black p-1 text-xs font-black text-black" />
                    <input v-model.number="v.stock_actual" type="number" placeholder="Stock" required class="w-16 rounded-lg border-2 border-black p-1 text-xs font-black text-black" />
                    <input v-model.number="v.stock_minimo" type="number" placeholder="Mínimo" required class="w-16 rounded-lg border-2 border-black p-1 text-xs font-black text-black" />
                    <button type="button" @click="nuevaPrenda.variantes.splice(idx, 1)" class="text-red-700 font-black px-1 cursor-pointer">✕</button>
                  </div>
                </div>
              </div>

              <div class="pt-4 border-t-2 border-black flex justify-end gap-2">
                <button type="button" @click="mostrarModalCrear = false" class="rounded-xl border-2 border-black px-4 py-2 text-xs font-black text-black">
                  Cancelar
                </button>
                <button type="submit" class="rounded-xl bg-indigo-800 border-2 border-black px-4 py-2 text-xs font-black text-white shadow-md hover:bg-indigo-900 cursor-pointer">
                  Guardar Prenda
                </button>
              </div>
            </form>
          </div>
        </div>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_URL = 'http://localhost:8000/api/v1'

const usuarioAutenticado = ref(null)
const formularioLogin = ref({ rol: 'vendedor', password: '' })
const errorLogin = ref('')

// Ganancias obtenidas directamente de la BD
const gananciasDiarias = ref(0)
const gananciasMensuales = ref(0)

const prendas = ref([])
const alertasStock = ref([])
const codigoBusqueda = ref('')
const mostrarModalCrear = ref(false)

const nuevaPrenda = ref({
  nombre: '',
  variantes: [
    { talle: 'S', precio_venta: 0, stock_actual: 10, stock_minimo: 3 },
    { talle: 'M', precio_venta: 0, stock_actual: 10, stock_minimo: 3 }
  ]
})

const iniciarSesion = () => {
  errorLogin.value = ''
  const { rol, password } = formularioLogin.value

  if (rol === 'admin' && password === 'admin123') {
    usuarioAutenticado.value = { rol: 'admin' }
  } else if (rol === 'vendedor' && password === 'ventas123') {
    usuarioAutenticado.value = { rol: 'vendedor' }
  } else {
    errorLogin.value = 'Contraseña incorrecta para el perfil seleccionado.'
    return
  }

  localStorage.setItem('usuario_stock', JSON.stringify(usuarioAutenticado.value))
  cargarDatos()
}

const cerrarSesion = () => {
  usuarioAutenticado.value = null
  formularioLogin.value.password = ''
  localStorage.removeItem('usuario_stock')
}

const agregarFilaVariante = () => {
  nuevaPrenda.value.variantes.push({ talle: '', precio_venta: 0, stock_actual: 0, stock_minimo: 0 })
}

// Cargar prendas y llamar al endpoint de ganancias
const cargarDatos = async () => {
  try {
    const resPrendas = await fetch(`${API_URL}/prendas/`)
    if (resPrendas.ok) prendas.value = await resPrendas.json()

    const resAlertas = await fetch(`${API_URL}/prendas/alertas/bajo-stock`)
    if (resAlertas.ok) alertasStock.value = await resAlertas.json()

    // Cargar Ganancias si es Administrador
    if (usuarioAutenticado.value?.rol === 'admin') {
      const resGanancias = await fetch(`${API_URL}/ventas/reporte-ganancias`)
      if (resGanancias.ok) {
        const datos = await resGanancias.json()
        gananciasDiarias.value = datos.ganancia_diaria
        gananciasMensuales.value = datos.ganancia_mensual
      }
    }
  } catch (error) {
    console.error("Error al conectar con la base de datos:", error)
  }
}

const guardarPrenda = async () => {
  try {
    const response = await fetch(`${API_URL}/prendas/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevaPrenda.value)
    })

    if (response.ok) {
      mostrarModalCrear.value = false
      nuevaPrenda.value = { nombre: '', variantes: [{ talle: 'S', precio_venta: 0, stock_actual: 10, stock_minimo: 3 }] }
      await cargarDatos()
    }
  } catch (error) {
    console.error("Error guardando prenda:", error)
  }
}

const buscarPorCodigo = async () => {
  if (!codigoBusqueda.value.trim()) return
  try {
    const res = await fetch(`${API_URL}/prendas/codigo/${codigoBusqueda.value.trim()}`)
    if (res.ok) {
      const prenda = await res.json()
      alert(`Prenda: ${prenda.nombre}\nVariantes: ${prenda.variantes.length}`)
    } else {
      alert("Código no registrado.")
    }
  } catch (e) {
    console.error(e)
  } finally {
    codigoBusqueda.value = ''
  }
}

const descargarPDF = (idPrenda) => {
  window.open(`${API_URL}/prendas/${idPrenda}/pdf-codigos`, '_blank')
}

onMounted(() => {
  const sesionGuardada = localStorage.getItem('usuario_stock')
  if (sesionGuardada) {
    usuarioAutenticado.value = JSON.parse(sesionGuardada)
    cargarDatos()
  }
})
</script>