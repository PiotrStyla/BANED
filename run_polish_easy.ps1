# BANED Polish Training Pipeline - Easy 4K Dataset
# Full pipeline: Generate → Clean → KB → Train → Evaluate

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BANED POLISH TRAINING - EASY 4K" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Generate Polish dataset
Write-Host "[1/7] Generating Polish Easy dataset (4000 samples)..." -ForegroundColor Yellow
python generate_dataset_pl.py --easy_real 2000 --easy_fake 2000 --hard_real 0 --hard_fake 0 --extreme_real 0 --extreme_fake 0 --output_prefix fnn_pl_easy --seed 42

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Dataset generation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Polish dataset generated" -ForegroundColor Green
Write-Host ""

# Step 2: Clean data
Write-Host "[2/7] Cleaning Polish data..." -ForegroundColor Yellow
python prep_data.py fnn_pl_easy_real_easy_2000.csv fnn_pl_easy_fake_easy_2000.csv fnn_pl_easy_all_4k_clean.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Data cleaning failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Data cleaned" -ForegroundColor Green
Write-Host ""

# Step 3: Generate Knowledge Base for Polish
Write-Host "[3/7] Generating Polish Knowledge Base (Apriori)..." -ForegroundColor Yellow
python apriori_algo.py fnn_pl_easy_all_4k_clean.csv real_pl_easy_4k_support.csv fake_pl_easy_4k_support.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: KB generation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Knowledge Base generated" -ForegroundColor Green
Write-Host ""

# Step 4: Merge data
Write-Host "[4/7] Merging Polish datasets..." -ForegroundColor Yellow
python merge_data.py fnn_pl_easy_all_4k_clean.csv fnn_pl_easy_all_4k_merged.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Data merging failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Data merged" -ForegroundColor Green
Write-Host ""

# Step 5: Train CNN on Polish data
Write-Host "[5/7] Training CNN on Polish Easy dataset..." -ForegroundColor Yellow
python cnn.py fnn_pl_easy_real_easy_2000.csv fnn_pl_easy_fake_easy_2000.csv --epochs 10 --mc_samples 50 --output_prob fnn_pl_easy_all_4k_cnn_prob.npy

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: CNN training failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ CNN trained successfully" -ForegroundColor Green
Write-Host ""

# Step 6: Calculate metrics
Write-Host "[6/7] Calculating Polish model performance..." -ForegroundColor Yellow
python calculate_optimized.py fnn_pl_easy_all_4k_clean.csv fnn_pl_easy_all_4k_cnn_prob.npy real_pl_easy_4k_support.csv fake_pl_easy_4k_support.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Metrics calculation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Metrics calculated" -ForegroundColor Green
Write-Host ""

# Step 7: Summary
Write-Host "[7/7] Polish Easy 4K Training Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESULTS SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dataset: Polish Easy 4K (2000 real + 2000 fake)" -ForegroundColor White
Write-Host "Model: models/model.pth (Polish)" -ForegroundColor White
Write-Host "Vocabulary: models/vocab.txt (Polish)" -ForegroundColor White
Write-Host "KB Patterns: real_pl_easy_4k_support.csv + fake_pl_easy_4k_support.csv" -ForegroundColor White
Write-Host ""
Write-Host "Check the terminal output above for accuracy and loss metrics!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review Polish patterns in KB files" -ForegroundColor White
Write-Host "  2. Train Hard dataset: ./run_polish_hard.ps1" -ForegroundColor White
Write-Host "  3. Compare with English model performance" -ForegroundColor White
Write-Host ""
