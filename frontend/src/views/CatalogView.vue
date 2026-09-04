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
            class="px-4 py-2.5 bg-white hover:bg-slate-100/80 text-slate-900 font-bold text-xs rounded-xl border border-slate-200 shadow-xs flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>Ir a Caja (POS)</span>
          </router-link>

          <button
            v-if="esAdmin"
            @click="abrirModalCrear"
            class="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md shadow-indigo-600/10 flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Nueva Prenda</span>
          </button>
        </div>
      </div>

      <!-- Estado de Error General -->
      <div v-if="errorCarga" class="p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-center gap-3 text-sm text-rose-700 font-semibold">
        <svg class="w-5 h-5 shrink-0 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ errorCarga }}</span>
        <button @click="cargarDatos" class="ml-auto text-xs underline font-bold cursor-pointer hover:no-underline">Reintentar</button>
      </div>

      <!-- Tarjetas de Métricas Rápidas (Solo Admin) -->
      <section v-if="esAdmin" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <p class="text-xs font-bold uppercase tracking-wider text-slate-500">Ganancia Real Hoy</p>
            <div v-if="cargando" class="mt-1 h-9 w-36 bg-slate-100 rounded-lg animate-pulse"></div>
            <h3 v-else class="text-2xl sm:text-3xl font-black text-slate-900 mt-1 tracking-tight">
              ${{ Number(gananciasDiarias || 0).toLocaleString('es-AR') }}
            </h3>
          </div>
          <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-2xl shrink-0">💵</div>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs flex items-center justify-between">
          <div>
            <p class="text-xs font-bold uppercase tracking-wider text-slate-500">Ganancia Real del Mes</p>
            <div v-if="cargando" class="mt-1 h-9 w-36 bg-slate-100 rounded-lg animate-pulse"></div>
            <div v-else class="flex items-center gap-2 mt-1">
              <h3 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
                {{ mostrarGananciaMes ? `$${Number(gananciasMensuales || 0).toLocaleString('es-AR')}` : '••••••' }}
              </h3>
              <button
                @click="mostrarGananciaMes = !mostrarGananciaMes"
                class="p-1 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors cursor-pointer"
                :title="mostrarGananciaMes ? 'Ocultar monto' : 'Mostrar monto'"
                type="button"
              >
                <svg v-if="mostrarGananciaMes" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 4.411m0 0L21 21" />
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-2xl shrink-0">📈</div>
        </div>
      </section>

      <!-- Barra de Búsqueda y Filtros -->
      <section class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
        <label for="search-barcode" class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
          Buscar por Código de Barras, Nombre o Categoría
        </label>
        <div class="flex flex-col sm:flex-row gap-2.5">
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
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 font-medium text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
            />
          </div>
          <button
            @click="buscarPorCodigo"
            class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl transition-colors cursor-pointer shrink-0"
          >
            Buscar
          </button>
          <button
            v-if="filtroActivo"
            @click="limpiarFiltro"
            class="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition-colors cursor-pointer shrink-0"
          >
            Limpiar
          </button>
        </div>
        <p v-if="mensajeBusqueda" class="text-xs font-semibold text-indigo-600 mt-2 flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {{ mensajeBusqueda }}
        </p>
      </section>

      <!-- Cuadrícula: Alertas y Listado de Prendas -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Alertas Bajo Stock -->
        <div class="lg:col-span-1">
          <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-2 border-b border-slate-100">
              <h2 class="text-sm font-black text-slate-900 flex items-center gap-2">
                <span class="relative flex h-2.5 w-2.5">
                  <span v-if="alertasStock.length > 0" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5" :class="alertasStock.length > 0 ? 'bg-rose-500' : 'bg-emerald-500'"></span>
                </span>
                Stock Crítico ({{ alertasStock.length }})
              </h2>
            </div>

            <!-- Skeleton -->
            <div v-if="cargando" class="space-y-2">
              <div v-for="i in 4" :key="i" class="p-3 rounded-xl bg-slate-50 space-y-1.5">
                <div class="h-3.5 bg-slate-200 rounded animate-pulse w-3/4"></div>
                <div class="h-3 bg-slate-100 rounded animate-pulse w-1/2"></div>
              </div>
            </div>

            <div v-else-if="alertasStock.length === 0" class="py-8 text-center text-slate-400 text-xs font-medium">
              <svg class="w-8 h-8 mx-auto text-emerald-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Sin alertas activas. Stock en nivel correcto.
            </div>

            <ul v-else class="divide-y divide-slate-100 max-h-[400px] overflow-y-auto pr-1 space-y-2">
              <li v-for="item in alertasStock" :key="item.id_stock_prenda" class="pt-2 first:pt-0">
                <div class="p-3 rounded-xl bg-rose-50/60 space-y-1">
                  <div class="flex justify-between items-start gap-2">
                    <span class="font-extrabold text-slate-900 text-xs leading-tight">{{ item.prenda?.nombre || 'Prenda' }}</span>
                    <span class="bg-rose-100 text-rose-700 font-bold text-[10px] px-2 py-0.5 rounded-md uppercase shrink-0">
                      {{ item.talle }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-[11px] text-slate-500 font-medium">
                    <span>Stock: <strong class="text-rose-600 font-bold">{{ item.stock_actual }}</strong> (Mín: {{ item.stock_minimo }})</span>
                    <span class="font-mono text-slate-400 text-[10px]">{{ item.codigo_barras }}</span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Tabla de Prendas -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">
            <div class="p-4 bg-slate-50/50 flex justify-between items-center border-b border-slate-100">
              <h2 class="text-sm font-black text-slate-900">
                Catálogo de Prendas
                <span class="ml-1.5 text-slate-400 font-bold">({{ prendasFiltradas.length }})</span>
              </h2>
            </div>

            <!-- Skeleton de tabla -->
            <div v-if="cargando" class="divide-y divide-slate-100">
              <div v-for="i in 6" :key="i" class="p-4 flex items-center gap-4">
                <div class="w-8 h-4 bg-slate-100 rounded animate-pulse"></div>
                <div class="flex-1 space-y-1.5">
                  <div class="h-3.5 bg-slate-200 rounded animate-pulse w-1/2"></div>
                  <div class="h-3 bg-slate-100 rounded animate-pulse w-1/3"></div>
                </div>
                <div class="flex gap-1.5">
                  <div class="w-14 h-6 bg-slate-100 rounded-lg animate-pulse"></div>
                  <div class="w-14 h-6 bg-slate-100 rounded-lg animate-pulse"></div>
                </div>
              </div>
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50/50 text-[11px] font-black uppercase tracking-wider text-slate-400 border-b border-slate-100">
                    <th class="py-3 px-4">ID</th>
                    <th class="py-3 px-4">Nombre / Categoría</th>
                    <th class="py-3 px-4 hidden sm:table-cell">Tela</th>
                    <th class="py-3 px-4">Variantes (Talle / Stock)</th>
                    <th v-if="esAdmin" class="py-3 px-4 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 text-xs font-medium text-slate-700">
                  <tr v-for="prenda in prendasFiltradas" :key="prenda.id_prenda" class="hover:bg-slate-50/80 transition-colors">
                    <td class="py-3.5 px-4 font-bold text-slate-300">#{{ prenda.id_prenda }}</td>
                    <td class="py-3.5 px-4">
                      <span class="font-extrabold text-slate-900">{{ prenda.nombre }}</span>
                      <span class="block text-[11px] font-medium text-slate-500">{{ prenda.categoria }}</span>
                    </td>
                    <td class="py-3.5 px-4 text-slate-600 font-semibold hidden sm:table-cell">{{ prenda.tipo_tela }}</td>
                    <td class="py-3.5 px-4">
                      <div class="flex flex-wrap gap-1.5">
                        <span
                          v-for="v in prenda.variantes"
                          :key="v.id_stock_prenda"
                          class="inline-flex items-center gap-1 rounded-lg px-2 py-1 text-[11px] font-bold"
                          :class="v.stock_actual <= v.stock_minimo ? 'bg-rose-50 text-rose-700 ring-1 ring-rose-200' : 'bg-slate-100 text-slate-700'"
                          :title="v.stock_actual <= v.stock_minimo ? 'Stock bajo' : ''"
                        >
                          {{ v.talle }}: <strong class="text-slate-900">{{ v.stock_actual }}u.</strong>
                          <span class="text-slate-500 hidden lg:inline">(${{ Number(v.precio_venta).toLocaleString('es-AR') }})</span>
                        </span>
                      </div>
                    </td>
                    <td v-if="esAdmin" class="py-3.5 px-4 text-right">
                      <div class="flex items-center justify-end gap-1.5">
                        <button
                          @click="abrirModalEditar(prenda)"
                          title="Modificar prenda"
                          class="text-xs font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 px-2.5 py-1.5 rounded-lg transition-colors cursor-pointer inline-flex items-center gap-1"
                        >
                          ✏️ <span class="hidden sm:inline">Editar</span>
                        </button>
                        <button
                          @click="descargarPDF(prenda.id_prenda)"
                          title="Imprimir etiquetas"
                          class="text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 px-2.5 py-1.5 rounded-lg transition-colors cursor-pointer inline-flex items-center gap-1"
                        >
                          🖨️ <span class="hidden sm:inline">PDF</span>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="prendasFiltradas.length === 0 && !cargando">
                    <td :colspan="esAdmin ? 5 : 4" class="py-14 text-center">
                      <svg class="w-10 h-10 mx-auto text-slate-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                      <p class="text-sm text-slate-400 font-medium">No se encontraron prendas registradas en el inventario.</p>
                      <button v-if="esAdmin" @click="abrirModalCrear" class="mt-3 text-xs font-bold text-indigo-600 hover:underline cursor-pointer">
                        + Agregar primera prenda
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

      <!-- Modal Crear Prenda -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="mostrarModalCrear"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm"
          @click.self="cerrarModal"
        >
          <transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
          >
            <div v-if="mostrarModalCrear" class="bg-white rounded-3xl shadow-2xl max-w-lg w-full overflow-hidden max-h-[90vh] flex flex-col">
              <div class="px-6 py-4 flex items-center justify-between bg-slate-50/70 border-b border-slate-100">
                <h3 class="text-base font-black text-slate-900">{{ idPrendaEditando ? 'Modificar Prenda' : 'Registrar Nueva Prenda' }}</h3>
                <button
                  @click="cerrarModal"
                  class="text-slate-400 hover:text-slate-600 hover:bg-slate-100 p-1.5 rounded-lg transition-colors cursor-pointer"
                  aria-label="Cerrar modal"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <form @submit.prevent="guardarPrenda" class="p-6 space-y-4 overflow-y-auto">
                <div>
                  <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Nombre de la Prenda *</label>
                  <input
                    v-model="nuevaPrenda.nombre"
                    type="text" required placeholder="Ej: Camisa Manga Larga"
                    class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  />
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Categoría *</label>
                    <input
                      v-model="nuevaPrenda.categoria"
                      type="text" required placeholder="Ej: Camisas"
                      class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                    />
                  </div>
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Tipo de Tela *</label>
                    <input
                      v-model="nuevaPrenda.tipo_tela"
                      type="text" required placeholder="Ej: Algodón"
                      class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider">Talles, Precios y Cantidades</label>
                    <button v-if="!idPrendaEditando" type="button" @click="agregarFilaVariante" class="text-xs font-bold text-indigo-600 hover:text-indigo-700 cursor-pointer flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                      </svg>
                      Agregar Talle
                    </button>
                  </div>

                  <div class="space-y-2 max-h-[200px] overflow-y-auto pr-1">
                    <div v-if="nuevaPrenda.variantes.length === 0" class="py-4 text-center text-xs text-slate-400 bg-slate-50 rounded-xl">
                      Sin variantes. Haga clic en "Agregar Talle".
                    </div>
                    <div v-for="(v, idx) in nuevaPrenda.variantes" :key="idx" class="flex items-center gap-2 bg-slate-50 border border-slate-100 p-2.5 rounded-xl">
                      <input v-model="v.talle" type="text" placeholder="Talle" :disabled="!!idPrendaEditando" required class="w-16 px-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:bg-slate-100 disabled:text-slate-500" />
                      <input v-model.number="v.precio_venta" type="number" step="0.01" min="0" placeholder="Precio $" required class="flex-1 min-w-0 px-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
                      <input v-model.number="v.stock_actual" type="number" min="0" placeholder="Stock" required class="w-16 px-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
                      <input v-model.number="v.stock_minimo" type="number" min="0" placeholder="Mín." required class="w-16 px-2 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500" />
                      <button v-if="!idPrendaEditando" type="button" @click="nuevaPrenda.variantes.splice(idx, 1)" class="text-rose-500 hover:text-rose-700 hover:bg-rose-50 p-1.5 rounded-lg transition-colors cursor-pointer shrink-0" aria-label="Eliminar variante">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                <div v-if="errorCrear" class="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs font-semibold text-rose-700 flex items-center gap-2">
                  <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ errorCrear }}
                </div>

                <div class="pt-4 border-t border-slate-100 flex justify-end gap-2.5">
                  <button
                    type="button"
                    @click="cerrarModal"
                    class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors cursor-pointer"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    :disabled="guardando"
                    class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-xs transition-colors cursor-pointer flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
                  >
                    <svg v-if="guardando" class="animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    {{ guardando ? 'Guardando...' : (idPrendaEditando ? 'Guardar Cambios' : 'Guardar Prenda') }}
                  </button>
                </div>
              </form>
            </div>
          </transition>
        </div>
      </transition>

    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import Navbar from '../components/PrendasManager.vue'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const usuarioAutenticado = ref(null)
