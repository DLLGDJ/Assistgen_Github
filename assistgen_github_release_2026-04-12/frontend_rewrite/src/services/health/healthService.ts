import { getJson } from '../http/apiClient'
import type { HealthResponse } from '../../shared/types/api'

export async function fetchHealth(): Promise<HealthResponse> {
  return getJson<HealthResponse>('/health')
}

