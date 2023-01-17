import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'layout',
        component: () => import('@/views/LayoutView'),
        children: [
            {
                path: "/",
                redirect: "task"
            },
            {
                path: 'task',
                name: 'task',
                component: () => import('@/views/task/TaskView'),
                children: [
                    {
                        path: "/",
                        redirect: "activity"
                    },
                    {
                        path: 'activity',
                        name: 'activity',
                        component: () => import('@/views/task/activity/ActivityView'),
                        children: [
                            {
                                path: "/",
                                redirect: "list"
                            }, {
                                path: 'list',
                                name: 'list',
                                component: () => import('@/views/task/activity/ListView'),
                            }, {
                                path: 'create',
                                name: 'create',
                                component: () => import('@/views/task/activity/CreateView'),
                            }
                        ],
                    }, {
                        path: 'fans',
                        name: 'fans',
                        component: () => import('@/views/task/FansView'),
                    }, {
                        path: 'promo',
                        name: 'promo',
                        component: () => import('@/views/task/PromoView'),
                    }, {
                        path: 'statistics',
                        name: 'statistics',
                        component: () => import('@/views/task/StatisticsView'),
                    },
                ]
            }, {
                path: 'msg',
                name: 'msg',
                component: () => import('@/views/msg/MsgView'),
                children: [
                    {
                        path: "/",
                        redirect: "push"
                    },
                    {
                        path: 'push',
                        name: 'push',
                        component: () => import('@/views/msg/PushView'),
                    }, {
                        path: 'sop',
                        name: 'sop',
                        component: () => import('@/views/msg/SopView'),
                    },
                ]
            },
            {
                path: 'auth',
                name: 'auth',
                component: () => import('@/views/auth/AuthView'),
            },
        ]
    },
    {
        path: '/about',
        name: 'about',
        component: () => import('@/views/AboutView.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/LoginView')
    },

]

const router = new VueRouter({
    mode: 'history',
    routes,
})

export default router
