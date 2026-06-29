<template>
  <div>
    <!-- Nav bar -->
    <div class="bg-white border-b border-slate-200">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 py-3">
        <router-link to="/exercises" class="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-rc-navy transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          All Exercises
        </router-link>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-24 gap-4">
      <div class="w-8 h-8 border-2 border-rc-red border-t-transparent rounded-full animate-spin"/>
      <p class="text-sm text-slate-500">Loading exercise...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="max-w-2xl mx-auto px-4 py-16 text-center">
      <p class="text-red-600 text-sm mb-3">{{ error }}</p>
      <button @click="loadExercise" class="text-sm underline text-slate-500">Retry</button>
    </div>

    <template v-else-if="exercise">
      <!-- Exercise header -->
      <div class="bg-rc-navy">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 py-10">
          <div class="flex items-center gap-2 mb-3">
            <span :class="statusBadge" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border">
              <span class="w-1.5 h-1.5 rounded-full bg-current"/>
              {{ exercise.status }}
            </span>
            <span class="text-white/40 text-xs font-mono">{{ exercise.exercise_code }}</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-bold text-white mb-1">{{ exercise.exercise_title }}</h1>
          <p class="text-white/55 text-sm">{{ exercise.entity }}</p>

          <div class="flex flex-wrap gap-5 mt-6">
            <div>
              <div class="text-white/40 text-xs uppercase tracking-wide mb-0.5">Opens</div>
              <div class="text-white/90 text-sm font-medium">{{ formatDate(exercise.open_date) }}</div>
            </div>
            <div class="w-px bg-white/10"/>
            <div>
              <div class="text-white/40 text-xs uppercase tracking-wide mb-0.5">Deadline</div>
              <div class="text-rc-red font-semibold text-sm">{{ formatDate(exercise.close_date) }}</div>
            </div>
            <div v-if="exercise.total_bids" class="w-px bg-white/10"/>
            <div v-if="exercise.total_bids">
              <div class="text-white/40 text-xs uppercase tracking-wide mb-0.5">Applications</div>
              <div class="text-white/90 text-sm font-medium">{{ exercise.total_bids }} received</div>
            </div>
          </div>
        </div>
      </div>

      <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 space-y-6">
        <!-- Advertisement -->
        <div v-if="exercise.advertisement_text" class="bg-white rounded-xl border border-slate-200 shadow-card p-6">
          <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">About This Exercise</h2>
          <div class="prose prose-sm max-w-none text-slate-700" v-html="exercise.advertisement_text"/>
        </div>

        <!-- Instructions -->
        <div v-if="exercise.portal_instructions" class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <div class="flex items-start gap-3">
            <div class="w-8 h-8 bg-amber-100 rounded-lg flex items-center justify-center shrink-0 mt-0.5">
              <svg class="w-4 h-4 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div>
              <h2 class="text-sm font-semibold text-amber-900 mb-2">How to Apply</h2>
              <div class="prose prose-sm max-w-none text-amber-800" v-html="exercise.portal_instructions"/>
            </div>
          </div>
        </div>

        <!-- Categories -->
        <div>
          <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">
            {{ exercise.status === 'Published' ? 'Select a Category to Apply' : 'Categories' }}
          </h2>

          <!-- Not logged in prompt -->
          <div v-if="!isLoggedIn && exercise.status === 'Published'" class="bg-rc-navy rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4 mb-4">
            <div>
              <p class="text-white font-semibold mb-0.5">Ready to apply?</p>
              <p class="text-white/60 text-sm">Log in to select a category and submit your application.</p>
            </div>
            <a
              :href="`/login?redirect-to=/prequal/exercises/${exerciseId}`"
              class="shrink-0 px-5 py-2.5 bg-rc-red text-white text-sm font-semibold rounded-lg hover:bg-rc-red-dark transition-colors shadow-sm"
            >
              Log In to Apply
            </a>
          </div>

          <!-- Category cards -->
          <div class="grid gap-3 sm:grid-cols-2">
            <button
              v-for="cat in exercise.categories"
              :key="cat.category"
              :disabled="!isLoggedIn || exercise.status !== 'Published'"
              :class="[
                'relative text-left rounded-xl border-2 p-5 transition-all duration-150',
                selectedCategory === cat.category
                  ? 'border-rc-red bg-red-50 shadow-card-hover'
                  : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-card',
                (!isLoggedIn || exercise.status !== 'Published') && 'opacity-60 cursor-not-allowed',
                isLoggedIn && exercise.status === 'Published' && 'cursor-pointer',
              ]"
              @click="selectCategory(cat)"
            >
              <!-- Selected indicator -->
              <div
                :class="[
                  'absolute top-4 right-4 w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all',
                  selectedCategory === cat.category ? 'border-rc-red bg-rc-red' : 'border-slate-300 bg-white',
                ]"
              >
                <svg v-if="selectedCategory === cat.category" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
              </div>

              <div class="pr-8">
                <p class="font-semibold text-slate-900 text-sm leading-snug mb-1">{{ cat.category_title }}</p>
                <p class="text-xs text-slate-400 mb-3">{{ cat.category_type }}</p>
                <div class="flex items-baseline gap-1">
                  <span class="text-lg font-bold text-rc-navy">KES {{ formatAmount(effectiveFee(cat)) }}</span>
                  <span class="text-xs text-slate-400">application fee</span>
                </div>
              </div>
            </button>
          </div>

          <!-- Apply button -->
          <div v-if="isLoggedIn && exercise.status === 'Published'" class="mt-5">
            <div v-if="!selectedCategory" class="text-center py-3">
              <p class="text-sm text-slate-400">Select a category above to continue.</p>
            </div>
            <div v-else class="flex items-center justify-between bg-white rounded-xl border border-slate-200 shadow-card p-4">
              <div>
                <p class="text-sm font-semibold text-slate-900">{{ selectedCategoryTitle }}</p>
                <p class="text-xs text-slate-400">Fee: <span class="font-semibold text-rc-navy">KES {{ formatAmount(selectedFee) }}</span> (paid via M-Pesa)</p>
              </div>
              <button
                :disabled="creating"
                class="flex items-center gap-2 px-6 py-2.5 bg-rc-red text-white text-sm font-semibold rounded-lg hover:bg-rc-red-dark disabled:opacity-50 transition-colors shadow-sm"
                @click="startApplication"
              >
                <span v-if="creating" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/>
                {{ creating ? 'Starting...' : 'Start Application' }}
              </button>
            </div>

            <div v-if="applyError" class="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-sm text-red-700">{{ applyError }}</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { frappeRequest } from 'frappe-ui'
