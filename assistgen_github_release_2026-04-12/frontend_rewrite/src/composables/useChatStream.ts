import { ref } from 'vue'
import { streamChat } from '../services/chat/chatService'

export type ChatContext = {
  userId?: string
  conversationId?: string
}

export function useChatStream() {
  const input = ref('')
  const output = ref('')
  const loading = ref(false)

  async function sendStream(context: ChatContext = {}) {
    if (!input.value.trim() || loading.value) return
    loading.value = true
    output.value = ''

    try {
      await streamChat(input.value, (delta) => {
        output.value += `${delta}\n`
      }, context)
    } catch (err) {
      output.value = `流式请求失败: ${String(err)}`
    } finally {
      loading.value = false
    }
  }

  return {
    input,
    output,
    loading,
    sendStream
  }
}
