import {createApp} from 'vue'
import App from './App.vue'
import Vue from 'vue'

createApp(App).mount('#app')


// 配置全局样式
import '@/assets/css/global.css'

// 配置全局自定义设置
import settings from '@/assets/js/settings'

Vue.prototype.$settings = settings;
// 在所有需要与后台交互的组件中：this.$settings.base_url + '再拼接具体后台路由'



