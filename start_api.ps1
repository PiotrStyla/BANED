# Start BANED API Server
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "BANED API Server" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "torch", "numpy")
$missingPackages = @()

foreach ($package in $packages) {
    $installed = python -m pip show $package 2>$null
    if (-not $installed) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "Missing packages: $($missingPackages -join ', ')" -ForegroundColor Red
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
    Write-Host ""
}

# Check if model is prepared
if (-not (Test-Path "models/model.pth")) {
    Write-Host "Model not found! Preparing deployment..." -ForegroundColor Yellow
    python prepare_deployment.py
    Write-Host ""
    
    if (-not (Test-Path "models/model.pth")) {
        Write-Host "⚠️  WARNING: Model weights not found!" -ForegroundColor Red
        Write-Host "The API will start but predictions will fail." -ForegroundColor Red
        Write-Host ""
        Write-Host "To fix this, train a model first:" -ForegroundColor Yellow
        Write-Host "  python cnn.py -r fnn_real_10k_clean.csv -f fnn_fake_10k_clean.csv --epochs 30 --test_split 0.2" -ForegroundColor Yellow
        Write-Host ""
    }
}

# Start server
Write-Host "Starting API server..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Web Interface: Open static/index.html in your browser" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
