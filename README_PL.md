# BANED - Bayesian-Augmented News Evaluation and Detection

Minimalna implementacja pipeline'u BANED do wykrywania fake newsów, łącząca CNN z MC Dropout oraz bazę wiedzy opartą na algorytmie Apriori.

## 🚀 Szybki Start

### Instalacja

```bash
pip install -r requirements.txt
```

### Uruchomienie pełnego pipeline'u

```bash
# Windows PowerShell
.\run_all.ps1

# Lub krok po kroku
python prep_data.py -i fnn_real.csv -o fnn_real_clean.csv
python prep_data.py -i fnn_fake.csv -o fnn_fake_clean.csv
python apriori_algo.py -i fnn_real_clean.csv --min_support 0.10 --out real_support.csv
python apriori_algo.py -i fnn_fake_clean.csv --min_support 0.10 --out fake_support.csv
python merge_data.py fnn_real_clean.csv fnn_fake_clean.csv fnn_all_clean.csv
python cnn.py -r fnn_real_clean.csv -f fnn_fake_clean.csv --epochs 5 --mc_samples 20
python calculate.py fnn_all_clean.csv --probabilities fnn_all_clean_cnn_prob.npy --fake_support fake_support.csv --real_support real_support.csv
```

## 📁 Struktura Projektu

```
baned-test/
├── fnn_real.csv              # Dataset prawdziwych wiadomości (60 przykładów)
├── fnn_fake.csv              # Dataset fake newsów (73 przykłady)
├── prep_data.py              # Preprocessing i czyszczenie tekstu
├── apriori_algo.py           # Generowanie bazy wiedzy (Apriori)
├── cnn.py                    # CNN z MC Dropout
├── calculate.py              # Fuzja predykcji CNN + KB, metryki
├── merge_data.py             # Łączenie CSV z labelkami
├── analyze_patterns.py       # Analiza wzorców Knowledge Base
├── compare_results.py        # Szczegółowe porównanie wyników
├── run_all.ps1              # Automatyczny pipeline (Windows)
├── requirements.txt          # Zależności Python
└── README.md                 # Dokumentacja
```

## 🎯 Pipeline BANED

### 1. Preprocessing (`prep_data.py`)
- Czyszczenie tekstu (lowercase, usuwanie znaków specjalnych, URL)
- Normalizacja białych znaków
- Filtrowanie pustych wierszy

### 2. Knowledge Base (`apriori_algo.py`)
- Algorytm Apriori do znajdowania częstych wzorców słów
- Separate patterns dla real i fake news
- Parametr `min_support` kontroluje próg częstości (0.10-0.20 recommended)

### 3. Model CNN (`cnn.py`)
- Prosta architektura CNN z embedding layer
- 3 convolution filters (kernel size: 3, 4, 5)
- Dropout dla regularizacji i MC Dropout
- MC Dropout inference (20 stochastycznych przejść) dla oszacowania niepewności

### 4. Fuzja i Metryki (`calculate.py`)
- Łączenie predykcji CNN z Knowledge Base support
- Kalkulacja accuracy, per-class metrics
- Analiza wpływu KB na klasyfikację

### 5. Analiza (`analyze_patterns.py`, `compare_results.py`)
- Szczegółowa analiza wzorców w KB
- Porównanie predykcji CNN vs BANED (fused)
- Identyfikacja przypadków gdzie KB pomaga/szkodzi

## 📊 Wyniki (133 próbki)

### Dataset
- **60 Real News**: Realistyczne wiadomości (polityka, nauka, gospodarka)
- **73 Fake News**: Absurdalne teorie spiskowe i fałszywe twierdzenia zdrowotne
- **682 słów** w słowniku

### Accuracy
- **CNN**: 100% (133/133)
- **BANED (fused)**: 100% (133/133)

### Knowledge Base Patterns

**Real News (4 wzorce):**
- `for` (15.0%) - oficjalne komunikaty
- `new` (11.7%) - odkrycia i innowacje
- `announces` (10.0%) - ogłoszenia
- `department` (10.0%) - instytucje

**Fake News (8 wzorców):**
- `all` (17.8%) - absolutne twierdzenia
- `in` (17.8%) - pseudo-naukowy kontekst
- `for` (12.3%)
- `to` (11.0%)
- `secret` (11.0%) - teorie spiskowe
- `cures` (9.6%) - fałszywe lekarstwa
- `by` (9.6%)
- `eating` (9.6%) - absurdalne diety

### Średnia liczba dopasowanych wzorców
- Real news: 0.47 real patterns, 0.22 fake patterns
- Fake news: 0.14 real patterns, 0.99 fake patterns ✅

## 🔬 Kluczowe Spostrzeżenia

### ✅ Co działa:
1. Fake news ma charakterystyczne wzorce językowe ("all", "secret", "cures")
2. KB poprawnie identyfikuje typ wiadomości (0.99 fake patterns w fake news)
3. CNN osiąga perfekcyjną accuracy na tym zbiorze

### ⚠️ Uwagi:
1. Słowa "for", "in", "to" występują w obu typach - false positives
2. KB może obniżać pewność dla poprawnie sklasyfikowanych tekstów
3. Potrzebne jest filtrowanie wspólnych słów

## 🛠️ Parametry do eksperymentowania

### Apriori
```bash
--min_support 0.10  # Niższe = więcej wzorców (0.05-0.20)
```

### CNN Training
```bash
--epochs 5          # Liczba epok (3-10)
--dropout_p 0.5     # Dropout probability (0.3-0.7)
--mc_samples 20     # MC Dropout samples (10-50)
--batch_size 8      # Batch size (4-16)
```

### Knowledge Base Fusion
```bash
--limit 20          # Top-K patterns to use (10-50)
```

## 📈 Rozszerzanie Datasetu

Dodaj więcej przykładów do `fnn_real.csv` i `fnn_fake.csv`:

```csv
text
Your news headline or text here
Another example
...
```

Zalecane minimum: 50+ przykładów każdego typu dla lepszych wzorców KB.

## 🤝 Wkład w projekt

Fork oryginalnego repo: [BANED Repository](https://github.com/PiotrStyla/BANED)

### Zmiany w tym forku:
- ✅ Uproszczona, standalone implementacja
- ✅ Kompletne przykładowe dane (60 real + 73 fake)
- ✅ Zautomatyzowany pipeline (run_all.ps1)
- ✅ Narzędzia do analizy wzorców KB
- ✅ Szczegółowa dokumentacja PL

## 📚 Referencje

Bazowane na research paper BANED (Bayesian-Augmented News Evaluation and Detection).

## 📄 Licencja

Zgodnie z licencją oryginalnego repozytorium.

---

**Autor forka**: PiotrStyla  
**Data**: Listopad 2025
