#!/usr/bin/env python3
"""
Generates web_dashboard/presentation.html - Interactive 16:9 Slide Deck Presentation
Features:
- Keyboard navigation (Left, Right, Space, Home, End, F for Fullscreen)
- Touch / Click controls
- 1-Click Print / Save as PDF button (@media print optimized)
- Download Link for pre-compiled PDF
- Direct Link to Live Dashboard
"""

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AudioMental • Probability & Statistics Project Presentation</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {
      --bg-dark: #0b0f19;
      --card-dark: #111827;
      --card-border: #1f2937;
      --accent: #6366f1;
    }
    body {
      background-color: var(--bg-dark);
      color: #f3f4f6;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      overflow-x: hidden;
      user-select: none;
    }
    .slide {
      display: none;
      min-height: 100vh;
      width: 100vw;
      padding: 2.5rem 4rem;
      box-sizing: border-box;
      opacity: 0;
      transform: translateY(12px);
      transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1), transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .slide.active {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      opacity: 1;
      transform: translateY(0);
    }
    .glass-card {
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .formula-box {
      background: #0d1527;
      border: 1px solid #1e293b;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      overflow-x: auto;
      max-width: 100%;
      word-break: break-word;
    }

    /* Print to PDF rules */
    @media print {
      body {
        background-color: #0b0f19 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .no-print {
        display: none !important;
      }
      .slide {
        display: flex !important;
        opacity: 1 !important;
        transform: none !important;
        page-break-after: always !important;
        break-after: page !important;
        min-height: 100vh !important;
        width: 100% !important;
        padding: 2rem !important;
      }
    }
  </style>
</head>
<body class="flex flex-col min-h-screen">

  <!-- Top Slide Navigation Controls Bar (Hidden during print) -->
  <header class="no-print sticky top-0 z-50 bg-gray-950/80 backdrop-blur border-b border-gray-800 px-6 py-2.5 flex items-center justify-between text-xs">
    <div class="flex items-center gap-3">
      <div class="w-7 h-7 rounded-lg bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-sm">
        🎧
      </div>
      <div>
        <span class="font-bold text-white tracking-wide">AudioMental Presentation</span>
        <span class="text-gray-400 text-[11px] hidden sm:inline">• Probability & Statistics Course Evaluation</span>
      </div>
    </div>

    <!-- Slide Navigation & Action Buttons -->
    <div class="flex items-center gap-2">
      <span id="slide-indicator" class="font-mono text-gray-300 font-bold px-2 py-1 rounded bg-gray-900 border border-gray-800">1 / 14</span>
      <button onclick="prevSlide()" class="px-2.5 py-1.5 rounded-lg bg-gray-900 hover:bg-gray-800 text-gray-200 border border-gray-800 transition-colors" title="Previous Slide (Left Arrow)">◀</button>
      <button onclick="nextSlide()" class="px-2.5 py-1.5 rounded-lg bg-gray-900 hover:bg-gray-800 text-gray-200 border border-gray-800 transition-colors" title="Next Slide (Right Arrow / Space)">▶</button>
      <button onclick="toggleFullscreen()" class="px-2.5 py-1.5 rounded-lg bg-gray-900 hover:bg-gray-800 text-gray-300 border border-gray-800 transition-colors hidden md:inline" title="Toggle Fullscreen (F)">⛶</button>
      
      <div class="h-4 w-[1px] bg-gray-800 mx-1"></div>

      <!-- Print / PDF Buttons -->
      <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-colors flex items-center gap-1.5 shadow-sm" title="Print or Save as PDF">
        <span>🖨️</span> Save as PDF
      </button>
      <a href="AudioMental_ProbStats_Presentation.pdf" download class="px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 transition-colors flex items-center gap-1.5" title="Download Pre-Compiled PDF">
        <span>📥</span> Download PDF
      </a>
      <a href="index.html" class="px-3 py-1.5 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 transition-colors flex items-center gap-1.5">
        <span>⚡</span> Live Dashboard
      </a>
    </div>
  </header>

  <!-- ===================================================================== -->
  <!-- SLIDE 1: TITLE & AUTHORS -->
  <!-- ===================================================================== -->
  <section class="slide active" id="slide-1">
    <div class="flex items-center justify-between">
      <span class="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs tracking-wider uppercase">Course Evaluation Presentation</span>
      <span class="text-xs text-gray-400 font-mono">Dataset: Kaggle MxMH (N = 735)</span>
    </div>

    <div class="my-auto py-6">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 text-xs font-mono font-semibold mb-4">
        <span>📊</span> PROBABILITY & STATISTICS PROJECT
      </div>
      <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mb-3">
        AudioMental
      </h1>
      <h2 class="text-xl sm:text-2xl font-bold text-indigo-400 mb-2">
        Statistical & Inferential Modeling of Music Genre Preferences on Psychological Well-Being
      </h2>
      <p class="text-sm text-gray-400 max-w-3xl">
        A rigorous empirical investigation applying Continuous Gaussian PDFs, Bivariate OLS Regression, Welch's Two-Sample t-Tests, Pearson Chi-Square Contingency, and Discrete Binomial Probability modeling on the Kaggle MxMH Survey.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
        <div class="glass-card p-4 rounded-xl border-l-4 border-indigo-500">
          <span class="text-xs text-gray-400 block mb-1">Author & Team Member</span>
          <h4 class="text-base font-bold text-white">Shubh Shetgaonkar</h4>
          <span class="text-xs text-indigo-400 font-mono font-semibold">25BCE2878</span>
          
        </div>
        <div class="glass-card p-4 rounded-xl border-l-4 border-purple-500">
          <span class="text-xs text-gray-400 block mb-1">Author & Team Member</span>
          <h4 class="text-base font-bold text-white">Riddhi Kotowar</h4>
          <span class="text-xs text-purple-400 font-mono font-semibold">25CBE2554</span>
          
        </div>
        <div class="glass-card p-4 rounded-xl border-l-4 border-pink-500">
          <span class="text-xs text-gray-400 block mb-1">Author & Team Member</span>
          <h4 class="text-base font-bold text-white">Ashmeetha Carol Noronha</h4>
          <span class="text-xs text-pink-400 font-mono font-semibold">25BDS0162</span>
          
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 1 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 2: RESEARCH MOTIVATION & OBJECTIVES -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-2">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Research Formulation</span>
      <h2 class="text-2xl font-bold text-white mt-1">Project Motivation & Scientific Objectives</h2>
      <p class="text-xs text-gray-400">Investigating whether subjective musical taste has statistically measurable links with clinical mental health scores.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 my-auto py-4">
      <div class="glass-card p-5 rounded-xl border-t-2 border-rose-500 flex flex-col justify-between">
        <div>
          <span class="text-xs text-rose-400 font-bold uppercase tracking-wider">Research Questions</span>
          <h3 class="text-base font-bold text-white mt-1 mb-2">Core Scientific Inquiries</h3>
          <ul class="text-xs text-gray-300 space-y-2">
            <li><strong>RQ1:</strong> Does daily music listening duration correlate linearly with self-reported anxiety severity?</li>
            <li><strong>RQ2:</strong> Do workplace listeners experience lower psychological strain than non-workplace listeners?</li>
            <li><strong>RQ3:</strong> Does preference for intense genres (Metal, Rock) associate with higher incidence of clinical anxiety or depression?</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-gray-800 text-[11px] text-gray-400">
          Focus: Separating emotional perception from rigorous statistical reality.
        </div>
      </div>

      <div class="glass-card p-5 rounded-xl border-t-2 border-indigo-500 flex flex-col justify-between">
        <div>
          <span class="text-xs text-indigo-400 font-bold uppercase tracking-wider">Course Alignment</span>
          <h3 class="text-base font-bold text-white mt-1 mb-2">Statistical Curriculum Framework</h3>
          <ul class="text-xs text-gray-300 space-y-1.5">
            <li><strong>1. Descriptive Stats:</strong> Mean, variance, IQR, Tukey fences.</li>
            <li><strong>2. Continuous Modeling:</strong> Gaussian PDF fitting & histogram scaling.</li>
            <li><strong>3. Correlation:</strong> Pearson linear vs. Spearman rank-order.</li>
            <li><strong>4. Regression:</strong> OLS bivariate equation (ŷ = β₀ + β₁x).</li>
            <li><strong>5. Hypothesis Tests:</strong> Welch's two-sample t-test & CI.</li>
            <li><strong>6. Categorical:</strong> Pearson's Chi-Square (χ²) test.</li>
            <li><strong>7. Discrete Modeling:</strong> Binomial PMF & Bayes theorem.</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-gray-800 text-[11px] text-gray-400">
          Satisfies all core probability & inferential statistics requirements.
        </div>
      </div>

      <div class="glass-card p-5 rounded-xl border-t-2 border-emerald-500 flex flex-col justify-between">
        <div>
          <span class="text-xs text-emerald-400 font-bold uppercase tracking-wider">Executive Takeaway</span>
          <h3 class="text-base font-bold text-white mt-1 mb-2">Key Empirical Conclusions</h3>
          <ul class="text-xs text-gray-300 space-y-2">
            <li><strong>Weak Linear Trend:</strong> Pearson r = 0.0497 (p = 0.1787). Hours do not linearly dictate anxiety.</li>
            <li><strong>Monotonic Trend:</strong> Spearman ρ = 0.0941 (p = 0.0107*). Indicates subtle monotonic rank association.</li>
            <li><strong>Workplace Invariance:</strong> Welch t = -0.9791 (p = 0.3285). Working with music does not alter anxiety.</li>
            <li><strong>Genre Independence:</strong> χ² = 6.9182 (p = 0.3285). Genre choice is independent of high anxiety.</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-gray-800 text-[11px] text-emerald-400 font-semibold">
          73.7% survey-wide report music directly improves mental well-being.
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 2 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 3: DATASET ANATOMY & PREPROCESSING -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-3">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Data Pipeline</span>
      <h2 class="text-2xl font-bold text-white mt-1">Dataset Anatomy & Preprocessing Pipeline</h2>
      <p class="text-xs text-gray-400">Transformation of raw survey records into structured, distribution-ready statistical vectors.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">ETL Data Validation Protocol</h3>
        <ul class="text-xs text-gray-300 space-y-2">
          <li><strong>Raw Ingestion:</strong> 736 submissions collected across international demographics.</li>
          <li><strong>Filtering & Scrubbing:</strong> Dropped 1 unparseable record with missing primary genre bounds (Final N = 735).</li>
          <li><strong>Continuous Truncation:</strong> Daily listening hours validated to physical boundaries [0, 24] hours/day.</li>
          <li><strong>Discrete Likert Scales:</strong> Anxiety, Depression, Insomnia, OCD scored integer discrete [0, 10].</li>
          <li><strong>Nominal Categorical:</strong> 16 unique musical genres (Rock, Pop, Metal, Classical, Video Game, Folk, EDM, etc.).</li>
          <li><strong>Binary Workplace Feature:</strong> Listens while working? [Yes (n=578, 78.6%), No (n=154, 21.0%)].</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Global Baseline Parameters (N = 735)</h3>
        <table class="w-full text-xs text-left">
          <thead class="text-gray-400 uppercase bg-gray-900 border-b border-gray-800">
            <tr>
              <th class="py-1.5 px-2">Metric Variable</th>
              <th class="py-1.5 px-2">Mean (x̄)</th>
              <th class="py-1.5 px-2">SD (s)</th>
              <th class="py-1.5 px-2">Median</th>
              <th class="py-1.5 px-2">IQR [Q1, Q3]</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-800">
            <tr><td class="py-1.5 px-2 font-bold text-white">Anxiety Score</td><td>5.83</td><td>2.79</td><td>6.0</td><td>[4.0, 8.0] (4.0)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Depression Score</td><td>4.80</td><td>3.03</td><td>5.0</td><td>[2.0, 7.0] (5.0)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Insomnia Score</td><td>3.74</td><td>3.09</td><td>3.0</td><td>[1.0, 6.0] (5.0)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">OCD Score</td><td>2.63</td><td>2.85</td><td>2.0</td><td>[0.0, 4.0] (4.0)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Listening Hours</td><td>3.71 hrs</td><td>3.03</td><td>3.0 hrs</td><td>[2.0, 5.0] (3.0)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Participant Age</td><td>25.2 yrs</td><td>12.05</td><td>21.0 yrs</td><td>[18.0, 28.0] (10.0)</td></tr>
          </tbody>
        </table>
        <div class="formula-box p-2.5 rounded-lg text-[11px] text-cyan-300">
          s = √[ (1 / (n - 1)) · ∑(xᵢ - x̄)² ] (Bessel's Unbiased Estimator)
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 3 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 4: DESCRIPTIVE STATISTICS & FIVE-NUMBER SUMMARY -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-4">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Descriptive Statistics</span>
      <h2 class="text-2xl font-bold text-white mt-1">Location, Dispersion & Five-Number Summary Analysis</h2>
      <p class="text-xs text-gray-400">Evaluating central tendency and non-parametric spread across psychological dimensions.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Theoretical Formulas & Dispersion Metrics</h3>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          x̄ = (1 / n) · ∑xᵢ   (Sample Mean)
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          s² = (1 / (n - 1)) · ∑(xᵢ - x̄)²   (Sample Variance)
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          IQR = Q₃ - Q₁   |   Fences: [Q₁ - 1.5·IQR, Q₃ + 1.5·IQR]
        </div>
        <ul class="text-xs text-gray-300 space-y-1.5 pt-2">
          <li>• <strong>Robustness:</strong> Mean & variance are sensitive to extreme listening outliers.</li>
          <li>• <strong>Median Resilience:</strong> The median (Q2) remains unaffected by skewed distributions.</li>
          <li>• <strong>Tukey Outlier Fences:</strong> Implemented in our comparative boxplots to isolate abnormal participants.</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Work vs Non-Work Comparative Boxplot Data</h3>
        <table class="w-full text-xs text-left">
          <thead class="text-gray-400 uppercase bg-gray-900 border-b border-gray-800">
            <tr>
              <th class="py-1.5 px-2">Statistic</th>
              <th class="py-1.5 px-2">Working = YES (n=578)</th>
              <th class="py-1.5 px-2">Working = NO (n=154)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-800">
            <tr><td class="py-1.5 px-2 font-bold text-white">Mean (x̄)</td><td>5.88</td><td>5.62</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Std Dev (s)</td><td>2.76</td><td>2.90</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Q1 (25th percentile)</td><td>4.0</td><td>3.0</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Median (50th percentile)</td><td class="text-emerald-400 font-bold">6.0</td><td class="text-emerald-400 font-bold">6.0 (Identical)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Q3 (75th percentile)</td><td class="text-emerald-400 font-bold">8.0</td><td class="text-emerald-400 font-bold">8.0 (Identical)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">IQR (Q3 - Q1)</td><td>4.0</td><td>5.0</td></tr>
          </tbody>
        </table>
        <div class="p-3 bg-gray-900/80 rounded-lg border border-gray-800 text-[11px] text-gray-300">
          <strong class="text-emerald-400">Key Finding:</strong> Both groups exhibit identical median scores (6.0) and Q3 thresholds (8.0). Workplace listening neither elevates nor depresses clinical anxiety.
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 4 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 5: CONTINUOUS GAUSSIAN DENSITY MODELING -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-5">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Continuous Probability</span>
      <h2 class="text-2xl font-bold text-white mt-1">Continuous Gaussian Probability Density Modeling</h2>
      <p class="text-xs text-gray-400">Superimposing theoretical Normal distributions N(μ, σ²) onto discrete empirical histograms.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Gaussian Probability Density Function</h3>
        <div class="formula-box p-3 rounded-lg text-xs text-cyan-300 leading-relaxed">
          f(x; μ, σ) = [ 1 / (σ√(2π)) ] · exp[ -(x - μ)² / (2σ²) ]
        </div>
        <div class="formula-box p-3 rounded-lg text-xs text-purple-300 leading-relaxed">
          h(x) = N · Δx · f(x; μ, σ)   (Histogram Frequency Scaling)
        </div>
        <ul class="text-xs text-gray-300 space-y-2 pt-1">
          <li>• <strong>Binning Step Size:</strong> Step width Δx = (x_max - x_min) / k where k is the number of bins.</li>
          <li>• <strong>Scaling Alignment:</strong> Multiplying continuous PDF f(x) by N · Δx equates the continuous integral area directly with discrete bin count frequencies.</li>
          <li>• <strong>Skewness Observations:</strong> Anxiety exhibits a slight negative skew with mode at 6-7, while OCD shows severe right skew with mode at 0-1.</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Interactive Histogram Studio Capabilities</h3>
        <ul class="text-xs text-gray-300 space-y-2.5">
          <li>• <strong>Live Bin Slider:</strong> Real-time re-aggregation of 735 observations from k = 5 to k = 20 bins.</li>
          <li>• <strong>Normal Curve Overlay:</strong> Recalculates sample mean and standard deviation, drawing SVG Gaussian bell curves.</li>
          <li>• <strong>Mean & Median Reference Lines:</strong> Cyan dashed line for sample mean (5.83), amber line for median (6.0).</li>
          <li>• <strong>Hover Bin Inspector:</strong> Floating tooltip displays exact bin boundaries [a, b), frequency, and percentage share.</li>
        </ul>
        <div class="p-3 bg-indigo-950/40 rounded-lg border border-indigo-500/30 text-[11px] text-indigo-300">
          📥 <strong>Vector SVG Export:</strong> All generated curves and histograms export directly to pure vector SVG files for publication without loss of resolution.
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 5 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 6: BIVARIATE CORRELATION: PEARSON VS SPEARMAN -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-6">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Bivariate Association</span>
      <h2 class="text-2xl font-bold text-white mt-1">Correlation Analysis: Pearson Linear vs. Spearman Rank</h2>
      <p class="text-xs text-gray-400">Evaluating monotonic vs linear dependency between daily music listening hours and anxiety.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <div class="flex justify-between items-center">
          <h3 class="text-base font-bold text-white">Pearson Product-Moment (r)</h3>
          <span class="px-2 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/40 font-mono">p = 0.1787 (n.s.)</span>
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          r = Cov(X,Y) / (s_X · s_Y) = +0.0497
        </div>
        <ul class="text-xs text-gray-300 space-y-1.5">
          <li>• <strong>Hypothesis:</strong> H₀: ρ = 0 vs. H₁: ρ ≠ 0</li>
          <li>• <strong>Test Statistic:</strong> t = r√[(n - 2)/(1 - r²)] = 1.35 (df = 733)</li>
          <li>• <strong>Decision:</strong> t = 1.35 < t_crit (1.963), p = 0.1787 > 0.05.</li>
          <li>• <strong>Conclusion:</strong> <strong>Fail to Reject H₀</strong>. There is no statistically significant linear relationship between listening duration and anxiety.</li>
          <li>• <strong>Coefficient of Determination:</strong> R² = r² = 0.0025 (only 0.25% variance explained).</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <div class="flex justify-between items-center">
          <h3 class="text-base font-bold text-white">Spearman Rank-Order (ρ)</h3>
          <span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono">p = 0.0107 *</span>
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          ρ = 1 - [ 6 · ∑dᵢ² ] / [ n · (n² - 1) ] = +0.0941
        </div>
        <ul class="text-xs text-gray-300 space-y-1.5">
          <li>• <strong>Hypothesis:</strong> H₀: No monotonic association between ranks.</li>
          <li>• <strong>Decision:</strong> p = 0.0107 < α = 0.05. <strong>Reject H₀</strong>.</li>
          <li>• <strong>Statistical Nuance:</strong> Why does Spearman detect significance while Pearson fails?</li>
          <li>  1. <strong>Robust to Discrete Ties:</strong> The 0-10 anxiety scale has extensive ties.</li>
          <li>  2. <strong>Non-Linear Monotonicity:</strong> Higher listening hours weakly accompany higher rank orders of anxiety, without obeying strict linear proportionality.</li>
        </ul>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 6 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 7: ORDINARY LEAST SQUARES (OLS) REGRESSION -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-7">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Regression Modeling</span>
      <h2 class="text-2xl font-bold text-white mt-1">Ordinary Least Squares (OLS) Bivariate Regression</h2>
      <p class="text-xs text-gray-400">Quantifying the linear predictor model between listening duration and psychological distress.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">OLS Model Formulation & Parameter Estimates</h3>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          ŷ = β₀ + β₁·x   |   β₁ = Cov(X,Y) / Var(X)   |   β₀ = ȳ - β₁·x̄
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-purple-300 font-bold">
          Anxiety_Hat = 5.6698 + 0.0458 · (Hours)
        </div>
        <ul class="text-xs text-gray-300 space-y-2 pt-1">
          <li>• <strong>Slope (β₁ = 0.0458):</strong> For each additional hour listened daily, predicted anxiety rises by only 0.046 points.</li>
          <li>• <strong>Intercept (β₀ = 5.6698):</strong> Baseline predicted anxiety for an individual listening to zero music.</li>
          <li>• <strong>ANOVA F-Test:</strong> F(1, 733) = 1.815, p = 0.1787. Regression model fails to attain statistical significance.</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Interactive Scatter Studio Capabilities</h3>
        <ul class="text-xs text-gray-300 space-y-2">
          <li>• <strong>N=735 Circle Rendering:</strong> Renders all 735 surveyed participants as interactive vector circles with customizable opacity and point radius.</li>
          <li>• <strong>Participant Inspector:</strong> Hovering over any circle displays participant ID, Age, Daily Hours, Genre, Working status, and Music effect.</li>
          <li>• <strong>Genre Subsetting:</strong> Filter by Rock, Pop, Metal, Classical, etc. Live OLS recalculates slope, intercept, and r instantly.</li>
        </ul>
        <div class="p-3 bg-amber-500/10 rounded-lg border border-amber-500/30 text-[11px] text-amber-300">
          ⚠️ <strong>Defense Takeaway:</strong> Pop culture frequently assumes heavy music consumption reflects clinical depression; OLS proves daily listening hours explain less than 0.3% of anxiety variance.
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 7 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 8: TWO-SAMPLE HYPOTHESIS TESTING: WELCH'S T-TEST -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-8">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Hypothesis Testing</span>
      <h2 class="text-2xl font-bold text-white mt-1">Two-Sample Welch's t-Test & Confidence Intervals</h2>
      <p class="text-xs text-gray-400">Testing whether listening while working causes statistically significant shifts in anxiety.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Hypothesis & Welch-Satterthwaite Formulation</h3>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          H₀: μ_work = μ_nowork   vs.   H₁: μ_work ≠ μ_nowork
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          t = (x̄₁ - x̄₂) / √[ (s₁²/n₁) + (s₂²/n₂) ] = -0.9791
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-purple-300">
          Welch Satterthwaite df = 230.6 (Robust to unequal variances)
        </div>
        <ul class="text-xs text-gray-300 space-y-1.5 pt-1">
          <li>• <strong>Group 1 (Working to Music):</strong> n₁ = 578, x̄₁ = 5.88, s₁ = 2.76</li>
          <li>• <strong>Group 2 (No Music at Work):</strong> n₂ = 154, x̄₂ = 5.62, s₂ = 2.90</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Critical Rejection Boundaries & Decision</h3>
        <ul class="text-xs text-gray-300 space-y-2">
          <li>• <strong>Significance Level:</strong> α = 0.05 (Two-tailed critical boundary: ±1.970).</li>
          <li>• <strong>Observed Statistic:</strong> t = -0.9791 falls inside acceptance region [-1.970, +1.970].</li>
          <li>• <strong>p-Value:</strong> p = 0.3285 > 0.05. High probability of observing this data under H₀.</li>
          <li>• <strong>Decision:</strong> <strong class="text-emerald-400">FAIL TO REJECT H₀</strong>. Listening while working does not significantly alter anxiety.</li>
          <li>• <strong>95% Confidence Interval for (μ₁ - μ₂):</strong> [-0.772, +0.260] (includes 0).</li>
          <li>• <strong>Cohen's d:</strong> d = 0.09 (negligible effect size < 0.20).</li>
        </ul>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 8 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 9: CONTINGENCY & CHI-SQUARE TEST OF INDEPENDENCE -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-9">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Categorical Analysis</span>
      <h2 class="text-2xl font-bold text-white mt-1">Contingency Tables & Chi-Square (χ²) Independence Test</h2>
      <p class="text-xs text-gray-400">Evaluating whether primary music genre preference associates with high clinical anxiety severity.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Chi-Square Test Formulation</h3>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          H₀: Genre and Anxiety are Independent<br>
          H₁: Genre and Anxiety are Associated
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          χ² = ∑ᵢ ∑ⱼ [ (Oᵢⱼ - Eᵢⱼ)² / Eᵢⱼ ]   |   Eᵢⱼ = (Rᵢ · Cⱼ) / N
        </div>
        <ul class="text-xs text-gray-300 space-y-1.5 pt-1">
          <li>• <strong>Contingency Table:</strong> 7 Genres (Classical, EDM, Metal, Pop, Rock, Video Game, Other) × 2 Severity Levels (High ≥ 6 vs Normal < 6).</li>
          <li>• <strong>Sample Size:</strong> N = 735.</li>
          <li>• <strong>Cochran's Rule Verified:</strong> All expected cell frequencies Eᵢⱼ > 5.</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Results & Cramer's V Effect Size</h3>
        <ul class="text-xs text-gray-300 space-y-2">
          <li>• <strong>Chi-Square Statistic:</strong> χ² = 6.9182 (df = 6).</li>
          <li>• <strong>p-Value:</strong> p = 0.3285 > 0.05.</li>
          <li>• <strong>Statistical Decision:</strong> <strong class="text-emerald-400">FAIL TO REJECT H₀</strong>. Music genre preference and clinical anxiety severity are independent.</li>
          <li>• <strong>Cramer's V:</strong> V = √[ χ² / (n · min(r-1, c-1)) ] = 0.097 (negligible association < 0.10).</li>
        </ul>
        <div class="p-3 bg-gray-900 rounded-lg border border-gray-800 text-[11px] text-gray-300">
          <strong>Academic Meaning:</strong> Debunks the common cultural assumption that listeners of heavier genres (e.g., Metal, Rock) possess disproportionately higher clinical anxiety rates.
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 9 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 10: DISCRETE PROBABILITY: BINOMIAL DISTRIBUTION -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-10">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Discrete Probability</span>
      <h2 class="text-2xl font-bold text-white mt-1">Discrete Probability: Binomial Distribution PMF & CDF</h2>
      <p class="text-xs text-gray-400">Modeling random variable X ~ Bin(n, p) for clinical risk forecasting in survey cohorts.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Binomial Model Formulation & Moments</h3>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          P(X = k) = C(n, k) · pᵏ · (1 - p)ⁿ⁻ᵏ
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-purple-300">
          E[X] = n·p = 6.03   |   Var(X) = n·p·(1-p) = 2.395   |   σ = 1.548
        </div>
        <ul class="text-xs text-gray-300 space-y-1.5 pt-1">
          <li>• <strong>Random Variable X:</strong> Number of high-anxiety respondents (score ≥ 6) in random sample of size n.</li>
          <li>• <strong>Empirical Parameter:</strong> Base sample proportion p̂ = 443 / 735 = 0.6027 (60.27%).</li>
          <li>• <strong>Baseline Scenario (n = 10 trials):</strong> Expected value E[X] = 6.03.</li>
          <li>• <strong>Peak Mode:</strong> Peak probability at k = 6 with P(X = 6) = 0.2508 (25.08%).</li>
          <li>• <strong>Extreme Event Improbability:</strong> P(X = 0) = (1 - 0.6027)¹⁰ = 0.000088 (< 0.01%).</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Interactive PMF Calculator Capabilities</h3>
        <ul class="text-xs text-gray-300 space-y-2">
          <li>• <strong>Parametric Sliders:</strong> Interactive controls for sample size n (5 to 30), success rate p (0.05 to 0.95), and target threshold k.</li>
          <li>• <strong>Highlighted Mode:</strong> Highlights target bar k in glowing neon purple.</li>
          <li>• <strong>Cumulative CDF Calculation:</strong> P(X ≤ 6) = 60.9%.</li>
          <li>• <strong>Central Limit Convergence:</strong> Demonstrates binomial convergence to normal distribution as n increases.</li>
        </ul>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 10 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 11: BAYESIAN PROBABILITY & CONDITIONAL LIKELIHOOD -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-11">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Conditional Probability</span>
      <h2 class="text-2xl font-bold text-white mt-1">Bayesian Probability & Conditional Likelihood Modeling</h2>
      <p class="text-xs text-gray-400">Updating prior probabilities to evaluate genre-conditional anxiety risk: P(High Anxiety | Genre).</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Bayes' Law & Prior Updating</h3>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          P(A | B) = [ P(B | A) · P(A) ] / P(B)
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-purple-300">
          Prior P(High Anxiety) = 0.6027 (60.3%)
        </div>
        <ul class="text-xs text-gray-300 space-y-2 pt-1">
          <li>• <strong>Event A:</strong> Participant reports High Anxiety (Score ≥ 6).</li>
          <li>• <strong>Event B:</strong> Participant primary genre is Genre G.</li>
          <li>• <strong>Posterior P(A | B):</strong> The updated conditional probability given their music preference.</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Ranked Conditional Likelihood Across Genres</h3>
        <table class="w-full text-xs text-left">
          <thead class="text-gray-400 uppercase bg-gray-900 border-b border-gray-800">
            <tr>
              <th class="py-1.5 px-2">Genre</th>
              <th class="py-1.5 px-2">n</th>
              <th class="py-1.5 px-2">P(High Anxiety | Genre)</th>
              <th class="py-1.5 px-2">Relative Risk (vs 60.3%)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-800">
            <tr><td class="py-1.5 px-2 font-bold text-white">Folk</td><td>30</td><td class="text-rose-400 font-bold">76.7%</td><td>+27.3% (Highest Risk)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Lofi</td><td>10</td><td>70.0%</td><td>+16.1%</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Pop</td><td>114</td><td>66.7%</td><td>+10.7%</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Rock</td><td>188</td><td>64.4%</td><td>+6.8%</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Metal</td><td>88</td><td>61.4%</td><td>+1.9%</td></tr>
            <tr class="bg-gray-900/50"><td class="py-1.5 px-2 font-bold text-amber-300">Survey Baseline</td><td>735</td><td class="text-amber-300 font-bold">60.3%</td><td>1.00 (Prior Baseline)</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Classical</td><td>53</td><td>56.6%</td><td>-6.1%</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Video Game</td><td>44</td><td>54.5%</td><td>-9.6%</td></tr>
            <tr><td class="py-1.5 px-2 font-bold text-white">Latin</td><td>3</td><td>33.3%</td><td>-44.8% (Smallest Sample)</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 11 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 12: HIGH-PERFORMANCE UI & VISUAL ENGINE -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-12">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Software Engineering</span>
      <h2 class="text-2xl font-bold text-white mt-1">Interactive Mathematical Visualizer & UI Architecture</h2>
      <p class="text-xs text-gray-400">How AudioMental translates complex statistical theory into responsive, GPU-accelerated visualizations.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">60fps Fluid Polar Coordinate Morphing</h3>
        <div class="formula-box p-2.5 rounded-lg text-xs text-cyan-300">
          ease(t) = 1 - (1 - t)³   |   x(t) = x_start + (x_target - x_start) · ease(t)
        </div>
        <div class="formula-box p-2.5 rounded-lg text-xs text-purple-300">
          xᵢ = cx + rᵢ · cos(θᵢ)   |   yᵢ = cy - rᵢ · sin(θᵢ)
        </div>
        <ul class="text-xs text-gray-300 space-y-1.5 pt-1">
          <li>• <strong>Radar Morphing:</strong> When clicking from Gospel to Rock, the 4 polygon vertices smoothly stretch and glide along axes via requestAnimationFrame.</li>
          <li>• <strong>Donut Arc Tweening:</strong> Circumference C = 2πr; dash-arrays interpolate continuously without snapping.</li>
          <li>• <strong>Rolling Odometers:</strong> KPI values smoothly count up from 0 to final target values.</li>
        </ul>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Zero-Dependency Offline Reliability</h3>
        <ul class="text-xs text-gray-300 space-y-2">
          <li>• <strong>Pure Native Web Stack:</strong> 100% vanilla JavaScript & SVG. Requires no external CDN script dependencies.</li>
          <li>• <strong>Dual Deployment:</strong> Runs as a live HTTP server or as a self-contained offline HTML file.</li>
          <li>• <strong>Silky Tab Crossfades:</strong> Crossfading .view-panel states glide out (-8px) and in (+14px) smoothly.</li>
          <li>• <strong>Staggered Leaderboard Race:</strong> Ranking bars expand with 0.85s ease and index * 45ms offsets.</li>
        </ul>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 12 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 13: COMPREHENSIVE FINDINGS MATRIX -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-13">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Summary of Findings</span>
      <h2 class="text-2xl font-bold text-white mt-1">Comprehensive Hypothesis Testing Verification Matrix</h2>
      <p class="text-xs text-gray-400">Consolidated empirical verification across all primary research questions and statistical tests.</p>
    </div>

    <div class="glass-card p-5 rounded-xl my-auto py-4 space-y-3">
      <table class="w-full text-xs text-left">
        <thead class="text-gray-400 uppercase bg-gray-900 border-b border-gray-800">
          <tr>
            <th class="py-2 px-3">Statistical Method</th>
            <th class="py-2 px-3">Null Hypothesis (H₀)</th>
            <th class="py-2 px-3">Test Statistic</th>
            <th class="py-2 px-3">p-Value</th>
            <th class="py-2 px-3">Decision (α=0.05)</th>
            <th class="py-2 px-3">Academic Conclusion</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-800 text-gray-300">
          <tr>
            <td class="py-2 px-3 font-bold text-white">Welch's t-Test</td>
            <td>μ_work = μ_nowork</td>
            <td class="font-mono">t = -0.9791 (df=230.6)</td>
            <td class="font-mono text-amber-400 font-bold">0.3285</td>
            <td><span class="px-2 py-0.5 rounded bg-gray-800 text-gray-300 font-bold text-[10px]">Fail to Reject H₀</span></td>
            <td>Workplace listening does not alter anxiety.</td>
          </tr>
          <tr>
            <td class="py-2 px-3 font-bold text-white">Chi-Square (χ²)</td>
            <td>Genre & Anxiety Independent</td>
            <td class="font-mono">χ² = 6.9182 (df=6)</td>
            <td class="font-mono text-amber-400 font-bold">0.3285</td>
            <td><span class="px-2 py-0.5 rounded bg-gray-800 text-gray-300 font-bold text-[10px]">Fail to Reject H₀</span></td>
            <td>Music genre preference is independent of anxiety.</td>
          </tr>
          <tr>
            <td class="py-2 px-3 font-bold text-white">Pearson Correlation</td>
            <td>ρ = 0 (Linear trend)</td>
            <td class="font-mono">r = +0.0497 (t=1.35)</td>
            <td class="font-mono text-amber-400 font-bold">0.1787</td>
            <td><span class="px-2 py-0.5 rounded bg-gray-800 text-gray-300 font-bold text-[10px]">Fail to Reject H₀</span></td>
            <td>Listening hours do not linearly dictate anxiety.</td>
          </tr>
          <tr>
            <td class="py-2 px-3 font-bold text-white">Spearman Rank</td>
            <td>ρ_s = 0 (Monotonic trend)</td>
            <td class="font-mono">ρ = +0.0941</td>
            <td class="font-mono text-emerald-400 font-bold">0.0107 *</td>
            <td><span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[10px]">Reject H₀</span></td>
            <td>Weak positive monotonic rank association exists.</td>
          </tr>
          <tr>
            <td class="py-2 px-3 font-bold text-white">Binomial Model</td>
            <td>p = 0.50 (Chance)</td>
            <td class="font-mono">z = 5.57 (p̂=0.603)</td>
            <td class="font-mono text-emerald-400 font-bold">< 0.0001 ***</td>
            <td><span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[10px]">Reject H₀</span></td>
            <td>Statistically significant majority report anxiety ≥ 6.</td>
          </tr>
          <tr>
            <td class="py-2 px-3 font-bold text-white">One-Way ANOVA</td>
            <td>μ₁ = μ₂ = ... = μ_k</td>
            <td class="font-mono">F = 1.34 (df=15, 719)</td>
            <td class="font-mono text-amber-400 font-bold">0.1712</td>
            <td><span class="px-2 py-0.5 rounded bg-gray-800 text-gray-300 font-bold text-[10px]">Fail to Reject H₀</span></td>
            <td>Mean anxiety does not differ significantly across genres.</td>
          </tr>
        </tbody>
      </table>

      <div class="p-3 bg-gray-900 rounded-lg border border-gray-800 text-xs text-gray-300">
        <strong class="text-amber-400">Core Conclusion:</strong> Music preferences act as a therapeutic coping mechanism (73.7% reported improvement), but baseline anxiety and depression distributions remain statistically invariant across genres.
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 13 of 14</span>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- SLIDE 14: ACKNOWLEDGMENTS & TEAM ROLES -->
  <!-- ===================================================================== -->
  <section class="slide" id="slide-14">
    <div>
      <span class="px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold text-xs uppercase">Course Submission</span>
      <h2 class="text-2xl font-bold text-white mt-1">Acknowledgments, Team Roles & Deliverables</h2>
      <p class="text-xs text-gray-400">Final submission details for Probability & Statistics Course Evaluation.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-5 my-auto py-4">
      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3">
        <h3 class="text-base font-bold text-white">Project Authors & Student Identification</h3>
        <div class="space-y-3 text-xs">
          <div class="p-3 bg-gray-900/60 rounded-lg border border-gray-800">
            <h4 class="font-bold text-base text-white">Shubh Shetgaonkar</h4>
            <span class="text-indigo-400 font-mono font-semibold text-xs">Registration No: 25BCE2878</span>
          </div>
          <div class="p-3 bg-gray-900/60 rounded-lg border border-gray-800">
            <h4 class="font-bold text-base text-white">Riddhi Kotowar</h4>
            <span class="text-purple-400 font-mono font-semibold text-xs">Registration No: 25CBE2554</span>
          </div>
          <div class="p-3 bg-gray-900/60 rounded-lg border border-gray-800">
            <h4 class="font-bold text-base text-white">Ashmeetha Carol Noronha</h4>
            <span class="text-pink-400 font-mono font-semibold text-xs">Registration No: 25BDS0162</span>
          </div>
        </div>
      </div>

      <div class="md:col-span-6 glass-card p-5 rounded-xl space-y-3 flex flex-col justify-between">
        <div>
          <h3 class="text-base font-bold text-white mb-2">Project Repository & Deliverables</h3>
          <ul class="text-xs text-gray-300 space-y-2">
            <li><strong>Interactive Web App:</strong> <a href="index.html" class="text-indigo-400 underline font-mono">http://localhost:8080</a></li>
            <li><strong>Standalone Offline File:</strong> <span class="font-mono text-gray-300">genre_stats_dashboard.html</span></li>
            <li><strong>Presentation PDF:</strong> <a href="AudioMental_ProbStats_Presentation.pdf" download class="text-indigo-400 underline font-mono">AudioMental_ProbStats_Presentation.pdf</a></li>
            <li><strong>Academic Paper:</strong> <span class="font-mono text-gray-300">music_mental_health_report.md</span></li>
            <li><strong>Verification R Script:</strong> <span class="font-mono text-gray-300">additional_analysis.R</span></li>
          </ul>
        </div>
        <div class="p-4 bg-indigo-950/40 rounded-xl border border-indigo-500/30 text-center">
          <h4 class="text-lg font-extrabold text-white">Thank You!</h4>
          <p class="text-xs text-gray-400 mt-1">Open for Questions & Discussion in Probability & Statistics Review</p>
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between text-xs text-gray-500 border-t border-gray-800 pt-3">
      <span>AudioMental • Probability & Statistics Presentation</span>
      <span>Slide 14 of 14</span>
    </div>
  </section>

  <!-- Interactive Slide Navigation Script -->
  <script>
    let currentSlide = 1;
    const totalSlides = 14;

    function showSlide(num) {
      if (num < 1 || num > totalSlides) return;
      document.querySelectorAll('.slide').forEach((s, idx) => {
        if (idx + 1 === num) {
          s.classList.add('active');
        } else {
          s.classList.remove('active');
        }
      });
      currentSlide = num;
      document.getElementById('slide-indicator').textContent = `${currentSlide} / ${totalSlides}`;
      window.scrollTo(0, 0);
    }

    function nextSlide() {
      if (currentSlide < totalSlides) showSlide(currentSlide + 1);
    }

    function prevSlide() {
      if (currentSlide > 1) showSlide(currentSlide - 1);
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'Home') {
        e.preventDefault();
        showSlide(1);
      } else if (e.key === 'End') {
        e.preventDefault();
        showSlide(totalSlides);
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      }
    });
  </script>
</body>
</html>
'''

with open('Music-and-Mental-Health-Relation/web_dashboard/presentation.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated web_dashboard/presentation.html successfully!")
