import Vue from 'vue/dist/vue.esm.js'

import Router from 'vue-router'
import Console from '@/components/Console'
import MultiExec from '@/components/MultiExec'
import TemplateManage from '@/components/TemplateManage'
import Environment from '@/components/Environment'
import Release from '@/components/Release'

Vue.use(Router)
import Base from "../components/Base";
import Login from "../components/Login";
import ShowCenter from "../components/ShowCenter";
import Host from '@/components/Host';
import ReleaseApply from '@/components/ReleaseApply'
import ReleaseResult from '@/components/ReleaseResult'

const router = new Router({
    // mode: "history",
    mode: "hash",
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login,
        },
        {
            path: '/uric',
            name: 'Base',
            component: Base,
            children: [
                {
                    path: '',  // 访问路径： 父级路由 + 当前路由
                    name: 'ShowCenter',
                    component: ShowCenter,
                },
                {
                    path: '/workbench',  // 访问路径： 父级路由 + 当前路由
                    name: 'ShowCenter',
                    component: ShowCenter,
                },
                {
                    path: 'host',
                    name: 'Host',
                    component: Host,
                },
                {
                    path: 'console/:id',
                    name: 'Console',
                    component: Console,
                },
                {
                    path: 'multi_exec',
                    name: 'MultiExec',
                    component: MultiExec,
                },
                {
                    path: 'template_manage',
                    name: 'TemplateManage',
                    component: TemplateManage,
                },
                {
                    path: 'environment',
                    name: 'Environment',
                    component: Environment,
                },
                {
                    path: 'release',
                    name: 'Release',
                    component: Release,
                },
                {
                    path: 'Release_apply',
                    name: 'ReleaseApply',
                    component: ReleaseApply,
                },
                {
                    path: 'release_result/:id',
                    name: 'ReleaseResult',
                    component: ReleaseResult,
                },
            ]
        },

    ]
})


// 路由守卫[导航守卫]
import axios from "axios"
import settings from "../settings.js"

router.beforeEach((to, from, next) => {
    if (to.name === 'Login') {
        next()
        return
    }
    let token = sessionStorage.token || localStorage.token;
    // 验证jwt token
    axios.post(`${settings.host}/users/refresh_jwt_token/`, {
        token, // token: token,
    }).then(response => {
        // 保存返回的新token
        sessionStorage.token = response.data.token;
        next()
    }).catch(error => {
        alert("对不起，您尚未登录或登录已超时，请重新登录！")
        next("/")
    })

})

export default router