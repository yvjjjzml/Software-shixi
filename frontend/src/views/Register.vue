<template>
  <div class="register-page">
    <!-- ===== 螺旋粒子开幕 ===== -->
    <div class="spiral-intro" v-if="showIntro" :class="{ 'fade-out': introFading }">
      <canvas ref="canvasRef" class="spiral-canvas"></canvas>
      <div class="spiral-text">
        <h1>这一刻，改变未来</h1>
        <div class="sub">AI KNOWLEDGE WORKBENCH</div>
        <div class="line"></div>
      </div>
      <button class="spiral-skip" @click="endIntro">跳过 →</button>
    </div>

    <!-- ===== 注册页 — 左右分栏 ===== -->
    <div class="register-wrapper" :class="{ 'wrapper-show': !showIntro }">
      <!-- 左侧深色区 -->
      <div class="register-left">
        <div class="left-content">
          <div class="brand">
            <div class="brand-icon"><el-icon :size="32"><Notebook /></el-icon></div>
            <h2 class="brand-title">AI智能知识管理工作台</h2>
          </div>
          <p class="brand-desc">智能笔记 · AI问答 · 知识管理 · 数据洞察</p>
          <div class="deco-shapes">
            <div class="deco-circle c1"></div>
            <div class="deco-circle c2"></div>
            <div class="deco-circle c3"></div>
            <div class="deco-dot d1"></div>
            <div class="deco-dot d2"></div>
            <div class="deco-dot d3"></div>
          </div>
          <div class="features">
            <div class="feature-item"><el-icon><EditPen /></el-icon><span>Markdown笔记</span></div>
            <div class="feature-item"><el-icon><ChatDotRound /></el-icon><span>AI智能问答</span></div>
            <div class="feature-item"><el-icon><DataAnalysis /></el-icon><span>数据可视化</span></div>
          </div>
        </div>
      </div>

      <!-- 右侧注册表单 -->
      <div class="register-right">
        <div class="form-card">
          <h1 class="form-title">创建新账户</h1>
          <p class="form-subtitle">加入AI智能知识管理工作台</p>

          <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleRegister" class="register-form">
            <el-form-item prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名（至少3位）" size="large" prefix-icon="User" />
            </el-form-item>
            <el-form-item prop="nickname">
              <el-input v-model="form.nickname" placeholder="请输入昵称" size="large" prefix-icon="UserFilled" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="form.password" type="password" placeholder="请输入密码（至少6位）" size="large" prefix-icon="Lock" show-password />
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input v-model="form.confirmPassword" type="password" placeholder="请确认密码" size="large" prefix-icon="Lock" show-password @keyup.enter="handleRegister" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" class="register-btn" :loading="loading" @click="handleRegister">注 册</el-button>
            </el-form-item>
          </el-form>

          <div class="form-footer">
            <span>已有账号？</span>
            <router-link to="/login" class="footer-link">立即登录</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { authApi } from '../api'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const showIntro = ref(sessionStorage.getItem('introPlayed') ? false : true)
const introFading = ref(false)
const canvasRef = ref<HTMLCanvasElement>()
let animId = 0
let running = true

function endIntro() {
  if (!running) return
  running = false
  introFading.value = true
  sessionStorage.setItem('introPlayed', '1')
  cancelAnimationFrame(animId)
  setTimeout(() => { showIntro.value = false }, 800)
}

