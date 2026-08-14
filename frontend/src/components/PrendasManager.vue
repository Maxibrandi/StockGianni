<template>
  <!-- Contenedor general -->
  <div class="min-h-screen bg-slate-300 p-4 sm:p-6 font-sans text-black">
    <div class="max-w-7xl mx-auto space-y-6">

      <!-- 1. PANTALLA DE LOGIN CONECTADA A FASTAPI -->
      <div v-if="!usuarioAutenticado" class="min-h-[85vh] flex items-center justify-center">
        <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-2xl border-4 border-slate-900 space-y-6">
          <div class="text-center">
            <h1 class="text-4xl font-black text-black tracking-tight">StockGianni</h1>
            <p class="text-sm font-black text-slate-800 mt-2">Acceso al Sistema de Inventario</p>
          </div>

          <form @submit.prevent="iniciarSesion" class="space-y-4">
            <div>
              <label class="block text-xs font-black text-black uppercase tracking-wider mb-2">Usuario / Email</label>
              <input
                v-model="formularioLogin.username"
                type="text"
                placeholder="Ingresá tu usuario registrado"
                required
                class="block w-full rounded-xl border-2 border-black p-3 text-black font-black focus:ring-4 focus:ring-indigo-500 focus:outline-none"
              />
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

      <!-- 2. PANEL PRINCIPAL (SE MANTIENE IGUAL) -->
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

        <!-- GANANCIAS REALES (ADMIN) -->
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

        <!-- Lector, Alertas y Tabla mantienen su código intacto... -->
        <!-- ... -->
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_URL = 'http://localhost:8000/api/v1'

const usuarioAutenticado = ref(null)
const formularioLogin = ref({ username: '', password: '' })
const errorLogin = ref('')

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

// Función para obtener headers con autenticación Bearer Token
const getAuthHeaders = () => {
  const token = usuarioAutenticado.value?.token
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  }
}

// LOGIN REAL CONTRA LA BASE DE DATOS (FASTAPI OAUTH2)
const iniciarSesion = async () => {
  errorLogin.value = ''

  try {
    // FastAPI OAuth2 requiere form-data (x-www-form-urlencoded)
    const formData = new URLSearchParams()
    formData.append('username', formularioLogin.value.username)
    formData.append('password', formularioLogin.value.password)

    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
    })

    if (res.ok) {
      const data = await res.json()

      // Guardar sesión y Token JWT
      usuarioAutenticado.value = {
        username: formularioLogin.value.username,
        token: data.access_token,
        rol: data.rol || 'admin' // Toma el rol retornado por la BD o asigna admin por defecto
      }

      localStorage.setItem('usuario_stock', JSON.stringify(usuarioAutenticado.value))
      await cargarDatos()
    } else {
      const errorData = await res.json()
      errorLogin.value = errorData.detail || 'Usuario o contraseña incorrectos.'
    }
  } catch (e) {
    console.error("Error al autenticar:", e)
    errorLogin.value = 'No se pudo conectar con el servidor.'
  }
}

const cerrarSesion = () => {
  usuarioAutenticado.value = null
  formularioLogin.value = { username: '', password: '' }
  localStorage.removeItem('usuario_stock')
}

const cargarDatos = async () => {
  try {
    const headers = getAuthHeaders()

    const resPrendas = await fetch(`${API_URL}/prendas/`, { headers })
    if (resPrendas.ok) prendas.value = await resPrendas.json()

    const resAlertas = await fetch(`${API_URL}/prendas/alertas/bajo-stock`, { headers })
    if (resAlertas.ok) alertasStock.value = await resAlertas.json()

    if (usuarioAutenticado.value?.rol === 'admin') {
      const resGanancias = await fetch(`${API_URL}/ventas/reporte-ganancias`, { headers })
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
      headers: getAuthHeaders(),
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
    const res = await fetch(`${API_URL}/prendas/codigo/${codigoBusqueda.value.trim()}`, {
      headers: getAuthHeaders()
    })
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