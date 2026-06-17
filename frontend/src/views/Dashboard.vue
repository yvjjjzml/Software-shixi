<template>
  <div class="dashboard">
    <!-- ===== Hero 欢迎区 ===== -->
    <div class="hero">
      <div class="hero-left">
        <div class="hero-greeting">
          <span class="hero-wave">👋</span>
          <span class="hero-time">{{ greetingText }}</span>
        </div>
        <h1 class="hero-title">{{ userStore.user?.nickname || '用户' }}的知识库</h1>
        <p class="hero-desc">你已经积累了 <strong>{{ stats.total_notes || 0 }}</strong> 篇笔记，继续保持学习的热情</p>
      </div>
      <div class="hero-right">
        <div class="hero-stats">
          <div class="hero-stat-item">
            <div class="hero-stat-num">{{ stats.total_notes || 0 }}</div>
            <div class="hero-stat-label">笔记</div>
          </div>
          <div class="hero-stat-divider"></div>
          <div class="hero-stat-item">
            <div class="hero-stat-num">{{ stats.total_views || 0 }}</div>
            <div class="hero-stat-label">浏览</div>
          </div>
          <div class="hero-stat-divider"></div>
          <div class="hero-stat-item">
            <div class="hero-stat-num">{{ publishedCount }}</div>
            <div class="hero-stat-label">已发布</div>
          </div>
        </div>
        <el-button class="demo-btn-hero" :loading="demoLoading" @click="handleLoadDemo">
          <el-icon><MagicStick /></el-icon>
          <span>加载演示数据</span>
        </el-button>
      </div>
    </div>

    <!-- ===== 快捷入口 ===== -->
    <div class="quick-actions">
      <div class="quick-card" @click="$router.push('/notes/create')">
        <div class="quick-icon" style="background: linear-gradient(135deg, #14b8a6, #0d9488)">
          <el-icon :size="24"><EditPen /></el-icon>
        </div>
        <div class="quick-text">
          <div class="quick-title">写笔记</div>
          <div class="quick-sub">记录新的想法</div>
        </div>
      </div>
      <div class="quick-card" @click="$router.push('/ai-chat')">
        <div class="quick-icon" style="background: linear-gradient(135deg, #fbbf24, #f59e0b)">
          <el-icon :size="24"><ChatDotRound /></el-icon>
        </div>
        <div class="quick-text">
          <div class="quick-title">AI问答</div>
          <div class="quick-sub">向知识库提问</div>
        </div>
      </div>
      <div class="quick-card" @click="$router.push('/search')">
        <div class="quick-icon" style="background: linear-gradient(135deg, #34d399, #10b981)">
          <el-icon :size="24"><Search /></el-icon>
        </div>
        <div class="quick-text">
          <div class="quick-title">搜索</div>
          <div class="quick-sub">查找笔记内容</div>
        </div>
      </div>
      <div class="quick-card" @click="$router.push('/notes')">
        <div class="quick-icon" style="background: linear-gradient(135deg, #fb923c, #f97316)">
          <el-icon :size="24"><Document /></el-icon>
        </div>
        <div class="quick-text">
          <div class="quick-title">全部笔记</div>
          <div class="quick-sub">管理你的知识</div>
        </div>
      </div>
    </div>

    <!-- ===== 统计 + 图表 ===== -->
    <div class="main-grid">
      <!-- 左侧：图表 -->
      <div class="charts-col">
        <div class="chart-card">
          <div class="chart-header">
            <h3>📈 活跃趋势</h3>
            <span class="chart-badge">近7天</span>
          </div>
          <div ref="trendChartRef" class="chart-body"></div>
        </div>

        <div class="chart-row-2">
          <div class="chart-card">
            <div class="chart-header">
              <h3>📊 笔记状态</h3>
            </div>
            <div ref="statusChartRef" class="chart-body"></div>
          </div>
          <div class="chart-card">
            <div class="chart-header">
              <h3>🏷️ 标签分布</h3>
            </div>
            <div ref="tagChartRef" class="chart-body"></div>
          </div>
        </div>

        <!-- 热力图 + 散点图 -->
        <div class="chart-row-2">
          <div class="chart-card">
            <div class="chart-header">
              <h3>🔥 活跃热力图</h3>
              <span class="chart-badge">7天×24小时</span>
            </div>
            <div ref="heatmapChartRef" class="chart-body"></div>
          </div>
          <div class="chart-card">
            <div class="chart-header">
              <h3>🔵 字数vs浏览量</h3>
            </div>
            <div ref="scatterChartRef" class="chart-body"></div>
          </div>
        </div>
      </div>

      <!-- 右侧：词云 + 最近笔记 -->
      <div class="side-col">
        <div class="chart-card">
          <div class="chart-header">
            <h3>☁️ 内容词云</h3>
          </div>
          <div ref="wordcloudRef" class="chart-body"></div>
        </div>

        <div class="recent-card">
          <div class="chart-header">
            <h3>📝 最近笔记</h3>
            <router-link to="/notes" class="view-all">查看全部</router-link>
          </div>
          <div class="recent-list">
            <div v-for="note in recentNotes" :key="note.id" class="recent-item" @click="$router.push(`/notes/${note.id}`)">
              <div class="recent-title">{{ note.title }}</div>
              <div class="recent-meta">
                <span class="recent-tag" v-for="tag in (note.tags || '').split(',').slice(0, 2)" :key="tag">{{ tag }}</span>
                <span class="recent-time">{{ formatTime(note.updated_at) }}</span>
              </div>
            </div>
            <div v-if="!recentNotes.length" class="recent-empty">暂无笔记，去创建一篇吧</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import { dashboardApi, noteApi, demoApi } from '../api'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const stats = ref<any>({})
