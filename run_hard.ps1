# BANED Pipeline - Hard Examples Test
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BANED Pipeline - HARD EXAMPLES TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Clean data
Write-Host "`n[1/5] Cleaning hard examples data..." -ForegroundColor Yellow
python prep_data.py -i fnn_real_hard.csv -o fnn_real_hard_clean.csv
python prep_data.py -i fnn_fake_hard.csv -o fnn_fake_hard_clean.csv

# Step 2: Generate knowledge base
Write-Host "`n[2/5] Generating knowledge base with Apriori..." -ForegroundColor Yellow
python apriori_algo.py -i fnn_real_hard_clean.csv --min_support 0.10 --out real_hard_support.csv
python apriori_algo.py -i fnn_fake_hard_clean.csv --min_support 0.10 --out fake_hard_support.csv

# Step 3: Merge data
Write-Host "`n[3/5] Merging datasets..." -ForegroundColor Yellow
python merge_data.py fnn_real_hard_clean.csv fnn_fake_hard_clean.csv fnn_all_hard_clean.csv

# Step 4: Train CNN
Write-Host "`n[4/5] Training CNN with MC Dropout..." -ForegroundColor Yellow
python cnn.py -r fnn_real_hard_clean.csv -f fnn_fake_hard_clean.csv --epochs 10 --mc_samples 20 --out_probs fnn_all_hard_cnn_prob.npy

# Step 5: Calculate metrics
Write-Host "`n[5/5] Calculating calibrated metrics..." -ForegroundColor Yellow
python calculate.py fnn_all_hard_clean.csv --probabilities fnn_all_hard_cnn_prob.npy --fake_support fake_hard_support.csv --real_support real_hard_support.csv --limit 20

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Hard examples pipeline completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
