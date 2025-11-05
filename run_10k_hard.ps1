# BANED Pipeline - 10K Hard Examples
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BANED Pipeline - 10K HARD EXAMPLES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Clean data
Write-Host "`n[1/5] Cleaning data..." -ForegroundColor Yellow
python prep_data.py -i fnn_real_hard_1k.csv -o fnn_real_hard_10k_clean.csv
python prep_data.py -i fnn_fake_hard_1k.csv -o fnn_fake_hard_10k_clean.csv

# Step 2: Generate knowledge base
Write-Host "`n[2/5] Generating knowledge base..." -ForegroundColor Yellow
python apriori_algo.py -i fnn_real_hard_10k_clean.csv --min_support 0.10 --out real_hard_10k_support.csv
python apriori_algo.py -i fnn_fake_hard_10k_clean.csv --min_support 0.10 --out fake_hard_10k_support.csv

# Step 3: Merge data
Write-Host "`n[3/5] Merging datasets..." -ForegroundColor Yellow
python merge_data.py fnn_real_hard_10k_clean.csv fnn_fake_hard_10k_clean.csv fnn_all_hard_10k_clean.csv

# Step 4: Train CNN (80/20 split)
Write-Host "`n[4/5] Training CNN (this may take several minutes)..." -ForegroundColor Yellow
python cnn.py -r fnn_real_hard_10k_clean.csv -f fnn_fake_hard_10k_clean.csv --epochs 30 --mc_samples 30 --out_probs fnn_all_hard_10k_cnn_prob.npy --test_split 0.2 --batch_size 16 --seed 42

# Step 5: Calculate metrics
Write-Host "`n[5/5] Calculating metrics..." -ForegroundColor Yellow
python calculate_optimized.py fnn_all_hard_10k_clean.csv --probabilities fnn_all_hard_10k_cnn_prob.npy --fake_support fake_hard_10k_support.csv --real_support real_hard_10k_support.csv --limit 30

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "10K Hard pipeline completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
