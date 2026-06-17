import axios from 'axios'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
})

// 请求拦截器 - 自动添加token
api.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})

// 响应拦截器 - 统一错误处理
api.interceptors.response.use(
  response => {
    const { data } = response
    if (data.code === 401) {
      const userStore = useUserStore()
      userStore.logout()
      // 用 router 跳转而非 window.location.href，避免整页刷新重播螺旋动画
      window.location.hash = ''
      window.location.replace('/login')
      return Promise.reject(new Error('未授权'))
    }
    return data
  },
  error => {
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

// ========== 认证 ==========
export const authApi = {
  register: (data: { username: string; password: string; nickname?: string }) =>
    api.post('/auth/register', data),
  login: (data: { username: string; password: string }) =>
    api.post('/auth/login', data),
  getProfile: () => api.get('/auth/profile')
}

// ========== 笔记 ==========
export const noteApi = {
  getList: (params?: any) => api.get('/notes', { params }),
  getDetail: (id: number) => api.get(`/notes/${id}`),
  create: (data: any) => api.post('/notes', data),
  update: (id: number, data: any) => api.put(`/notes/${id}`, data),
  delete: (id: number) => api.delete(`/notes/${id}`),
  updateStatus: (id: number, status: string) => api.put(`/notes/${id}/status`, { status })
}

// ========== AI ==========
export const aiApi = {
  summarize: (data: { note_id?: number; content?: string }) =>
    api.post('/ai/summarize', data),
  autoTag: (data: { note_id?: number; content?: string }) =>
    api.post('/ai/auto-tag', data),
  ask: (data: { question: string }) => api.post('/ai/ask', data),
  recommend: (id: number) => api.get(`/ai/recommend/${id}`)
}

// ========== 数据看板 ==========
export const dashboardApi = {
  getStats: () => api.get('/dashboard/stats'),
  getWordcloud: () => api.get('/dashboard/wordcloud')
}

// ========== 搜索 ==========
export const searchApi = {
  search: (params: any) => api.get('/search', { params })
}

// ========== 管理 ==========
export const adminApi = {
  getUsers: () => api.get('/admin/users'),
  getNotes: (params?: any) => api.get('/admin/notes', { params }),
  deleteUser: (id: number) => api.delete(`/admin/users/${id}`)
}

// ========== 演示数据 ==========
export const demoApi = {
  initData: () => api.post('/demo/init')
}

// ========== 笔记导入导出 ==========
export const fileApi = {
  importNote: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/notes/import', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  exportNote: (id: number) => api.get(`/notes/${id}/export`, { responseType: 'blob' })
}

// ========== AI润色 ==========
export const aiPolishApi = {
  polish: (data: { content: string; style?: string }) => api.post('/ai/polish', data)
}

// ========== 模板 ==========
export const templateApi = {
  getList: () => api.get('/templates')
}

// ========== 标签 ==========
export const tagApi = {
  getList: () => api.get('/tags'),
  delete: (name: string) => api.delete(`/tags/${name}`)
}

// ========== 个人中心 ==========
export const profileApi = {
  update: (data: { nickname?: string; old_password?: string; new_password?: string }) => api.put('/auth/profile', data)
}

export default api
