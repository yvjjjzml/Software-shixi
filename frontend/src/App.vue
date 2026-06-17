<template>
  <router-view />
</template>

<style>
/* 全局CSS变量 */
:root {
  /* 主色 — 青蓝 Teal */
  --primary: #14b8a6;
  --primary-light: #2dd4bf;
  --primary-dark: #0d9488;
  /* 功能色 — 柔和版 */
  --success: #34d399;
  --warning: #fbbf24;
  --danger: #f87171;
  /* 中性色 — 浅暖调 */
  --bg: #f0fdfa;
  --bg-card: #ffffff;
  --text-primary: #134e4a;
  --text-secondary: #5eead4;
  --text-muted: #99f6e4;
  --border: #ccfbf1;
  /* 字体 */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif;
  /* 圆角 */
  --radius-sm: 6px;
  --radius: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  background-color: var(--bg);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
}

/* 全局过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 美化滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Element Plus 主题覆盖 */
:root {
  --el-color-primary: #14b8a6;
  --el-color-primary-light-3: #2dd4bf;
  --el-color-primary-light-5: #5eead4;
  --el-color-primary-light-7: #99f6e4;
  --el-color-primary-light-8: #ccfbf1;
  --el-color-primary-light-9: #f0fdfa;
  --el-color-primary-dark-2: #0d9488;
  --el-color-success: #34d399;
  --el-color-warning: #fbbf24;
  --el-color-danger: #f87171;
  --el-border-radius-base: 8px;
  --el-font-family: var(--font-family);
}

/* 全局按钮样式 */
.el-button {
  border-radius: var(--radius) !important;
  font-weight: 500;
  transition: all 0.2s ease !important;
}

.el-button:hover {
  transform: translateY(-1px);
}

/* 全局卡片样式 */
.el-card {
  border-radius: var(--radius-lg) !important;
  border: none !important;
  box-shadow: var(--shadow) !important;
  transition: all 0.2s ease !important;
}

.el-card:hover {
  box-shadow: var(--shadow-md) !important;
}

/* 全局输入框样式 */
.el-input__wrapper {
  border-radius: var(--radius) !important;
}

.el-textarea__inner {
  border-radius: var(--radius) !important;
}

/* 全局标签样式 */
.el-tag {
  border-radius: 20px !important;
  font-weight: 500;
}
</style>
