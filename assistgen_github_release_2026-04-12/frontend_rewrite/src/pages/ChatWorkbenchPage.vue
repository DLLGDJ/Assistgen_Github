<script setup lang="ts">
import { ref } from 'vue'
import HealthCard from '../features/health/components/HealthCard.vue'
import ChatStreamCard from '../features/chat/components/ChatStreamCard.vue'
import ConversationPanel from '../features/conversations/components/ConversationPanel.vue'

const activeUserId = ref('demo-user')
const activeConversationId = ref('')
const activeConversationName = ref('未选择会话')

function handleConversationStateChange(payload: {
  userId: string
  conversationId: string
  conversationName: string
}) {
  activeUserId.value = payload.userId
  activeConversationId.value = payload.conversationId
  activeConversationName.value = payload.conversationName || '未选择会话'
}
</script>

<template>
  <main class="page">
    <h1>AssistGen 合规原创改版 - 前端模块化版</h1>
    <HealthCard />
    <ConversationPanel @state-change="handleConversationStateChange" />
    <ChatStreamCard
      :user-id="activeUserId"
      :conversation-id="activeConversationId"
      :conversation-name="activeConversationName"
    />
  </main>
</template>

<style scoped>
.page {
  max-width: 960px;
  margin: 24px auto;
  font-family: Arial, sans-serif;
}
</style>
