<template>
  <div>
    <!-- Subnav -->
    <div class="bg-white border-b border-slate-200">
      <div class="max-w-2xl mx-auto px-4 sm:px-6 py-3">
        <router-link to="/applications" class="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-rc-navy transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          My Applications
        </router-link>
      </div>
    </div>

    <div class="max-w-2xl mx-auto px-4 sm:px-6 py-10">
      <!-- Page title -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-rc-navy">Application Fee Payment</h1>
        <p class="text-sm text-slate-500 mt-1">Pay via M-Pesa to activate your application.</p>
      </div>

      <!-- Loading app -->
      <div v-if="appLoading" class="flex items-center justify-center py-16">
        <div class="w-7 h-7 border-2 border-rc-red border-t-transparent rounded-full animate-spin"/>
      </div>

      <template v-else-if="appDoc">
        <!-- Summary card -->
        <div class="bg-rc-navy rounded-xl p-6 mb-6">
          <div class="grid grid-cols-2 gap-4 text-sm mb-5">
            <div>
              <div class="text-white/45 text-xs uppercase tracking-wide mb-0.5">Application</div>
              <div class="text-white font-mono text-xs">{{ applicationId }}</div>
            </div>
            <div>
              <div class="text-white/45 text-xs uppercase tracking-wide mb-0.5">Exercise</div>
              <div class="text-white text-xs">{{ appDoc.exercise }}</div>
            </div>
            <div class="col-span-2">
              <div class="text-white/45 text-xs uppercase tracking-wide mb-0.5">Category</div>
              <div class="text-white text-sm font-medium">{{ appDoc.category }}</div>
            </div>
          </div>
          <div class="border-t border-white/15 pt-4 flex items-center justify-between">
            <span class="text-white/60 text-sm">Amount Due</span>
            <span class="text-white text-2xl font-bold">KES {{ formatAmount(appDoc.amount_due || 5000) }}</span>
          </div>
        </div>

        <!-- Already paid -->
        <div v-if="appDoc.payment_status === 'Paid'" class="bg-white rounded-xl border border-slate-200 shadow-card p-8 text-center">
          <div class="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-7 h-7 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <h2 class="text-lg font-bold text-slate-900 mb-1">Payment Confirmed</h2>
          <p class="text-sm text-slate-500 mb-6">Your application is active. Complete all sections and submit before the deadline.</p>
          <router-link
            :to="`/exercises/${appDoc.exercise}/apply/${applicationId}`"
            class="inline-flex items-center gap-2 px-6 py-2.5 bg-rc-red text-white font-semibold text-sm rounded-lg hover:bg-rc-red-dark transition-colors shadow-sm"
          >
            Continue Application &rarr;
          </router-link>
        </div>

        <!-- Payment flow -->
        <div v-else class="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
          <!-- Steps indicator -->
          <div class="flex border-b border-slate-100">
            <div
              v-for="(label, i) in ['Enter Phone', 'Confirm on Phone', 'Done']"
              :key="i"
              :class="[
                'flex-1 py-3 text-center text-xs font-medium transition-colors',
                currentStep === i ? 'text-rc-red border-b-2 border-rc-red bg-red-50/50' : 'text-slate-400',
              ]"
            >
              {{ label }}
            </div>
          </div>

          <!-- Step 0: phone entry -->
          <div v-if="currentStep === 0" class="p-6">
            <p class="text-sm text-slate-600 mb-5">
              Enter your Safaricom M-Pesa number below. You will receive a push notification to confirm payment.
            </p>
            <div class="mb-5">
              <label class="block text-xs font-semibold text-slate-600 mb-2">M-Pesa Phone Number</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3.5">
                  <span class="text-slate-400 text-sm font-medium">+254</span>
                </div>
                <input
                  v-model="phoneLocal"
                  type="tel"
                  placeholder="7xx xxx xxx"
                  maxlength="9"
                  class="w-full pl-14 pr-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-rc-red focus:border-transparent"
                  @keyup.enter="initiatePush"
                />
              </div>
              <p class="mt-1.5 text-xs text-slate-400">e.g. 722 345 678 (without leading 0)</p>
            </div>

            <button
              :disabled="submitting || !phoneLocal"
              class="w-full flex items-center justify-center gap-2 py-3 bg-rc-red text-white font-semibold text-sm rounded-lg hover:bg-rc-red-dark disabled:opacity-50 transition-colors shadow-sm"
              @click="initiatePush"
            >
              <span v-if="submitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/>
              {{ submitting ? 'Sending...' : 'Send M-Pesa Request' }}
            </button>
            <p v-if="payError" class="mt-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">{{ payError }}</p>
          </div>

          <!-- Step 1: waiting -->
          <div v-else-if="currentStep === 1" class="p-8 text-center">
            <div class="w-14 h-14 border-4 border-slate-200 border-t-rc-red rounded-full animate-spin mx-auto mb-5"/>
            <h2 class="text-base font-bold text-slate-900 mb-2">Check Your Phone</h2>
            <p class="text-sm text-slate-500 mb-1">
              An M-Pesa prompt has been sent to <strong class="text-slate-700">+254{{ phoneLocal }}</strong>.
            </p>
            <p class="text-sm text-slate-500 mb-6">Enter your M-Pesa PIN to complete payment.</p>
            <button @click="cancelPolling" class="text-sm text-slate-400 hover:text-slate-600 underline transition-colors">
              Cancel and try again
            </button>
          </div>

          <!-- Step 2: success -->
          <div v-else-if="currentStep === 2" class="p-8 text-center">
            <div class="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-7 h-7 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <h2 class="text-lg font-bold text-slate-900 mb-1">Payment Successful!</h2>
            <p class="text-sm text-slate-500 mb-1">M-Pesa Receipt: <span class="font-mono font-semibold text-slate-700">{{ mpesaReceipt }}</span></p>
            <p class="text-sm text-slate-500 mb-6">Your application is now active.</p>
            <router-link
              :to="`/exercises/${appDoc.exercise}/apply/${applicationId}`"
              class="inline-flex items-center gap-2 px-6 py-2.5 bg-rc-red text-white font-semibold text-sm rounded-lg hover:bg-rc-red-dark transition-colors shadow-sm"
            >
              Continue Application &rarr;
            </router-link>
          </div>

          <!-- Step -1: failed -->
          <div v-else-if="currentStep === -1" class="p-8 text-center">
            <div class="w-14 h-14 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-7 h-7 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </div>
            <h2 class="text-lg font-bold text-slate-900 mb-1">Payment Failed</h2>
            <p class="text-sm text-slate-500 mb-6">{{ failureReason }}</p>
            <button
              @click="resetForm"
              class="px-6 py-2.5 border-2 border-rc-navy text-rc-navy font-semibold text-sm rounded-lg hover:bg-rc-navy hover:text-white transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { frappeRequest } from 'frappe-ui'