const esAdmin = computed(() => {
  const rol = (usuarioAutenticado.value?.rol || '').toLowerCase()
  return rol === 'admin' || rol === 'administrador'
})

const cargando = ref(false)
const errorCarga = ref('')
const guardando = ref(false)
const gananciasDiarias = ref(0)
const gananciasMensuales = ref(0)
const mostrarGananciaMes = ref(false)
const prendas = ref([])
const alertasStock = ref([])
const codigoBusqueda = ref('')
const mensajeBusqueda = ref('')
const filtroActivo = ref(false)
const mostrarModalCrear = ref(false)
const idPrendaEditando = ref(null)
const errorCrear = ref('')

const toast = reactive({ visible: false, message: '', type: 'success' })
let toastTimer = null

const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.message = message
  toast.type = type
  toast.visible = true
  toastTimer = setTimeout(() => { toast.visible = false }, 3500)
}

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

const cerrarModal = () => {
  mostrarModalCrear.value = false
  idPrendaEditando.value = null
  errorCrear.value = ''
}

const abrirModalCrear = () => {
  errorCrear.value = ''
  idPrendaEditando.value = null
  nuevaPrenda.value = {
    nombre: '',
    categoria: '',
    tipo_tela: '',
    variantes: [
      { talle: 'S', precio_venta: 15000, stock_actual: 10, stock_minimo: 3 },
      { talle: 'M', precio_venta: 15000, stock_actual: 10, stock_minimo: 3 }
    ]
  }
  mostrarModalCrear.value = true
}

