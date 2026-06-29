<template>
  <div>
    <!-- Page header -->
    <div class="bg-rc-navy">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        <h1 class="text-2xl font-bold text-white">My Applications</h1>
        <p class="text-white/55 text-sm mt-1">Track and manage your prequalification applications.</p>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <!-- Loading -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20 gap-4">
        <div class="w-8 h-8 border-2 border-rc-red border-t-transparent rounded-full animate-spin"/>
        <p class="text-sm text-slate-500">Loading applications...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="!applications.length" class="text-center py-20">
        <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <h3 class="text-base font-semibold text-slate-700 mb-1">No Applications Yet</h3>
        <p class="text-sm text-slate-400 mb-6">You haven't started any applications. Browse open exercises to get started.</p>
        <router-link
          to="/exercises"
          class="inline-flex items-center gap-2 px-5 py-2.5 bg-rc-red text-white font-semibold text-sm rounded-lg hover:bg-rc-red-dark transition-colors shadow-sm"
        >
          Browse Open Exercises &rarr;
        </router-link>
      </div>

      <!-- Applications list -->
      <div v-else class="space-y-3">
        <div
          v-for="app in applications"
          :key="app.name"
          class="bg-white rounded-xl border border-slate-200 shadow-card hover:shadow-card-hover transition-shadow"
        >
          <!-- Red left accent for action-needed apps -->
          <div class="flex overflow-hidden rounded-xl">
            <div :class="['w-1 shrink-0', accentColor(app)]"/>
            <div class="flex-1 p-5 flex flex-col sm:flex-row sm:items-center gap-4">
              <!-- Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center flex-wrap gap-2 mb-2">
                  <span :class="statusBadge(app.status)" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border">
                    {{ app.status }}
                  </span>
                  <span :class="payBadge(app.payment_status)" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs border">
                    <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">
                      <path v-if="app.payment_status === 'Paid'" fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                      <path v-else fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
                    </svg>
                    {{ app.payment_status }}
                  </span>
                </div>
                <p class="font-semibold text-slate-900 truncate">{{ app.exercise }}</p>
                <p class="text-sm text-slate-500 mt-0.5">{{ app.category }}</p>

                <!-- Score (if evaluated) -->
                <div v-if="app.technical_score > 0" class="mt-2 flex items-center gap-3">
                  <div class="flex-1 max-w-32 bg-slate-100 rounded-full h-1.5">
                    <div
                      :class="[app.pass_fail === 'Pass' ? 'bg-green-500' : 'bg-red-500']"
                      :style="{ width: Math.min(app.technical_score, 100) + '%' }"
                      class="h-1.5 rounded-full"
                    />
                  </div>
                  <span class="text-xs font-semibold" :class="app.pass_fail === 'Pass' ? 'text-green-700' : 'text-red-600'">
                    {{ app.technical_score }}% — {{ app.pass_fail }}
                  </span>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex items-center gap-2 shrink-0">
                <router-link
                  v-if="app.payment_status !== 'Paid'"
                  :to="`/applications/${app.name}/pay`"
                  class="flex items-center gap-1.5 px-4 py-2 bg-rc-red text-white text-xs font-semibold rounded-lg hover:bg-rc-red-dark transition-colors"
                >
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                  </svg>
                  Pay Now
                </router-link>

                <router-link
                  v-else-if="app.status === 'Active'"
                  :to="`/exercises/${app.exercise}/apply/${app.name}`"
                  class="flex items-center gap-1.5 px-4 py-2 bg-rc-navy text-white text-xs font-semibold rounded-lg hover:bg-rc-navy-light transition-colors"
                >
                  Continue &rarr;
                </router-link>

                <router-link
                  v-else
                  :to="`/exercises/${app.exercise}/apply/${app.name}`"
                  class="flex items-center gap-1.5 px-4 py-2 border border-slate-200 text-slate-600 text-xs font-medium rounded-lg hover:bg-slate-50 transition-colors"
                >
                  View
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { frappeRequest } from 'frappe-ui'

const loading = ref(true)
const applications = ref([])

onMounted(async () => {
  try {
    const res = await frappeRequest({
      url: '/api/method/frappe.client.get_list',
      params: {
        doctype: 'Prequal Application',
        fields: JSON.stringify(['name', 'exercise', 'category', 'status', 'payment_status', 'submission_date', 'technical_score', 'pass_fail']),
        order_by: 'creation desc',
        limit_page_length: 100,
      },
    })
    applications.value = res.message || []
  } finally {
    loading.value = false
  }
})

function statusBadge(status) {
  if (status === 'Prequalified') return 'bg-green-50 text-green-700 border-green-200'
  if (status === 'Submitted') return 'bg-blue-50 text-blue-700 border-blue-200'
  if (status === 'Active') return 'bg-indigo-50 text-indigo-700 border-indigo-200'
  if (status === 'Not Prequalified') return 'bg-red-50 text-red-700 border-red-200'
  return 'bg-slate-100 text-slate-500 border-slate-200'
}

function payBadge(status) {
  return status === 'Paid'
    ? 'bg-green-50 text-green-700 border-green-200'
    : 'bg-amber-50 text-amber-700 border-amber-200'
}

function accentColor(app) {
  if (app.payment_status !== 'Paid') return 'bg-rc-red'
  if (app.status === 'Active') return 'bg-rc-navy'
  if (app.status === 'Prequalified') return 'bg-green-500'
  if (app.status === 'Not Prequalified') return 'bg-red-400'
  return 'bg-slate-300'
}
</script>
