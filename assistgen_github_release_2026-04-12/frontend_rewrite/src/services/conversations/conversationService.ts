import { deleteJson, getJson, postJson, putJson } from '../http/apiClient'
import type {
  ApiResponse,
  ConversationMessage,
  ConversationSummary,
  CreateConversationRequest,
  RenameConversationRequest,
} from '../../shared/types/api'

export async function listUserConversations(userId: string): Promise<ConversationSummary[]> {
  const res = await getJson<ApiResponse<ConversationSummary[]>>(
    `/api/conversations/user/${encodeURIComponent(userId)}`,
  )
  return res.data ?? []
}

export async function getConversationMessages(conversationId: string): Promise<ConversationMessage[]> {
  const res = await getJson<ApiResponse<ConversationMessage[]>>(
    `/api/conversations/${encodeURIComponent(conversationId)}/messages`,
  )
  return res.data ?? []
}

export async function createConversation(payload: CreateConversationRequest): Promise<ConversationSummary> {
  const res = await postJson<ApiResponse<ConversationSummary>>('/api/conversations', payload)
  return res.data
}

export async function renameConversation(conversationId: string, payload: RenameConversationRequest): Promise<ConversationSummary> {
  const res = await putJson<ApiResponse<ConversationSummary>>(
    `/api/conversations/${encodeURIComponent(conversationId)}/name`,
    payload,
  )
  return res.data
}

export async function deleteConversation(conversationId: string): Promise<boolean> {
  const res = await deleteJson<ApiResponse<{ deleted: boolean }>>(
    `/api/conversations/${encodeURIComponent(conversationId)}`,
  )
  return Boolean(res.data?.deleted)
}

