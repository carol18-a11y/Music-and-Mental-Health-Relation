import csv
import json
import math
import os
from collections import defaultdict, Counter

def calc_stats(values):
    if not values:
        return {'count': 0, 'mean': 0.0, 'median': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
    vals = sorted(values)
    n = len(vals)
    mean = sum(vals) / n
    median = vals[n // 2] if n % 2 != 0 else (vals[n // 2 - 1] + vals[n // 2]) / 2.0
    variance = sum((x - mean) ** 2 for x in vals) / (n - 1) if n > 1 else 0.0
    std = math.sqrt(variance)
    return {
        'count': n,
        'mean': round(mean, 2),
        'median': round(median, 2),
        'min': round(vals[0], 2),
        'max': round(vals[-1], 2),
        'std': round(std, 2)
    }

def get_bucket(val, thresholds):
    # thresholds e.g. [(0, 3, 'Low (0-3)'), (4, 6, 'Moderate (4-6)'), (7, 10, 'High (7-10)')]
    for low, high, label in thresholds:
        if low <= val <= high:
            return label
    return 'Other'

def process():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(base_dir)

    # Search for CSV in possible locations
    candidates = [
        os.path.join(repo_dir, 'Data', 'mxmh_survey_results.csv'),
        os.path.join(repo_dir, 'data', 'mxmh_survey_results.csv'),
        os.path.join(base_dir, '..', 'Data', 'mxmh_survey_results.csv'),
        os.path.join(base_dir, 'mxmh_survey_results.csv'),
        'Music-and-Mental-Health-Relation/Data/mxmh_survey_results.csv',
        'Data/mxmh_survey_results.csv',
    ]

    csv_path = None
    for c in candidates:
        if os.path.exists(c):
            csv_path = c
            break

    if not csv_path:
        raise FileNotFoundError("Could not locate mxmh_survey_results.csv in Data/ directory.")

    with open(csv_path, mode='r', encoding='utf-8') as f:
        raw_rows = list(csv.DictReader(f))

    required_vars = ['Age', 'Hours per day', 'Anxiety', 'Depression', 'Insomnia', 'OCD', 'Fav genre']
    cleaned = []
    for idx, r in enumerate(raw_rows):
        if all(r[v].strip() != '' for v in required_vars):
            try:
                r_clean = {
                    'id': idx + 1,
                    'age': float(r['Age']),
                    'hours': float(r['Hours per day']),
                    'anxiety': float(r['Anxiety']),
                    'depression': float(r['Depression']),
                    'insomnia': float(r['Insomnia']),
                    'ocd': float(r['OCD']),
                    'bpm': float(r['BPM']) if r.get('BPM', '').strip() else None,
                    'genre': r['Fav genre'].strip(),
                    'streaming': r['Primary streaming service'].strip() or 'Unknown',
                    'working': r['While working'].strip(),
                    'instrumentalist': r['Instrumentalist'].strip(),
                    'composer': r['Composer'].strip(),
                    'exploratory': r['Exploratory'].strip(),
                    'foreign_languages': r['Foreign languages'].strip(),
                    'effects': r['Music effects'].strip() or 'Unknown',
                    'raw_frequencies': {
                        g: r.get(f'Frequency [{g}]', 'Never')
                        for g in [
                            'Classical', 'Country', 'EDM', 'Folk', 'Gospel', 'Hip hop',
                            'Jazz', 'K pop', 'Latin', 'Lofi', 'Metal', 'Pop', 'R&B',
                            'Rap', 'Rock', 'Video game music'
                        ]
                    }
                }
                cleaned.append(r_clean)
            except ValueError:
                pass

    total_n = len(cleaned)

    # Global Stats
    global_anxiety = calc_stats([r['anxiety'] for r in cleaned])
    global_depression = calc_stats([r['depression'] for r in cleaned])
    global_insomnia = calc_stats([r['insomnia'] for r in cleaned])
    global_ocd = calc_stats([r['ocd'] for r in cleaned])
    global_hours = calc_stats([r['hours'] for r in cleaned])
    global_age = calc_stats([r['age'] for r in cleaned])
    global_effects = Counter(r['effects'] for r in cleaned)
    global_working = Counter(r['working'] for r in cleaned)

    global_data = {
        'total_respondents': total_n,
        'anxiety': global_anxiety,
        'depression': global_depression,
        'insomnia': global_insomnia,
        'ocd': global_ocd,
        'hours': global_hours,
        'age': global_age,
        'effects_pct': {
            k: round(v / total_n * 100, 1) for k, v in global_effects.items() if k != 'Unknown'
        },
        'working_pct': round((global_working.get('Yes', 0) / total_n) * 100, 1),
        'high_anxiety_rate': round(sum(1 for r in cleaned if r['anxiety'] >= 6) / total_n * 100, 1),
        'high_depression_rate': round(sum(1 for r in cleaned if r['depression'] >= 6) / total_n * 100, 1)
    }

    # Per Genre Stats
    genres_list = sorted(list(set(r['genre'] for r in cleaned)))
    genre_data = {}

    genre_colors = {
        'Rock': '#ef4444',
        'Pop': '#ec4899',
        'Metal': '#64748b',
        'Classical': '#d97706',
        'Video game music': '#8b5cf6',
        'EDM': '#06b6d4',
        'R&B': '#f59e0b',
        'Hip hop': '#10b981',
        'Folk': '#84cc16',
        'K pop': '#f43f5e',
        'Country': '#b45309',
        'Rap': '#6366f1',
        'Jazz': '#14b8a6',
        'Lofi': '#a855f7',
        'Gospel': '#eab308',
        'Latin': '#f97316'
    }

    genre_emojis = {
        'Rock': '🎸',
        'Pop': '🎤',
        'Metal': '🤘',
        'Classical': '🎻',
        'Video game music': '🎮',
        'EDM': '⚡',
        'R&B': '🎷',
        'Hip hop': '🎧',
        'Folk': '🪕',
        'K pop': '✨',
        'Country': '🤠',
        'Rap': '🎙️',
        'Jazz': '🎺',
        'Lofi': '☕',
        'Gospel': '🕊️',
        'Latin': '💃'
    }

    for g in genres_list:
        g_rows = [r for r in cleaned if r['genre'] == g]
        gn = len(g_rows)
        if gn == 0:
            continue

        anx_stats = calc_stats([r['anxiety'] for r in g_rows])
        dep_stats = calc_stats([r['depression'] for r in g_rows])
        ins_stats = calc_stats([r['insomnia'] for r in g_rows])
        ocd_stats = calc_stats([r['ocd'] for r in g_rows])
        hrs_stats = calc_stats([r['hours'] for r in g_rows])
        age_stats = calc_stats([r['age'] for r in g_rows])

        bpm_vals = [r['bpm'] for r in g_rows if r['bpm'] is not None and 30 <= r['bpm'] <= 250]
        bpm_stats = calc_stats(bpm_vals) if bpm_vals else {'mean': 0, 'count': 0}

        # Severity distributions
        severity_thresholds = [(0, 3, 'Low (0-3)'), (4, 6, 'Moderate (4-6)'), (7, 10, 'High (7-10)')]
        anx_dist = Counter(get_bucket(r['anxiety'], severity_thresholds) for r in g_rows)
        dep_dist = Counter(get_bucket(r['depression'], severity_thresholds) for r in g_rows)
        ins_dist = Counter(get_bucket(r['insomnia'], severity_thresholds) for r in g_rows)
        ocd_dist = Counter(get_bucket(r['ocd'], severity_thresholds) for r in g_rows)

        # Listening hours distribution
        hrs_thresholds = [(0, 1.99, '< 2 hrs'), (2, 3.99, '2 - 4 hrs'), (4, 5.99, '4 - 6 hrs'), (6, 24, '6+ hrs')]
        hrs_dist = Counter(get_bucket(r['hours'], hrs_thresholds) for r in g_rows)

        # Age distribution
        age_thresholds = [(0, 17.99, '< 18'), (18, 24.99, '18 - 24'), (25, 34.99, '25 - 34'), (35, 49.99, '35 - 49'), (50, 120, '50+')]
        age_dist = Counter(get_bucket(r['age'], age_thresholds) for r in g_rows)

        # Music effects
        effects_counter = Counter(r['effects'] for r in g_rows)
        eff_clean = {
            'Improve': effects_counter.get('Improve', 0),
            'No effect': effects_counter.get('No effect', 0),
            'Worsen': effects_counter.get('Worsen', 0)
        }
        eff_pct = {
            k: round((v / gn) * 100, 1) for k, v in eff_clean.items()
        }

        # Streaming services
        streaming_counter = Counter(r['streaming'] for r in g_rows)
        streaming_list = [
            {'name': k, 'count': v, 'pct': round((v / gn) * 100, 1)}
            for k, v in streaming_counter.most_common()
        ]

        # Habits
        work_yes = sum(1 for r in g_rows if r['working'] == 'Yes')
        inst_yes = sum(1 for r in g_rows if r['instrumentalist'] == 'Yes')
        comp_yes = sum(1 for r in g_rows if r['composer'] == 'Yes')
        expl_yes = sum(1 for r in g_rows if r['exploratory'] == 'Yes')
        for_yes = sum(1 for r in g_rows if r['foreign_languages'] == 'Yes')

        # Working vs Non-working anxiety comparison within this genre
        work_rows = [r for r in g_rows if r['working'] == 'Yes']
        nowork_rows = [r for r in g_rows if r['working'] == 'No']
        work_anx_mean = round(sum(r['anxiety'] for r in work_rows) / len(work_rows), 2) if work_rows else 0
        nowork_anx_mean = round(sum(r['anxiety'] for r in nowork_rows) / len(nowork_rows), 2) if nowork_rows else 0

        # Cross-genre frequencies: For listeners of genre G, how often do they listen to other genres?
        cross_freq = {}
        for other_g in [
            'Classical', 'Country', 'EDM', 'Folk', 'Gospel', 'Hip hop',
            'Jazz', 'K pop', 'Latin', 'Lofi', 'Metal', 'Pop', 'R&B',
            'Rap', 'Rock', 'Video game music'
        ]:
            c_counts = Counter(r['raw_frequencies'].get(other_g, 'Never') for r in g_rows)
            cross_freq[other_g] = {
                'Very frequently': c_counts.get('Very frequently', 0),
                'Sometimes': c_counts.get('Sometimes', 0),
                'Rarely': c_counts.get('Rarely', 0),
                'Never': c_counts.get('Never', 0),
                'score': round(
                    (c_counts.get('Very frequently', 0) * 3 +
                     c_counts.get('Sometimes', 0) * 2 +
                     c_counts.get('Rarely', 0) * 1) / (gn * 3) * 100, 1
                )
            }

        # High anxiety conditional probability (score >= 6)
        high_anx_n = sum(1 for r in g_rows if r['anxiety'] >= 6)
        high_anx_prob = round(high_anx_n / gn, 3)

        # High depression conditional probability (score >= 6)
        high_dep_n = sum(1 for r in g_rows if r['depression'] >= 6)
        high_dep_prob = round(high_dep_n / gn, 3)

        # Compact respondent sample (up to 50 items for table)
        sample_records = [
            {
                'id': r['id'],
                'age': int(r['age']),
                'hours': r['hours'],
                'anxiety': int(r['anxiety']),
                'depression': int(r['depression']),
                'insomnia': int(r['insomnia']),
                'ocd': int(r['ocd']),
                'effects': r['effects'],
                'working': r['working'],
                'streaming': r['streaming']
            }
            for r in g_rows
        ]

        genre_data[g] = {
            'name': g,
            'color': genre_colors.get(g, '#6366f1'),
            'emoji': genre_emojis.get(g, '🎵'),
            'count': gn,
            'pct_of_total': round((gn / total_n) * 100, 1),
            'anxiety': anx_stats,
            'depression': dep_stats,
            'insomnia': ins_stats,
            'ocd': ocd_stats,
            'hours': hrs_stats,
            'age': age_stats,
            'bpm': bpm_stats,
            'high_anxiety_rate': round(high_anx_prob * 100, 1),
            'high_depression_rate': round(high_dep_prob * 100, 1),
            'effects_counts': eff_clean,
            'effects_pct': eff_pct,
            'distributions': {
                'anxiety': [
                    {'label': 'Low (0-3)', 'count': anx_dist.get('Low (0-3)', 0), 'pct': round(anx_dist.get('Low (0-3)', 0) / gn * 100, 1)},
                    {'label': 'Moderate (4-6)', 'count': anx_dist.get('Moderate (4-6)', 0), 'pct': round(anx_dist.get('Moderate (4-6)', 0) / gn * 100, 1)},
                    {'label': 'High (7-10)', 'count': anx_dist.get('High (7-10)', 0), 'pct': round(anx_dist.get('High (7-10)', 0) / gn * 100, 1)},
                ],
                'depression': [
                    {'label': 'Low (0-3)', 'count': dep_dist.get('Low (0-3)', 0), 'pct': round(dep_dist.get('Low (0-3)', 0) / gn * 100, 1)},
                    {'label': 'Moderate (4-6)', 'count': dep_dist.get('Moderate (4-6)', 0), 'pct': round(dep_dist.get('Moderate (4-6)', 0) / gn * 100, 1)},
                    {'label': 'High (7-10)', 'count': dep_dist.get('High (7-10)', 0), 'pct': round(dep_dist.get('High (7-10)', 0) / gn * 100, 1)},
                ],
                'hours': [
                    {'label': '< 2 hrs', 'count': hrs_dist.get('< 2 hrs', 0), 'pct': round(hrs_dist.get('< 2 hrs', 0) / gn * 100, 1)},
                    {'label': '2 - 4 hrs', 'count': hrs_dist.get('2 - 4 hrs', 0), 'pct': round(hrs_dist.get('2 - 4 hrs', 0) / gn * 100, 1)},
                    {'label': '4 - 6 hrs', 'count': hrs_dist.get('4 - 6 hrs', 0), 'pct': round(hrs_dist.get('4 - 6 hrs', 0) / gn * 100, 1)},
                    {'label': '6+ hrs', 'count': hrs_dist.get('6+ hrs', 0), 'pct': round(hrs_dist.get('6+ hrs', 0) / gn * 100, 1)},
                ],
                'age': [
                    {'label': '< 18', 'count': age_dist.get('< 18', 0), 'pct': round(age_dist.get('< 18', 0) / gn * 100, 1)},
                    {'label': '18 - 24', 'count': age_dist.get('18 - 24', 0), 'pct': round(age_dist.get('18 - 24', 0) / gn * 100, 1)},
                    {'label': '25 - 34', 'count': age_dist.get('25 - 34', 0), 'pct': round(age_dist.get('25 - 34', 0) / gn * 100, 1)},
                    {'label': '35 - 49', 'count': age_dist.get('35 - 49', 0), 'pct': round(age_dist.get('35 - 49', 0) / gn * 100, 1)},
                    {'label': '50+', 'count': age_dist.get('50+', 0), 'pct': round(age_dist.get('50+', 0) / gn * 100, 1)},
                ]
            },
            'habits': {
                'working_pct': round((work_yes / gn) * 100, 1),
                'instrumentalist_pct': round((inst_yes / gn) * 100, 1),
                'composer_pct': round((comp_yes / gn) * 100, 1),
                'exploratory_pct': round((expl_yes / gn) * 100, 1),
                'foreign_languages_pct': round((for_yes / gn) * 100, 1),
                'working_anxiety': work_anx_mean,
                'non_working_anxiety': nowork_anx_mean
            },
            'streaming_services': streaming_list,
            'cross_genre_affinity': cross_freq,
            'sample_records': sample_records
        }

    # Rankings across genres
    rankings = {
        'by_count': sorted([{'name': g, 'val': genre_data[g]['count'], 'sub': f"{genre_data[g]['pct_of_total']}%"} for g in genres_list], key=lambda x: x['val'], reverse=True),
        'by_anxiety': sorted([{'name': g, 'val': genre_data[g]['anxiety']['mean'], 'sub': f"High: {genre_data[g]['high_anxiety_rate']}%"} for g in genres_list], key=lambda x: x['val'], reverse=True),
        'by_depression': sorted([{'name': g, 'val': genre_data[g]['depression']['mean'], 'sub': f"High: {genre_data[g]['high_depression_rate']}%"} for g in genres_list], key=lambda x: x['val'], reverse=True),
        'by_insomnia': sorted([{'name': g, 'val': genre_data[g]['insomnia']['mean'], 'sub': f"Std: {genre_data[g]['insomnia']['std']}"} for g in genres_list], key=lambda x: x['val'], reverse=True),
        'by_ocd': sorted([{'name': g, 'val': genre_data[g]['ocd']['mean'], 'sub': f"Std: {genre_data[g]['ocd']['std']}"} for g in genres_list], key=lambda x: x['val'], reverse=True),
        'by_hours': sorted([{'name': g, 'val': genre_data[g]['hours']['mean'], 'sub': f"Med: {genre_data[g]['hours']['median']}h"} for g in genres_list], key=lambda x: x['val'], reverse=True),
        'by_improve_rate': sorted([{'name': g, 'val': genre_data[g]['effects_pct']['Improve'], 'sub': f"n={genre_data[g]['count']}"} for g in genres_list], key=lambda x: x['val'], reverse=True)
    }

    # Load R Statistical Analysis Tables
    tables_dir = os.path.join(repo_dir, 'R_analysis', 'tables')
    r_stats = {
        'descriptive': [],
        'confidence_intervals': [],
        't_test': {},
        'chi_square': {},
        'correlation': [],
        'binomial': [],
        'basic_probability': [],
        'conditional_probability': [],
        'contingency_table': [],
        'bayes': [
            {'genre': 'Rock', 'prior': 0.2558, 'likelihood': 0.6436, 'posterior': 0.2731, 'pct': '27.3%'},
            {'genre': 'Pop', 'prior': 0.1551, 'likelihood': 0.6667, 'posterior': 0.1716, 'pct': '17.2%'},
            {'genre': 'Metal', 'prior': 0.1197, 'likelihood': 0.5682, 'posterior': 0.1129, 'pct': '11.3%'}
        ],
        'plots_gallery': [
            {
                'id': 'anxiety_histogram',
                'title': 'Anxiety Score Distribution',
                'type': 'Frequency Histogram & Density',
                'file': 'r_plots/anxiety_histogram.png',
                'x_label': 'Self-Reported Anxiety Score (0 to 10)',
                'y_label': 'Number of Respondents',
                'r_code': 'hist(analysis_data$Anxiety, breaks = seq(-0.5, 10.5, by = 1), col = "lightblue", border = "black")',
                'insight': 'Multimodal distribution with heavy concentration in the high anxiety spectrum (scores 6-8). Mean is 5.83, median is 6.0, standard deviation is 2.79.',
                'interpretation': 'Shows that over 60.3% of the surveyed sample experiences elevated anxiety (>= 6/10), justifying the binary thresholding for conditional probability models.'
            },
            {
                'id': 'hours_vs_anxiety',
                'title': 'Listening Hours vs. Anxiety',
                'type': 'Bivariate Scatter Plot & OLS Regression',
                'file': 'r_plots/hours_vs_anxiety.png',
                'x_label': 'Daily Listening Hours',
                'y_label': 'Anxiety Score (0-10)',
                'r_code': 'plot(cor_data$Hours.per.day, cor_data$Anxiety, pch = 19, col = "steelblue"); abline(lm(Anxiety ~ Hours.per.day), lwd = 2)',
                'insight': 'Near-flat linear regression slope. Pearson correlation r = 0.050 (p = 0.179, not statistically significant at alpha = 0.05).',
                'interpretation': 'Linear regression fails to find evidence that higher daily music consumption directly increases anxiety. However, Spearman rank correlation detects a weak positive monotonic trend (rho = 0.094, p = 0.011).'
            },
            {
                'id': 'anxiety_by_working',
                'title': 'Anxiety by Work Listening Status',
                'type': 'Two-Sample Comparative Boxplot',
                'file': 'r_plots/anxiety_by_working.png',
                'x_label': 'Listen While Working? (Yes / No)',
                'y_label': 'Anxiety Score (0-10)',
                'r_code': 'boxplot(Anxiety ~ While.working, data = test_data, col = c("lightblue", "lightgreen"))',
                'insight': 'Both groups exhibit an identical median score of 6.0 and closely matching interquartile ranges (IQR).',
                'interpretation': 'Welch two-sample t-test (t = -0.9791, p = 0.3285) fails to reject the null hypothesis, demonstrating that anxiety does not significantly differ between workplace listeners and non-workplace listeners.'
            },
            {
                'id': 'genre_anxiety_stacked_bar',
                'title': 'Anxiety Group by Music Genre',
                'type': 'Stacked Categorical Bar Chart (Contingency)',
                'file': 'r_plots/genre_anxiety_stacked_bar.png',
                'x_label': 'Favorite Music Genre',
                'y_label': 'Number of Respondents',
                'r_code': 'barplot(t(chi_table), beside = FALSE, legend.text = TRUE, col = c("lightblue", "salmon"))',
                'insight': 'Compares the counts of High Anxiety (>=6) vs Normal Anxiety across top genres (Classical, EDM, Metal, Pop, Rock, Video game music, Other).',
                'interpretation': 'Chi-Square test of independence yields X-squared = 6.9182, df = 6, p = 0.3285. We fail to reject H0, meaning music genre preference and high anxiety classification are statistically independent.'
            },
            {
                'id': 'conditional_probability_genre',
                'title': 'Conditional Probability P(High Anxiety | Genre)',
                'type': 'Categorical Conditional Probability Bar Chart',
                'file': 'r_plots/conditional_probability_genre.png',
                'x_label': 'Music Genre',
                'y_label': 'P(High Anxiety | Genre)',
                'r_code': 'barplot(conditional_probability$P_High_Anxiety, names.arg = conditional_probability$Genre, ylim = c(0, 1), col = "skyblue")',
                'insight': 'Ranks genres by conditional likelihood of reporting high anxiety. Folk (0.767) and Lofi (0.700) lead, followed by Pop (0.667) and Rock (0.644).',
                'interpretation': 'Useful for Bayesian conditioning: while Folk has highest conditional probability, Rock has far larger sample size, making Rock responsible for the greatest absolute share of high-anxiety listeners.'
            },
            {
                'id': 'binomial_distribution',
                'title': 'Binomial Probability Distribution PMF',
                'type': 'Discrete Probability Mass Function (n=10, p=0.6027)',
                'file': 'r_plots/binomial_distribution.png',
                'x_label': 'Number of High-Anxiety Respondents (k)',
                'y_label': 'Probability P(X = k)',
                'r_code': 'barplot(binomial_results$Probability, names.arg = binomial_results$High_Anxiety_Count, col = "lightgreen", border = "black")',
                'insight': 'Models random variable X ~ Binomial(n=10, p=0.6027). Expected value E[X] = np = 6.03. Peak probability occurs at k = 6 with P(X = 6) = 0.2508.',
                'interpretation': 'Demonstrates practical application of the Binomial PMF formula: P(X=k) = C(n,k) * p^k * (1-p)^(n-k). Extremely low probability (< 0.0001) of finding 0 high-anxiety respondents in a random sample of 10.'
            }
        ]
    }

    if os.path.exists(tables_dir):
        # Descriptive
        descriptive_file = os.path.join(tables_dir, 'descriptive_statistics.csv')
        if os.path.exists(descriptive_file):
            with open(descriptive_file, encoding='utf-8') as f:
                r_stats['descriptive'] = [
                    {
                        'variable': r['Variable'],
                        'count': int(r['Count']),
                        'mean': round(float(r['Mean']), 3),
                        'median': float(r['Median']),
                        'variance': round(float(r['Variance']), 3),
                        'std': round(float(r['Standard_Deviation']), 3),
                        'min': float(r['Minimum']),
                        'max': float(r['Maximum'])
                    }
                    for r in csv.DictReader(f)
                ]

        # Confidence intervals
        ci_file = os.path.join(tables_dir, 'confidence_intervals.csv')
        if os.path.exists(ci_file):
            with open(ci_file, encoding='utf-8') as f:
                r_stats['confidence_intervals'] = [
                    {
                        'variable': r['Variable'],
                        'while_working': r['While_Working'],
                        'count': int(r['Count']),
                        'mean': round(float(r['Mean']), 3),
                        'ci_lower': round(float(r['CI_Lower']), 3),
                        'ci_upper': round(float(r['CI_Upper']), 3),
                        'margin_of_error': round((float(r['CI_Upper']) - float(r['CI_Lower'])) / 2.0, 3)
                    }
                    for r in csv.DictReader(f)
                ]

        # T-test
        ttest_file = os.path.join(tables_dir, 't_test_results.csv')
        if os.path.exists(ttest_file):
            with open(ttest_file, encoding='utf-8') as f:
                t_row = next(csv.DictReader(f))
                r_stats['t_test'] = {
                    'test': t_row['Test'],
                    't_stat': round(float(t_row['T_Statistic']), 4),
                    'df': round(float(t_row['Degrees_of_Freedom']), 2),
                    'p_val': round(float(t_row['P_Value']), 4),
                    'ci_lower': round(float(t_row['CI_Lower']), 4),
                    'ci_upper': round(float(t_row['CI_Upper']), 4),
                    'h0': 'Mean anxiety is equal between workplace listeners and non-workplace listeners (μ_work - μ_nowork = 0)',
                    'h1': 'Mean anxiety differs between workplace listeners and non-workplace listeners (μ_work - μ_nowork ≠ 0)',
                    'alpha': 0.05,
                    'decision': 'Fail to reject H₀',
                    'conclusion': 'No statistically significant difference in anxiety scores between respondents who listen while working and those who do not (t = -0.9791, p = 0.3285 > 0.05, 95% CI [-0.7723, 0.2595] contains 0).'
                }

        # Chi square
        chi_file = os.path.join(tables_dir, 'chi_square_results.csv')
        if os.path.exists(chi_file):
            with open(chi_file, encoding='utf-8') as f:
                c_row = next(csv.DictReader(f))
                r_stats['chi_square'] = {
                    'test': c_row['Test'],
                    'chi_square': round(float(c_row['Chi_Square']), 4),
                    'df': int(c_row['Degrees_of_Freedom']),
                    'p_val': round(float(c_row['P_Value']), 4),
                    'cramer_v': 0.097,
                    'h0': 'Favorite music genre and anxiety severity level (High vs Normal) are independent',
                    'h1': 'Favorite music genre and anxiety severity level are dependent / associated',
                    'alpha': 0.05,
                    'decision': 'Fail to reject H₀',
                    'conclusion': 'There is insufficient evidence to conclude an association between preferred music genre and high anxiety classification (χ² = 6.9182, df = 6, p = 0.3285 > 0.05).'
                }

        # Chi square contingency table
        ctable_file = os.path.join(tables_dir, 'chi_square_contingency_table.csv')
        if os.path.exists(ctable_file):
            with open(ctable_file, encoding='utf-8') as f:
                r_stats['contingency_table'] = list(csv.DictReader(f))

        # Correlation
        cor_file = os.path.join(tables_dir, 'correlation_results.csv')
        if os.path.exists(cor_file):
            with open(cor_file, encoding='utf-8') as f:
                r_stats['correlation'] = [
                    {
                        'method': r['Method'],
                        'correlation': round(float(r['Correlation']), 4),
                        'p_value': round(float(r['P_Value']), 4),
                        'significant_05': float(r['P_Value']) < 0.05
                    }
                    for r in csv.DictReader(f)
                ]

        # Binomial
        bin_file = os.path.join(tables_dir, 'binomial_distribution.csv')
        if os.path.exists(bin_file):
            with open(bin_file, encoding='utf-8') as f:
                r_stats['binomial'] = [
                    {
                        'k': int(r['High_Anxiety_Count']),
                        'prob': round(float(r['Probability']), 5),
                        'pct': round(float(r['Probability']) * 100, 2)
                    }
                    for r in csv.DictReader(f)
                ]

        # Conditional probability
        cond_file = os.path.join(tables_dir, 'conditional_probability.csv')
        if os.path.exists(cond_file):
            with open(cond_file, encoding='utf-8') as f:
                r_stats['conditional_probability'] = [
                    {
                        'genre': r['Genre'],
                        'count': int(r['Count']),
                        'p_high_anxiety': round(float(r['P_High_Anxiety']), 4),
                        'pct': round(float(r['P_High_Anxiety']) * 100, 1)
                    }
                    for r in csv.DictReader(f)
                ]

        # Basic probability
        basic_file = os.path.join(tables_dir, 'basic_probability.csv')
        if os.path.exists(basic_file):
            with open(basic_file, encoding='utf-8') as f:
                r_stats['basic_probability'] = [
                    {
                        'event': r['Event'],
                        'count': int(r['Count']),
                        'prob': round(float(r['Probability']), 4),
                        'pct': round(float(r['Probability']) * 100, 1)
                    }
                    for r in csv.DictReader(f)
                ]

    # Pre-calculated data specifically for client-side live SVG rendering of all 6 graphs
    anx_counts = Counter(int(r['anxiety']) for r in cleaned)
    hist_list = [{'score': s, 'count': anx_counts.get(s, 0), 'pct': round((anx_counts.get(s, 0) / total_n) * 100, 1)} for s in range(11)]

    # Boxplot calculations
    def compute_box(vals):
        s = sorted(vals)
        n = len(s)
        def q_val(p):
            idx = p * (n - 1)
            i = int(idx)
            rem = idx - i
            return s[i] + rem * (s[i+1] - s[i]) if i < n - 1 else s[i]
        q1 = round(q_val(0.25), 2)
        med = round(q_val(0.50), 2)
        q3 = round(q_val(0.75), 2)
        iqr = q3 - q1
        low = round(max(s[0], q1 - 1.5 * iqr), 2)
        high = round(min(s[-1], q3 + 1.5 * iqr), 2)
        mean_val = round(sum(s) / n, 2)
        return {'n': n, 'min': s[0], 'q1': q1, 'median': med, 'q3': q3, 'max': s[-1], 'mean': mean_val, 'lower_whisker': low, 'upper_whisker': high}

    # Boxplot calculations for all 4 clinical dimensions (Anxiety, Depression, Insomnia, OCD)
    box_metrics = {}
    for m_key in ['anxiety', 'depression', 'insomnia', 'ocd']:
        w_yes = [r[m_key] for r in cleaned if r['working'] == 'Yes']
        w_no = [r[m_key] for r in cleaned if r['working'] == 'No']
        box_metrics[m_key] = {
            'yes': compute_box(w_yes),
            'no': compute_box(w_no)
        }

    # Rich scatter points with all dimensions for interactive GUI controls
    scatter_pts = [
        {
            'id': r['id'],
            'age': r['age'],
            'x': round(r['hours'], 2),
            'anxiety': round(r['anxiety'], 1),
            'depression': round(r['depression'], 1),
            'insomnia': round(r['insomnia'], 1),
            'ocd': round(r['ocd'], 1),
            'genre': r['genre'],
            'working': r['working'],
            'effects': r['effects']
        }
        for r in cleaned
    ]

    r_stats['live_plots'] = {
        'histogram': hist_list,
        'boxplot': box_metrics['anxiety'], # default anxiety
        'box_metrics': box_metrics,
        'scatter': {
            'slope': 0.0458,
            'intercept': 5.6698,
            'r': 0.0497,
            'p': 0.1787,
            'points': scatter_pts
        }
    }

    full_payload = {
        'global': global_data,
        'genres': genre_data,
        'rankings': rankings,
        'all_genre_names': genres_list,
        'r_statistics': r_stats
    }

    # Save to JSON in the web_dashboard directory
    out_json = os.path.join(base_dir, 'genre_data.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(full_payload, f, indent=2)

    # Also save as a JS variable for direct file:// browser opening
    out_js = os.path.join(base_dir, 'genre_data.js')
    with open(out_js, 'w', encoding='utf-8') as f:
        f.write('window.GENRE_DATA = ' + json.dumps(full_payload, indent=2) + ';')

    print(f"Data prepared successfully: {len(genres_list)} genres, {total_n} respondents.")

if __name__ == '__main__':
    process()
