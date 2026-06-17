<template>
  <div class="ai-chat">
    <el-card shadow="never" class="chat-card">
      <template #header>
        <div class="chat-header">
          <el-icon :size="24" color="#409EFF"><ChatDotRound /></el-icon>
          <span>AI知识问答助手</span>
          <el-tag type="info" effect="plain" size="small">基于您的笔记库</el-tag>
        </div>
      </template>

      <!-- 聊天消息区 -->
      <div class="chat-messages" ref="messagesRef">
        <div v-if="messages.length === 0" class="empty-chat">
          <el-icon :size="64" color="#dcdfe6"><ChatDotRound /></el-icon>
          <p>向AI提问，基于您的笔记库智能回答</p>
          <div class="quick-questions">
            <el-button v-for="q in quickQuestions" :key="q" size="small" round @click="askQuestion(q)">
              {{ q }}
            </el-button>
          </div>
        </div>

        <div v-for="(msg, i) in messages" :key="i" :class="['message', msg.role]">
          <div class="message-avatar">
            <el-avatar v-if="msg.role === 'user'" :size="36" style="background:#409EFF">
              {{ userStore.user?.nickname?.charAt(0) || 'U' }}
            </el-avatar>
            <el-avatar v-else :size="36" style="background:#67C23A">
              <el-icon><ChatDotRound /></el-icon>
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="renderMarkdown(msg.content)"></div>
            <!-- 引用笔记 -->
            <div v-if="msg.sourceNotes?.length" class="source-notes">
              <div class="source-title">📚 引用笔记：</div>
              <el-tag v-for="n in msg.sourceNotes" :key="n.id" size="small" type="warning"
                effect="plain" style="cursor:pointer" @click="$router.push(`/notes/${n.id}`)">
                {{ n.title }}
              </el-tag>
            </div>
          </div>
        </div>

        <div v-if="asking" class="message assistant">
          <div class="message-avatar">
            <el-avatar :size="36" style="background:#67C23A"><el-icon><ChatDotRound /></el-icon></el-avatar>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="chat-input">
        <el-input v-model="inputText" placeholder="输入您的问题..." size="large"
          :disabled="asking" @keyup.enter="sendMessage">
          <template #append>
            <el-button type="primary" :icon="Promotion" :loading="asking" @click="sendMessage">
              发送
            </el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { Promotion } from '@element-plus/icons-vue'
import { marked } from 'marked'
import { aiApi } from '../api'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const messages = ref<any[]>([])
const inputText = ref('')
const asking = ref(false)
const messagesRef = ref<HTMLElement>()

const quickQuestions = [
  '总结一下我最近的笔记',
  '我的笔记主要涉及哪些主题？',
  '推荐一些值得回顾的笔记'
]

function renderMarkdown(text: string): string {
  try { return marked(text || '') } catch { return text }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

async function askQuestion(question: string) {
  if (!question.trim() || asking.value) return

  messages.value.push({ role: 'user', content: question })
  inputText.value = ''
  scrollToBottom()

  asking.value = true
  try {
    const res: any = await aiApi.ask({ question })
    if (res.code === 200) {
      messages.value.push({
        role: 'assistant',
        content: res.data.answer,
        sourceNotes: res.data.source_notes || []
      })
    } else {
      messages.value.push({ role: 'assistant', content: '抱歉，回答失败：' + (res.msg || '未知错误') })
    }
  } catch {
    messages.value.push({ role: 'assistant', content: '网络错误，请稍后重试' })
  } finally {
    asking.value = false
    scrollToBottom()
  }
}

function sendMessage() {
  askQuestion(inputText.value)
}
</script>

<style scoped>
.chat-card {
  height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
}

.chat-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding-bottom: 0;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 0 0 16px;
}

.empty-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #c0c4cc;
}

.empty-chat p {
  margin: 16px 0;
  font-size: 15px;
}

.quick-questions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  background: #409EFF;
  color: #fff;
  border-radius: 12px 2px 12px 12px;
  padding: 12px 16px;
}

.message.assistant .message-content {
  background: #f4f4f5;
  color: #303133;
  border-radius: 2px 12px 12px 12px;
  padding: 12px 16px;
}

.message-text {
  line-height: 1.7;
  font-size: 14px;
}

.message-text :deep(p) { margin: 4px 0; }
.message-text :deep(code) { background: rgba(0,0,0,0.08); padding: 1px 4px; border-radius: 3px; }
.message-text :deep(pre) { background: #1e1e1e; color: #d4d4d4; padding: 10px; border-radius: 6px; overflow-x: auto; margin: 8px 0; }

.source-notes {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(0,0,0,0.06);
}

.source-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #c0c4cc;
  border-radius: 50%;
  animation: typing 1.2s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1); }
}

.chat-input {
  padding: 16px 0;
}
</style>
