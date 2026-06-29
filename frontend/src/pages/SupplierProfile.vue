<template>
  <div>
    <!-- Page header -->
    <div class="bg-rc-navy">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 py-8 flex items-end justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-white">Supplier Profile</h1>
          <p class="text-white/55 text-sm mt-1">Keep your company information up to date.</p>
        </div>
        <span
          v-if="profileDoc"
          :class="profileDoc.profile_status === 'Complete' ? 'bg-green-500/20 text-green-300 border-green-500/30' : 'bg-amber-500/20 text-amber-300 border-amber-500/30'"
          class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-current"/>
          Profile {{ profileDoc.profile_status }}
        </span>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-24 gap-4">
      <div class="w-8 h-8 border-2 border-rc-red border-t-transparent rounded-full animate-spin"/>
    </div>

    <!-- No profile yet -->
    <div v-else-if="!profileDoc" class="max-w-2xl mx-auto px-4 py-16 text-center">
      <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-7 h-7 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
        </svg>
      </div>
      <h3 class="text-base font-semibold text-slate-700 mb-1">No Profile Found</h3>
      <p class="text-sm text-slate-400 mb-6">Create your supplier profile to start applying for prequalification exercises.</p>
      <button
        :disabled="creating"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-rc-red text-white font-semibold text-sm rounded-lg hover:bg-rc-red-dark disabled:opacity-50 transition-colors shadow-sm"
        @click="createProfile"
      >
        <span v-if="creating" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/>
        Create Profile
      </button>
    </div>

    <!-- Profile form -->
    <form v-else @submit.prevent="saveProfile" class="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-5">

      <!-- Company Information -->
      <section class="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center gap-3">
          <div class="w-8 h-8 bg-rc-navy rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <h2 class="font-semibold text-rc-navy">Company Information</h2>
        </div>
        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div class="sm:col-span-2">
            <label class="field-label">Company / Organisation Name <span class="text-rc-red">*</span></label>
            <input v-model="form.company_name" type="text" required class="field-input" placeholder="e.g. Prestige Office Solutions Ltd" />
          </div>
          <div>
            <label class="field-label">Organisation Type</label>
            <select v-model="form.organisation_type" class="field-input">
              <option>Limited Company</option>
              <option>Sole Proprietorship</option>
              <option>Partnership</option>
              <option>NGO / CBO</option>
              <option>Government Agency</option>
            </select>
          </div>
          <div>
            <label class="field-label">Registration Number (CPR)</label>
            <input v-model="form.reg_number" type="text" class="field-input" placeholder="CPR/YYYY/XXXXXX" />
          </div>
          <div>
            <label class="field-label">KRA PIN Number</label>
            <input v-model="form.pin_number" type="text" class="field-input" placeholder="P05XXXXXXXX" />
          </div>
          <div>
            <label class="field-label">Website</label>
            <input v-model="form.website" type="url" class="field-input" placeholder="https://www.company.co.ke" />
          </div>
          <div>
            <label class="field-label">P.O. Box</label>
            <input v-model="form.po_box" type="text" class="field-input" placeholder="P.O. Box XXXXX-XXXXX" />
          </div>
          <div>
            <label class="field-label">Main Office Location</label>
            <input v-model="form.main_office_location" type="text" class="field-input" placeholder="e.g. Westlands, Nairobi" />
          </div>
          <div>
            <label class="field-label">Branch Offices</label>
            <input v-model="form.branch_offices" type="text" class="field-input" placeholder="e.g. Mombasa, Kisumu" />
          </div>
        </div>
      </section>

      <!-- Contact Person -->
      <section class="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center gap-3">
          <div class="w-8 h-8 bg-rc-navy rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <h2 class="font-semibold text-rc-navy">Contact Person</h2>
        </div>
        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label class="field-label">Full Name <span class="text-rc-red">*</span></label>
            <input v-model="form.contact_person_name" type="text" required class="field-input" />
          </div>
          <div>
            <label class="field-label">Position / Title</label>
            <input v-model="form.contact_person_position" type="text" class="field-input" placeholder="e.g. Managing Director" />
          </div>
          <div>
            <label class="field-label">Email Address <span class="text-rc-red">*</span></label>
            <input v-model="form.contact_email" type="email" required class="field-input" />
          </div>
          <div>
            <label class="field-label">Phone Number <span class="text-rc-red">*</span></label>
            <input v-model="form.contact_phone" type="tel" required class="field-input" placeholder="07XX XXX XXX" />
          </div>
          <div>
            <label class="field-label">Company Email</label>
            <input v-model="form.company_email" type="email" class="field-input" />
          </div>
          <div>
            <label class="field-label">Company Phone</label>
            <input v-model="form.company_phone" type="tel" class="field-input" placeholder="020 XXX XXXX" />
          </div>
        </div>
      </section>

      <!-- Banking Details -->
      <section class="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center gap-3">
          <div class="w-8 h-8 bg-rc-navy rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
            </svg>
          </div>
          <h2 class="font-semibold text-rc-navy">Banking Details</h2>
        </div>
        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label class="field-label">Bank Name</label>
            <input v-model="form.bank_name" type="text" class="field-input" placeholder="e.g. Equity Bank Kenya Ltd" />
          </div>
          <div>
            <label class="field-label">Branch</label>
            <input v-model="form.bank_branch" type="text" class="field-input" placeholder="e.g. Westlands Branch" />
          </div>
          <div>
            <label class="field-label">Account Name</label>
            <input v-model="form.account_name" type="text" class="field-input" />
          </div>
          <div>
            <label class="field-label">Account Number</label>
            <input v-model="form.account_number" type="text" class="field-input" />
          </div>
        </div>
      </section>

      <!-- Save bar -->
      <div class="flex items-center justify-between bg-white rounded-xl border border-slate-200 shadow-card px-5 py-4">
        <div>
          <p v-if="saveSuccess" class="text-sm text-green-700 font-medium flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
            </svg>
            Profile saved successfully.
          </p>
          <p v-else-if="saveError" class="text-sm text-red-600">{{ saveError }}</p>
          <p v-else class="text-xs text-slate-400">Changes are not automatically saved.</p>
        </div>
        <div class="flex items-center gap-2">
          <button type="button" @click="resetForm" class="px-4 py-2 text-sm font-medium text-slate-600 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors">
            Reset
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="flex items-center gap-2 px-5 py-2 bg-rc-red text-white text-sm font-semibold rounded-lg hover:bg-rc-red-dark disabled:opacity-50 transition-colors shadow-sm"
          >
            <span v-if="saving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/>
            {{ saving ? 'Saving...' : 'Save Profile' }}
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { frappeRequest } from 'frappe-ui'

