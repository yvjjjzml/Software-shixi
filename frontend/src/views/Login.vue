<template>
  <div class="login-page">
    <!-- ===== 螺旋粒子开幕 ===== -->
    <div class="spiral-intro" v-if="showIntro" :class="{ 'fade-out': introFading }">
      <canvas ref="canvasRef" class="spiral-canvas"></canvas>
      <div class="spiral-overlay">
        <div class="corner-text tl">AI KNOWLEDGE</div>
        <div class="corner-text tr">WORKBENCH</div>
        <div class="corner-text bl">v1.0</div>
        <div class="corner-text br">2026</div>
        <div class="center-ring">
          <div class="ring r1"></div>
          <div class="ring r2"></div>
          <div class="ring r3"></div>
        </div>
        <div class="data-stream">
          <div class="stream-line" v-for="i in 8" :key="i"></div>
        </div>
        <div class="corner-deco tl-deco"></div>
        <div class="corner-deco tr-deco"></div>
        <div class="corner-deco bl-deco"></div>
        <div class="corner-deco br-deco"></div>
      </div>
      <button class="spiral-skip" @click="endIntro">跳过 →</button>
    </div>

    <!-- ===== 登录页 — 左右分栏 ===== -->
    <div class="login-wrapper" :class="{ 'wrapper-show': !showIntro }">
      <!-- 左侧：深色装饰区 -->
      <div class="login-left">
        <div class="left-content">
          <div class="brand">
            <div class="brand-icon">
              <el-icon :size="32"><Notebook /></el-icon>
            </div>
            <h2 class="brand-title">AI智能知识管理工作台</h2>
          </div>
          <p class="brand-desc">智能笔记 · AI问答 · 知识管理 · 数据洞察</p>

          <!-- 装饰图形 -->
          <div class="deco-shapes">
            <div class="deco-circle c1"></div>
            <div class="deco-circle c2"></div>
            <div class="deco-circle c3"></div>
            <div class="deco-line l1"></div>
            <div class="deco-line l2"></div>
            <div class="deco-dot d1"></div>
            <div class="deco-dot d2"></div>
            <div class="deco-dot d3"></div>
          </div>

          <!-- 底部特性 -->
          <div class="features">
            <div class="feature-item">
              <el-icon><EditPen /></el-icon>
              <span>Markdown笔记</span>
            </div>
            <div class="feature-item">
              <el-icon><ChatDotRound /></el-icon>
              <span>AI智能问答</span>
            </div>
            <div class="feature-item">
              <el-icon><DataAnalysis /></el-icon>
              <span>数据可视化</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：登录表单 -->
      <div class="login-right">
        <div class="form-card">
          <h1 class="form-title">欢迎回来</h1>
          <p class="form-subtitle">登录您的账户继续使用</p>

          <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin" class="login-form">
            <el-form-item prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名" size="large" prefix-icon="User" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" class="login-btn" :loading="loading" @click="handleLogin">
                登 录
              </el-button>
            </el-form-item>
          </el-form>

          <div class="demo-section">
            <div class="divider"><span class="divider-text">或者</span></div>
            <el-button size="large" class="demo-btn" :loading="demoLoading" @click="handleDemo">
              <el-icon><MagicStick /></el-icon>
              <span>一键体验（演示数据）</span>
            </el-button>
          </div>

          <div class="form-footer">
            <span>还没有账号？</span>
            <router-link to="/register" class="footer-link">立即注册</router-link>
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
import { authApi, demoApi } from '../api'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const demoLoading = ref(false)