const recentNotes = ref<any[]>([])
const demoLoading = ref(false)
const trendChartRef = ref<HTMLElement>()
const statusChartRef = ref<HTMLElement>()
const tagChartRef = ref<HTMLElement>()
const wordcloudRef = ref<HTMLElement>()
const heatmapChartRef = ref<HTMLElement>()
const scatterChartRef = ref<HTMLElement>()

const publishedCount = computed(() => stats.value.status_stats?.published || 0)

const greetingText = computed(() => {
  const h = new Date().getHours()
  if (h < 6) return '夜深了'
  if (h < 12) return '早上好'
  if (h < 14) return '中午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

function formatTime(t: string) {
  if (!t) return ''
  const d = new Date(t)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前'
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前'
  return t.slice(5, 10)
}

const chartColors = {
  primary: '#14b8a6',
  palette: ['#14b8a6', '#34d399', '#fbbf24', '#fb923c', '#2dd4bf', '#5eead4', '#f9a8d4', '#a78bfa', '#fdba74', '#94a3b8']
}

async function loadData() {
  const [statsRes, wordRes, notesRes]: any = await Promise.all([
    dashboardApi.getStats(),
    dashboardApi.getWordcloud(),
    noteApi.getList({ page: 1, per_page: 5 })
  ])

  if (statsRes.code === 200) {
    stats.value = statsRes.data
    await nextTick()
    renderTrendChart(statsRes.data.trend || [])
    renderStatusChart(statsRes.data.status_stats || {})
    renderTagChart(statsRes.data.tag_stats || [])
    renderHeatmap(statsRes.data.heatmap || [])
    renderScatter(statsRes.data.scatter || [])
    renderHeatmap(statsRes.data.heatmap || [])
    renderScatter(statsRes.data.scatter || [])
  }

  if (wordRes.code === 200) {
    await nextTick()
    renderWordcloud(wordRes.data.words || [])
  }

  if (notesRes.code === 200) {
    recentNotes.value = notesRes.data.notes || []
  }
}

function renderTrendChart(data: any[]) {
  if (!trendChartRef.value) return
  const chart = echarts.init(trendChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'white', borderColor: '#ccfbf1', borderWidth: 1, textStyle: { color: '#134e4a' } },
    xAxis: { type: 'category', data: data.map(d => d.date.slice(5)), axisLine: { lineStyle: { color: '#ccfbf1' } }, axisLabel: { color: '#5eead4' } },
    yAxis: { type: 'value', minInterval: 1, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: '#5eead4' }, splitLine: { lineStyle: { color: '#f0fdfa' } } },
    series: [{
      data: data.map(d => d.count), type: 'line', smooth: true, symbol: 'circle', symbolSize: 8,
      lineStyle: { color: chartColors.primary, width: 3 },
      itemStyle: { color: chartColors.primary, borderColor: 'white', borderWidth: 2 },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(20,184,166,0.2)' }, { offset: 1, color: 'rgba(20,184,166,0.02)' }]) }
    }],
    grid: { left: 50, right: 20, top: 20, bottom: 30 }
  })
}