function initSpiral() {
  nextTick(() => {
    const canvas = canvasRef.value
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    let W: number, H: number, cx: number, cy: number
    const particles: any[] = []
    const spirals: any[] = []
    let t = 0

    function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; cx = W / 2; cy = H / 2 }
    resize()
    window.addEventListener('resize', resize)

    const colors = ['rgba(251,146,60,', 'rgba(253,186,116,', 'rgba(251,191,36,', 'rgba(251,191,36,', 'rgba(244,114,182,', 'rgba(251,146,60,']

    for (let i = 0; i < 6; i++) {
      spirals.push({ angle: (Math.PI * 2 / 6) * i, speed: 0.003 + Math.random() * 0.002, maxRadius: Math.max(W, H) * 0.7, color: colors[i % colors.length], offset: Math.random() * 100 })
    }

    function spawnParticles() {
      for (const sp of spirals) {
        const angle = sp.angle + t * sp.speed
        const r = 30 + (t * 0.8 + sp.offset) % sp.maxRadius
        const x = cx + Math.cos(angle) * r
        const y = cy + Math.sin(angle) * r
        if (Math.random() < 0.4) particles.push({ x, y, color: sp.color + (0.5 + Math.random() * 0.5) + ')', size: 1 + Math.random() * 3, vx: (Math.random() - 0.5) * 0.8, vy: (Math.random() - 0.5) * 0.8, life: 80 + Math.random() * 60, maxLife: 140, decay: 0.97 })
      }
      if (Math.random() < 0.15) {
        const angle = Math.random() * Math.PI * 2; const dist = Math.random() * 80
        particles.push({ x: cx + Math.cos(angle) * dist, y: cy + Math.sin(angle) * dist, color: colors[Math.floor(Math.random() * colors.length)] + '0.6)', size: 1.5, vx: 0, vy: 0, life: 50 + Math.random() * 30, maxLife: 80, decay: 0.97 })
      }
    }

    function draw() {
      ctx.fillStyle = 'rgba(26,10,10,0.12)'; ctx.fillRect(0, 0, W, H)
      for (const sp of spirals) {
        ctx.beginPath(); ctx.strokeStyle = sp.color + '0.08)'; ctx.lineWidth = 1
        for (let i = 0; i < 300; i++) {
          const angle = sp.angle + (t + i) * sp.speed; const r = 30 + ((t + i) * 0.8 + sp.offset) % sp.maxRadius
          const x = cx + Math.cos(angle) * r; const y = cy + Math.sin(angle) * r
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y)
        }
        ctx.stroke()
      }
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i]; p.x += p.vx; p.y += p.vy; p.life--; p.vx *= p.decay; p.vy *= p.decay
        const alpha = p.life / p.maxLife
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2); ctx.fillStyle = p.color.replace(/[\d.]+\)$/, (alpha * 0.8) + ')'); ctx.fill()
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size * alpha * 3, 0, Math.PI * 2); ctx.fillStyle = p.color.replace(/[\d.]+\)$/, (alpha * 0.15) + ')'); ctx.fill()
        if (p.life <= 0) particles.splice(i, 1)
      }
      const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, 100 + Math.sin(t * 0.02) * 30)
      grd.addColorStop(0, 'rgba(251,146,60,0.06)'); grd.addColorStop(1, 'rgba(251,146,60,0)')
      ctx.fillStyle = grd; ctx.fillRect(cx - 150, cy - 150, 300, 300)
      t++; if (running) animId = requestAnimationFrame(draw)
    }

    spawnParticles(); const si = setInterval(spawnParticles, 50); draw()
    setTimeout(endIntro, 5500)
    onUnmounted(() => { clearInterval(si); cancelAnimationFrame(animId); window.removeEventListener('resize', resize) })
  })
}

onMounted(() => { initSpiral() })

const form = reactive({ username: '', nickname: '', password: '', confirmPassword: '' })
const validateConfirm = (rule: any, value: string, callback: any) => { if (value !== form.password) callback(new Error('两次输入的密码不一致')); else callback() }
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }, { min: 3, message: '用户名至少3位', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
  confirmPassword: [{ required: true, message: '请确认密码', trigger: 'blur' }, { validator: validateConfirm, trigger: 'blur' }]
}

async function handleRegister() {
  await formRef.value?.validate(); loading.value = true
  try {
    const res: any = await authApi.register({ username: form.username, password: form.password, nickname: form.nickname || form.username })
    if (res.code === 200) { userStore.setAuth(res.data.token, res.data.user); ElMessage.success('注册成功'); router.push('/dashboard') }
    else { ElMessage.error(res.msg || '注册失败') }
  } catch (e: any) { ElMessage.error(e.response?.data?.msg || '注册失败') }
  finally { loading.value = false }
}
</script>

