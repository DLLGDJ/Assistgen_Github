<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useConversations } from '../../../composables/useConversations'

const emit = defineEmits<{
  (e: 'state-change', payload: { userId: string; conversationId: string; conversationName: string }): void
}>()

const {
  userId,
  conversations,
  selectedConversationId,
  selectedConversation,
  selectedMessages,
  loadingConversations,
  loadingMessages,
  error,
  loadForUser,
  selectConversation,
  createNewConversation,
  renameSelectedConversation,
  deleteSelectedConversation,
} = useConversations()

const createName = ref('新会话')
const renameName = ref('')

const selectedTitle = computed(() => selectedConversation.value?.name ?? '未选择会话')

function emitState() {
  emit('state-change', {
    userId: userId.value,
    conversationId: selectedConversationId.value,
    conversationName: selectedConversation.value?.name ?? '',
  })
}

watch([userId, selectedConversation], emitState, { immediate: true })

onMounted(() => {
  void loadForUser()
})

async function handleLoadUser() {
  await loadForUser()
  emitState()
}

async function handleCreate() {
  const name = createName.value.trim() || '新会话'
  await createNewConversation(name)
  createName.value = '新会话'
  emitState()
}

async function handleRename() {
  const name = renameName.value.trim()
  if (!name || !selectedConversationId.value) return
  await renameSelectedConversation(name)
  emitState()
}

async function handleDelete() {
  await deleteSelectedConversation()
  emitState()
}

async function handlePickConversation(id: string) {
  await selectConversation(id)
  emitState()
}
</script>

<template>
  <section class="card">
    <div class="header-row">
      <h2>会话中心</h2>
      <button @click="handleLoadUser" :disabled="loadingConversations">刷新列表</button>
    </div>

    <div class="toolbar">
      <label>
        用户 ID
        <input v-model="userId" type="text" placeholder="demo-user" />
      </label>
      <button @click="handleLoadUser" :disabled="loadingConversations">加载会话</button>
    </div>

    <div class="toolbar spaced-top">
      <label>
        新会话名称
        <input v-model="createName" type="text" placeholder="新会话" />
      </label>
      <button @click="handleCreate">创建会话</button>
    </div>

    <div class="layout spaced-top">
      <div>
        <h3>会话列表</h3>
        <p v-if="loadingConversations">会话加载中...</p>
        <p v-else-if="conversations.length === 0">暂无会话</p>
        <ul class="list">
          <li v-for="item in conversations" :key="item.id">
            <button
              class="item-btn"
              :class="{ active: item.id === selectedConversationId }"
              @click="handlePickConversation(item.id)"
            >
              <span>{{ item.name }}</span>
              <small>{{ item.updated_at }}</small>
            </button>
          </li>
        </ul>
      </div>

      <div>
        <h3>{{ selectedTitle }}</h3>
        <p v-if="loadingMessages">历史消息加载中...</p>
        <p v-else-if="selectedMessages.length === 0">暂无历史消息</p>
        <div v-else class="messages">
          <article v-for="message in selectedMessages" :key="message.id" class="message">
            <div class="message-meta">
              <strong>{{ message.role }}</strong>
              <span>{{ message.created_at }}</span>
            </div>
            <p>{{ message.content }}</p>
          </article>
        </div>
      </div>
    </div>

    <div class="toolbar spaced-top">
      <label>
        重命名当前会话
        <input v-model="renameName" type="text" placeholder="输入新名称" :disabled="!selectedConversationId" />
      </label>
      <button @click="handleRename" :disabled="!selectedConversationId">保存名称</button>
      <button class="danger" @click="handleDelete" :disabled="!selectedConversationId">删除当前会话</button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
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
  align-items: center;
  gap: 12px;
}
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: end;
}
.spaced-top {
  margin-top: 12px;
}
label {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
input {
  min-width: 220px;
  padding: 8px 10px;
}
.layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 16px;
}
.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.item-btn {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  text-align: left;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #fff;
}
.item-btn.active {
  border-color: #3b82f6;
  background: #eff6ff;
}
.messages {
  display: grid;
  gap: 10px;
}
.message {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 10px 12px;
  background: #fafafa;
}
.message-meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 12px;
  color: #666;
}
.error {
  color: #b91c1c;
  margin-top: 12px;
}
.danger {
  color: #fff;
  background: #dc2626;
}
@media (max-width: 860px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>