// ===== 螺旋粒子 =====
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

    function resize() {
      W = canvas.width = window.innerWidth
      H = canvas.height = window.innerHeight
      cx = W / 2; cy = H / 2
    }
    resize()
    window.addEventListener('resize', resize)

    // 换色：青蓝+金色+紫色系
    const colors = [
      'rgba(251,146,60,', 'rgba(253,186,116,', 'rgba(251,191,36,',
      'rgba(251,191,36,', 'rgba(244,114,182,', 'rgba(251,146,60,',
    ]

    const spiralCount = 6
    for (let i = 0; i < spiralCount; i++) {
      spirals.push({
        angle: (Math.PI * 2 / spiralCount) * i,
        speed: 0.003 + Math.random() * 0.002,
        maxRadius: Math.max(W, H) * 0.7,
        color: colors[i % colors.length],
        offset: Math.random() * 100,
      })
    }

    function spawnParticles() {
      for (const sp of spirals) {
        const angle = sp.angle + t * sp.speed
        const r = 30 + (t * 0.8 + sp.offset) % sp.maxRadius
        const x = cx + Math.cos(angle) * r
        const y = cy + Math.sin(angle) * r
        if (Math.random() < 0.4) {
          particles.push({ x, y, color: sp.color + (0.5 + Math.random() * 0.5) + ')', size: 1 + Math.random() * 3, vx: (Math.random() - 0.5) * 0.8, vy: (Math.random() - 0.5) * 0.8, life: 80 + Math.random() * 60, maxLife: 140, decay: 0.97 })
        }
      }
      if (Math.random() < 0.15) {
        const angle = Math.random() * Math.PI * 2
        const dist = Math.random() * 80
        particles.push({ x: cx + Math.cos(angle) * dist, y: cy + Math.sin(angle) * dist, color: colors[Math.floor(Math.random() * colors.length)] + '0.6)', size: 1.5, vx: 0, vy: 0, life: 50 + Math.random() * 30, maxLife: 80, decay: 0.97 })
      }
    }

        // 额外：漂浮小点
    const floatingDots: any[] = []
    for (let i = 0; i < 60; i++) {
      floatingDots.push({
        x: Math.random() * W, y: Math.random() * H,
        size: 0.5 + Math.random() * 2,
        speed: 0.1 + Math.random() * 0.3,
        alpha: 0.1 + Math.random() * 0.3,
        color: colors[Math.floor(Math.random() * colors.length)],
      })
    }

    function draw() {
      ctx.fillStyle = 'rgba(26,10,10,0.12)'
      ctx.fillRect(0, 0, W, H)

      // 网格线（极淡）
      ctx.strokeStyle = 'rgba(251,146,60,0.015)'
      ctx.lineWidth = 0.5
      const gridSize = 80
      for (let x = 0; x < W; x += gridSize) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke()
      }
      for (let y = 0; y < H; y += gridSize) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke()
      }

      // 螺旋线
      for (const sp of spirals) {
        ctx.beginPath()
        ctx.strokeStyle = sp.color + '0.08)'
        ctx.lineWidth = 1
        for (let i = 0; i < 300; i++) {
          const angle = sp.angle + (t + i) * sp.speed
          const r = 30 + ((t + i) * 0.8 + sp.offset) % sp.maxRadius
          const x = cx + Math.cos(angle) * r
          const y = cy + Math.sin(angle) * r
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y)
        }
        ctx.stroke()
      }

      // 粒子
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i]
        p.x += p.vx; p.y += p.vy; p.life--
        p.vx *= p.decay; p.vy *= p.decay
        const alpha = p.life / p.maxLife
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2)
        ctx.fillStyle = p.color.replace(/[\.\d]+\)$/, (alpha * 0.8) + ')'); ctx.fill()
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size * alpha * 3, 0, Math.PI * 2)
        ctx.fillStyle = p.color.replace(/[\.\d]+\)$/, (alpha * 0.15) + ')'); ctx.fill()
        if (p.life <= 0) particles.splice(i, 1)
      }

      // 漂浮小点
      for (const d of floatingDots) {
        d.y -= d.speed
        d.x += Math.sin(t * 0.01 + d.y * 0.01) * 0.3
        if (d.y < -10) { d.y = H + 10; d.x = Math.random() * W }
        ctx.beginPath(); ctx.arc(d.x, d.y, d.size, 0, Math.PI * 2)
        ctx.fillStyle = d.color + d.alpha + ')'
        ctx.fill()
      }

      // 中心光晕
      const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, 100 + Math.sin(t * 0.02) * 30)
      grd.addColorStop(0, 'rgba(251,146,60,0.06)'); grd.addColorStop(1, 'rgba(251,146,60,0)')
      ctx.fillStyle = grd; ctx.fillRect(cx - 150, cy - 150, 300, 300)

      t++
      if (running) animId = requestAnimationFrame(draw)
    }

    spawnParticles()
    const spawnInterval = setInterval(spawnParticles, 50)
    draw()
    setTimeout(endIntro, 5500)
    onUnmounted(() => { clearInterval(spawnInterval); cancelAnimationFrame(animId); window.removeEventListener('resize', resize) })
  })
}

onMounted(() => { initSpiral() })

// ===== 登录逻辑 =====
const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res: any = await authApi.login(form)
    if (res.code === 200) {
      userStore.setAuth(res.data.token, res.data.user)
      ElMessage.success('登录成功')
      router.push('/dashboard')
    } else { ElMessage.error(res.msg || '登录失败') }
  } catch (e: any) { ElMessage.error(e.response?.data?.msg || '登录失败') }
  finally { loading.value = false }
}

async function handleDemo() {
  demoLoading.value = true
  try {
    const loginRes: any = await authApi.login({ username: 'admin', password: 'admin123' })
    if (loginRes.code !== 200) { ElMessage.error('演示登录失败'); return }
    userStore.setAuth(loginRes.data.token, loginRes.data.user)
    try { await demoApi.initData() } catch {}
    ElMessage.success('演示数据已准备就绪')
    router.push('/dashboard')
  } catch (e: any) { ElMessage.error('演示登录失败，请检查后端服务') }
  finally { demoLoading.value = false }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f0fdfa;
  position: relative;
  overflow: hidden;
}

