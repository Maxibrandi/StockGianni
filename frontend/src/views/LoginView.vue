<template>
  <div class="min-h-screen bg-slate-300 flex items-center justify-center p-4 font-sans text-black">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-2xl border-4 border-black space-y-6">
      <div class="text-center">
        <h1 class="text-4xl font-black text-black">StockGianni</h1>
        <p class="text-sm font-black text-slate-800 mt-2">Sistema de Inventario & Ventas</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-xs font-black text-black uppercase mb-1">Usuario / Email</label>
          <input
            v-model="creds.username"
            type="text" required
            class="w-full rounded-xl border-2 border-black p-3 text-black font-black focus:ring-4 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-xs font-black text-black uppercase mb-1">Contraseña</label>
          <input
            v-model="creds.password"
            type="password" required
            class="w-full rounded-xl border-2 border-black p-3 text-black font-black focus:ring-4 focus:ring-indigo-500 focus:outline-none"
          />
        </div>

        <div v-if="error" class="p-3 bg-red-200 border-2 border-red-800 rounded-xl text-xs font-black text-red-950 text-center">
          {{ error }}
        </div>

        <button
          type="submit"
          class="w-full rounded-xl bg-indigo-900 hover:bg-indigo-950 py-3.5 text-sm font-black text-white shadow-lg border-2 border-black cursor-pointer"
        >
          Iniciar Sesión
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API_URL = 'http://localhost:8000/api/v1'
const router = useRouter()
const creds = ref({ username: '', password: '' })
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  try {
    // Petición a /api/v1/auth/login (ajustar segun si recibe JSON o Form Data)
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(creds.value)
    })

    if (res.ok) {
      const data = await res.json()
      // Guardar token y rol obtenido del backend
      const user = { token: data.access_token, rol: data.rol || 'admin' }
      localStorage.setItem('usuario_stock', JSON.stringify(user))

      if (user.rol === 'admin') router.push('/dashboard')
      else router.push('/pos')
    } else {
      error.value = 'Credenciales inválidas.'
    }
  } catch (e) {
    // Bypass demo en caso de estar probando localmente sin token
    if (creds.value.password === 'admin123') {
      localStorage.setItem('usuario_stock', JSON.stringify({ rol: 'admin' }))
      router.push('/dashboard')
    } else {
      error.value = 'Error de conexión con el servidor.'
    }
  }
}
</script>