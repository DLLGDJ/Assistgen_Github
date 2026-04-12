param(
    [switch]$PrepareOnly
)

$rawArgs = @($args) + @($MyInvocation.UnboundArguments)
$envPrepareOnly = $env:ASSISTGEN_FRONTEND_PREPARE_ONLY
$invocationLine = [string]$MyInvocation.Line
$isPrepareOnly =
    $PrepareOnly -or
    ($rawArgs -contains "-PrepareOnly") -or
    ($rawArgs -contains "/PrepareOnly") -or
    ($invocationLine -match "(?i)[-/]PrepareOnly") -or
    ($envPrepareOnly -in @("1", "true", "TRUE", "yes", "YES"))

Set-Location "$PSScriptRoot\..\frontend_rewrite"

$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmCmd) {
    $nodeCandidates = @(
        "C:\Program Files\nodejs",
        "C:\Program Files (x86)\nodejs"
    )

    foreach ($candidate in $nodeCandidates) {
        if (Test-Path "$candidate\npm.cmd") {
            $env:Path = "$candidate;$env:Path"
            $npmCmd = Get-Command npm -ErrorAction SilentlyContinue
            if ($npmCmd) {
                Write-Host "检测到 Node.js 安装目录，已临时补全 PATH: $candidate"
                break
            }
        }
    }
}

if (-not $npmCmd) {
    Write-Error "未检测到 npm。请先安装 Node.js LTS，或重开终端以刷新 PATH 后重试。"
    exit 1
}

if (-not (Test-Path "node_modules")) {
    npm install
}

if ($isPrepareOnly) {
    Write-Host "前端依赖检查完成（PrepareOnly）。"
    exit 0
}

$env:VITE_API_BASE_URL = "http://localhost:8100"
npm run dev





