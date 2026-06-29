<template>
  <div>
    <!-- Subnav -->
    <div class="bg-white border-b border-slate-200">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
        <router-link to="/applications" class="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-rc-navy transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          My Applications
        </router-link>
        <span class="text-xs font-mono text-slate-400">{{ applicationId }}</span>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="initialLoading" class="flex flex-col items-center justify-center py-24 gap-4">
      <div class="w-8 h-8 border-2 border-rc-red border-t-transparent rounded-full animate-spin"/>
      <p class="text-sm text-slate-500">Loading application...</p>
    </div>

    <div v-else-if="!appDoc" class="max-w-2xl mx-auto px-4 py-16 text-center">
      <p class="text-red-600 text-sm">Application not found.</p>
    </div>

    <div v-else class="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <!-- Application header -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-card p-5 mb-6">
        <div class="flex items-start justify-between flex-wrap gap-3">
          <div>
            <h1 class="font-bold text-rc-navy text-lg">{{ appDoc.exercise }}</h1>
            <p class="text-slate-500 text-sm mt-0.5">{{ appDoc.category }}</p>
          </div>
          <span :class="statusClass(appDoc.status)" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border">
            {{ appDoc.status }}
          </span>
        </div>

        <!-- Notices -->
        <div v-if="appDoc.payment_status !== 'Paid'" class="mt-4 p-3.5 bg-amber-50 border border-amber-200 rounded-lg flex items-center justify-between gap-3">
          <div class="flex items-center gap-2.5">
            <svg class="w-4 h-4 text-amber-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <p class="text-sm text-amber-800">Payment is required before you can fill in and submit this application.</p>
          </div>
          <router-link :to="`/applications/${applicationId}/pay`" class="shrink-0 px-3 py-1.5 bg-amber-600 text-white text-xs font-semibold rounded-lg hover:bg-amber-700 transition-colors">
            Pay Now
          </router-link>
        </div>

        <div v-if="appDoc.edit_locked" class="mt-4 p-3.5 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2.5">
          <svg class="w-4 h-4 text-green-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
          </svg>
          <p class="text-sm text-green-800 font-medium">Application submitted — view only.</p>
        </div>
      </div>

      <div v-if="sections.length" class="flex gap-6">
        <!-- Sidebar navigation -->
        <div class="w-52 shrink-0 hidden md:block">
          <div class="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden sticky top-24">
            <div class="px-3 py-2.5 border-b border-slate-100">
              <p class="text-xs font-semibold text-slate-400 uppercase tracking-widest">Sections</p>
            </div>
            <nav class="p-2">
              <button
                v-for="(sec, idx) in sections"
                :key="sec.name"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center gap-2.5',
                  currentSectionIdx === idx
                    ? 'bg-rc-red text-white font-medium'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900',
                ]"
                @click="navigateToSection(idx)"
              >
                <span
                  :class="[
                    'w-5 h-5 rounded-full flex items-center justify-center text-xs shrink-0',
                    currentSectionIdx === idx ? 'bg-white/25 text-white' : 'bg-slate-100 text-slate-500',
                  ]"
                >{{ idx + 1 }}</span>
                <span class="truncate">{{ sec.section_name }}</span>
              </button>
            </nav>
          </div>
        </div>

        <!-- Main content -->
        <div class="flex-1 min-w-0">
          <!-- Mobile section tabs -->
          <div class="md:hidden flex gap-1.5 overflow-x-auto pb-2 mb-4 scrollbar-hide">
            <button
              v-for="(sec, idx) in sections"
              :key="sec.name"
              :class="[
                'px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap shrink-0 transition-colors',
                currentSectionIdx === idx ? 'bg-rc-red text-white' : 'bg-white border border-slate-200 text-slate-600',
              ]"
              @click="navigateToSection(idx)"
            >
              {{ idx + 1 }}. {{ sec.section_name }}
            </button>
          </div>

          <!-- Questions card -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-card">
            <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
              <h2 class="font-semibold text-rc-navy">{{ currentSection?.section_name }}</h2>
              <span class="text-xs text-slate-400">{{ currentSectionIdx + 1 }} of {{ sections.length }}</span>
            </div>

            <div v-if="loadingQuestions" class="flex items-center justify-center py-16">
              <div class="w-6 h-6 border-2 border-rc-red border-t-transparent rounded-full animate-spin"/>
            </div>

            <div v-else class="p-6 space-y-7">
              <div v-for="q in currentQuestions" :key="q.name">
                <label class="block text-sm font-semibold text-slate-800 mb-1.5">
                  {{ q.question_text }}
                  <span v-if="q.is_mandatory" class="text-rc-red ml-0.5">*</span>
                </label>
                <p v-if="q.help_text" class="text-xs text-slate-400 mb-2.5">{{ q.help_text }}</p>

                <!-- Text -->
                <input
                  v-if="['Text', 'Email', 'Phone', 'URL'].includes(q.question_type)"
                  v-model="responses[q.name]"
                  :type="q.question_type === 'Email' ? 'email' : q.question_type === 'URL' ? 'url' : 'text'"
                  :disabled="isLocked"
                  class="input-field"
                />

                <!-- Long text -->
                <textarea
                  v-else-if="q.question_type === 'Long Text'"
                  v-model="responses[q.name]"
                  rows="4"
                  :disabled="isLocked"
                  class="input-field resize-none"
                />

                <!-- Number / Currency -->
                <input
                  v-else-if="['Number', 'Currency', 'Percentage'].includes(q.question_type)"
                  v-model="responses[q.name]"
                  type="number"
                  :disabled="isLocked"
                  class="input-field"
                />

                <!-- Date -->
                <input
                  v-else-if="q.question_type === 'Date'"
                  v-model="responses[q.name]"
                  type="date"
                  :disabled="isLocked"
                  class="input-field"
                />

                <!-- Yes/No -->
                <div v-else-if="q.question_type === 'Yes/No'" class="flex gap-4">
                  <label
                    v-for="opt in ['Yes', 'No']"
                    :key="opt"
                    :class="[
                      'flex items-center gap-2 px-4 py-2.5 rounded-lg border-2 cursor-pointer transition-all text-sm font-medium',
                      responses[q.name] === opt
                        ? opt === 'Yes' ? 'border-green-500 bg-green-50 text-green-700' : 'border-red-400 bg-red-50 text-red-700'
                        : 'border-slate-200 text-slate-600 hover:border-slate-300',
                      isLocked && 'pointer-events-none opacity-70',
                    ]"
                  >
                    <input type="radio" :value="opt" v-model="responses[q.name]" :disabled="isLocked" class="sr-only" />
                    <span :class="['w-4 h-4 rounded-full border-2', responses[q.name] === opt ? (opt === 'Yes' ? 'border-green-500 bg-green-500' : 'border-red-400 bg-red-400') : 'border-slate-300']"/>
                    {{ opt }}
                  </label>
                </div>

                <!-- Select -->
                <select
                  v-else-if="q.question_type === 'Select'"
                  v-model="responses[q.name]"
                  :disabled="isLocked"
                  class="input-field"
                >
                  <option value="">-- Select an option --</option>
                  <option v-for="opt in optionsList(q.options)" :key="opt" :value="opt">{{ opt }}</option>
                </select>

                <!-- File upload -->
                <div v-else-if="q.question_type === 'File Upload'">
                  <div v-if="responses[q.name]" class="flex items-center gap-3 p-3 bg-green-50 border border-green-200 rounded-lg mb-2">
                    <svg class="w-4 h-4 text-green-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <span class="text-xs text-green-700 truncate">{{ fileNames[q.name] || 'File uploaded' }}</span>
                  </div>
                  <label v-if="!isLocked" class="flex flex-col items-center gap-2 px-4 py-6 border-2 border-dashed border-slate-300 rounded-lg cursor-pointer hover:border-rc-red hover:bg-red-50/30 transition-colors group">
                    <svg class="w-6 h-6 text-slate-400 group-hover:text-rc-red transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"/>
                    </svg>
                    <span class="text-xs text-slate-500 group-hover:text-rc-red">
                      {{ fileUploading[q.name] ? 'Uploading...' : 'Click to upload or drag & drop' }}
                    </span>
                    <input type="file" class="hidden" :disabled="isLocked || fileUploading[q.name]" @change="(e) => handleFileUpload(q.name, e)" />
                  </label>
                </div>

                <!-- Checkbox -->
                <div v-else-if="q.question_type === 'Checkbox'">
                  <label class="flex items-center gap-2.5 cursor-pointer">
                    <input
                      type="checkbox"
                      :checked="responses[q.name] === '1' || responses[q.name] === true"
                      :disabled="isLocked"
                      class="w-4 h-4 rounded border-slate-300 text-rc-red focus:ring-rc-red"
                      @change="(e) => responses[q.name] = e.target.checked ? '1' : '0'"
                    />
                    <span class="text-sm text-slate-700">Yes, I confirm</span>
                  </label>
                </div>

                <!-- Fallback text -->
                <input
                  v-else
                  v-model="responses[q.name]"
                  type="text"
                  :disabled="isLocked"
                  class="input-field"
                />
              </div>
            </div>

            <!-- Footer actions -->
            <div class="px-6 py-4 border-t border-slate-100 flex items-center justify-between gap-3">
              <button
                v-if="currentSectionIdx > 0"
                class="flex items-center gap-1.5 px-4 py-2 border border-slate-200 text-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 transition-colors"
                @click="saveAndNavigate(currentSectionIdx - 1)"
              >
                &larr; Previous
              </button>
              <div v-else/>

              <div class="flex items-center gap-2">
                <span v-if="saveSuccess" class="text-xs text-green-600 font-medium flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                  </svg>
                  Saved
                </span>

                <button
                  v-if="!isLocked && appDoc.payment_status === 'Paid' && currentSectionIdx < sections.length - 1"
                  :disabled="saving"
                  class="flex items-center gap-1.5 px-4 py-2 bg-rc-navy text-white text-sm font-medium rounded-lg hover:bg-rc-navy-light disabled:opacity-50 transition-colors"
                  @click="saveAndNavigate(currentSectionIdx + 1)"
                >
                  <span v-if="saving" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"/>
                  Save &amp; Next &rarr;
                </button>

                <button
                  v-else-if="!isLocked && appDoc.payment_status === 'Paid' && currentSectionIdx === sections.length - 1"
                  :disabled="submitting"
                  class="flex items-center gap-1.5 px-5 py-2 bg-rc-red text-white text-sm font-semibold rounded-lg hover:bg-rc-red-dark disabled:opacity-50 transition-colors shadow-sm"
                  @click="submitApplication"
                >
                  <span v-if="submitting" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"/>
                  {{ submitting ? 'Submitting...' : 'Submit Application' }}
                </button>

                <button
                  v-else-if="currentSectionIdx < sections.length - 1"
                  class="flex items-center gap-1.5 px-4 py-2 border border-slate-200 text-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 transition-colors"
                  @click="currentSectionIdx++"
                >
                  Next &rarr;
                </button>
              </div>
            </div>
          </div>

          <p v-if="saveError" class="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{{ saveError }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { frappeRequest } from 'frappe-ui'
