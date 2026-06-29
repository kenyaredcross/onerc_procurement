import frappeUIPreset from 'frappe-ui/tailwind'

export default {
  presets: [frappeUIPreset],
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
    './node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
    './node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'rc-red': '#ee2435',
        'rc-red-dark': '#c41e2d',
        'rc-navy': '#011e41',
        'rc-navy-light': '#0a3060',
      },
      boxShadow: {
        card: '0 1px 3px 0 rgba(1,30,65,0.08), 0 1px 2px -1px rgba(1,30,65,0.05)',
        'card-hover': '0 4px 12px 0 rgba(1,30,65,0.12)',
      },
    },
  },
  plugins: [],
}
