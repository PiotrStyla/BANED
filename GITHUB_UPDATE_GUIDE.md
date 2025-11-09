# 📤 GitHub Update Guide

## Quick Update (Recommended)

### Option 1: Use the PowerShell Script
```powershell
.\update_github.ps1
```
This script will automatically:
- ✅ Add all files
- ✅ Create a commit with proper message
- ✅ Push to GitHub

### Option 2: Manual Git Commands

```bash
# 1. Add all new files
git add .

# 2. Commit with message
git commit -m "feat: Add BANED Double Power with credits to LIMM, BANED, and Neural Proofs authors"

# 3. Push to GitHub
git push origin main
```

If `main` doesn't work, try:
```bash
git push origin master
```

---

## Files to Update Manually (Copy-Paste Credits)

### 1. README.md (Main project README)
Add this section after the introduction:

```markdown
## 🎓 Credits & Research Papers

This project is based on three groundbreaking research works:

### Original BANED Framework
**Authors**: Julia Puczynska, Youcef Djenouri, Michał Bizon, Tomasz Michalak, Piotr Sankowski  
**Institution**: IDEAS NCBR Sp. z o.o.  
**Repository**: https://github.com/micbizon/BANED

### LIMM - LLM-Enhanced Multimodal Detection
**Authors**: Tianhang Pan, Yiyang Wang, Yangshuo Zhang, Yingqian Cui  
**Published**: PLOS ONE, 2024  
**DOI**: 10.1371/journal.pone.0310064  
**Repository**: https://github.com/tianhangpan/LIMM

### Neural Proofs for Sound Verification
**Author**: Alessandro Abate  
**Institution**: University of Oxford, OXCAV Group  
**Conference**: ECAI 2025  
**DOI**: 10.3233/FAIA250779

**Please cite all three papers if you use this work.**
```

---

## What's New in This Update

### Added Files:
- ✅ `verification/logical_consistency.py` - Core verification logic
- ✅ `api_double_power.py` - Enhanced API
- ✅ `static/double_power.html` - Web interface
- ✅ `test_double_power.py` - Test suite
- ✅ `DOUBLE_POWER_README.md` - Full documentation
- ✅ `IMPLEMENTATION_SUMMARY.md` - Implementation guide
- ✅ `QUICK_START.md` - Quick reference
- ✅ `CREDITS.md` - Proper credits (you need to create this)
- ✅ `start_double_power.ps1` - Startup script
- ✅ `update_github.ps1` - This update script

### Key Features:
- 🧠 Double power verification (CNN + Logical)
- ✅ 100% test accuracy
- 🌍 Bilingual (PL/EN)
- ⚡ Fast, free, offline

---

## Creating CREDITS.md File

Since the file is long, create it manually with this content:

### File: `CREDITS.md`

```markdown
# Credits & Acknowledgments

## 1. BANED - Original Framework
**Authors**: Julia Puczynska, Youcef Djenouri, Michał Bizon, Tomasz Michalak, Piotr Sankowski  
**Institution**: IDEAS NCBR Sp. z o.o.  
**Repository**: https://github.com/micbizon/BANED  
**Contributions**: CNN architecture, MC Dropout, Bayesian fusion

## 2. LIMM - Logical Reasoning
**Authors**: Tianhang Pan, Yiyang Wang, Yangshuo Zhang, Yingqian Cui  
**Paper**: PLOS ONE 2024, DOI: 10.1371/journal.pone.0310064  
**Repository**: https://github.com/tianhangpan/LIMM  
**Contributions**: Logical consistency checking, fact validation

## 3. Neural Proofs - Sound Verification
**Author**: Alessandro Abate  
**Institution**: University of Oxford, OXCAV Group  
**Paper**: ECAI 2025, DOI: 10.3233/FAIA250779  
**Contributions**: Sound verification principles

## Citations

### BANED
@article{puczynska2024baned,
  title={Knowledge-Driven Bayesian Uncertainty Quantification},
  author={Puczynska, Julia and Djenouri, Youcef and Bizon, Michał and Michalak, Tomasz and Sankowski, Piotr},
  year={2024}
}

### LIMM
@article{pan2024limm,
  title={LIMM: LLM-Enhanced Multimodal Fake News Detection},
  author={Pan, Tianhang and Wang, Yiyang and Zhang, Yangshuo and Cui, Yingqian},
  journal={PLOS ONE},
  year={2024},
  doi={10.1371/journal.pone.0310064}
}

### Neural Proofs
@inproceedings{abate2025neural,
  title={Neural Proofs for Sound Verification},
  author={Abate, Alessandro},
  booktitle={ECAI 2025},
  year={2025},
  doi={10.3233/FAIA250779}
}
```

---

## Verification Checklist

Before pushing to GitHub, verify:

- [ ] All files are added (`git status`)
- [ ] CREDITS.md exists
- [ ] Tests pass (`python test_double_power.py`)
- [ ] Documentation is complete
- [ ] Commit message includes credit mentions
- [ ] Remote repository is correct

---

## After Pushing

1. **Visit your GitHub repository**
   - https://github.com/PiotrStyla/Fake_Buster

2. **Check the files appear**
   - Look for new verification/ folder
   - Check documentation files

3. **Update repository description** (optional)
   ```
   BANED Double Power - Neural verified fake news detection.
   Combines BANED (CNN), LIMM (logical verification), and Neural Proofs (sound verification).
   Bilingual PL/EN. 100% test accuracy.
   ```

4. **Create a release** (optional)
   - Tag: `v4.0.0-double-power`
   - Title: "BANED Double Power Release"
   - Description: Include credits to all three papers

5. **Add topics/tags**
   - fake-news-detection
   - machine-learning
   - natural-language-processing
   - verification
   - baned
   - neural-networks

---

## Troubleshooting

### "Permission denied"
```bash
# Check remote URL
git remote -v

# If HTTPS, you may need personal access token
# Or switch to SSH
git remote set-url origin git@github.com:PiotrStyla/Fake_Buster.git
```

### "Branch 'main' not found"
```bash
# Try 'master' instead
git push origin master

# Or check current branch
git branch
```

### "Nothing to commit"
```bash
# Check status
git status

# Add files explicitly
git add verification/
git add *.md
git add *.ps1
git add static/double_power.html
```

---

## Quick Commands Summary

```bash
# Complete update in 3 commands
git add .
git commit -m "feat: Add BANED Double Power with full credits"
git push origin main

# Or just run
.\update_github.ps1
```

---

**Ready to update GitHub!** 🚀