const abrirModalEditar = (prenda) => {
  errorCrear.value = ''
  idPrendaEditando.value = prenda.id_prenda
  nuevaPrenda.value = {
    nombre: prenda.nombre,
    categoria: prenda.categoria,
    tipo_tela: prenda.tipo_tela,
    variantes: prenda.variantes.map(v => ({
      id_stock_prenda: v.id_stock_prenda,
      talle: v.talle,
      precio_venta: Number(v.precio_venta),
      stock_actual: Number(v.stock_actual),
      stock_minimo: Number(v.stock_minimo)
    }))
  }
  mostrarModalCrear.value = true
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
  cargando.value = true
  errorCarga.value = ''
  try {
    const headers = getAuthHeaders()

    const requests = [
      fetch(`${API_URL}/prendas/`, { headers }),
      fetch(`${API_URL}/prendas/alertas/reposicion`, { headers })
    ]

    if (esAdmin.value) {
      requests.push(fetch(`${API_URL}/reportes/resumen`, { headers }))
    }

    const [resPrendas, resAlertas, resGanancias] = await Promise.all(requests)

    if (resPrendas?.ok) prendas.value = await resPrendas.json()
    if (resAlertas?.ok) alertasStock.value = await resAlertas.json()
    if (resGanancias?.ok) {
      const datos = await resGanancias.json()
      gananciasDiarias.value = datos.ganancia_diaria
      gananciasMensuales.value = datos.ganancia_mensual
    }
  } catch (error) {
    console.error('Error al conectar con el servidor:', error)
    errorCarga.value = 'No se pudo conectar con el servidor. Verifique que el backend esté activo.'
  } finally {
    cargando.value = false
  }
}