/* ===== 螺旋开幕 ===== */
.spiral-intro {
  position: fixed; inset: 0; z-index: 9999;
  background: #1a0a0a;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
  transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.spiral-intro.fade-out { opacity: 0; pointer-events: none; }
.spiral-canvas { position: absolute; inset: 0; }
.spiral-overlay { position: absolute; inset: 0; z-index: 2; pointer-events: none; }

/* 四角文字 */
.corner-text {
  position: absolute; font-size: 11px; letter-spacing: 4px;
  color: rgba(251,146,60,0.25); font-weight: 300;
  opacity: 0; animation: corner-fade-in 1.5s ease 0.8s forwards;
}
.tl { top: 32px; left: 32px; }
.tr { top: 32px; right: 32px; }
.bl { bottom: 32px; left: 32px; }
.br { bottom: 32px; right: 32px; }
@keyframes corner-fade-in { to { opacity: 1; } }

/* 中心同心环 */
.center-ring {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
.ring {
  position: absolute; top: 50%; left: 50%;
  border-radius: 50%; border: 1px solid;
  transform: translate(-50%, -50%);
}
.r1 { width: 200px; height: 200px; border-color: rgba(251,146,60,0.08); animation: ring-pulse 4s ease infinite; }
.r2 { width: 340px; height: 340px; border-color: rgba(168,85,247,0.06); animation: ring-pulse 4s ease 1.3s infinite; }
.r3 { width: 480px; height: 480px; border-color: rgba(251,191,36,0.04); animation: ring-pulse 4s ease 2.6s infinite; }
@keyframes ring-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  50% { transform: translate(-50%, -50%) scale(1.08); opacity: 0.5; }
}

/* 数据流线 */
.data-stream {
  position: absolute; inset: 0; overflow: hidden;
}
.stream-line {
  position: absolute; width: 1px; height: 0;
  background: linear-gradient(180deg, transparent, rgba(251,146,60,0.15), transparent);
  animation: stream-down 3s ease-in-out infinite;
}
.stream-line:nth-child(1) { left: 12%; animation-delay: 0s; }
.stream-line:nth-child(2) { left: 25%; animation-delay: 0.4s; }
.stream-line:nth-child(3) { left: 38%; animation-delay: 0.8s; }
.stream-line:nth-child(4) { left: 50%; animation-delay: 1.2s; }
.stream-line:nth-child(5) { left: 62%; animation-delay: 1.6s; }
.stream-line:nth-child(6) { left: 75%; animation-delay: 2s; }
.stream-line:nth-child(7) { left: 88%; animation-delay: 2.4s; }
.stream-line:nth-child(8) { left: 95%; animation-delay: 2.8s; }
@keyframes stream-down {
  0% { top: -10%; height: 0; opacity: 0; }
  20% { height: 120px; opacity: 1; }
  80% { height: 120px; opacity: 1; }
  100% { top: 110%; height: 0; opacity: 0; }
}

/* 四角装饰线 */
.corner-deco {
  position: absolute; width: 40px; height: 40px;
  opacity: 0; animation: corner-fade-in 1.5s ease 1.2s forwards;
}
.tl-deco { top: 20px; left: 20px; border-top: 1px solid rgba(251,146,60,0.2); border-left: 1px solid rgba(251,146,60,0.2); }
.tr-deco { top: 20px; right: 20px; border-top: 1px solid rgba(168,85,247,0.2); border-right: 1px solid rgba(168,85,247,0.2); }
.bl-deco { bottom: 20px; left: 20px; border-bottom: 1px solid rgba(251,191,36,0.2); border-left: 1px solid rgba(251,191,36,0.2); }
.br-deco { bottom: 20px; right: 20px; border-bottom: 1px solid rgba(167,139,250,0.2); border-right: 1px solid rgba(167,139,250,0.2); }

.spiral-skip {
  position: absolute; bottom: 40px; right: 40px; z-index: 10;
  padding: 8px 20px; border-radius: 20px;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.35); font-size: 12px; cursor: pointer;
  transition: 0.3s; font-family: inherit; letter-spacing: 1px;
}
.spiral-skip:hover { background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.7); }

/* ===== 左右分栏 ===== */
.login-wrapper {
  display: flex;
  min-height: 100vh;
  opacity: 0;
  transition: opacity 0.6s ease;
}
.login-wrapper.wrapper-show { opacity: 1; }

