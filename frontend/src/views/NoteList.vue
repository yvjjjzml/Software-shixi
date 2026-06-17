<template>
  <div class="note-list-page">
    <!-- 搜索筛选栏 -->
    <div class="filter-card">
      <div class="filter-row">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索笔记标题/内容"
          clearable
          prefix-icon="Search"
          class="search-input"
          @keyup.enter="loadNotes"
          @clear="loadNotes"
        />
        <el-select v-model="filters.status" placeholder="状态" clearable @change="loadNotes" class="filter-select">
          <el-option label="草稿" value="draft" />
          <el-option label="已发布" value="published" />
          <el-option label="已归档" value="archived" />
        </el-select>
        <el-input v-model="filters.category" placeholder="分类" clearable @change="loadNotes" class="filter-input" />
        <el-input v-model="filters.tags" placeholder="标签" clearable @change="loadNotes" class="filter-input" />
        <el-button type="primary" @click="loadNotes" :icon="Search">搜索</el-button>
        <el-upload
          :show-file-list="false"
          accept=".txt,.md"
          :before-upload="handleImport"
        >
          <el-button type="success" plain :icon="Upload">导入笔记</el-button>
        </el-upload>
        <el-button type="primary" plain @click="$router.push('/notes/create')" :icon="Plus">新建笔记</el-button>
      </div>
    </div>

    <!-- 笔记卡片列表 -->
    <div class="note-grid" v-loading="loading">
      <el-empty v-if="!loading && notes.length === 0" description="暂无笔记，快去创建吧！" />

      <div v-for="note in notes" :key="note.id" class="note-card" @click="$router.push(`/notes/${note.id}`)">
        <div class="note-card-header">
          <h3 class="note-title">{{ note.title }}</h3>
          <span :class="['status-badge', note.status]">{{ statusLabel(note.status) }}</span>
        </div>
        <p class="note-summary">{{ note.summary || note.content.slice(0, 120) + '...' }}</p>
        <div class="note-card-footer">
          <div class="note-tags">
            <span v-for="tag in parseTags(note.tags)" :key="tag" class="tag-pill">{{ tag }}</span>
          </div>
          <div class="note-meta">
            <span class="note-date">{{ formatDate(note.updated_at) }}</span>
            <div class="note-actions">
              <el-button size="small" type="primary" text @click.stop="$router.push(`/notes/${note.id}/edit`)">
                编辑
              </el-button>
              <el-popconfirm title="确定删除该笔记？" @confirm="handleDelete(note.id)">
                <template #reference>
                  <el-button size="small" type="danger" text @click.stop>删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <el-pagination
        background
        layout="total, prev, pager, next, jumper"
        :total="total"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus, Upload } from '@element-plus/icons-vue'
import { noteApi, fileApi } from '../api'

const notes = ref<any[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const loading = ref(false)

const filters = reactive({
  keyword: '',
  status: '',
  category: '',
  tags: ''
})

const statusLabels: Record<string, string> = {
  draft: '草稿',
  published: '已发布',
  archived: '已归档'
}

function statusLabel(status: string): string {
  return statusLabels[status] || status
}

async function loadNotes() {
  loading.value = true
  try {
    const res: any = await noteApi.getList({
      page: currentPage.value,
      per_page: pageSize.value,
      ...filters
    })
    if (res.code === 200) {
      notes.value = res.data.notes
      total.value = res.data.total
    }
  } finally {
    loading.value = false
  }
}

async function handleDelete(id: number) {
  const res: any = await noteApi.delete(id)
  if (res.code === 200) {
    ElMessage.success('删除成功')
    loadNotes()
  }
}

async function handleImport(file: File) {
  try {
    const res: any = await fileApi.importNote(file)
    if (res.code === 200) {
      ElMessage.success('导入成功')
      loadNotes()
    } else {
      ElMessage.error(res.msg || '导入失败')
    }
  } catch {
    ElMessage.error('导入失败')
  }
  return false
}

function handlePageChange(page: number) {
  currentPage.value = page
  loadNotes()
}

function parseTags(tags: string): string[] {
  return tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : []
}

function formatDate(dateStr: string): string {
  if (!dateStr) return ''
  return dateStr.slice(0, 16).replace('T', ' ')
}

onMounted(loadNotes)
</script>

<style scoped>
.note-list-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 筛选栏 */
.filter-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  box-shadow: var(--shadow);
}

.filter-row {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
}

.filter-select {
  width: 120px;
}

.filter-input {
  width: 140px;
}

/* 笔记网格 */
.note-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}

/* 笔记卡片 */
.note-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.note-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.note-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.note-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

/* 状态标签 */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  flex-shrink: 0;
}

.status-badge.draft {
  background: #f1f5f9;
  color: #64748b;
}

.status-badge.published {
  background: #ecfdf5;
  color: #10b981;
}

.status-badge.archived {
  background: #fff7ed;
  color: #f97316;
}

.note-summary {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.note-card-footer {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: auto;
}

.note-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  background: #f1f5f9;
  color: var(--primary);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.note-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note-date {
  font-size: 12px;
  color: var(--text-muted);
}

.note-actions {
  display: flex;
  gap: 4px;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  padding: 8px 0;
}
</style>
