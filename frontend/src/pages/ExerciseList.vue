<template>
  <div>
    <!-- Hero -->
    <div class="bg-rc-navy">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-14 sm:py-20">
        <div class="max-w-2xl">
          <div class="inline-flex items-center gap-2 bg-white/10 rounded-full px-3 py-1 mb-5">
            <div class="w-2 h-2 bg-rc-red rounded-full animate-pulse"/>
            <span class="text-white/80 text-xs font-medium tracking-wide uppercase">Open for Applications</span>
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold text-white leading-tight mb-4">
            Supplier Prequalification Portal
          </h1>
          <p class="text-white/65 text-base leading-relaxed">
            Kenya Red Cross Society invites qualified suppliers to apply for prequalification.
            Prequalified suppliers will be considered for procurement of goods, works and services.
          </p>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-10">

      <!-- Loading -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20 gap-4">
        <div class="w-8 h-8 border-2 border-rc-red border-t-transparent rounded-full animate-spin"/>
        <p class="text-sm text-slate-500">Loading exercises...</p>
      </div>

      <template v-else>
        <!-- Active exercises -->
        <section v-if="publishedExercises.length">
          <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">Open Exercises</h2>
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 mb-12">
            <router-link
              v-for="ex in publishedExercises"
              :key="ex.name"
              :to="`/exercises/${ex.name}`"
              class="group bg-white rounded-xl border border-slate-200 shadow-card hover:shadow-card-hover hover:border-rc-red/30 transition-all duration-200 overflow-hidden"
            >
              <!-- Red top bar -->
              <div class="h-1 bg-rc-red"/>
              <div class="p-5">
                <div class="flex items-start justify-between mb-3">
                  <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-green-50 border border-green-200 text-xs font-medium text-green-700">
                    <span class="w-1.5 h-1.5 bg-green-500 rounded-full"/>
                    Open
                  </span>
                  <span class="text-xs font-mono text-slate-400">{{ ex.exercise_code }}</span>
                </div>
                <h3 class="font-semibold text-slate-900 group-hover:text-rc-red transition-colors leading-snug mb-1 text-sm">
                  {{ ex.exercise_title }}
                </h3>
                <p class="text-xs text-slate-400 mb-4">{{ ex.entity }}</p>
                <div class="space-y-1.5">
                  <div class="flex items-center gap-2 text-xs text-slate-500">
                    <svg class="w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    Opens {{ formatDate(ex.open_date) }}
                  </div>
                  <div class="flex items-center gap-2 text-xs">
                    <svg class="w-3.5 h-3.5 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <span class="font-medium text-amber-700">Closes {{ formatDate(ex.close_date) }}</span>
                  </div>
                </div>
              </div>
              <div class="px-5 py-3 border-t border-slate-100 bg-slate-50/50 flex items-center justify-between">
                <span class="text-xs text-slate-400">Application fees from KES 5,000</span>
                <span class="text-xs font-semibold text-rc-red group-hover:gap-1.5 flex items-center gap-1 transition-all">
                  Apply <span class="group-hover:translate-x-0.5 transition-transform inline-block">&rarr;</span>
                </span>
              </div>
            </router-link>
          </div>
        </section>

        <!-- No open exercises -->
        <div v-else class="text-center py-20">
          <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-7 h-7 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
          </div>
          <h3 class="text-base font-semibold text-slate-700 mb-1">No Open Exercises</h3>
          <p class="text-sm text-slate-400">There are no active prequalification exercises at this time. Please check back later.</p>
        </div>

        <!-- Past exercises -->
        <section v-if="completedExercises.length">
          <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">Past Exercises</h2>
          <div class="bg-white rounded-xl border border-slate-200 shadow-card divide-y divide-slate-100">
            <div
              v-for="ex in completedExercises"
              :key="ex.name"
              class="px-5 py-3.5 flex items-center justify-between"
            >
              <div class="flex items-center gap-3">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 text-xs font-medium">
                  Closed
                </span>
                <div>
                  <span class="text-sm text-slate-700">{{ ex.exercise_title }}</span>
                  <span class="ml-2 text-xs text-slate-400 font-mono">{{ ex.exercise_code }}</span>
                </div>
              </div>
              <span class="text-xs text-slate-400 hidden sm:block">{{ formatDate(ex.close_date) }}</span>
            </div>
          </div>
        </section>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { frappeRequest } from 'frappe-ui'

const loading = ref(true)
const allExercises = ref([])

onMounted(async () => {
  try {
    const res = await frappeRequest({
      url: '/api/method/frappe.client.get_list',
      params: {
        doctype: 'Prequal Exercise',
        fields: JSON.stringify(['name', 'exercise_code', 'exercise_title', 'status', 'entity', 'open_date', 'close_date']),
        filters: JSON.stringify([['status', 'in', ['Published', 'Completed']]]),
        order_by: 'open_date desc',
        limit_page_length: 50,
      },
    })
    allExercises.value = res.message || []
  } finally {
    loading.value = false
  }
})

const publishedExercises = computed(() => allExercises.value.filter((e) => e.status === 'Published'))
const completedExercises = computed(() => allExercises.value.filter((e) => e.status === 'Completed'))

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('en-KE', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>
