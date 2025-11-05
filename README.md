# BANED - Minimal Test Setup

Minimalna struktura do testowania pipeline'u BANED (Bayesian-Augmented News Evaluation and Detection).

## Instalacja

```powershell
pip install -r requirements.txt
```

## Szybki start - pełny pipeline

### Krok 1: Czyszczenie danych
```powershell
python prep_data.py -i fnn_real.csv -o fnn_real_clean.csv
python prep_data.py -i fnn_fake.csv -o fnn_fake_clean.csv
```

### Krok 2: Generowanie bazy wiedzy (Apriori)
```powershell
python apriori_algo.py -i fnn_real_clean.csv --min_support 0.4 --out real_support.csv
python apriori_algo.py -i fnn_fake_clean.csv --min_support 0.4 --out fake_support.csv
```

### Krok 3: Łączenie danych
```powershell
python merge_data.py fnn_real_clean.csv fnn_fake_clean.csv fnn_all_clean.csv
```

### Krok 4: Trening CNN
```powershell
python cnn.py -r fnn_real_clean.csv -f fnn_fake_clean.csv --epochs 5 --mc_samples 20
```

### Krok 5: Kalkulacja metryk
```powershell
python calculate.py fnn_all_clean.csv --probabilities fnn_all_clean_cnn_prob.npy --fake_support fake_support.csv --real_support real_support.csv --limit 20
```

## Szybkie uruchomienie

Użyj skryptu `run_all.ps1` aby uruchomić cały pipeline jedną komendą:
```powershell
.\run_all.ps1
```

## Pliki wyjściowe

- `*_clean.csv` - oczyszczone dane
- `*_support.csv` - wzorce z bazy wiedzy
- `fnn_all_clean_cnn_prob.npy` - predykcje CNN
- Metryki wyświetlane w konsoli
