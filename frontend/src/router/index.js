import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import CatalogView from '../views/CatalogView.vue'
import VentasView from '../views/VentasView.vue'

const routes = [
  { path: '/', name: 'login', component: LoginView },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/catalogo', name: 'catalogo', component: CatalogView, meta: { requiresAuth: true } },
  { path: '/pos', name: 'ventas', component: VentasView, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guardia de seguridad para rutas
router.beforeEach((to, from, next) => {
  let user = null
  try {
    user = JSON.parse(localStorage.getItem('usuario_stock'))
  } catch (e) {
    user = null
  }

  if (to.meta.requiresAuth && (!user || !user.token)) {
    return next({ name: 'login' })
  }

  if (to.meta.role) {
    const userRole = (user?.rol || '').toLowerCase()
    const isAdmin = userRole === 'admin' || userRole === 'administrador'
    if (to.meta.role === 'admin' && !isAdmin) {
      return next({ name: 'catalogo' })
    }
  }

  if (to.name === 'login' && user?.token) {
    const userRole = (user?.rol || '').toLowerCase()
    if (userRole === 'admin' || userRole === 'administrador') {
      return next({ name: 'dashboard' })
    } else {
      return next({ name: 'ventas' })
    }
  }

  next()
})

export default router