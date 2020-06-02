import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/register',
    component: () => import('@/views/register/index'),
    hidden: true
  },
  //@password
  {
    path: '/retrievePassword',
    component: () => import('@/views/retrievePassword/index'),
    hidden: true
  },
  {
    path: '/successRedirect',
    component: () => import('@/views/SuccessRedirect/index')
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  
  

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '我的主页', icon: 'dashboard' }
    }]
  },
  
  {
      path: '/Calendar',
      component: Layout,
      children: [
        {
          path: 'index',
          name: 'Calendar',
          component: () => import('@/views/Calendar/index'),
          meta: { title: '我的日历', icon: 'calendar' }
        }
      ]
    },
    {
      path: '/Eventlist',
      component: Layout,
      children: [
        {
          path: 'index',
          name: 'Eventlist',
          component: () => import('@/views/Eventlist/index'),
          meta: { title: '我的DDL', icon: 'list' }
        }
      ]
    },
  {
      path: '/Course',
      component: Layout,
      children: [
        {
          path: 'index',
          name: 'Course',
          component: () => import('@/views/Course/index'),
          meta: { title: '我的课程', icon: 'course' }
        }
      ]
    },
  
  {
      path: '/Message',
      component: Layout,
      children: [
        {
          path: 'index',
          name: 'Message',
          component: () => import('@/views/Message/index'),
          meta: { title: '消息中心', icon: 'message' }
        }
      ]
    },
  
  {
      path: '/Userinfo',
      component: Layout,
      children: [
        {
          path: 'index',
          name: 'Userinfo',
          component: () => import('@/views/Userinfo/index'),
          meta: { title: '个人中心', icon: 'settings' }
        }
      ]
    },

    {
      path: '/Feedback',
      component: Layout,
      children: [
        {
          path: 'index',
          name: 'Feedback',
          component: () => import('@/views/Feedback/index'),
          meta: { title: '用户反馈', icon: 'link' }
        }
      ]
    },

    {
      path: '/About',
      component: Layout,
      children: [
        {
          path: 'index',
          name: 'About',
          component: () => import('@/views/About/index'),
          meta: { title: '关于我们', icon: 'eye' }
        }
      ]
    },


  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
