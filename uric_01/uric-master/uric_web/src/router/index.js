import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [

    {
        path: '/',
        name: 'Login',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../components/Login.vue')
    },
    {
        path: '/uric',
        name: 'Base',
        component: () => import(/* webpackChunkName: "about" */ '../components/Base.vue'),
        children: [
            {
                path: 'workbench',  // 访问路径： 父级路由 + 当前路由
                name: 'ShowCenter',
                component: () => import(/* webpackChunkName: "about" */ '../components/ShowCenter.vue')
            },
            {
                path: 'host',
                name: 'Host',
                component: () => import(/* webpackChunkName: "about" */ '../components/Host.vue')
            },
            {
                path: 'console/:id',
                name: 'Console',
                component: () => import(/* webpackChunkName: "about" */ '../components/Console.vue')
            },
            {
                path: 'multi_exec',
                name: 'MultiExec',
                component: () => import(/* webpackChunkName: "about" */ '../components/MultiExec.vue')
            },
            {
                path: 'template_manage',
                name: 'TemplateManage',
                component: () => import(/* webpackChunkName: "about" */ '../components/TemplateManage.vue')
            },
            {
                path: 'environment',
                name: 'Environment',
                component: () => import(/* webpackChunkName: "about" */ '../components/Environment.vue')
            },
            {
                 path: 'release',
                 name: 'Release',
                 component: () => import(/* webpackChunkName: "about" */ '../components/Release.vue')
             }
        ]
    },

]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

// 路由守卫[导航守卫]
import axios from "axios"
import settings from "../settings.js"
router.beforeEach((to, from, next) => {
  if(to.name === 'Login'){
    next()
    return
  }
  let token = sessionStorage.token || localStorage.token;
  // 验证jwt token
  axios.post(`${settings.host}/users/refresh_jwt_token/`,{
    token, // token: token,
  }).then(response=>{
      // 保存返回的新token
      sessionStorage.token = response.data.token;
      next()
  }).catch(error=>{
      // alert("对不起，您尚未登录或登录已超时，请重新登录！")
      next("/")
  })

})
export default router