function renderStatusChart(data: Record<string, number>) {
  if (!statusChartRef.value) return
  const chart = echarts.init(statusChartRef.value)
  const labels: Record<string, string> = { draft: '草稿', published: '已发布', archived: '已归档' }
  const colors: Record<string, string> = { draft: '#fbbf24', published: '#14b8a6', archived: '#94a3b8' }
  chart.setOption({
    tooltip: { trigger: 'item', backgroundColor: 'white', borderColor: '#ccfbf1', borderWidth: 1, textStyle: { color: '#134e4a' } },
    legend: { bottom: 10, textStyle: { color: '#5eead4' } },
    series: [{
      type: 'pie', radius: ['40%', '70%'], center: ['50%', '45%'],
      label: { formatter: '{b}: {c}', color: '#5eead4' },
      data: Object.entries(data).map(([k, v]) => ({ name: labels[k] || k, value: v, itemStyle: { color: colors[k] || chartColors.primary } })),
      emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.1)' } }
    }]
  })
}

function renderTagChart(data: any[]) {
  if (!tagChartRef.value) return
  const chart = echarts.init(tagChartRef.value)
  chart.setOption({
    tooltip: { backgroundColor: 'white', borderColor: '#ccfbf1', borderWidth: 1, textStyle: { color: '#134e4a' } },
    xAxis: { type: 'category', data: data.map(d => d.name), axisLine: { lineStyle: { color: '#ccfbf1' } }, axisLabel: { color: '#5eead4', rotate: 30 } },
    yAxis: { type: 'value', minInterval: 1, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: '#5eead4' }, splitLine: { lineStyle: { color: '#f0fdfa' } } },
    series: [{
      type: 'bar',
      data: data.map((d, i) => ({ value: d.count, itemStyle: { color: chartColors.palette[i % chartColors.palette.length], borderRadius: [6, 6, 0, 0] } })),
      barWidth: '60%'
    }],
    grid: { left: 50, right: 20, top: 10, bottom: 50 }
  })
}

function renderWordcloud(words: any[]) {
  if (!wordcloudRef.value || !words.length) return
  const chart = echarts.init(wordcloudRef.value)
  chart.setOption({
    series: [{
      type: 'wordCloud', shape: 'circle', sizeRange: [14, 60], rotationRange: [-30, 30], rotationStep: 15, gridSize: 10,
      textStyle: { fontFamily: 'var(--font-family)', fontWeight: 'bold', color: () => chartColors.palette[Math.floor(Math.random() * chartColors.palette.length)] },
      emphasis: { textStyle: { textShadowBlur: 3, textShadowColor: 'rgba(0,0,0,0.1)' } },
      data: words
    }]
  })
}

async function handleLoadDemo() {
  demoLoading.value = true
  try {
    const res: any = await demoApi.initData()
    if (res.code === 200) {
      ElMessage.success('演示数据已加载')
      loadData()
    } else {
      ElMessage.info(res.msg || '已有数据')
    }
  } catch {
    ElMessage.error('加载失败')
  } finally {
    demoLoading.value = false
  }
}