import { useRouter } from 'vue-router'

const props = defineProps({ exerciseId: String, applicationId: String })
const router = useRouter()

const initialLoading = ref(true)
const appDoc = ref(null)
const sections = ref([])
const currentSectionIdx = ref(0)
const currentQuestions = ref([])
const responses = ref({})
const fileNames = ref({})
const fileUploading = ref({})
const loadingQuestions = ref(false)
const saving = ref(false)
const submitting = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)

const currentSection = computed(() => sections.value[currentSectionIdx.value])
const isLocked = computed(() => appDoc.value?.an || appDoc.value?.payment_status !== 'Paid')

onMounted(async () => {
  try {
    const [appRes, secRes] = await Promise.all([
      frappeRequest({ url: '/api/method/frappe.client.get', params: { doctype: 'Prequal Application', name: props.applicationId } }),
      frappeRequest({
        url: '/api/method/frappe.client.get_list',
        params: {
          doctype: 'Question Section',
          fields: JSON.stringify(['name', 'section_name', 'sort_order']),
          order_by: 'sort_order asc',
          limit_page_length: 50,
        },
      }),
    ])
    appDoc.value = appRes.message
    sections.value = secRes.message || []
    if (sections.value.length) {
      await loadSectionQuestions(sections.value[0].name)
    }
  } finally {
    initialLoading.value = false
  }
})

