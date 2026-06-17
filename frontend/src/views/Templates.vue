<template>
  <div class="templates-page">
    <div class="page-header">
      <h2>📝 笔记模板</h2>
      <p class="page-desc">选择一个模板快速创建笔记</p>
    </div>

    <div class="template-grid" v-loading="loading">
      <div
        v-for="tpl in templates"
        :key="tpl.id"
        class="template-card"
        @click="useTemplate(tpl)"
      >
        <div class="template-icon">{{ tpl.icon }}</div>
        <h3 class="template-name">{{ tpl.name }}</h3>
        <p class="template-desc">{{ getDesc(tpl.id) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { templateApi } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const templates = ref<any[]>([])
const loading = ref(false)

const descMap: Record<string, string> = {
  meeting: '记录会议议题、决议事项和后续行动',
  daily: '每日工作完成情况、问题和明日计划',
  study: '学习笔记模板，包含核心概念和思考总结',
  project: '项目方案模板，技术选型和实施计划',
  bug: 'Bug报告模板，复现步骤和解决方案',
  review: '读书笔记模板，核心观点和精彩摘录'
}

function getDesc(id: string): string {
  return descMap[id] || ''
}

async function loadTemplates() {
  loading.value = true
  try {
    const res: any = await templateApi.getList()
    if (res.code === 200) {
      templates.value = res.data
    }
  } finally {
    loading.value = false
  }
}

function useTemplate(tpl: any) {
  router.push({ path: '/notes/create', query: { template: tpl.id } })
}

onMounted(loadTemplates)
</script>

<style scoped>
.templates-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header h2 {
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.page-desc {
  color: var(--text-secondary);
  font-size: 14px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.template-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: all 0.25s ease;
  text-align: center;
  border: 2px solid transparent;
}

.template-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.template-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.template-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.template-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}
</style>