function renderHeatmap(data) {
  if (!heatmapChartRef.value || !data.length) return
  const chart = echarts.init(heatmapChartRef.value)
  const days = ['6天前', '5天前', '4天前', '3天前', '前天', '昨天', '今天']
  const hours = Array.from({ length: 24 }, (_, i) => i + ':00')
  chart.setOption({
    tooltip: { formatter: (p) => days[p.value[0]] + ' ' + hours[p.value[1]] + '<br>创建 ' + p.value[2] + ' 篇' },
    xAxis: { type: 'category', data: hours, axisLabel: { color: '#5eead4', fontSize: 10 }, splitArea: { show: true } },
    yAxis: { type: 'category', data: days, axisLabel: { color: '#5eead4' } },
    visualMap: { min: 0, max: 5, calculable: true, orient: 'horizontal', left: 'center', bottom: 0, inRange: { color: ['#f0fdfa', '#14b8a6', '#0d9488'] }, textStyle: { color: '#5eead4' } },
    series: [{ type: 'heatmap', data: data, label: { show: false }, emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' } } }],
    grid: { left: 60, right: 20, top: 10, bottom: 50 }
  })
}

function renderScatter(data) {
  if (!scatterChartRef.value || !data.length) return
  const chart = echarts.init(scatterChartRef.value)
  chart.setOption({
    tooltip: { formatter: (p) => '字数: ' + p.value[0] + '<br>浏览: ' + p.value[1] },
    xAxis: { type: 'value', name: '字数', axisLabel: { color: '#5eead4' }, splitLine: { lineStyle: { color: '#f0fdfa' } } },
    yAxis: { type: 'value', name: '浏览量', axisLabel: { color: '#5eead4' }, splitLine: { lineStyle: { color: '#f0fdfa' } } },
    series: [{
      type: 'scatter', symbolSize: 14,
      data: data.map((d) => [d.x, d.y]),
      itemStyle: { color: '#14b8a6', opacity: 0.7 },
      emphasis: { itemStyle: { color: '#0d9488', shadowBlur: 8, shadowColor: 'rgba(20,184,166,0.3)' } }
    }],
    grid: { left: 60, right: 20, top: 20, bottom: 40 }
  })
}


onMounted(loadData)
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ===== Hero 欢迎区 ===== */
.hero {
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 50%, #2dd4bf 100%);
  border-radius: 20px;
  padding: 32px 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
}

.hero::after {
  content: '';
  position: absolute;
  bottom: -30%;
  right: 20%;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
}

.hero-left { position: relative; z-index: 1; }

.hero-greeting {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.hero-wave { font-size: 20px; }

.hero-title {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.hero-desc {
  font-size: 14px;
  opacity: 0.85;
}

.hero-desc strong {
  font-size: 18px;
  font-weight: 700;
}

.hero-right { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: flex-end; gap: 16px; }

.hero-stats {
  display: flex;
  align-items: center;
  gap: 24px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 20px 28px;
}

.hero-stat-item { text-align: center; }

.hero-stat-num {
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
}

.hero-stat-label {
  font-size: 13px;
  opacity: 0.8;
  margin-top: 6px;
}

.hero-stat-divider {
  width: 1px;
  height: 36px;
  background: rgba(255, 255, 255, 0.2);
}

/* 演示数据按钮 */
.demo-btn-hero {
  padding: 10px 20px;
  border-radius: 12px !important;
  background: rgba(255, 255, 255, 0.15) !important;
  border: 1px solid rgba(255, 255, 255, 0.25) !important;
  color: white !important;
  font-size: 13px;
  font-weight: 500;
  backdrop-filter: blur(10px);
  transition: all 0.25s ease !important;
}

.demo-btn-hero:hover {
  background: rgba(255, 255, 255, 0.25) !important;
  transform: translateY(-1px);
}

.demo-btn-hero .el-icon {
  margin-right: 6px;
}

/* ===== 快捷入口 ===== */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.quick-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.quick-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.quick-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.quick-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.quick-sub {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

/* ===== 主网格 ===== */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 20px;
}

.charts-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.side-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ===== 图表卡片 ===== */
.chart-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  transition: all 0.2s ease;
}

.chart-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.chart-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0fdfa;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chart-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-badge {
  font-size: 11px;
  padding: 3px 10px;
  background: #f0fdfa;
  color: #0d9488;
  border-radius: 20px;
  font-weight: 500;
}

.chart-body {
  height: 280px;
  padding: 16px;
}

/* ===== 最近笔记 ===== */
.recent-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.view-all {
  font-size: 13px;
  color: #14b8a6;
  text-decoration: none;
  font-weight: 500;
}

.view-all:hover { color: #0d9488; }

.recent-list {
  padding: 0 16px;
}

.recent-item {
  padding: 14px 0;
  border-bottom: 1px solid #f0fdfa;
  cursor: pointer;
  transition: all 0.15s ease;
}

.recent-item:last-child { border-bottom: none; }

.recent-item:hover .recent-title { color: #14b8a6; }

.recent-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 6px;
  transition: color 0.15s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recent-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.recent-tag {
  font-size: 11px;
  padding: 2px 8px;
  background: #f0fdfa;
  color: #0d9488;
  border-radius: 10px;
}

.recent-time {
  font-size: 12px;
  color: var(--text-secondary);
  margin-left: auto;
}

.recent-empty {
  padding: 24px;
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary);
}

@media (max-width: 1200px) {
  .quick-actions { grid-template-columns: repeat(2, 1fr); }
  .main-grid { grid-template-columns: 1fr; }
  .chart-row-2 { grid-template-columns: 1fr; }
}
</style>
