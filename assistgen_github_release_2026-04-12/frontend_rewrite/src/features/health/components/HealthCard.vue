<script setup lang="ts">
import { useHealthCheck } from '../../../composables/useHealthCheck'

const { statusText, loading, runHealthCheck } = useHealthCheck()
</script>

<template>
  <section class="card">
    <h2>服务健康检查</h2>
    <button @click="runHealthCheck" :disabled="loading">
      {{ loading ? '检查中...' : '检查后端健康状态' }}
    </button>
    <p>health: {{ statusText }}</p>
  </section>
</template>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}
</style>

