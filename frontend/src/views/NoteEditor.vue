<template>
  <div class="note-editor-page">
    <div class="editor-card">
      <!-- 顶部表单区域 -->
      <div class="editor-header">
        <el-input
          v-model="form.title"
          placeholder="请输入笔记标题"
          class="title-input"
          size="large"
        />
        <div class="meta-row">
          <el-input v-model="form.category" placeholder="分类（如：技术、生活）" class="meta-input" />
          <el-input v-model="form.tags" placeholder="标签（逗号分隔）" class="meta-input" />
          <el-select v-model="form.status" class="meta-select">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </div>
      </div>

      <!-- 工具栏 -->
      <div class="editor-toolbar">
        <div class="toolbar-left">
          <el-button size="small" @click="togglePreview" :type="showPreview ? 'primary' : 'default'">
            <el-icon><View /></el-icon>
            {{ showPreview ? '关闭预览' : 'Markdown预览' }}
          </el-button>
          <el-button size="small" type="primary" plain @click="handleAISummary" :loading="aiLoading.summary">
            <el-icon><MagicStick /></el-icon>AI生成摘要
          </el-button>
          <el-button size="small" type="success" plain @click="handleAITag" :loading="aiLoading.tag">
            <el-icon><PriceTag /></el-icon>AI自动标签
          </el-button>
        </div>
      </div>

      <!-- 编辑区域 -->
      <div class="editor-body" :class="{ 'with-preview': showPreview }">
        <div class="editor-pane">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="20"
            placeholder="支持 Markdown 格式..."
            class="content-textarea"
          />
        </div>
        <div v-if="showPreview" class="preview-pane">
          <div class="preview-content" v-html="renderedContent"></div>
        </div>
      </div>

      <!-- AI摘要展示 -->
      <div v-if="form.summary" class="summary-section">
        <div class="summary-header">
          <el-icon><MagicStick /></el-icon>
          <span>AI摘要</span>
        </div>
        <div class="summary-content">{{ form.summary }}</div>
      </div>

      <!-- 底部操作栏 -->
      <div class="editor-footer">
        <el-button size="large" @click="$router.back()">取消</el-button>
        <el-button type="primary" size="large" @click="handleSave" :loading="saving">
          {{ isEdit ? '保存修改' : '创建笔记' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import { noteApi, aiApi, templateApi } from '../api'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const showPreview = ref(false)

const form = reactive({
  title: '',
  content: '',
  category: '',
  tags: '',
  status: 'draft',
  summary: ''
})

const aiLoading = reactive({ summary: false, tag: false })

const renderedContent = computed(() => {
  try {
    return marked(form.content || '')
  } catch {
    return form.content
  }
})

function togglePreview() {
  showPreview.value = !showPreview.value
}

async function loadNote() {
  if (!route.params.id) return
  const res: any = await noteApi.getDetail(Number(route.params.id))
  if (res.code === 200) {
    Object.assign(form, {
      title: res.data.title,
      content: res.data.content,
      category: res.data.category || '',
      tags: res.data.tags || '',
      status: res.data.status,
      summary: res.data.summary || ''
    })
  }
}

async function loadTemplate() {
  const templateId = route.query.template as string
  if (!templateId) return
  try {
    const res: any = await templateApi.getList()
    if (res.code === 200) {
      const tpl = res.data.find((t: any) => t.id === templateId)
      if (tpl) {
        form.content = tpl.content
        form.title = tpl.name
        ElMessage.success(`已加载模板：${tpl.name}`)
      }
    }
  } catch {
    ElMessage.error('加载模板失败')
  }
}

async function handleSave() {
  if (!form.title.trim() || !form.content.trim()) {
    ElMessage.warning('标题和内容不能为空')
    return
  }
  saving.value = true
  try {
    let res: any
    if (isEdit.value) {
      res = await noteApi.update(Number(route.params.id), form)
    } else {
      res = await noteApi.create(form)
    }
    if (res.code === 200) {
      ElMessage.success(isEdit.value ? '修改成功' : '创建成功')
      router.push('/notes')
    }
  } finally {
    saving.value = false
  }
}

async function handleAISummary() {
  if (!form.content.trim()) {
    ElMessage.warning('请先输入内容')
    return
  }
  aiLoading.summary = true
  try {
    const res: any = await aiApi.summarize({
      note_id: isEdit.value ? Number(route.params.id) : undefined,
      content: form.content
    })
    if (res.code === 200) {
      form.summary = res.data.summary
      ElMessage.success('摘要生成成功')
    }
  } finally {
    aiLoading.summary = false
  }
}

async function handleAITag() {
  if (!form.content.trim()) {
    ElMessage.warning('请先输入内容')
    return
  }
  aiLoading.tag = true
  try {
    const res: any = await aiApi.autoTag({
      note_id: isEdit.value ? Number(route.params.id) : undefined,
      content: form.title + '\n' + form.content
    })
    if (res.code === 200) {
      form.tags = res.data.tags
      ElMessage.success('标签生成成功')
    }
  } finally {
    aiLoading.tag = false
  }
}

onMounted(async () => {
  await loadNote()
  await loadTemplate()
})
</script>

<style scoped>
.note-editor-page {
  max-width: 1200px;
  margin: 0 auto;
}

.editor-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

/* 头部 */
.editor-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.title-input :deep(.el-input__wrapper) {
  font-size: 20px;
  font-weight: 600;
  box-shadow: none !important;
  padding: 8px 0;
}

.title-input :deep(.el-input__inner) {
  color: var(--text-primary);
}

.meta-row {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.meta-input {
  flex: 1;
}

.meta-select {
  width: 120px;
}

/* 工具栏 */
.editor-toolbar {
  padding: 12px 24px;
  border-bottom: 1px solid var(--border);
  background: #fafbfc;
}

.toolbar-left {
  display: flex;
  gap: 8px;
}

/* 编辑区域 */
.editor-body {
  display: flex;
  min-height: 500px;
}

.editor-pane {
  flex: 1;
  padding: 0;
}

.editor-pane :deep(.el-textarea__inner) {
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 20px 24px;
  font-size: 15px;
  line-height: 1.8;
  resize: none;
  font-family: var(--font-family);
}

.preview-pane {
  flex: 1;
  border-left: 1px solid var(--border);
  padding: 20px 24px;
  overflow-y: auto;
  max-height: 500px;
  background: #fafbfc;
}

.preview-content {
  line-height: 1.8;
  font-size: 15px;
  color: var(--text-primary);
}

.preview-content :deep(h1) { font-size: 24px; margin: 16px 0 12px; font-weight: 700; }
.preview-content :deep(h2) { font-size: 20px; margin: 14px 0 10px; font-weight: 600; }
.preview-content :deep(h3) { font-size: 17px; margin: 12px 0 8px; font-weight: 600; }
.preview-content :deep(p) { margin: 8px 0; }
.preview-content :deep(code) { background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 13px; color: var(--primary); }
.preview-content :deep(pre) { background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 12px 0; }
.preview-content :deep(pre code) { background: none; color: inherit; padding: 0; }
.preview-content :deep(blockquote) { border-left: 3px solid var(--primary); padding-left: 12px; color: var(--text-secondary); margin: 12px 0; }
.preview-content :deep(ul), .preview-content :deep(ol) { padding-left: 20px; margin: 8px 0; }
.preview-content :deep(li) { margin: 4px 0; }

/* AI摘要 */
.summary-section {
  margin: 0 24px 20px;
  background: #f0f9ff;
  border-radius: var(--radius);
  padding: 16px;
  border: 1px solid #bae6fd;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 8px;
}

.summary-content {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}

/* 底部操作栏 */
.editor-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: #fafbfc;
}
</style>
