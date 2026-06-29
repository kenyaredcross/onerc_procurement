import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

import {
  FrappeUI,
  Button,
  Input,
  TextInput,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  setConfig,
  frappeRequest,
  FeatherIcon,
} from 'frappe-ui'

let pinia = createPinia()
let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI)
app.use(pinia)
app.use(router)

app.component('Button', Button)
app.component('TextInput', TextInput)
app.component('Input', Input)
app.component('FormControl', FormControl)
app.component('ErrorMessage', ErrorMessage)
app.component('Dialog', Dialog)
app.component('Alert', Alert)
app.component('Badge', Badge)
app.component('FeatherIcon', FeatherIcon)

if (import.meta.env.DEV) {
  frappeRequest({
    url: '/api/method/onerc_procurement.www.prequal.get_context_for_dev',
  }).then((values) => {
    for (let key in values) {
      window[key] = values[key]
    }
    app.mount('#app')
  })
} else {
  app.mount('#app')
}
