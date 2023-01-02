import Vue from 'vue'
import App from './App.vue'
import router from './router'

import settings from "./settings";
Vue.prototype.$settings = settings;  // prototype 原型链

// ajax
import axios from "axios"
axios.defaults.withCredentials = false; // 是否在ajax请求时允许携带cookie到服务端
axios.defaults.baseURL = settings.host;
axios.defaults.timeout = 30000;
Vue.prototype.$axios = axios;
// 引入 ant-design-vue;

// import Antd from 'ant-design-vue';
import Antd from 'ant-design-vue';
Vue.use(Antd);
import 'ant-design-vue/dist/antd.css';

// 引入 echarts
import * as echarts from 'echarts';
Vue.prototype.$echarts = echarts;
//引入xterm
import 'xterm/css/xterm.css'
import 'xterm/lib/xterm'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
