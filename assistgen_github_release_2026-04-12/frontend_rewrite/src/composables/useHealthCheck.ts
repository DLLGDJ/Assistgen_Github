import { ref } from 'vue'
import { fetchHealth } from '../services/health/healthService'

export function useHealthCheck() {
  const statusText = ref('未检查')
  const loading = ref(false)

  async function runHealthCheck() {
    if (loading.value) return
    loading.value = true
    try {
      const data = await fetchHealth()
      statusText.value = `${data.status} (${data.service})`
    } catch (err) {
      statusText.value = String(err)
    } finally {
      loading.value = false
    }
  }

  return {
    statusText,
    loading,
    runHealthCheck
  }
}

