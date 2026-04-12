import { computed, ref } from 'vue'
import {
  createConversation,
  deleteConversation,
  getConversationMessages,
  listUserConversations,
  renameConversation,
} from '../services/conversations/conversationService'
import type { ConversationMessage, ConversationSummary } from '../shared/types/api'

export function useConversations() {
  const userId = ref('demo-user')
  const conversations = ref<ConversationSummary[]>([])
  const selectedConversationId = ref('')
  const selectedMessages = ref<ConversationMessage[]>([])
  const loadingConversations = ref(false)
  const loadingMessages = ref(false)
  const error = ref('')

  const selectedConversation = computed(() => {
    return conversations.value.find((item) => item.id === selectedConversationId.value) ?? null
  })

  async function loadMessages(conversationId: string) {
    if (!conversationId) {
      selectedMessages.value = []
      return
    }

    loadingMessages.value = true
    error.value = ''
    try {
      selectedMessages.value = await getConversationMessages(conversationId)
    } catch (err) {
      selectedMessages.value = []
      error.value = String(err)
    } finally {
      loadingMessages.value = false
    }
  }

  async function refreshConversations() {
    loadingConversations.value = true
    error.value = ''
    try {
      const items = await listUserConversations(userId.value)
      conversations.value = items

      const hasSelection = items.some((item) => item.id === selectedConversationId.value)
      const fallbackId = items[0]?.id ?? ''
      selectedConversationId.value = hasSelection ? selectedConversationId.value : fallbackId

      if (selectedConversationId.value) {
        await loadMessages(selectedConversationId.value)
      } else {
        selectedMessages.value = []
      }
    } catch (err) {
      conversations.value = []
      selectedConversationId.value = ''
      selectedMessages.value = []
      error.value = String(err)
    } finally {
      loadingConversations.value = false
    }
  }

  async function loadForUser(nextUserId?: string) {
    if (nextUserId !== undefined) {
      userId.value = nextUserId
    }
    await refreshConversations()
  }

  async function selectConversation(conversationId: string) {
    selectedConversationId.value = conversationId
    await loadMessages(conversationId)
  }

  async function createNewConversation(name: string) {
    error.value = ''
    const created = await createConversation({ user_id: userId.value, name })
    selectedConversationId.value = created.id
    await refreshConversations()
  }

  async function renameSelectedConversation(name: string) {
    if (!selectedConversationId.value) return
    error.value = ''
    await renameConversation(selectedConversationId.value, { name })
    await refreshConversations()
  }

  async function deleteSelectedConversation() {
    if (!selectedConversationId.value) return
    error.value = ''
    const deleted = await deleteConversation(selectedConversationId.value)
    if (!deleted) return
    selectedConversationId.value = ''
    await refreshConversations()
  }

  return {
    userId,
    conversations,
    selectedConversationId,
    selectedConversation,
    selectedMessages,
    loadingConversations,
    loadingMessages,
    error,
    loadForUser,
    refreshConversations,
    selectConversation,
    createNewConversation,
    renameSelectedConversation,
    deleteSelectedConversation,
  }
}

