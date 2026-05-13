const runtimeEnv = (import.meta as { env?: { VITE_API_BASE_URL?: string; DEV?: boolean } }).env

export const API_BASE_URL = runtimeEnv?.VITE_API_BASE_URL ?? (runtimeEnv?.DEV ? 'http://localhost:8100' : '')



