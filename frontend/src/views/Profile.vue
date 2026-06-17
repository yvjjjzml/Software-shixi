<template>
  <div class="profile-page">
    <!-- 用户信息卡片 -->
    <div class="profile-card">
      <div class="profile-header">
        <el-avatar :size="64" class="avatar-gradient">
          {{ userStore.user?.nickname?.charAt(0) || 'U' }}
        </el-avatar>
        <div class="profile-info">
          <h2>{{ userStore.user?.nickname || userStore.user?.username }}</h2>
          <p class="profile-meta">
            <span><el-icon><User /></el-icon> {{ userStore.user?.username }}</span>
            <span><el-icon><Medal /></el-icon> {{ userStore.user?.role === 'admin' ? '管理员' : '普通用户' }}</span>
          </p>
        </div>
      </div>
    </div>

    <!-- 修改昵称 -->
    <div class="form-card">
      <h3><el-icon><EditPen /></el-icon> 修改昵称</h3>
      <el-form :model="nicknameForm" label-width="80px" class="form-content">
        <el-form-item label="新昵称">
          <el-input v-model="nicknameForm.nickname" placeholder="请输入新昵称" maxlength="20" show-word-limit />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleUpdateNickname" :loading="loading.nickname">保存昵称</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 修改密码 -->
    <div class="form-card">
      <h3><el-icon><Lock /></el-icon> 修改密码</h3>
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="80px" class="form-content">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="passwordForm.old_password" type="password" placeholder="请输入旧密码" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordForm.new_password" type="password" placeholder="请输入新密码（至少6位）" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleUpdatePassword" :loading="loading.password">修改密码</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useUserStore } from '../stores/user'
import { profileApi } from '../api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const passwordFormRef = ref()

const nicknameForm = reactive({
  nickname: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const loading = reactive({
  nickname: false,
  password: false
})

const passwordRules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: Function) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function handleUpdateNickname() {
  if (!nicknameForm.nickname.trim()) {
    ElMessage.warning('请输入昵称')
    return
  }
  loading.nickname = true
  try {
    const res: any = await profileApi.update({ nickname: nicknameForm.nickname })
    if (res.code === 200) {
      ElMessage.success('昵称更新成功')
      // 更新 store 中的用户信息
      if (userStore.user) {
        userStore.user.nickname = nicknameForm.nickname
      }
      nicknameForm.nickname = ''
    } else {
      ElMessage.error(res.msg || '更新失败')
    }
  } finally {
    loading.nickname = false
  }
}

async function handleUpdatePassword() {
  if (!passwordFormRef.value) return
  await passwordFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    loading.password = true
    try {
      const res: any = await profileApi.update({
        old_password: passwordForm.old_password,
        new_password: passwordForm.new_password
      })
      if (res.code === 200) {
        ElMessage.success('密码修改成功')
        passwordForm.old_password = ''
        passwordForm.new_password = ''
        passwordForm.confirm_password = ''
      } else {
        ElMessage.error(res.msg || '修改失败')
      }
    } finally {
      loading.password = false
    }
  })
}
</script>

<style scoped>
.profile-page {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-gradient {
  background: linear-gradient(135deg, #99f6e4, #14b8a6) !important;
  color: #fff;
  font-weight: 600;
  font-size: 24px;
  flex-shrink: 0;
}

.profile-info h2 {
  font-size: 20px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.profile-meta {
  display: flex;
  gap: 16px;
  color: var(--text-secondary);
  font-size: 14px;
}

.profile-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
}

.form-card h3 {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}

.form-content {
  max-width: 400px;
}
</style>
