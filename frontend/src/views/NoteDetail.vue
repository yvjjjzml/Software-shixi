<template>
  <div class="note-detail" v-loading="loading">
    <el-card shadow="never" v-if="note">
      <div class="detail-header">
        <div class="header-left">
          <h1>{{ note.title }}</h1>
          <div class="meta">
            <StatusBadge :status="note.status" />
            <span class="meta-item"><el-icon><Folder /></el-icon> {{ note.category || '未分类' }}</span>
            <span class="meta-item"><el-icon><View /></el-icon> {{ note.view_count }} 次浏览</span>
            <span class="meta-item"><el-icon><Clock /></el-icon> {{ formatDate(note.updated_at) }}</span>
          </div>
          <div class="tags" v-if="note.tags">
            <el-tag v-for="tag in parseTags(note.tags)" :key="tag" type="info" effect="plain">{{ tag }}</el-tag>
          </div>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="$router.push(`/notes/${note.id}/edit`)">
            <el-icon><EditPen /></el-icon>编辑
          </el-button>
          <el-button @click="handleExport">
            <el-icon><Download /></el-icon>导出
          </el-button>
          <el-button type="warning" @click="showPolishDialog = true">
            <el-icon><MagicStick /></el-icon>AI润色
          </el-button>
          <el-button @click="handleStatusChange">
            <el-icon><Refresh /></el-icon>切换状态
          </el-button>
        </div>
      </div>

      <!-- AI摘要 -->
      <el-alert v-if="note.summary" type="info" :closable="false" style="margin:16px 0">
        <template #title>
          <el-icon><MagicStick /></el-icon> AI摘要
        </template>
        {{ note.summary }}
      </el-alert>

      <!-- 内容 -->
      <div class="content-area">
        <div class="rendered-content" v-html="renderedContent"></div>
      </div>

      <!-- AI操作 -->
      <div class="ai-actions">
        <el-button type="primary" @click="handleAISummary" :loading="aiLoading.summary">
          <el-icon><MagicStick /></el-icon>AI生成摘要
        </el-button>
        <el-button type="success" @click="handleAITag" :loading="aiLoading.tag">
          <el-icon><PriceTag /></el-icon>AI自动标签
        </el-button>
        <el-button type="warning" @click="loadRecommendations" :loading="aiLoading.recommend">
          <el-icon><Connection /></el-icon>AI关联推荐
        </el-button>
      </div>

      <!-- AI润色对话框 -->
      <el-dialog v-model="showPolishDialog" title="AI润色" width="480px">
        <div class="polish-dialog">
          <p style="margin-bottom:12px;color:#606266;">选择润色风格：</p>
          <el-radio-group v-model="polishStyle" class="polish-styles">
            <el-radio-button value="professional">专业正式</el-radio-button>
            <el-radio-button value="academic">学术论文</el-radio-button>
            <el-radio-button value="simple">简洁通俗</el-radio-button>
            <el-radio-button value="creative">生动创意</el-radio-button>
          </el-radio-group>
        </div>
        <template #footer>
          <el-button @click="showPolishDialog = false">取消</el-button>
          <el-button type="primary" @click="handlePolish" :loading="aiLoading.polish">开始润色</el-button>
        </template>
      </el-dialog>

      <!-- 关联推荐 -->
      <div v-if="recommendations.length > 0" class="recommendations">
        <h3>📌 AI推荐的相关笔记</h3>
        <div class="rec-list">
          <el-card v-for="rec in recommendations" :key="rec.id" shadow="hover" class="rec-card"
            @click="$router.push(`/notes/${rec.id}`)">
            <h4>{{ rec.title }}</h4>
            <p>{{ rec.summary || '暂无摘要' }}</p>
            <div class="rec-tags">
              <el-tag v-for="tag in parseTags(rec.tags)" :key="tag" size="small" type="info">{{ tag }}</el-tag>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import { noteApi, aiApi, fileApi, aiPolishApi } from '../api'
import StatusBadge from '../components/StatusBadge.vue'

