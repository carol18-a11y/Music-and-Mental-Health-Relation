# 🎧 Music Listening & Mental Health: Statistical Analysis & AudioMental Dashboard

An exploratory data science and statistical computing project investigating whether daily music listening habits (hours listened, preferred genre, listening while working) are correlated with self-reported mental health metrics (**Anxiety, Depression, Insomnia, and OCD**).

Includes an interactive **AudioMental Web Analytics Dashboard** that lets you explore stats, radar profiles, cross-genre affinities, and head-to-head comparisons for all 16 music genres with **zero external dependencies**.

---

## 📑 Table of Contents

- [Quickstart: Launching the Dashboard](#-quickstart-launching-the-dashboard)
- [Project Overview & Research Questions](#-project-overview--research-questions)
- [Key Insights & Statistical Findings](#-key-insights--statistical-findings)
- [Interactive Dashboard Features](#-interactive-dashboard-features)
- [Running the R Statistical Analysis](#-running-the-r-statistical-analysis)
- [Repository Structure](#-repository-structure)
- [Dataset Details](#-dataset-details)
- [Prerequisites & Requirements](#-prerequisites--requirements)
- [Limitations & Methodology](#-limitations--methodology)

---

## ⚡ Quickstart: Launching the Dashboard

You can explore the interactive analytics dashboard in **3 different ways**:

### Option 1: One-Click Shell Script (Recommended)
From the root of this repository, run:
```bash
./start_ui.sh
```
This automatically ensures data is synced and launches the local server at:
👉 **[http://localhost:8080](http://localhost:8080)**

---

### Option 2: Python Local Server
Run the lightweight built-in HTTP server:
```bash
python3 web_dashboard/server.py
```
Then navigate to `http://localhost:8080` in your web browser. (Press `Ctrl + C` to stop).

---

### Option 3: Direct Browser Launch (No Server Required!)
The dashboard is self-contained and pre-bundled. You do not even need a running web server:
- Open `web_dashboard/index.html` directly in Google Chrome, Firefox, Safari, or Microsoft Edge.
- On Linux / Ubuntu:
  ```bash
  xdg-open web_dashboard/index.html
  ```
- On macOS:
  ```bash
  open web_dashboard/index.html
  ```
- On Windows:
  Double-click `web_dashboard/index.html` in File Explorer.

---

## 🔬 Project Overview & Research Questions

This project explores the **Music & Mental Health Survey (MxMH)** dataset from Kaggle, answering key research questions:

1. **Association with Mental Health:** Is there a statistically significant association between daily music listening hours and self-reported anxiety, depression, insomnia, or OCD?
2. **Genre Differences:** How do self-reported mental health indicators differ across listeners of different primary genres?
3. **Listening While Working:** Does listening to music while working correlate with lower or higher anxiety?
4. **Perceived Music Impact:** What percentage of listeners report that music actively improves, worsens, or has no effect on their mental condition?

---

## 📊 Key Insights & Statistical Findings

Across 735 cleaned complete respondent records:
- **Global Averages (Scale 0–10):**
  - **Anxiety:** 5.83 / 10 (Median: 6.0, Std: 2.79)
  - **Depression:** 4.80 / 10 (Median: 5.0, Std: 3.03)
  - **Insomnia:** 3.74 / 10 (Median: 3.0, Std: 3.09)
  - **OCD:** 2.63 / 10 (Median: 2.0, Std: 2.84)
  - **Daily Listening Hours:** 3.57 hours/day (Median: 3.0h)
  - **Average Age:** 25.2 years (Range: 10–89)
- **Perceived Impact of Music:** **73.7%** report music **improves** their mental state, **23.0%** report **no effect**, and only **2.3%** report music **worsens** their condition.
- **Hours vs. Anxiety Correlation:** Pearson correlation $r = 0.050$ ($p = 0.179$, non-significant linear correlation), while Spearman rank correlation is $\rho = 0.094$ ($p = 0.011$).
- **Working Listeners:** 78.6% of respondents listen while working. Working listeners report average anxiety of 5.88 vs. 5.62 for non-working listeners.

### Summary Across All 16 Music Genres

| Genre | Sample Size ($n$) | Share (%) | Mean Anxiety | Mean Depression | Mean Insomnia | Mean OCD | Daily Hours | % Music Improves |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rock** | 188 | 25.6% | 6.12 | 5.24 | 3.88 | 2.68 | 3.63h | 67.0% |
| **Pop** | 114 | 15.5% | 6.07 | 4.49 | 3.37 | 2.86 | 2.91h | 74.6% |
| **Metal** | 88 | 12.0% | 5.76 | 5.07 | 4.56 | 2.40 | 3.60h | 76.1% |
| **Classical** | 53 | 7.2% | 4.89 | 4.08 | 3.79 | 2.38 | 2.88h | 73.6% |
| **Video Game Music** | 44 | 6.0% | 5.89 | 4.48 | 4.00 | 2.39 | 2.91h | 59.1% |
| **EDM** | 37 | 5.0% | 5.49 | 5.24 | 3.97 | 3.00 | 4.59h | 81.1% |
| **R&B** | 35 | 4.8% | 5.17 | 3.83 | 2.89 | 2.74 | 3.47h | 74.3% |
| **Hip Hop** | 34 | 4.6% | 6.12 | 5.88 | 3.47 | 2.59 | 3.96h | 88.2% |
| **Folk** | 30 | 4.1% | 6.57 | 5.07 | 3.63 | 2.20 | 3.24h | 76.7% |
| **K-Pop** | 26 | 3.5% | 6.23 | 4.42 | 3.46 | 2.54 | 4.00h | 73.1% |
| **Country** | 25 | 3.4% | 5.40 | 4.32 | 2.72 | 2.76 | 3.42h | 80.0% |
| **Rap** | 22 | 3.0% | 5.09 | 4.00 | 2.27 | 3.18 | 5.32h | 77.3% |
| **Jazz** | 20 | 2.7% | 5.90 | 4.50 | 3.85 | 2.80 | 5.42h | 80.0% |
| **Lofi** | 10 | 1.4% | 6.10 | 6.60 | 5.60 | 3.40 | 4.20h | 100.0% |
| **Gospel** | 6 | 0.8% | 4.83 | 2.67 | 5.33 | 0.33 | 2.38h | 100.0% |
| **Latin** | 3 | 0.4% | 4.33 | 3.00 | 3.33 | 1.67 | 6.67h | 33.3% |
| **Global Baseline** | **735** | **100%** | **5.83** | **4.80** | **3.74** | **2.63** | **3.57h** | **73.7%** |

---

## 🎛️ Interactive Dashboard Features

The dashboard (`web_dashboard/index.html`) is built using clean modern CSS and vanilla JavaScript with SVG charts:

1. **🎯 Genre Deep-Dive View:**
   - **Hero Summary:** Dynamic natural language summary comparing the genre to global norms.
   - **KPI Cards:** Anxiety, Depression, Insomnia, and OCD cards showing mean, median, deltas against global benchmarks, and severity splits (Low 0–3, Moderate 4–6, High 7–10).
   - **4-Axis Spider / Radar Chart:** Real-time SVG radar overlaying the genre polygon against the dataset baseline.
   - **Music Effects Donut Chart:** Interactive SVG chart displaying percentage of positive vs neutral vs negative perceptions.
   - **Work Status Analysis:** Anxiety comparisons for listeners who listen while working vs. those who don't.
   - **Cross-Genre Affinity:** Quantifies how frequently listeners of the selected genre also listen to the remaining 15 styles.
2. **⚖️ Head-to-Head Comparison Mode:**
   - Select any two genres (e.g. *Rock vs. Classical*, *Metal vs. Pop*, or *EDM vs. Lofi*).
   - Dual-layer radar plot overlay and direct metric comparison table with absolute differences and winner badges.
3. **🏆 Leaderboards & Rankings:**
   - Rank all 16 genres instantly by Highest Anxiety, Depression, Insomnia, OCD, Daily Listening Hours, Mental Health Improvement Rate, or Sample Size.
   - Click any leaderboard bar to instantly inspect that genre.
4. **📈 R Plots & Visualizations Gallery (New Tab):**
   - High-resolution gallery of all 6 graphical plot types generated in base R:
     - **Frequency Histogram & Density:** Distribution of Anxiety scores.
     - **Bivariate OLS Scatter Plot:** Daily listening hours vs. Anxiety with linear trendline.
     - **Two-Sample Tukey Boxplot:** Anxiety distributions for workplace listeners vs. non-listeners.
     - **Categorical Stacked Bar Plot:** Contingency distribution of anxiety severity across top genres.
     - **Conditional Probability Bar Chart:** Ranked $P(\text{High Anxiety} \mid \text{Genre})$ with Wilson intervals.
     - **Discrete Probability Distribution PMF:** Binomial distribution for $n = 10, p = 0.603$.
   - Interactive zoom modals, academic interpretations, variables plotted ($X$ vs. $Y$), and exact base R code snippets.
5. **🧪 Inferential Statistics & Hypothesis Testing Suite (New Tab):**
   - **Executive Decision Matrix:** Complete scorecard of Null ($H_0$), Alternative ($H_1$), test statistics, degrees of freedom, $p$-values, effect sizes (Cohen's $d$, Cramer's $V$, $r^2$), and decisions at $\alpha = 0.05$.
   - **Welch Two-Sample t-Test:** With an **interactive SVG Student's t-distribution bell curve** displaying shaded two-tailed rejection regions ($\alpha = 0.05$), critical boundaries ($t = \pm 1.970$), and observed statistic marker ($t = -0.9791$) inside the acceptance region.
   - **95% Confidence Intervals for Means:** Table and error bars for Anxiety, Depression, Insomnia, and OCD partitioned by work status.
   - **Chi-Square ($\chi^2$) Contingency Table:** Full $7 \times 2$ matrix testing genre and anxiety independence ($\chi^2 = 6.918, p = 0.328$).
   - **Pearson vs. Spearman Correlation:** Contrasting parametric linear ($r = 0.050, p = 0.179$) vs non-parametric monotonic rank correlation ($\rho = 0.094, p = 0.011$).
   - **Interactive Discrete Binomial Distribution Calculator:** Dynamic slider for sample size $n$ and target $k$, live updating formulas, expected value $E[X]$, variance, and SVG PMF bar chart.
   - **Bayes' Theorem Calculations:** Step-by-step posterior calculations for $P(\text{Rock} \mid \text{High Anxiety})$, $P(\text{Pop} \mid \text{High Anxiety})$, and $P(\text{Metal} \mid \text{High Anxiety})$.
6. **📋 Raw Survey Data Explorer:**
   - Searchable, paginated table of raw respondent records for the active genre with filtering by music effects.

---

## 📈 Running the R Statistical Analysis

The statistical modeling is implemented in `additional_analysis.R` using base R:

### In RStudio:
1. Open `MusicMentalHealth.Rproj`.
2. Open `additional_analysis.R`.
3. Run the script: `source("additional_analysis.R")`.

### From Terminal / Command Line:
```bash
Rscript additional_analysis.R
```

### Outputs Generated:
- **`R_analysis/tables/`**:
  - `descriptive_statistics.csv`
  - `basic_probability.csv`
  - `conditional_probability.csv` (probability of high anxiety per genre)
  - `confidence_intervals.csv` (95% CIs by work status)
  - `correlation_results.csv` (Pearson & Spearman)
  - `t_test_results.csv`
  - `chi_square_results.csv` & `chi_square_contingency_table.csv`
  - `binomial_distribution.csv`
  - `validation.csv`
- **`R_analysis/plots/`**:
  - `anxiety_histogram.png`
  - `hours_vs_anxiety.png`
  - `anxiety_by_working.png`
  - `genre_anxiety_stacked_bar.png`
  - `conditional_probability_genre.png`
  - `binomial_distribution.png`
- **`R_analysis/results_summary.txt`**: Consolidated text summary of all statistical findings.

---

## 📂 Repository Structure

```text
.
├── Data/
│   └── mxmh_survey_results.csv     # Raw Kaggle survey dataset (736 responses)
├── R_analysis/
│   ├── plots/                      # Generated visualization plots from R
│   ├── tables/                     # Generated statistical CSV tables
│   └── results_summary.txt         # Text summary of R statistical output
├── web_dashboard/
│   ├── index.html                  # Interactive single-page web UI dashboard
│   ├── prepare_data.py             # Data processing & ETL script (CSV -> JSON/JS)
│   ├── genre_data.json             # Structured pre-computed statistics JSON
│   ├── genre_data.js               # Inlined JS data object for offline/zero-server use
│   └── server.py                   # Lightweight zero-dependency HTTP server
├── additional_analysis.R           # Core R statistical analysis script
├── MusicMentalHealth.Rproj         # RStudio Project configuration
├── requirements.txt                # Optional Python dependencies (pandas, scipy, etc.)
├── start_ui.sh                     # One-click dashboard launcher script
└── README.md                       # Repository documentation & guide
```

---

## 💾 Dataset Details

The dataset (`Data/mxmh_survey_results.csv`) is sourced from the Kaggle Music & Mental Health Survey:
- **Rows:** 736 responses (735 complete cases used in analysis).
- **Core Columns:**
  - `Age`: Respondent age.
  - `Hours per day`: Hours spent listening to music per day.
  - `While working`: Whether the respondent listens while working (`Yes`/`No`).
  - `Instrumentalist` & `Composer`: Whether the respondent plays an instrument or composes.
  - `Fav genre`: Chosen favorite music genre (16 unique categories).
  - `BPM`: Beats per minute of preferred music (optional).
  - `Frequency [Classical...Video game music]`: Listening frequency per genre (`Never`, `Rarely`, `Sometimes`, `Very frequently`).
  - `Anxiety`, `Depression`, `Insomnia`, `OCD`: Self-reported scores from 0 (minimal/none) to 10 (extreme).
  - `Music effects`: Self-reported overall effect (`Improve`, `No effect`, `Worsen`).

---

## ⚙️ Prerequisites & Requirements

### For the Web Dashboard:
- **Python 3.8+** (Optional, only needed if running `server.py` or `prepare_data.py`).
  - Uses only Python standard library modules (`http.server`, `socketserver`, `json`, `csv`, `math`).
  - **No `pip install` required** for running the web dashboard!
- Any modern web browser (Chrome, Firefox, Edge, Safari).

### For the R Analysis (Optional):
- **R (>= 4.0.0)** or **RStudio**.
- Uses base R functions (no external CRAN packages strictly required).

---

## ⚠️ Limitations & Methodology

1. **Observational & Self-Reported:** The survey is observational; correlation does not imply causation. Mental health ratings are self-reported rather than clinically diagnosed.
2. **Self-Selected Sample:** Survey respondents were self-selected online, predominantly young adults (median age 21–22), so findings may not generalize across the broader global population.
3. **Sample Size Disparity:** Some genres have substantial sample sizes (e.g. Rock: $n = 188$, Pop: $n = 114$, Metal: $n = 88$), while others have limited representations (e.g. Latin: $n = 3$, Gospel: $n = 6$). Interpret smaller genre groups with appropriate caution.
