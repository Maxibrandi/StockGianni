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
        class="fixed bottom-5 right-5 z-50 flex items-center gap-3 px-4 py-3 rounded-2xl shadow-xl text-sm font-semibold max-w-sm"
        :class="toast.type === 'success' ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'"
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
            class="px-3.5 py-2 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs rounded-xl border border-slate-200 shadow-xs flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed"
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

      <!-- Estado de Error -->
      <div v-if="errorCarga" class="p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-center gap-3 text-sm text-rose-700 font-semibold">
        <svg class="w-5 h-5 shrink-0 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ errorCarga }}</span>
        <button @click="cargarDatosDashboard" class="ml-auto text-xs underline font-bold cursor-pointer hover:no-underline">Reintentar</button>
      </div>

      <!-- Tarjetas de Métricas Principales (KPIs) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">

        <!-- Ventas de Hoy -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Ventas Hoy</span>
            <div class="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-lg">💵</div>
          </div>
          <!-- Skeleton -->
          <div v-if="cargando" class="mt-3 space-y-2">
            <div class="h-8 bg-slate-100 rounded-lg animate-pulse w-3/4"></div>
            <div class="h-4 bg-slate-100 rounded-md animate-pulse w-1/2"></div>
          </div>
          <template v-else>
            <p class="text-2xl sm:text-3xl font-black text-slate-900 mt-3 tracking-tight">
              ${{ Number(resumen.ganancia_diaria || 0).toLocaleString('es-AR') }}
            </p>
            <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-emerald-700 bg-emerald-50 w-fit px-2 py-0.5 rounded-md">
              <span>{{ resumen.cantidad_ventas_hoy || 0 }} transacciones hoy</span>
            </div>
          </template>
        </div>

        <!-- Ventas del Mes -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Recaudación Mes</span>
            <div class="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-lg">📈</div>
          </div>
          <div v-if="cargando" class="mt-3 space-y-2">
            <div class="h-8 bg-slate-100 rounded-lg animate-pulse w-3/4"></div>
            <div class="h-4 bg-slate-100 rounded-md animate-pulse w-1/2"></div>
          </div>
          <template v-else>
            <div class="flex items-center gap-2 mt-3">
              <p class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
                {{ mostrarRecaudacionMes ? `$${Number(resumen.ganancia_mensual || 0).toLocaleString('es-AR')}` : '••••••' }}
              </p>
              <button
                @click="mostrarRecaudacionMes = !mostrarRecaudacionMes"
                class="p-1 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors cursor-pointer"
                :title="mostrarRecaudacionMes ? 'Ocultar monto' : 'Mostrar monto'"
                type="button"
              >
                <svg v-if="mostrarRecaudacionMes" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-indigo-700 bg-indigo-50 w-fit px-2 py-0.5 rounded-md">
              <span>{{ resumen.cantidad_ventas_mes || 0 }} ventas acumuladas</span>
            </div>
          </template>
        </div>

        <!-- Alertas de Reposición -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Stock Crítico</span>
            <div class="w-9 h-9 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center text-lg">⚠️</div>
          </div>
          <div v-if="cargando" class="mt-3 space-y-2">
            <div class="h-8 bg-slate-100 rounded-lg animate-pulse w-1/3"></div>
            <div class="h-4 bg-slate-100 rounded-md animate-pulse w-2/3"></div>
          </div>
          <template v-else>
            <p class="text-2xl sm:text-3xl font-black mt-3 tracking-tight" :class="alertasCount > 0 ? 'text-rose-600' : 'text-slate-900'">
              {{ alertasCount }}
            </p>
            <div
              class="flex items-center gap-1.5 mt-2 text-xs font-semibold w-fit px-2 py-0.5 rounded-md"
              :class="alertasCount > 0 ? 'text-rose-700 bg-rose-50' : 'text-slate-500 bg-slate-50'"
            >
              <span>{{ alertasCount > 0 ? 'Requiere reposición urgente' : 'Inventario en nivel óptimo' }}</span>
            </div>
          </template>
        </div>

        <!-- Catálogo Total -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative overflow-hidden">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Modelos Activos</span>
            <div class="w-9 h-9 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center text-lg">🏷️</div>
          </div>
          <div v-if="cargando" class="mt-3 space-y-2">
            <div class="h-8 bg-slate-100 rounded-lg animate-pulse w-1/3"></div>
            <div class="h-4 bg-slate-100 rounded-md animate-pulse w-1/2"></div>
          </div>
          <template v-else>
            <p class="text-2xl sm:text-3xl font-black text-slate-900 mt-3 tracking-tight">
              {{ totalPrendas }}
            </p>
            <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-slate-600 bg-slate-50 w-fit px-2 py-0.5 rounded-md">
              <span>Prendas en base de datos</span>
            </div>
          </template>
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
            <router-link to="/catalogo" class="text-xs font-bold text-indigo-600 hover:text-indigo-700 transition-colors">Ver catálogo &rarr;</router-link>
          </div>

          <!-- Skeleton -->
          <div v-if="cargando" class="space-y-3">
            <div v-for="i in 5" :key="i" class="p-3 rounded-xl bg-slate-50 flex items-center gap-3">
              <div class="w-6 h-6 bg-slate-200 rounded-lg animate-pulse shrink-0"></div>
              <div class="flex-1 space-y-1.5">
                <div class="h-3.5 bg-slate-200 rounded animate-pulse w-2/3"></div>
                <div class="h-3 bg-slate-100 rounded animate-pulse w-1/3"></div>
              </div>
              <div class="w-14 h-6 bg-slate-200 rounded-lg animate-pulse"></div>
            </div>
          </div>

          <div v-else-if="!resumen.productos_top || resumen.productos_top.length === 0" class="py-8 text-center text-slate-400 text-sm font-medium">
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
                <span class="w-6 h-6 rounded-lg bg-indigo-100 text-indigo-700 font-black text-xs flex items-center justify-center shrink-0">
                  {{ idx + 1 }}
                </span>
                <div>
                  <h4 class="text-xs sm:text-sm font-extrabold text-slate-900">{{ prod.nombre }}</h4>
                  <span class="text-[11px] font-bold text-slate-500">Talle: <strong class="text-slate-800">{{ prod.talle }}</strong></span>
                </div>
              </div>

              <div class="text-right shrink-0">
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
            <span class="text-xs font-bold px-2.5 py-1 rounded-full" :class="alertasCount > 0 ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'">
              {{ alertasCount }} {{ alertasCount === 1 ? 'faltante' : 'faltantes' }}
            </span>
          </div>

          <!-- Skeleton -->
          <div v-if="cargando" class="space-y-2.5">
            <div v-for="i in 3" :key="i" class="p-3 rounded-xl bg-slate-50 flex items-center gap-3">
              <div class="flex-1 space-y-1.5">
                <div class="h-3.5 bg-slate-200 rounded animate-pulse w-3/4"></div>
                <div class="h-3 bg-slate-100 rounded animate-pulse w-1/2"></div>
              </div>
              <div class="w-16 h-7 bg-slate-200 rounded-lg animate-pulse"></div>
            </div>
          </div>

          <div v-else-if="alertas.length === 0" class="py-8 text-center text-slate-400 text-sm font-medium">
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
              <div class="space-y-0.5 min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 truncate">{{ item.prenda?.nombre || 'Prenda' }}</h4>
                  <span class="text-[10px] font-black uppercase bg-white px-2 py-0.5 rounded border border-rose-200 text-rose-700 shrink-0">
                    Talle {{ item.talle }}
                  </span>
                </div>
                <div class="text-[11px] font-medium text-slate-600">
                  Stock: <strong class="text-rose-700 font-black">{{ item.stock_actual }}</strong> (Mín: {{ item.stock_minimo }}) &bull;
                  <span class="font-mono text-slate-400">{{ item.codigo_barras }}</span>
                </div>
              </div>

              <button
                @click="descargarPDF(item.id_prenda)"
                title="Imprimir etiquetas con código de barras"
                class="px-2.5 py-1.5 bg-white hover:bg-slate-100 text-slate-700 text-xs font-bold rounded-lg border border-slate-200 shadow-sm transition-colors shrink-0 cursor-pointer"
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
const router = useRouter()

