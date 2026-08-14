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
  const user = JSON.parse(localStorage.getItem('usuario_stock'))

  if (to.meta.requiresAuth && !user) {
    return next({ name: 'login' })
  }

  if (to.meta.role && user?.rol !== to.meta.role) {
    return next({ name: 'catalogo' })
  }

  next()
})

export default router