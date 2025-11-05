# BANED Pipeline - PowerShell Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BANED Pipeline - Full Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Clean data
Write-Host "`n[1/5] Cleaning data..." -ForegroundColor Yellow
python prep_data.py -i fnn_real.csv -o fnn_real_clean.csv
python prep_data.py -i fnn_fake.csv -o fnn_fake_clean.csv

# Step 2: Generate knowledge base
Write-Host "`n[2/5] Generating knowledge base with Apriori..." -ForegroundColor Yellow
python apriori_algo.py -i fnn_real_clean.csv --min_support 0.10 --out real_support.csv
python apriori_algo.py -i fnn_fake_clean.csv --min_support 0.10 --out fake_support.csv

# Step 3: Merge data
Write-Host "`n[3/5] Merging datasets..." -ForegroundColor Yellow
python merge_data.py fnn_real_clean.csv fnn_fake_clean.csv fnn_all_clean.csv

# Step 4: Train CNN
Write-Host "`n[4/5] Training CNN with MC Dropout..." -ForegroundColor Yellow
python cnn.py -r fnn_real_clean.csv -f fnn_fake_clean.csv --epochs 5 --mc_samples 20

# Step 5: Calculate metrics
Write-Host "`n[5/5] Calculating calibrated metrics..." -ForegroundColor Yellow
python calculate.py fnn_all_clean.csv --probabilities fnn_all_clean_cnn_prob.npy --fake_support fake_support.csv --real_support real_support.csv --limit 20

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Pipeline completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