/* 左侧深色区 */
.login-left {
  width: 45%;
  background: linear-gradient(160deg, #0d3b36 0%, #134e4a 40%, #1a5c56 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.left-content {
  position: relative;
  z-index: 2;
  padding: 60px;
  width: 100%;
}

.brand { margin-bottom: 24px; }

.brand-icon {
  width: 64px; height: 64px;
  background: linear-gradient(135deg, #a855f7, #c084fc);
  border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  color: white;
  margin-bottom: 20px;
  box-shadow: 0 8px 24px rgba(168, 85, 247, 0.3);
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  color: white;
  letter-spacing: 2px;
  line-height: 1.4;
}

.brand-desc {
  font-size: 14px;
  color: rgba(153, 246, 228, 0.6);
  letter-spacing: 4px;
  margin-bottom: 60px;
}

/* 装饰图形 */
.deco-shapes { position: absolute; inset: 0; pointer-events: none; }

.deco-circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(168, 85, 247, 0.15);
}
.c1 { width: 300px; height: 300px; top: -80px; right: -60px; animation: spin 25s linear infinite; }
.c2 { width: 200px; height: 200px; bottom: -40px; left: -40px; animation: spin-reverse 20s linear infinite; border-color: rgba(251, 191, 36, 0.1); }
.c3 { width: 120px; height: 120px; top: 40%; left: 60%; animation: spin 30s linear infinite; border-color: rgba(167, 139, 250, 0.1); }

.deco-line {
  position: absolute;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.2), transparent);
}
.l1 { width: 200px; top: 30%; left: 10%; transform: rotate(-15deg); }
.l2 { width: 150px; bottom: 25%; right: 15%; transform: rotate(20deg); }

.deco-dot {
  position: absolute;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: rgba(168, 85, 247, 0.3);
}
.d1 { top: 20%; left: 30%; animation: pulse 3s ease infinite; }
.d2 { top: 60%; left: 70%; animation: pulse 3s ease 1s infinite; background: rgba(251, 191, 36, 0.3); }
.d3 { top: 80%; left: 20%; animation: pulse 3s ease 2s infinite; background: rgba(167, 139, 250, 0.3); }

@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes spin-reverse { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }
@keyframes pulse { 0%, 100% { opacity: 0.3; transform: scale(1); } 50% { opacity: 1; transform: scale(1.5); } }

/* 底部特性 */
.features {
  display: flex;
  gap: 24px;
  margin-top: 40px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(153, 246, 228, 0.5);
  font-size: 13px;
}

.feature-item .el-icon { font-size: 16px; }

/* 右侧表单区 */
.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #f8fffe;
}

.form-card {
  width: 100%;
  max-width: 400px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: #134e4a;
  margin-bottom: 8px;
}

.form-subtitle {
  font-size: 14px;
  color: #d8b4fe;
  margin-bottom: 36px;
}

.login-form { margin-bottom: 24px; }
.login-form :deep(.el-form-item) { margin-bottom: 20px; }
.login-form :deep(.el-input__wrapper) {
  padding: 8px 16px; border-radius: 10px !important;
  box-shadow: 0 0 0 1px #ccfbf1 !important;
  background: white !important;
  transition: all 0.2s ease !important;
}
.login-form :deep(.el-input__wrapper:hover) { box-shadow: 0 0 0 1px #a855f7 !important; }
.login-form :deep(.el-input__wrapper.is-focus) { box-shadow: 0 0 0 2px #a855f7 !important; }

.login-btn {
  width: 100%; height: 48px;
  font-size: 16px; font-weight: 600;
  border-radius: 12px !important;
  background: linear-gradient(135deg, #a855f7, #9333ea) !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3) !important;
  transition: all 0.3s ease !important;
}
.login-btn:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4) !important; }

.demo-section { margin-bottom: 24px; }
.divider { display: flex; align-items: center; margin-bottom: 16px; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #ccfbf1; }
.divider-text { padding: 0 16px; font-size: 13px; color: #99f6e4; }

.demo-btn {
  width: 100%; height: 48px;
  font-size: 15px; font-weight: 500;
  border-radius: 12px !important;
  background: transparent !important;
  border: 2px dashed #ccfbf1 !important;
  color: #d8b4fe !important;
  transition: all 0.3s ease !important;
}
.demo-btn:hover { border-color: #a855f7 !important; color: #a855f7 !important; background: rgba(168, 85, 247, 0.05) !important; }
.demo-btn .el-icon { margin-right: 8px; }

.form-footer { text-align: center; font-size: 14px; color: #d8b4fe; }
.footer-link { color: #a855f7; text-decoration: none; font-weight: 500; margin-left: 4px; }
.footer-link:hover { color: #9333ea; }

@media (max-width: 900px) {
  .login-left { display: none; }
}
</style>
