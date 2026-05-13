import { API_BASE_URL } from '../../shared/config/env'

export function buildApiUrl(path: string): string {
  const prefix = API_BASE_URL.replace(/\/$/, '')
  return prefix ? `${prefix}${path}` : path
}

type RequestBody = Record<string, unknown> | unknown[] | string | number | boolean | null

type RequestOptions = {
  method?: string
  body?: RequestBody
  headers?: Record<string, string>
}

async function requestJson<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const res = await fetch(buildApiUrl(path), {
    method: options.method ?? 'GET',
    headers: {
      ...(options.body === undefined ? {} : { 'Content-Type': 'application/json' }),
      ...(options.headers ?? {})
    },
    body: options.body === undefined ? undefined : JSON.stringify(options.body)
  })

  if (!res.ok) {
    throw new Error(`request failed: ${res.status}`)
  }

  return (await res.json()) as T
}

export async function getJson<T>(path: string): Promise<T> {
  return requestJson<T>(path)
}

export async function postJson<T>(path: string, body?: RequestBody): Promise<T> {
  return requestJson<T>(path, { method: 'POST', body })
}

export async function putJson<T>(path: string, body?: RequestBody): Promise<T> {
  return requestJson<T>(path, { method: 'PUT', body })
}

export async function deleteJson<T>(path: string): Promise<T> {
  return requestJson<T>(path, { method: 'DELETE' })
}

