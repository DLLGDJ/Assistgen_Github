const API_BASE = (import.meta as { env?: { VITE_API_BASE_URL?: string } }).env?.VITE_API_BASE_URL ?? 'http://localhost:8100'

export async function fetchHealth(): Promise<{ status: string; service: string }> {
  const res = await fetch(`${API_BASE}/health`)
  if (!res.ok) {
    throw new Error(`health check failed: ${res.status}`)
  }
  return res.json()
}

export function streamChat(message: string, onDelta: (chunk: string) => void): Promise<void> {
  return new Promise((resolve, reject) => {
    const url = `${API_BASE}/api/chat`
    const source = new EventSourcePolyfill(url, {
      headers: { 'Content-Type': 'application/json' },
      payload: JSON.stringify({ message, stream: true }),
      method: 'POST'
    })

    source.onmessage = (e: MessageEvent) => {
      if (e.data === '[DONE]') {
        source.close()
        resolve()
        return
      }
      try {
        const data = JSON.parse(e.data) as { delta?: string }
        if (data.delta) onDelta(data.delta)
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

class EventSourcePolyfill {
  private xhr: XMLHttpRequest
  onmessage: ((ev: MessageEvent) => void) | null = null
  onerror: (() => void) | null = null

  constructor(url: string, init: { headers: Record<string, string>; payload: string; method: string }) {
    this.xhr = new XMLHttpRequest()
    this.xhr.open(init.method, url)
    Object.entries(init.headers).forEach(([k, v]) => this.xhr.setRequestHeader(k, v))

    let processedIndex = 0
    this.xhr.onreadystatechange = () => {
      if (this.xhr.readyState >= 3) {
        const next = this.xhr.responseText.slice(processedIndex)
        processedIndex = this.xhr.responseText.length
        for (const raw of next.split('\n\n')) {
          const line = raw.trim()
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
