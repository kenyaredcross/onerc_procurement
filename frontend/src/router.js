import { createRouter, createWebHistory } from 'vue-router'

function isLoggedIn() {
  return window.frappe?.session?.user && window.frappe.session.user !== 'Guest'
}

const routes = [
  {
    path: '/',
    redirect: '/exercises',
  },
  {
    path: '/exercises',
    name: 'ExerciseList',
    component: () => import('@/pages/ExerciseList.vue'),
  },
  {
    path: '/exercises/:exerciseId',
    name: 'ExerciseDetail',
    component: () => import('@/pages/ExerciseDetail.vue'),
    props: true,
  },
  {
    path: '/exercises/:exerciseId/apply/:applicationId',
    name: 'ApplicationForm',
    component: () => import('@/pages/ApplicationForm.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/applications/:applicationId/pay',
    name: 'PaymentPage',
    component: () => import('@/pages/PaymentPage.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/applications',
    name: 'MyApplications',
    component: () => import('@/pages/MyApplications.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'SupplierProfile',
    component: () => import('@/pages/SupplierProfile.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory('/prequal'),
  routes,
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !isLoggedIn()) {
    window.location.href = `/login?redirect-to=/prequal${to.path}`
    return false
  }
})

export default router
