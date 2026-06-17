<template>
  <div class="tag-cloud">
    <el-tag v-for="tag in tags" :key="tag.name" :type="getTagType(tag.count)"
      :size="getTagSize(tag.count)" effect="plain" class="cloud-tag"
      @click="$emit('select', tag.name)">
      {{ tag.name }} ({{ tag.count }})
    </el-tag>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  tags: Array<{ name: string; count: number }>
}>()

defineEmits(['select'])

function getTagType(count: number): '' | 'success' | 'warning' | 'danger' | 'info' {
  if (count >= 10) return 'danger'
  if (count >= 5) return 'warning'
  if (count >= 3) return 'success'
  return 'info'
}

function getTagSize(count: number): '' | 'small' | 'large' {
  if (count >= 10) return 'large'
  if (count >= 5) return ''
  return 'small'
}
</script>

<style scoped>
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px 0;
}

.cloud-tag {
  cursor: pointer;
  transition: transform 0.2s;
}

.cloud-tag:hover {
  transform: scale(1.1);
}
</style>
