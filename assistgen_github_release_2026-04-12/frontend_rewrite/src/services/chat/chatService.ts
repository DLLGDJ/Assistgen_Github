import { buildApiUrl } from '../http/apiClient'
import type { ChatDelta } from '../../shared/types/api'

type ChatContext = {
  userId?: string
  conversationId?: string
}

export function streamChat(
  message: string,
  onDelta: (chunk: string) => void,
  context: ChatContext = {},
): Promise<void> {
  return new Promise((resolve, reject) => {
    const source = new EventSourcePolyfill(buildApiUrl('/api/chat'), {
      headers: { 'Content-Type': 'application/json' },
      payload: JSON.stringify({
        message,
        stream: true,
        ...(context.userId ? { user_id: context.userId } : {}),
        ...(context.conversationId ? { conversation_id: context.conversationId } : {}),
      }),
      method: 'POST'
    })

    source.onmessage = (e: MessageEvent) => {
      if (e.data === '[DONE]') {
        source.close()
        resolve()
        return
      }
      try {
        const data = JSON.parse(e.data) as ChatDelta
        onDelta(data.delta ?? e.data)
      } catch {
        onDelta(e.data)
      }
    }

    source.onerror = () => {
      source.close()
      reject(new Error('SSE stream interrupted'))
    }
  })
}

type EventSourceInit = {
  headers: Record<string, string>
  payload: string
  method: string
}

class EventSourcePolyfill {
  private xhr: XMLHttpRequest
  onmessage: ((ev: MessageEvent) => void) | null = null
  onerror: (() => void) | null = null

  constructor(url: string, init: EventSourceInit) {
    this.xhr = new XMLHttpRequest()
    this.xhr.open(init.method, url)
    Object.entries(init.headers).forEach(([k, v]) => this.xhr.setRequestHeader(k, v))

    let processedIndex = 0
    this.xhr.onreadystatechange = () => {
      if (this.xhr.readyState >= 3) {
        const next = this.xhr.responseText.slice(processedIndex)
        processedIndex = this.xhr.responseText.length

        for (const block of next.split('\n\n')) {
          const line = block.trim()
          if (!line.startsWith('data:')) continue
          const payload = line.replace(/^data:\s*/, '')
          this.onmessage?.(new MessageEvent('message', { data: payload }))
        }
      }

      if (this.xhr.readyState === 4 && this.xhr.status >= 400) {
        this.onerror?.()
      }
    }

    this.xhr.send(init.payload)
  }

  close(): void {
    this.xhr.abort()
  }
}
