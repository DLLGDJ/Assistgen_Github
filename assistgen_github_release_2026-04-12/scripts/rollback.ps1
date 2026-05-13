param(
    [string]$BackendPort = "8000",
    [string]$FrontendPort = "5173"
)

Write-Host "[rollback] Switching back to original project endpoints..."
Write-Host "[rollback] Backend should point to original service port: $BackendPort"
Write-Host "[rollback] Frontend should point to original dev server port: $FrontendPort"
Write-Host "[rollback] This script keeps rollback manual and explicit to avoid accidental process kills."

Write-Host "[rollback] Suggested actions:"
Write-Host "1) Stop rewrite backend/frontend terminals."
Write-Host "2) Start original backend and frontend from their original directories."
Write-Host "3) Verify original /health and UI routing are restored."

