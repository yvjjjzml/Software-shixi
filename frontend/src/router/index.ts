import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '数据看板', icon: 'DataAnalysis' }
      },
      {
        path: 'notes',
        name: 'NoteList',
        component: () => import('../views/NoteList.vue'),
        meta: { title: '笔记管理', icon: 'Document' }
      },
      {
        path: 'notes/create',
        name: 'NoteCreate',
        component: () => import('../views/NoteEditor.vue'),
        meta: { title: '新建笔记', icon: 'EditPen' }
      },
      {
        path: 'notes/:id/edit',
        name: 'NoteEdit',
        component: () => import('../views/NoteEditor.vue'),
        meta: { title: '编辑笔记', icon: 'EditPen' }
      },
      {
        path: 'notes/:id',
        name: 'NoteDetail',
        component: () => import('../views/NoteDetail.vue'),
        meta: { title: '笔记详情', icon: 'View' }
      },
      {
        path: 'ai-chat',
        name: 'AiChat',
        component: () => import('../views/AiChat.vue'),
        meta: { title: 'AI问答', icon: 'ChatDotRound' }
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('../views/Search.vue'),
        meta: { title: '搜索检索', icon: 'Search' }
      },
      {
        path: 'admin',
        name: 'Admin',
        component: () => import('../views/Admin.vue'),
        meta: { title: '系统管理', icon: 'Setting', requiresAdmin: true }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/Profile.vue'),
        meta: { title: '个人中心', icon: 'User' }
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('../views/Tags.vue'),
        meta: { title: '标签管理', icon: 'Collection' }
      },
      {
        path: 'templates',
        name: 'Templates',
        component: () => import('../views/Templates.vue'),
        meta: { title: '笔记模板', icon: 'Files' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth !== false && !userStore.isLoggedIn) {
    next('/login')
    return
  }

  if (to.meta.requiresAdmin && userStore.user?.role !== 'admin') {
    next('/dashboard')
    return
  }

  next()
})

export default router
