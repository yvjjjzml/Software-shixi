<template>
  <el-tag :type="tagType" :effect="effect" size="small">{{ label }}</el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
  effect?: 'dark' | 'light' | 'plain'
}>()

const statusMap: Record<string, { label: string; type: string }> = {
  draft: { label: '草稿', type: 'warning' },
  published: { label: '已发布', type: 'success' },
  archived: { label: '已归档', type: 'info' }
}

const label = computed(() => statusMap[props.status]?.label || props.status)
const tagType = computed(() => (statusMap[props.status]?.type || 'info') as any)
const effect = computed(() => props.effect || 'light')
</script>
