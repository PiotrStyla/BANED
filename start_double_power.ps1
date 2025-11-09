# BANED Double Power - Startup Script
# Starts the enhanced API with neural verification

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  BANED DOUBLE POWER - Fake News Detection" -ForegroundColor Cyan
Write-Host "  Neural Verified System" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}
$pythonVersion = python --version
Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check dependencies
Write-Host "[2/4] Checking dependencies..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "torch", "numpy", "pydantic")
$missing = @()

foreach ($pkg in $packages) {
    $check = python -c "import $pkg" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missing += $pkg
        Write-Host "✗ Missing: $pkg" -ForegroundColor Red
    } else {
        Write-Host "✓ Found: $pkg" -ForegroundColor Green
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Installing missing packages..." -ForegroundColor Yellow
    $missingStr = $missing -join " "
    python -m pip install $missingStr
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install packages" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Check models
Write-Host "[3/4] Checking for models..." -ForegroundColor Yellow
$modelsExist = $false

if (Test-Path "models/model_pl.pth") {
    Write-Host "✓ Found: Polish model (models/model_pl.pth)" -ForegroundColor Green
    $modelsExist = $true
}
if (Test-Path "models/model.pth") {
    Write-Host "✓ Found: English model (models/model.pth)" -ForegroundColor Green
    $modelsExist = $true
}

if (-not $modelsExist) {
    Write-Host "⚠ Warning: No trained models found" -ForegroundColor Yellow
    Write-Host "  The API will work with verification-only mode" -ForegroundColor Yellow
    Write-Host "  To enable full double power, train models first:" -ForegroundColor Yellow
    Write-Host "    python cnn.py -r fnn_pl_hard_10k_real.csv -f fnn_pl_hard_10k_fake.csv" -ForegroundColor Cyan
}
Write-Host ""

# Start server
Write-Host "[4/4] Starting BANED Double Power API..." -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  API Server Starting..." -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📡 API URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🌐 Web Interface: file://$(Get-Location)/static/double_power.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Features Enabled:" -ForegroundColor Yellow
Write-Host "  🧠 Power 1: CNN Neural Network" -ForegroundColor Green
Write-Host "  ✓ Power 2: Logical Verification" -ForegroundColor Green
Write-Host "  🌍 Bilingual: Polish & English" -ForegroundColor Green
Write-Host "  🔍 Fact Database" -ForegroundColor Green
Write-Host "  ⚡ MC Dropout Uncertainty" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the API
python api_double_power.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Server failed to start" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Red
    exit 1
}