// 🌟 Inicializar vacío para que no cargue datos por defecto
const creds = ref({ username: '', password: '' })

const mostrarPassword = ref(false)
const cargando = ref(false)
const error = ref('')

const seleccionarRol = (rol) => {
  if (rol === 'admin') {
    creds.value = { username: 'admin@gianni.com', password: 'admin123' }
  } else {
    creds.value = { username: 'ventas@gianni.com', password: 'ventas123' }
  }
}

const handleLogin = async () => {
  error.value = ''
  cargando.value = true

  try {
    const formData = new URLSearchParams()
    formData.append('username', creds.value.username)
    formData.append('password', creds.value.password)

    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
    })

    if (res.ok) {
      const data = await res.json()
      const rolNormalized = (data.rol || '').toLowerCase()
      const user = {
        token: data.access_token,
        rol: rolNormalized,
        email: data.email,
        nombre: data.nombre
      }
      localStorage.setItem('usuario_stock', JSON.stringify(user))

      if (rolNormalized === 'admin' || rolNormalized === 'administrador') {
        router.push('/dashboard')
      } else {
        router.push('/pos')
      }
    } else {
      const errData = await res.json().catch(() => ({}))
      error.value = errData.detail || 'Credenciales inválidas. Compruebe usuario y contraseña.'
    }
  } catch (e) {
    console.error('Error en login:', e)
    error.value = 'No se pudo conectar con el servidor. Verifique que el backend esté activo.'
  } finally {
    cargando.value = false
  }
}
</script>