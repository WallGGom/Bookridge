import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false
Vue.use(VueCookies)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
