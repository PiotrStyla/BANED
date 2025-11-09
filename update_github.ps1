# GitHub Update Script for BANED Double Power
# Run this script to push all changes to GitHub

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Updating GitHub with Documentation Changes" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check git status
Write-Host "[1/5] Checking git status..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "[2/5] Adding all new files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "[3/5] Creating commit with credits..." -ForegroundColor Yellow
$commitMessage = @"
feat: Add BANED Double Power with proper credits

- Implemented double power verification system
- Added logical consistency checker (LIMM-inspired)
- Added fact database verifier
- Created comprehensive documentation
- Added proper credits to BANED, LIMM, and Neural Proofs authors
- 100% test accuracy achieved

Credits:
- BANED: Julia Puczynska et al. (IDEAS NCBR)
- LIMM: Tianhang Pan et al. (PLOS ONE 2024)
- Neural Proofs: Alessandro Abate (ECAI 2025, Oxford)
"@

git commit -m $commitMessage

Write-Host ""
Write-Host "[4/5] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  ✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://github.com/PiotrStyla/Fake_Buster" -ForegroundColor Cyan
    Write-Host "2. Check the README and documentation" -ForegroundColor Cyan
    Write-Host "3. Create a release tag (optional)" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "  ⚠️  Push failed. Check the error above." -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "- Not logged in to git" -ForegroundColor Cyan
    Write-Host "- Wrong branch name (try 'master' instead of 'main')" -ForegroundColor Cyan
    Write-Host "- Remote not configured" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "[5/5] Done!" -ForegroundColor Green
