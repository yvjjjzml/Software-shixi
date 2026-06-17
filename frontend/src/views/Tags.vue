<template>
  <div class="tags-page">
    <div class="page-header">
      <h2>🏷️ 标签管理</h2>
      <p class="page-desc">共 <strong>{{ tags.length }}</strong> 个标签</p>
    </div>

    <div class="tags-card" v-loading="loading">
      <el-table :data="tags" style="width: 100%" empty-text="暂无标签">
        <el-table-column label="标签名" min-width="200">
          <template #default="{ row }">
            <span class="tag-pill">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="使用次数" prop="count" width="120" align="center" />
        <el-table-column label="操作" width="120" align="center">
          <template #default="{ row }">
            <el-popconfirm
              title="确定删除该标签？删除后将从所有笔记中移除。"
              @confirm="handleDelete(row.name)"
            >
              <template #reference>
                <el-button type="danger" size="small" text>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { tagApi } from '../api'
import { ElMessage } from 'element-plus'

const tags = ref<any[]>([])
const loading = ref(false)

async function loadTags() {
  loading.value = true
  try {
    const res: any = await tagApi.getList()
    if (res.code === 200) {
      tags.value = res.data
    }
  } finally {
    loading.value = false
  }
}

async function handleDelete(name: string) {
  try {
    const res: any = await tagApi.delete(name)
    if (res.code === 200) {
      ElMessage.success('标签已删除')
      loadTags()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch {
    ElMessage.error('删除失败')
  }
}

onMounted(loadTags)
</script>

<style scoped>
.tags-page {
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

.page-desc strong {
  color: var(--primary);
  font-size: 18px;
}

.tags-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow);
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  padding: 4px 14px;
  background: linear-gradient(135deg, #f0fdfa, #ccfbf1);
  color: #0d9488;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid #99f6e4;
}
</style>
