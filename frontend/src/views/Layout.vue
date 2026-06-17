<template>
  <div class="layout">
    <!-- 左侧导航栏 — 浅色 -->
    <div class="sidebar">
      <div class="logo">
        <el-icon :size="26" color="#14b8a6"><Notebook /></el-icon>
        <span>知识工作台</span>
      </div>

      <el-menu :default-active="activeMenu" router background-color="transparent" text-color="#64748b"
        active-text-color="#0d9488" class="sidebar-menu">
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据看板</span>
        </el-menu-item>
        <el-menu-item index="/notes">
          <el-icon><Document /></el-icon>
          <span>笔记管理</span>
        </el-menu-item>
        <el-menu-item index="/notes/create">
          <el-icon><EditPen /></el-icon>
          <span>新建笔记</span>
        </el-menu-item>
        <el-menu-item index="/ai-chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>AI问答</span>
        </el-menu-item>
        <el-menu-item index="/search">
          <el-icon><Search /></el-icon>
          <span>搜索检索</span>
        </el-menu-item>

        <el-menu-item index="/templates">
          <el-icon><Files /></el-icon>
          <span>笔记模板</span>
        </el-menu-item>
        <el-menu-item index="/tags">
          <el-icon><Collection /></el-icon>
          <span>标签管理</span>
        </el-menu-item>

        <!-- 演示数据按钮 -->
        <div class="sidebar-demo">
          <el-button class="sidebar-demo-btn" :loading="demoLoading" @click="handleLoadDemo">
            <el-icon><MagicStick /></el-icon>
            <span>加载演示数据</span>
          </el-button>
        </div>

        <el-menu-item v-if="userStore.isAdmin" index="/admin">
          <el-icon><Setting /></el-icon>
          <span>系统管理</span>
        </el-menu-item>
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 右侧内容区 -->
    <div class="main-area">
      <!-- 顶部栏 -->
      <div class="topbar">
        <div class="page-title">{{ currentTitle }}</div>
        <div class="user-info">
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              <el-avatar :size="32" class="avatar-gradient">
                {{ userStore.user?.nickname?.charAt(0) || 'U' }}
              </el-avatar>
              <span class="username">{{ userStore.user?.nickname || userStore.user?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人信息
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 内容 — 带旋转淡入 -->
      <div class="content">
        <router-view v-slot="{ Component }">
          <transition name="page-rotate" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessageBox, ElMessage } from 'element-plus'
import { demoApi } from '../api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const demoLoading = ref(false)

async function handleLoadDemo() {
  demoLoading.value = true
  try {
    const res: any = await demoApi.initData()
    if (res.code === 200) {
      ElMessage.success('演示数据已加载')
      // 刷新当前页面数据
      router.replace('/dashboard').then(() => router.replace(route.path))
    } else {
      ElMessage.info(res.msg || '已有数据')
    }
  } catch {
    ElMessage.error('加载失败')
  } finally {
    demoLoading.value = false
  }
}

const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/notes/create') || path.includes('/edit')) return '/notes/create'
  if (path.startsWith('/notes/')) return '/notes'
  return path
})

const currentTitle = computed(() => {
  return (route.meta?.title as string) || 'AI智能知识管理工作台'
})

function handleCommand(cmd: string) {
  if (cmd === 'logout') {
    ElMessageBox.confirm('确定退出登录？', '提示', { type: 'warning' }).then(() => {
      userStore.logout()
      router.push('/login')
    }).catch(() => {})
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ===== 左侧导航 — 浅色 ===== */
.sidebar {
  width: 240px;
  background: #ffffff;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  box-shadow: 1px 0 4px rgba(0, 0, 0, 0.03);
}

.logo {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 10px;
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.sidebar-menu {
  flex: 1;
  border-right: none !important;
  padding: 8px 10px;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 42px;
  line-height: 42px;
  border-radius: 10px;
  margin-bottom: 4px;
  padding-left: 16px !important;
  transition: all 0.2s ease;
  font-size: 14px;
  color: #64748b !important;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: #f0fdfa !important;
  color: #334155 !important;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #eef2ff, #e0e7ff) !important;
  color: #0d9488 !important;
  font-weight: 600;
  position: relative;
}

.sidebar-menu :deep(.el-menu-item.is-active)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: #14b8a6;
  border-radius: 0 3px 3px 0;
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
  margin-right: 10px;
  font-size: 17px;
}

/* ===== 右侧内容区 ===== */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--bg);
}

.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #ffffff;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 14px;
}

.avatar-gradient {
  background: linear-gradient(135deg, #99f6e4, #14b8a6) !important;
  color: #fff;
  font-weight: 600;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* ===== 页面切换 — 旋转淡入 ===== */
.page-rotate-enter-active {
  animation: page-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.page-rotate-leave-active {
  animation: page-out 0.2s ease forwards;
}

@keyframes page-in {
  0% {
    opacity: 0;
    transform: perspective(600px) rotateY(-8deg) scale(0.96) translateX(20px);
  }
  100% {
    opacity: 1;
    transform: perspective(600px) rotateY(0deg) scale(1) translateX(0);
  }
}

@keyframes page-out {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(0.98);
  }
}

/* ===== 侧边栏演示按钮 ===== */
.sidebar-demo {
  padding: 12px 14px;
  margin: 4px 0;
}

.sidebar-demo-btn {
  width: 100%;
  height: 38px;
  border-radius: 10px !important;
  background: linear-gradient(135deg, #f0fdfa, #ccfbf1) !important;
  border: 1px dashed #99f6e4 !important;
  color: #0d9488 !important;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.25s ease !important;
}

.sidebar-demo-btn:hover {
  background: linear-gradient(135deg, #ccfbf1, #99f6e4) !important;
  border-color: #14b8a6 !important;
  transform: translateY(-1px);
}

.sidebar-demo-btn .el-icon {
  margin-right: 6px;
}
</style>
