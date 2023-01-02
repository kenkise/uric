import App from './App'
import router from './router'
import Vue from 'vue/dist/vue.esm.js'

import 'xterm/css/xterm.css'
import 'xterm/lib/xterm'

// 加载项目的业务配置文件
import settings from "./settings";
Vue.prototype.$settings = settings;  // prototype 原型链

// ajax
import axios from "axios"
axios.defaults.withCredentials = false; // 是否在ajax请求时允许携带cookie到服务端
axios.defaults.baseURL = settings.host;
axios.defaults.timeout = 30000;             // 请求超时的时间
Vue.prototype.$axios = axios;

Vue.config.productionTip = false

import 'ant-design-vue/dist/antd.css';
// import Antd from 'ant-design-vue';
import Antd from 'ant-design-vue';
Vue.use(Antd);


// echarts图标插件
import * as echarts from 'echarts';
Vue.prototype.$echarts = echarts;


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})



