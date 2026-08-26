<template>
  <header class="bg-white border-b border-slate-200/80 sticky top-0 z-40 backdrop-blur-md bg-white/90">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20">

        <!-- Logo y Marca -->
        <div class="flex items-center gap-3 sm:gap-4">
          <router-link to="/catalogo" class="flex items-center gap-3 group">
            <div class="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-200">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
            </div>
            <div>
              <span class="text-xl sm:text-2xl font-black tracking-tight text-slate-900 flex items-center gap-1.5">
                Stock<span class="text-indigo-600">Gianni</span>
              </span>
              <span class="hidden sm:block text-[10px] uppercase font-bold tracking-widest text-slate-700">Inventario & Punto de Venta</span>
            </div>
          </router-link>
        </div>

        <!-- Links de Navegación -->
        <nav class="hidden md:flex items-center gap-1.5">
          <router-link
            v-if="esAdmin"
            to="/dashboard"
            class="flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm font-semibold transition-all duration-200"
            :class="$route.name === 'dashboard' ? 'bg-indigo-50 text-indigo-700 font-bold shadow-xs' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Dashboard
          </router-link>

          <router-link
            to="/catalogo"
            class="flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm font-semibold transition-all duration-200"
            :class="$route.name === 'catalogo' ? 'bg-indigo-50 text-indigo-700 font-bold shadow-xs' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            Catálogo & Stock
          </router-link>

          <router-link
            to="/pos"
            class="flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm font-semibold transition-all duration-200"
            :class="$route.name === 'ventas' ? 'bg-emerald-50 text-emerald-700 font-bold shadow-xs' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            Punto de Venta (POS)
          </router-link>
        </nav>

        <!-- Perfil de Usuario y Acciones -->
        <div class="flex items-center gap-3">
          <div class="hidden sm:flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-slate-100/80 border border-slate-200/60">
            <div class="w-7 h-7 rounded-lg bg-indigo-100 text-indigo-700 font-bold text-xs flex items-center justify-center uppercase">
              {{ (usuario.nombre || usuario.email || 'U')[0] }}
            </div>
            <div class="text-left">
              <p class="text-xs font-bold text-slate-800 leading-none truncate max-w-[120px]">{{ usuario.nombre || usuario.email || 'Operador' }}</p>
              <span
                class="inline-block mt-0.5 text-[10px] font-extrabold uppercase tracking-wider px-1.5 py-0.2 rounded"
                :class="esAdmin ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'"
              >
                {{ usuario.rol }}
              </span>
            </div>
          </div>

          <button
            @click="cerrarSesion"
            title="Cerrar Sesión"
            class="p-2 sm:px-3 sm:py-2 rounded-xl text-slate-600 hover:text-red-600 hover:bg-red-50 border border-slate-200 transition-colors flex items-center gap-1.5 text-xs font-bold cursor-pointer"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span class="hidden sm:inline">Salir</span>
          </button>
        </div>

      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

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

const cerrarSesion = () => {
  localStorage.removeItem('usuario_stock')
  router.push('/')
}
</script>