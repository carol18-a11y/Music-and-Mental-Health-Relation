import csv
import json
import math
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
    csv_path = 'Music-and-Mental-Health-Relation/Data/mxmh_survey_results.csv'
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

    full_payload = {
        'global': global_data,
        'genres': genre_data,
        'rankings': rankings,
        'all_genre_names': genres_list
    }

    # Save to JSON
    with open('web_dashboard/genre_data.json', 'w', encoding='utf-8') as f:
        json.dump(full_payload, f, indent=2)

    # Also save as a JS variable for direct file:// browser opening
    with open('web_dashboard/genre_data.js', 'w', encoding='utf-8') as f:
        f.write('window.GENRE_DATA = ' + json.dumps(full_payload, indent=2) + ';')

    print(f"Data prepared successfully: {len(genres_list)} genres, {total_n} respondents.")

if __name__ == '__main__':
    process()