const guardarPrenda = async () => {
  errorCrear.value = ''
  guardando.value = true
  try {
    const esModificacion = !!idPrendaEditando.value
    const url = esModificacion ? `${API_URL}/prendas/${idPrendaEditando.value}` : `${API_URL}/prendas/`
    const method = esModificacion ? 'PUT' : 'POST'

    const payload = esModificacion
      ? {
          nombre: nuevaPrenda.value.nombre,
          categoria: nuevaPrenda.value.categoria,
          tipo_tela: nuevaPrenda.value.tipo_tela,
          variantes: nuevaPrenda.value.variantes.map(v => ({
            id_stock_prenda: v.id_stock_prenda,
            precio_venta: v.precio_venta,
            stock_actual: v.stock_actual,
            stock_minimo: v.stock_minimo
          }))
        }
      : nuevaPrenda.value

    const response = await fetch(url, {
      method,
      headers: getAuthHeaders(),
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      cerrarModal()
      showToast(esModificacion ? 'Prenda modificada correctamente.' : 'Prenda registrada correctamente.', 'success')
      await cargarDatos()
    } else {
      const err = await response.json().catch(() => ({}))
      errorCrear.value = err.detail || (esModificacion ? 'Error al modificar la prenda.' : 'Error al guardar la prenda. Verifique los datos.')
    }
  } catch (error) {
    console.error('Error guardando prenda:', error)
    errorCrear.value = 'Error de conexión con el servidor.'
  } finally {
    guardando.value = false
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