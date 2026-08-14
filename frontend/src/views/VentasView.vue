<template>
  <div class="min-h-screen bg-slate-300 p-4 font-sans text-black">
    <div class="max-w-7xl mx-auto space-y-4">

      <!-- Navbar Simplificado -->
      <header class="bg-white p-4 rounded-2xl shadow-md border-2 border-black flex justify-between items-center">
        <h1 class="text-2xl font-black text-black">Caja / Punto de Venta (POS)</h1>
        <div class="flex gap-2">
          <router-link to="/catalogo" class="px-4 py-2 bg-slate-200 border-2 border-black rounded-xl font-black text-xs">Ir al Catálogo</router-link>
        </div>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Columna Izquierda: Escáner y Búsqueda -->
        <div class="lg:col-span-2 space-y-4">
          <div class="bg-white p-5 rounded-2xl shadow-md border-2 border-black">
            <label class="block text-xs font-black uppercase mb-2">Escanear Código de Barras</label>
            <input
              v-model="codigoEscaneado"
              @keyup.enter="agregarAlCarrito"
              type="text"
              placeholder="Pase la lectora aquí..."
              autofocus
              class="w-full p-3 border-2 border-black rounded-xl font-black text-lg focus:ring-4 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <!-- Items del Carrito -->
          <div class="bg-white rounded-2xl shadow-md border-2 border-black overflow-hidden">
            <div class="p-4 bg-slate-200 border-b-2 border-black font-black text-sm">Detalle de la Venta</div>
            <table class="w-full text-left font-black text-sm">
              <thead>
                <tr class="bg-slate-100 border-b-2 border-black text-xs uppercase">
                  <th class="p-3">Producto</th>
                  <th class="p-3">Precio</th>
                  <th class="p-3">Cant.</th>
                  <th class="p-3">Subtotal</th>
                  <th class="p-3 text-right">Acción</th>
                </tr>
              </thead>
              <tbody class="divide-y-2 divide-slate-200">
                <tr v-for="(item, idx) in carrito" :key="idx">
                  <td class="p-3">{{ item.nombre }} (Talle: {{ item.talle }})</td>
                  <td class="p-3">${{ item.precio }}</td>
                  <td class="p-3">
                    <input v-model.number="item.cantidad" type="number" min="1" class="w-16 border-2 border-black rounded p-1 text-center font-black" />
                  </td>
                  <td class="p-3">${{ item.precio * item.cantidad }}</td>
                  <td class="p-3 text-right">
                    <button @click="carrito.splice(idx, 1)" class="text-red-700 font-black">✕</button>
                  </td>
                </tr>
                <tr v-if="carrito.length === 0">
                  <td colspan="5" class="p-6 text-center text-slate-600">Carrito vacío. Pase un código de barras para comenzar.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Columna Derecha: Cobro -->
        <div class="lg:col-span-1">
          <div class="bg-white p-6 rounded-2xl shadow-md border-2 border-black space-y-6">
            <h2 class="text-xl font-black border-b-2 border-black pb-2">Resumen de Cobro</h2>

            <div class="space-y-2">
              <div class="flex justify-between text-base font-black">
                <span>Total a Cobrar:</span>
                <span class="text-3xl text-emerald-800">${{ totalVenta }}</span>
              </div>
            </div>

            <button
              @click="procesarVenta"
              :disabled="carrito.length === 0"
              class="w-full py-4 bg-emerald-700 hover:bg-emerald-800 text-white font-black text-lg rounded-xl border-2 border-black shadow-lg disabled:opacity-50 cursor-pointer"
            >
              Confirmar Venta
            </button>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const API_URL = 'http://localhost:8000/api/v1'
const codigoEscaneado = ref('')
const carrito = ref([])

const totalVenta = computed(() => {
  return carrito.value.reduce((acc, item) => acc + (item.precio * item.cantidad), 0)
})

const agregarAlCarrito = async () => {
  if (!codigoEscaneado.value.trim()) return

  try {
    // Buscar la variante por código de barras
    const res = await fetch(`${API_URL}/prendas/codigo/${codigoEscaneado.value.trim()}`)
    if (res.ok) {
      const prenda = await res.json()
      // Tomar la primera variante coincidente
      const variante = prenda.variantes[0]

      carrito.value.push({
        id_stock_prenda: variante.id_stock_prenda,
        nombre: prenda.nombre,
        talle: variante.talle,
        precio: variante.precio_venta || 0,
        cantidad: 1
      })
    } else {
      alert("Código de barras no encontrado.")
    }
  } catch (e) {
    console.error(e)
  } finally {
    codigoEscaneado.value = ''
  }
}

const procesarVenta = async () => {
  try {
    const payload = {
      items: carrito.value.map(i => ({
        id_stock_prenda: i.id_stock_prenda,
        cantidad: i.cantidad,
        precio_unitario: i.precio
      })),
      total: totalVenta.value
    }

    const res = await fetch(`${API_URL}/ventas/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      alert("Venta registrada con éxito.")
      carrito.value = []
    } else {
      alert("Error al procesar la venta.")
    }
  } catch (e) {
    console.error("Error al registrar venta:", e)
  }
}
</script>