const loading = ref(true)
const creating = ref(false)
const profileDoc = ref(null)
const form = ref({})
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)

onMounted(loadProfile)

async function loadProfile() {
  loading.value = true
  try {
    const res = await frappeRequest({
      url: '/api/method/onerc_procurement.api.portal.get_my_supplier_profile',
    })
    if (res.message) {
      profileDoc.value = res.message
      populateForm(res.message)
    }
  } finally {
    loading.value = false
  }
}

function populateForm(doc) {
  form.value = {
    company_name: doc.company_name || '',
    organisation_type: doc.organisation_type || 'Limited Company',
    reg_number: doc.reg_number || '',
    pin_number: doc.pin_number || '',
    main_office_location: doc.main_office_location || '',
    branch_offices: doc.branch_offices || '',
    website: doc.website || '',
    po_box: doc.po_box || '',
    contact_person_name: doc.contact_person_name || '',
    contact_person_position: doc.contact_person_position || '',
    contact_email: doc.contact_email || '',
    contact_phone: doc.contact_phone || '',
    company_email: doc.company_email || '',
    company_phone: doc.company_phone || '',
    bank_name: doc.bank_name || '',
    bank_branch: doc.bank_branch || '',
    account_name: doc.account_name || '',
    account_number: doc.account_number || '',
  }
}

function resetForm() {
  if (profileDoc.value) populateForm(profileDoc.value)
}

async function createProfile() {
  creating.value = true
  try {
    const res = await frappeRequest({
      url: '/api/method/onerc_procurement.api.portal.create_supplier_profile',
    })
    if (res.message?.name) {
      await loadProfile()
    }
  } finally {
    creating.value = false
  }
}

async function saveProfile() {
  saving.value = true
  saveError.value = ''
  saveSuccess.value = false
  try {
    await frappeRequest({
      url: '/api/method/onerc_procurement.api.portal.save_supplier_profile',
      params: {
        supplier_name: profileDoc.value.name,
        data: JSON.stringify(form.value),
      },
    })
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 4000)
    await loadProfile()
  } catch (e) {
    saveError.value = e.message || 'Failed to save profile.'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.field-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.375rem;
}
.field-input {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  padding: 0.625rem 0.875rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #0f172a;
  outline: none;
  transition: box-shadow 0.15s ease, border-color 0.15s ease;
}
.field-input::placeholder {
  color: #94a3b8;
}
.field-input:focus {
  box-shadow: 0 0 0 2px #ee2435;
  border-color: transparent;
}
</style>
