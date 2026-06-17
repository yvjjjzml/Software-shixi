<template>
  <div class="search-page">
    <!-- 搜索栏 -->
    <el-card shadow="never" class="search-card">
      <el-row :gutter="16" align="middle">
        <el-col :span="10">
          <el-input v-model="keyword" placeholder="输入关键词搜索..." size="large" clearable
            prefix-icon="Search" @keyup.enter="doSearch" />
        </el-col>
        <el-col :span="5">
          <el-input v-model="tags" placeholder="标签筛选" size="large" clearable @keyup.enter="doSearch" />
        </el-col>
        <el-col :span="5">
          <el-input v-model="category" placeholder="分类筛选" size="large" clearable @keyup.enter="doSearch" />
        </el-col>
        <el-col :span="4">
          <el-button type="primary" size="large" style="width:100%" @click="doSearch" :loading="loading">
            搜索
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 搜索结果 -->
    <div class="results" v-loading="loading">
      <el-empty v-if="!loading && searched && results.length === 0" description="没有找到相关笔记" />

      <el-card v-for="note in results" :key="note.id" shadow="hover" class="result-card"
        @click="$router.push(`/notes/${note.id}`)">
        <div class="result-header">
          <h3 v-html="highlight(note.title)"></h3>
          <StatusBadge :status="note.status" />
        </div>
        <p class="result-content" v-html="highlight(note.content.slice(0, 200))"></p>
        <div class="result-meta">
          <div class="result-tags" v-if="note.tags">
            <el-tag v-for="tag in parseTags(note.tags)" :key="tag" size="small" type="info" effect="plain">
              {{ tag }}
            </el-tag>
          </div>
          <span class="result-date">{{ note.updated_at?.slice(0, 10) }}</span>
        </div>
      </el-card>

      <div class="pagination" v-if="total > 0">
        <el-pagination background layout="total, prev, pager, next"
          :total="total" :page-size="pageSize" :current-page="currentPage"
          @current-change="p => { currentPage = p; doSearch() }" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { searchApi } from '../api'
import StatusBadge from '../components/StatusBadge.vue'

const keyword = ref('')
const tags = ref('')
const category = ref('')
const results = ref<any[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const searched = ref(false)

function parseTags(t: string): string[] {
  return t ? t.split(',').map(s => s.trim()).filter(Boolean) : []
}

function highlight(text: string): string {
  if (!keyword.value.trim()) return text
  const escaped = keyword.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(${escaped})`, 'gi')
  return text.replace(regex, '<mark style="background:#fef08a;padding:0 2px;border-radius:2px">$1</mark>')
}

async function doSearch() {
  if (!keyword.value.trim() && !tags.value.trim() && !category.value.trim()) {
    ElMessage.warning('请输入搜索条件')
    return
  }
  loading.value = true
  searched.value = true
  try {
    const res: any = await searchApi.search({
      keyword: keyword.value,
      tags: tags.value,
      category: category.value,
      page: currentPage.value,
      per_page: pageSize.value
    })
    if (res.code === 200) {
      results.value = res.data.notes
      total.value = res.data.total
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.search-card {
  margin-bottom: 20px;
}

.result-card {
  margin-bottom: 12px;
  cursor: pointer;
  transition: transform 0.2s;
  border-radius: 8px;
}

.result-card:hover {
  transform: translateY(-2px);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.result-header h3 {
  font-size: 16px;
  color: #303133;
}

.result-content {
  font-size: 14px;
  color: #606266;
  line-height: 1.7;
  margin-bottom: 10px;
}

.result-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-tags {
  display: flex;
  gap: 4px;
}

.result-date {
  font-size: 12px;
  color: #c0c4cc;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