const route = useRoute()
const note = ref<any>(null)
const loading = ref(false)
const recommendations = ref<any[]>([])
const showPolishDialog = ref(false)
const polishStyle = ref('professional')
const aiLoading = reactive({ summary: false, tag: false, recommend: false, polish: false })

const renderedContent = computed(() => {
  try { return marked(note.value?.content || '') } catch { return note.value?.content || '' }
})

function parseTags(tags: string): string[] {
  return tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : []
}

function formatDate(d: string): string { return d ? d.slice(0, 16).replace('T', ' ') : '' }

async function loadNote() {
  loading.value = true
  try {
    const res: any = await noteApi.getDetail(Number(route.params.id))
    if (res.code === 200) note.value = res.data
  } finally { loading.value = false }
}

async function handleStatusChange() {
  const next: Record<string, string> = { draft: 'published', published: 'archived', archived: 'draft' }
  const newStatus = next[note.value.status] || 'draft'
  const res: any = await noteApi.updateStatus(note.value.id, newStatus)
  if (res.code === 200) {
    note.value.status = newStatus
    ElMessage.success('状态已更新')
  }
}

async function handleAISummary() {
  aiLoading.summary = true
  try {
    const res: any = await aiApi.summarize({ note_id: note.value.id })
    if (res.code === 200) {
      note.value.summary = res.data.summary
      ElMessage.success('摘要生成成功')
    }
  } finally { aiLoading.summary = false }
}

async function handleAITag() {
  aiLoading.tag = true
  try {
    const res: any = await aiApi.autoTag({ note_id: note.value.id })
    if (res.code === 200) {
      note.value.tags = res.data.tags
      ElMessage.success('标签生成成功')
    }
  } finally { aiLoading.tag = false }
}

async function loadRecommendations() {
  aiLoading.recommend = true
  try {
    const res: any = await aiApi.recommend(note.value.id)
    if (res.code === 200) recommendations.value = res.data.recommendations
  } finally { aiLoading.recommend = false }
}

async function handleExport() {
  try {
    const res: any = await fileApi.exportNote(note.value.id)
    const blob = new Blob([res], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${note.value.title}.md`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch {
    ElMessage.error('导出失败')
  }
}

async function handlePolish() {
  aiLoading.polish = true
  try {
    const res: any = await aiPolishApi.polish({
      content: note.value.content,
      style: polishStyle.value
    })
    if (res.code === 200) {
      note.value.content = res.data.polished
      showPolishDialog.value = false
      ElMessage.success('润色完成')
    }
  } finally {
    aiLoading.polish = false
  }
}

onMounted(loadNote)
</script>

<script lang="ts">
import { reactive } from 'vue'
</script>

<style scoped>
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.header-left h1 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 12px;
}

.meta {
  display: flex;
  gap: 16px;
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.header-right {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.content-area {
  padding: 20px;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin: 16px 0;
}

.rendered-content {
  line-height: 1.8;
  font-size: 15px;
  color: #303133;
}

.rendered-content :deep(h1) { font-size: 24px; margin: 16px 0 12px; }
.rendered-content :deep(h2) { font-size: 20px; margin: 14px 0 10px; }
.rendered-content :deep(h3) { font-size: 17px; margin: 12px 0 8px; }
.rendered-content :deep(p) { margin: 8px 0; }
.rendered-content :deep(code) { background: #f5f7fa; padding: 2px 6px; border-radius: 3px; }
.rendered-content :deep(pre) { background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 6px; overflow-x: auto; }
.rendered-content :deep(blockquote) { border-left: 4px solid #409EFF; padding-left: 12px; color: #606266; margin: 12px 0; }

.ai-actions {
  display: flex;
  gap: 12px;
  margin: 20px 0;
}

.recommendations {
  margin-top: 24px;
}

.recommendations h3 {
  margin-bottom: 12px;
  color: #303133;
}

.rec-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.rec-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.rec-card:hover { transform: translateY(-2px); }

.rec-card h4 {
  font-size: 15px;
  color: #303133;
  margin-bottom: 6px;
}

.rec-card p {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.rec-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
</style>
