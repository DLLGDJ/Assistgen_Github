param(
    [string]$BasePython = "",
    [switch]$PrepareOnly
)

Set-Location "$PSScriptRoot\..\backend_rewrite"

$projectBasePython = Join-Path (Get-Location) ".python-base\tools\python.exe"
$venvPython = Join-Path (Get-Location) ".venv\Scripts\python.exe"

if (-not (Test-Path $projectBasePython)) {
    Write-Host "Project-local Python runtime not found. Downloading..."
    $pkgPath = Join-Path (Get-Location) "python.3.12.10.nupkg"

    curl.exe -L "https://www.nuget.org/api/v2/package/python/3.12.10" -o $pkgPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to download project-local Python package."
        exit 1
    }

    if (Test-Path ".python-base") {
        Remove-Item ".python-base" -Recurse -Force
    }
    New-Item -ItemType Directory -Path ".python-base" | Out-Null

    tar -xf $pkgPath -C ".python-base"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to extract project-local Python package."
        exit 1
    }

    Remove-Item $pkgPath -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path $venvPython)) {
    if (-not $BasePython) {
        if (Test-Path $projectBasePython) {
            $BasePython = $projectBasePython
        }
    }

    if (-not $BasePython) {
        $cmd = Get-Command python -ErrorAction SilentlyContinue
        if ($cmd) {
            $BasePython = $cmd.Source
        }
    }

    if (-not $BasePython -or -not (Test-Path $BasePython)) {
        Write-Error "Base Python was not found."
        exit 1
    }

    & $BasePython -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create .venv."
        exit 1
    }
}

& $venvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies."
    exit 1
}

if ($PrepareOnly) {
    Write-Host "Backend virtual environment is ready: $venvPython"
    exit 0
}

& $venvPython -m uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload

