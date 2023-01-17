import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/element.js'
import HighchartsVue from 'highcharts-vue'

Vue.use(HighchartsVue)

Vue.config.productionTip = false

import settings from "@/assets/js/settings";
import "@/assets/css/global.css";

Vue.prototype.$settings = settings;

new Vue({
    router,
    store,
    render: h => h(App),
    settings
}).$mount('#app')