async function loadSectionQuestions(sectionName) {
  loadingQuestions.value = true
  try {
    const res = await frappeRequest({
      url: '/api/method/onerc_procurement.api.portal.get_section_questions',
      params: { section: sectionName, application: props.applicationId },
    })
    currentQuestions.value = res.message?.questions || []
    const existing = res.message?.responses || {}
    for (const qname in existing) {
      if (responses.value[qname] === undefined) {
        responses.value[qname] = existing[qname]
      }
    }
  } finally {
    loadingQuestions.value = false
  }
}

async function navigateToSection(idx) {
  if (idx === currentSectionIdx.value) return
  if (!isLocked.value && appDoc.value?.payment_status === 'Paid') {
    await doSave()
  }
  currentSectionIdx.value = idx
  await loadSectionQuestions(sections.value[idx].name)
}

async function saveAndNavigate(idx) {
  await doSave()
  if (!saveError.value) {
    currentSectionIdx.value = idx
    await loadSectionQuestions(sections.value[idx].name)
  }
}

async function doSave() {
  if (isLocked.value) return
  saving.value = true
  saveError.value = ''
  saveSuccess.value = false
  try {
    await frappeRequest({
      url: '/api/method/onerc_procurement.api.portal.save_responses',
      params: {
        application: props.applicationId,
        section: currentSection.value.name,
        responses: JSON.stringify(responses.value),
      },
    })
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 3000)
  } catch (e) {
    saveError.value = e.message || 'Failed to save. Please try again.'
  } finally {
    saving.value = false
  }
}