import { useRouter } from 'vue-router'

const props = defineProps({ exerciseId: String })
const router = useRouter()

const isLoggedIn = !!(window.frappe?.session?.user && window.frappe.session.user !== 'Guest')

const loading = ref(true)
const error = ref('')
const exercise = ref(null)
const selectedCategory = ref('')
const selectedCategoryTitle = ref('')
const selectedFee = ref(0)
const creating = ref(false)
const applyError = ref('')

const DEFAULT_FEE = 5000

function effectiveFee(cat) {
  return cat.fee_override > 0 ? cat.fee_override : DEFAULT_FEE
}

function selectCategory(cat) {
  if (!isLoggedIn || exercise.value?.status !== 'Published') return
  selectedCategory.value = cat.category
  selectedCategoryTitle.value = cat.category_title
  selectedFee.value = effectiveFee(cat)
}

const statusBadge = computed(() => {
  const s = exercise.value?.status
  if (s === 'Published') return 'bg-green-500/20 text-green-300 border-green-500/30'
  if (s === 'Completed') return 'bg-white/10 text-white/50 border-white/20'
  if (s === 'Draft') return 'bg-amber-500/20 text-amber-300 border-amber-500/30'
  return 'bg-white/10 text-white/50 border-white/20'
})

async function loadExercise() {
  loading.value = true
  error.value = ''
  try {
    const res = await frappeRequest({
      url: '/api/method/frappe.client.get',
      params: { doctype: 'Prequal Exercise', name: props.exerciseId },
    })
    exercise.value = res.message
  } catch (e) {
    error.value = e.message || 'Failed to load exercise.'
  } finally {
    loading.value = false
  }
}

async function startApplication() {
  if (!selectedCategory.value) return
  creating.value = true
  applyError.value = ''
  try {
    const res = await frappeRequest({
      url: '/api/method/onerc_procurement.api.portal.create_application',
      params: {
        exercise: props.exerciseId,
        category: selectedCategory.value,
      },
    })
    const app = res.message
    router.push(`/applications/${app.name}/pay`)
  } catch (e) {
    applyError.value = e.exc_type === 'ValidationError'
      ? e.message
      : (e.message || 'Failed to create application. Please try again.')
  } finally {
    creating.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('en-KE', { day: 'numeric', month: 'long', year: 'numeric' })
}
function formatAmount(n) {
  return Number(n).toLocaleString('en-KE')
}

onMounted(loadExercise)
</script>
