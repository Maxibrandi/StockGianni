<template>
  <div class="min-h-screen bg-slate-950 flex flex-col justify-center items-center p-4 sm:p-6 relative overflow-hidden font-sans">

    <!-- Elementos de Fondo con Gradientes Suaves -->
    <div class="absolute top-[-15%] left-[-10%] w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-[-15%] right-[-10%] w-[500px] h-[500px] bg-violet-600/20 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="w-full max-w-md relative z-10">

      <!-- Encabezado de Marca -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-violet-500 text-white shadow-xl shadow-indigo-500/25 mb-4 transform hover:scale-105 transition-transform duration-200">
          <svg class="w-9 h-9" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Stock<span class="text-indigo-400">Gianni</span>
        </h1>
        <p class="text-sm font-medium text-slate-400 mt-1">Sistema Integral de Inventario & Ventas</p>
      </div>

      <!-- Tarjeta Principal de Inicio de Sesión -->
      <div class="bg-slate-900/90 backdrop-blur-xl p-7 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl space-y-6">

        <!-- Selector Rápido de Cuenta Demo -->
        <div class="space-y-2">
          <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider">Acceso Rápido Demo</label>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              @click="seleccionarRol('admin')"
              :class="creds.username === 'admin@gianni.com' ? 'bg-indigo-600/20 border-indigo-500 text-indigo-300 font-bold' : 'bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-200'"
              class="px-3 py-2 rounded-xl border text-xs font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer"
            >
              <span>👑 Admin</span>
            </button>
            <button
              type="button"
              @click="seleccionarRol('vendedor')"
              :class="creds.username === 'ventas@gianni.com' ? 'bg-indigo-600/20 border-indigo-500 text-indigo-300 font-bold' : 'bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-200'"
              class="px-3 py-2 rounded-xl border text-xs font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer"
            >
              <span>🛒 Vendedor</span>
            </button>
          </div>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1.5">Correo Electrónico / Usuario</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                </svg>
              </div>
              <input
                v-model="creds.username"
                type="email"
                required
                placeholder="ejemplo@gianni.com"
                class="w-full pl-10 pr-4 py-3 bg-slate-800/80 border border-slate-700 rounded-xl text-white font-medium text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-300 mb-1.5">Contraseña</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                v-model="creds.password"
                :type="mostrarPassword ? 'text' : 'password'"
                required
                placeholder="••••••••"
                class="w-full pl-10 pr-10 py-3 bg-slate-800/80 border border-slate-700 rounded-xl text-white font-medium text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
              <button
                type="button"
                @click="mostrarPassword = !mostrarPassword"
                class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-500 hover:text-slate-300 cursor-pointer"
              >
                <svg v-if="!mostrarPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Mensaje de Error -->
          <div v-if="error" class="p-3 bg-red-950/60 border border-red-800/80 rounded-xl text-xs font-semibold text-red-300 flex items-center gap-2">
            <svg class="w-4 h-4 shrink-0 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ error }}</span>
          </div>

          <!-- Botón de Ingreso -->
          <button
            type="submit"
            :disabled="cargando"
            class="w-full py-3.5 px-4 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-sm font-bold rounded-xl shadow-lg shadow-indigo-600/30 transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
          >
            <svg v-if="cargando" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ cargando ? 'Ingresando al sistema...' : 'Iniciar Sesión' }}</span>
          </button>
        </form>

      </div>

      <!-- Footer Informativo -->
      <p class="text-center text-xs font-medium text-slate-500 mt-6">
        StockGianni &copy; {{ new Date().getFullYear() }} &bull; Gestión de Moda & Control de Stock
      </p>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
const router = useRouter()

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