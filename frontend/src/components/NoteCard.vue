<template>
  <el-card shadow="hover" class="note-card" @click="$emit('click')">
    <div class="card-header">
      <h3>{{ note.title }}</h3>
      <StatusBadge :status="note.status" />
    </div>
    <p class="card-content">{{ note.summary || note.content?.slice(0, 100) + '...' }}</p>
    <div class="card-footer">
      <div class="card-tags">
        <el-tag v-for="tag in parsedTags" :key="tag" size="small" type="info" effect="plain">
          {{ tag }}
        </el-tag>
      </div>
      <span class="card-date">{{ note.updated_at?.slice(0, 10) }}</span>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import StatusBadge from './StatusBadge.vue'

const props = defineProps<{ note: any }>()
defineEmits(['click'])

const parsedTags = computed(() => {
  return props.note.tags ? props.note.tags.split(',').map((t: string) => t.trim()).filter(Boolean) : []
})
</script>

<style scoped>
.note-card {
  cursor: pointer;
  transition: transform 0.2s;
  border-radius: 8px;
}

.note-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.card-header h3 {
  font-size: 15px;
  color: #303133;
  flex: 1;
  margin-right: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-content {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.card-date {
  font-size: 12px;
  color: #c0c4cc;
}
</style>
