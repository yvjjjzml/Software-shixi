<template>
  <div class="admin-page">
    <el-tabs v-model="activeTab">
      <!-- 用户管理 -->
      <el-tab-pane label="用户管理" name="users">
        <el-table :data="users" stripe v-loading="loadingUsers" style="width:100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="nickname" label="昵称" />
          <el-table-column prop="role" label="角色">
            <template #default="{ row }">
              <el-tag :type="row.role === 'admin' ? 'danger' : 'info'" size="small">
                {{ row.role === 'admin' ? '管理员' : '普通用户' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="注册时间" width="180" />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-popconfirm title="确定删除该用户？所有笔记将被删除！" @confirm="deleteUser(row.id)">
                <template #reference>
                  <el-button type="danger" size="small" text :disabled="row.role === 'admin'">
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 内容管理 -->
      <el-tab-pane label="内容管理" name="notes">
        <el-table :data="allNotes" stripe v-loading="loadingNotes" style="width:100%">
          <el-table-column prop="id" label="ID" width="70" />
          <el-table-column prop="title" label="标题" show-overflow-tooltip />
          <el-table-column prop="username" label="作者" width="120" />
          <el-table-column prop="category" label="分类" width="120" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <StatusBadge :status="row.status" />
            </template>
          </el-table-column>
          <el-table-column prop="view_count" label="浏览" width="80" />
          <el-table-column prop="updated_at" label="更新时间" width="180" />
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button type="primary" size="small" text @click="$router.push(`/notes/${row.id}`)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination" v-if="notesTotal > 0">
          <el-pagination background layout="total, prev, pager, next"
            :total="notesTotal" :page-size="20" :current-page="notesPage"
            @current-change="p => { notesPage = p; loadAllNotes() }" />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminApi } from '../api'
import StatusBadge from '../components/StatusBadge.vue'

const activeTab = ref('users')
const users = ref<any[]>([])
const allNotes = ref<any[]>([])
const loadingUsers = ref(false)
const loadingNotes = ref(false)
const notesTotal = ref(0)
const notesPage = ref(1)

async function loadUsers() {
  loadingUsers.value = true
  try {
    const res: any = await adminApi.getUsers()
    if (res.code === 200) users.value = res.data.users
  } finally { loadingUsers.value = false }
}

async function loadAllNotes() {
  loadingNotes.value = true
  try {
    const res: any = await adminApi.getNotes({ page: notesPage.value, per_page: 20 })
    if (res.code === 200) {
      allNotes.value = res.data.notes
      notesTotal.value = res.data.total
    }
  } finally { loadingNotes.value = false }
}

async function deleteUser(id: number) {
  const res: any = await adminApi.deleteUser(id)
  if (res.code === 200) {
    ElMessage.success('删除成功')
    loadUsers()
  }
}

onMounted(() => {
  loadUsers()
  loadAllNotes()
})
</script>

<style scoped>
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
