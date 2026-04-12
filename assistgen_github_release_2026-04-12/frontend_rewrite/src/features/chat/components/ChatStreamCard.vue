<script setup lang="ts">
import { toRefs } from 'vue'
import { useChatStream } from '../../../composables/useChatStream'

const props = defineProps<{
  userId: string
  conversationId: string
  conversationName: string
}>()

const { userId, conversationId, conversationName } = toRefs(props)
const { input, output, loading, sendStream } = useChatStream()

async function handleSend() {
  await sendStream({
    userId: userId.value,
    conversationId: conversationId.value,
  })
}
</script>

<template>
  <section class="card">
    <div class="header-row">
      <h2>流式对话</h2>
      <small>当前会话：{{ conversationName || '未选择会话' }}</small>
    </div>
    <textarea v-model="input" rows="4" placeholder="输入问题" />
    <button @click="handleSend" :disabled="loading">
      {{ loading ? '请求中...' : '发送流式请求' }}
    </button>
    <pre>{{ output }}</pre>
  </section>
</template>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
}
textarea {
  width: 100%;
  margin-bottom: 8px;
}
pre {
  background: #f7f7f7;
  border-radius: 4px;
  padding: 8px;
  white-space: pre-wrap;
}
</style>
