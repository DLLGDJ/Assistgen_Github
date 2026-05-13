export type ApiResponse<T> = {
  code: number
  message: string
  data: T
}

export type HealthResponse = {
  status: string
  service: string
}

export type ChatDelta = {
  delta?: string
}

export type ConversationMessage = {
  id: string
  role: string
  content: string
  created_at: string
}

export type ConversationSummary = {
  id: string
  user_id: string
  name: string
  created_at: string
  updated_at: string
  messages?: ConversationMessage[]
}

export type CreateConversationRequest = {
  user_id: string
  name: string
}

export type RenameConversationRequest = {
  name: string
}
