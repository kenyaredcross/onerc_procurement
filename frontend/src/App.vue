<template>
  <div class="min-h-full flex flex-col bg-slate-50">
    <!-- Header -->
    <header class="bg-rc-navy shadow-sm sticky top-0 z-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="h-16 flex items-center justify-between gap-4">
          <!-- Logo + wordmark -->
          <router-link to="/exercises" class="flex items-center gap-3 shrink-0">
            <div class="w-8 h-8 bg-rc-red rounded-sm flex items-center justify-center shadow-sm">
              <svg viewBox="0 0 20 20" fill="white" class="w-5 h-5">
                <rect x="8" y="2" width="4" height="16" rx="1"/>
                <rect x="2" y="8" width="16" height="4" rx="1"/>
              </svg>
            </div>
            <div class="leading-tight hidden sm:block">
              <div class="text-white font-bold text-sm tracking-wide">Kenya Red Cross</div>
              <div class="text-white/60 text-xs">Supplier Portal</div>
            </div>
            <div class="text-white font-bold text-sm sm:hidden">KRCS Portal</div>
          </router-link>

          <!-- Nav -->
          <nav class="flex items-center gap-1">
            <router-link
              to="/exercises"
              class="px-3 py-2 rounded text-sm text-white/75 hover:text-white hover:bg-white/10 transition-colors"
              active-class="text-white bg-white/15"
            >
              Exercises
            </router-link>
            <router-link
              v-if="isLoggedIn"
              to="/applications"
              class="px-3 py-2 rounded text-sm text-white/75 hover:text-white hover:bg-white/10 transition-colors"
              active-class="text-white bg-white/15"
            >
              My Applications
            </router-link>
            <router-link
              v-if="isLoggedIn"
              to="/profile"
              class="px-3 py-2 rounded text-sm text-white/75 hover:text-white hover:bg-white/10 transition-colors"
              active-class="text-white bg-white/15"
            >
              Profile
            </router-link>

            <div class="w-px h-5 bg-white/20 mx-1"/>

            <a
              v-if="isLoggedIn"
              href="/api/method/logout"
              class="px-3 py-2 rounded text-sm text-white/60 hover:text-white hover:bg-white/10 transition-colors"
            >
              Logout
            </a>
            <a
              v-else
              href="/login?redirect-to=/prequal"
              class="px-4 py-2 rounded text-sm font-semibold bg-rc-red text-white hover:bg-rc-red-dark transition-colors shadow-sm"
            >
              Login
            </a>
          </nav>
        </div>
      </div>
    </header>

    <!-- Content -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-rc-navy mt-auto">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-6 h-6 bg-rc-red rounded-sm flex items-center justify-center">
            <svg viewBox="0 0 20 20" fill="white" class="w-3.5 h-3.5">
              <rect x="8" y="2" width="4" height="16" rx="1"/>
              <rect x="2" y="8" width="16" height="4" rx="1"/>
            </svg>
          </div>
          <span class="text-white/80 text-xs">Kenya Red Cross Society &mdash; Supplier Prequalification</span>
        </div>
        <span class="text-white/40 text-xs">© {{ new Date().getFullYear() }} KRCS. All rights reserved.</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
const isLoggedIn = !!(window.frappe?.session?.user && window.frappe.session.user !== 'Guest')
</script>