<style scoped>
.register-page { min-height: 100vh; background: #f0fdfa; position: relative; overflow: hidden; }

/* 螺旋开幕 */
.spiral-intro { position: fixed; inset: 0; z-index: 9999; background: #1a0a0a; display: flex; align-items: center; justify-content: center; overflow: hidden; transition: opacity 0.8s cubic-bezier(0.4,0,0.2,1); }
.spiral-intro.fade-out { opacity: 0; pointer-events: none; }
.spiral-canvas { position: absolute; inset: 0; }
.spiral-text { position: relative; z-index: 2; text-align: center; opacity: 0; transform: scale(0.6); animation: spiral-text-in 1.8s cubic-bezier(0.16,1,0.3,1) 1.2s forwards; }
.spiral-text h1 { font-size: 52px; font-weight: 800; letter-spacing: 6px; color: transparent; background: linear-gradient(135deg, #a855f7, #fbbf24, #a78bfa, #c084fc); background-size: 300% 300%; -webkit-background-clip: text; background-clip: text; animation: gradient-shift 4s ease infinite; margin: 0; text-shadow: 0 0 60px rgba(251,146,60,0.3); }
.spiral-text .sub { font-size: 16px; color: rgba(255,255,255,0.4); letter-spacing: 12px; margin-top: 16px; font-weight: 300; }
.spiral-text .line { width: 0; height: 2px; margin: 20px auto 0; background: linear-gradient(90deg, transparent, #fb923c, transparent); animation: line-expand 1.5s cubic-bezier(0.16,1,0.3,1) 2.4s forwards; }
.spiral-skip { position: absolute; bottom: 40px; right: 40px; z-index: 10; padding: 8px 20px; border-radius: 20px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.35); font-size: 12px; cursor: pointer; transition: 0.3s; font-family: inherit; letter-spacing: 1px; }
.spiral-skip:hover { background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.7); }
@keyframes spiral-text-in { 0% { opacity: 0; transform: scale(0.6) translateY(20px); filter: blur(8px); } 100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); } }
@keyframes gradient-shift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes line-expand { to { width: 120px; } }

/* 左右分栏 */
.register-wrapper { display: flex; min-height: 100vh; opacity: 0; transition: opacity 0.6s ease; }
.register-wrapper.wrapper-show { opacity: 1; }

.register-left { width: 45%; background: linear-gradient(160deg, #0d3b36 0%, #134e4a 40%, #1a5c56 100%); display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }
.left-content { position: relative; z-index: 2; padding: 60px; width: 100%; }
.brand { margin-bottom: 24px; }
.brand-icon { width: 64px; height: 64px; background: linear-gradient(135deg, #a855f7, #c084fc); border-radius: 18px; display: flex; align-items: center; justify-content: center; color: white; margin-bottom: 20px; box-shadow: 0 8px 24px rgba(251,146,60,0.3); }
.brand-title { font-size: 28px; font-weight: 700; color: white; letter-spacing: 2px; line-height: 1.4; }
.brand-desc { font-size: 14px; color: rgba(153,246,228,0.6); letter-spacing: 4px; margin-bottom: 60px; }

.deco-shapes { position: absolute; inset: 0; pointer-events: none; }
.deco-circle { position: absolute; border-radius: 50%; border: 1px solid rgba(251,146,60,0.15); }
.c1 { width: 300px; height: 300px; top: -80px; right: -60px; animation: spin 25s linear infinite; }
.c2 { width: 200px; height: 200px; bottom: -40px; left: -40px; animation: spin-reverse 20s linear infinite; border-color: rgba(251,191,36,0.1); }
.c3 { width: 120px; height: 120px; top: 40%; left: 60%; animation: spin 30s linear infinite; border-color: rgba(251,191,36,0.1); }
.deco-dot { position: absolute; width: 6px; height: 6px; border-radius: 50%; background: rgba(251,146,60,0.3); }
.d1 { top: 20%; left: 30%; animation: pulse 3s ease infinite; }
.d2 { top: 60%; left: 70%; animation: pulse 3s ease 1s infinite; background: rgba(251,191,36,0.3); }
.d3 { top: 80%; left: 20%; animation: pulse 3s ease 2s infinite; background: rgba(251,191,36,0.3); }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes spin-reverse { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }
@keyframes pulse { 0%, 100% { opacity: 0.3; transform: scale(1); } 50% { opacity: 1; transform: scale(1.5); } }

.features { display: flex; gap: 24px; margin-top: 40px; }
.feature-item { display: flex; align-items: center; gap: 8px; color: rgba(153,246,228,0.5); font-size: 13px; }
.feature-item .el-icon { font-size: 16px; }

.register-right { flex: 1; display: flex; align-items: center; justify-content: center; padding: 40px; background: #f8fffe; }
.form-card { width: 100%; max-width: 400px; }
.form-title { font-size: 28px; font-weight: 700; color: #134e4a; margin-bottom: 8px; }
.form-subtitle { font-size: 14px; color: #d8b4fe; margin-bottom: 36px; }

.register-form { margin-bottom: 24px; }
.register-form :deep(.el-form-item) { margin-bottom: 20px; }
.register-form :deep(.el-input__wrapper) { padding: 8px 16px; border-radius: 10px !important; box-shadow: 0 0 0 1px #ccfbf1 !important; background: white !important; transition: all 0.2s ease !important; }
.register-form :deep(.el-input__wrapper:hover) { box-shadow: 0 0 0 1px #a855f7 !important; }
.register-form :deep(.el-input__wrapper.is-focus) { box-shadow: 0 0 0 2px #a855f7 !important; }

.register-btn { width: 100%; height: 48px; font-size: 16px; font-weight: 600; border-radius: 12px !important; background: linear-gradient(135deg, #a855f7, #9333ea) !important; border: none !important; box-shadow: 0 4px 15px rgba(251,146,60,0.3) !important; transition: all 0.3s ease !important; }
.register-btn:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(251,146,60,0.4) !important; }

.form-footer { text-align: center; font-size: 14px; color: #d8b4fe; }
.footer-link { color: #a855f7; text-decoration: none; font-weight: 500; margin-left: 4px; }
.footer-link:hover { color: #9333ea; }

@media (max-width: 900px) { .register-left { display: none; } }
</style>