const props = defineProps({ applicationId: String })

const appLoading = ref(true)
const appDoc = ref(null)
const phoneLocal = ref('')
const currentStep = ref(0)
const submitting = ref(false)
const payError = ref('')
const mpesaReceipt = ref('')
const failureReason = ref('')
const paymentName = ref('')
let pollTimer = null

onMounted(async () => {
  try {
    const res = await frappeRequest({
      url: '/api/method/frappe.client.get',
      params: { doctype: 'Prequal Application', name: props.applicationId },
    })
    appDoc.value = res.message
    if (appDoc.value?.payment_status === 'Paid') currentStep.value = 2
  } finally {
    appLoading.value = false
  }
})

async function initiatePush() {
  if (!phoneLocal.value) { payError.value = 'Please enter your M-Pesa phone number.'; return }
  submitting.value = true
  payError.value = ''
  try {
    const full = '254' + phoneLocal.value.replace(/^0/, '').replace(/\s/g, '')
    const res = await frappeRequest({
      url: '/api/method/onerc_procurement.api.payment.initiate_stk_push',
      params: { application: props.applicationId, phone_number: full },
    })
    paymentName.value = res.message?.payment_name
    currentStep.value = 1
    startPolling()
  } catch (e) {
    payError.value = e.message || 'Failed to send M-Pesa request. Please try again.'
  } finally {
    submitting.value = false
  }
}

function startPolling() {
  let attempts = 0
  pollTimer = setInterval(async () => {
    attempts++
    if (attempts > 24) {
      clearInterval(pollTimer)
      failureReason.value = 'Payment timed out after 2 minutes. Please try again.'
      currentStep.value = -1
      return
    }
    try {
      const res = await frappeRequest({
        url: '/api/method/onerc_procurement.api.payment.get_payment_status',
        params: { payment_name: paymentName.value },
      })
      if (res.message?.status === 'Completed') {
        clearInterval(pollTimer)
        mpesaReceipt.value = res.message.mpesa_receipt || ''
        currentStep.value = 2
      } else if (res.message?.status === 'Failed') {
        clearInterval(pollTimer)
        failureReason.value = res.message.failure_reason || 'Payment was declined by M-Pesa.'
        currentStep.value = -1
      }
    } catch (_) {}
  }, 5000)
}

function cancelPolling() {
  clearInterval(pollTimer)
  currentStep.value = 0
}
function resetForm() {
  currentStep.value = 0
  payError.value = ''
}
onUnmounted(() => clearInterval(pollTimer))

function formatAmount(n) {
  return Number(n).toLocaleString('en-KE')
}
</script>