async function handleFileUpload(questionName, event) {
  const file = event.target.files[0]
  if (!file) return
  fileUploading.value[questionName] = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('is_private', 1)
    formData.append('doctype', 'Prequal Application')
    formData.append('docname', props.applicationId)
    const res = await fetch('/api/method/upload_file', {
      method: 'POST',
      headers: { 'X-Frappe-CSRF-Token': window.csrf_token },
      body: formData,
    })
    const data = await res.json()
    if (data.message?.file_url) {
      responses.value[questionName] = data.message.file_url
      fileNames.value[questionName] = file.name
    }
  } catch (e) {
    saveError.value = 'File upload failed.'
  } finally {
    fileUploading.value[questionName] = false
  }
}

async function submitApplication() {
  submitting.value = true
  saveError.value = ''
  try {
    await doSave()
    await frappeRequest({
      url: '/api/method/onerc_procurement.api.portal.submit_application',
      params: { application: props.applicationId },
    })
    router.push('/applications')
  } catch (e) {
    saveError.value = e.message || 'Submission failed. Please try again.'
  } finally {
    submitting.value = false
  }
}

function optionsList(opts) {
  return (opts || '').split('\n').map((s) => s.trim()).filter(Boolean)
}

function statusClass(status) {
  if (status === 'Prequalified') return 'bg-green-50 text-green-700 border-green-200'
  if (status === 'Submitted') return 'bg-blue-50 text-blue-700 border-blue-200'
  if (status === 'Active') return 'bg-indigo-50 text-indigo-700 border-indigo-200'
  if (status === 'Not Prequalified') return 'bg-red-50 text-red-700 border-red-200'
  return 'bg-slate-100 text-slate-500 border-slate-200'
}
</script>

<style scoped>
.input-field {
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
.input-field:focus {
  box-shadow: 0 0 0 2px #ee2435;
  border-color: transparent;
}
.input-field:disabled {
  background-color: #f8fafc;
  color: #94a3b8;
  cursor: not-allowed;
}
</style>
