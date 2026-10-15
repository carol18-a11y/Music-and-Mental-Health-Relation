# Music Listening and Mental Health (R)

A probability and statistics project studying whether daily music listening
is associated with self-reported anxiety (and depression, insomnia, OCD).

## Research question
Is there a relationship between hours of music listened per day and
self-reported anxiety, and does it differ by favourite genre or by
listening while working?

## Data
`data/mxmh_survey_results.csv` (Music & Mental Health survey, Kaggle).
Add the dataset citation and link here. It is a self-selected online
survey, so results do not generalise to the whole population.

## How to run
1. Open `MusicMentalHealth.Rproj` in RStudio.
2. Make sure the data file is in the `data/` folder.
3. Run `source("additional_analysis.R")`.

Only base R is used; no packages need to be installed.
Tables and plots are written to `outputs/R_analysis/`.

## Methods
Descriptive statistics, basic and conditional probability (with Wilson
confidence intervals), Bayes' theorem, confidence intervals for means,
Pearson and Spearman correlation (Holm-adjusted), simple and multiple
linear regression, Welch t-test (Cohen's d), ANOVA and Kruskal-Wallis,
chi-square test (Cramer's V), and the binomial distribution.

## Key findings
Fill in after running on the real data: correlation and regression slope,
t-test and chi-square results with effect sizes, and which genres had
reliable sample sizes.

## Limitations
- Observational, self-reported data: association is not causation.
- Self-selected sample; the "high anxiety" cutoff is a choice (see
  `cutoff_sensitivity.csv`).
- Multiple tests were run, so some significant results may be chance.
