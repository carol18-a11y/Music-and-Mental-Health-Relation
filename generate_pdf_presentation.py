#!/usr/bin/env python3
"""
AudioMental: Statistical & Inferential Modeling of Music Genre Preferences on Mental Health
Comprehensive Probability & Statistics Course Presentation PDF Generator
Authors:
  - Shubh Shetgaonkar (25BCE2878)
  - Riddhi Kotowar (25CBE2554)
  - Ashmeetha Carol Noronha (25BDS0162)
"""

import os
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# 16:9 Widescreen dimensions: 1152 x 648 points (16in x 9in at 72dpi)
PAGE_WIDTH = 1152
PAGE_HEIGHT = 648

# Color Palette (Dark Academic Theme matching AudioMental UI)
BG_DARK = colors.HexColor('#0b0f19')
CARD_BG = colors.HexColor('#111827')
CARD_BORDER = colors.HexColor('#1f2937')
CARD_INNER = colors.HexColor('#182234')
TEXT_WHITE = colors.HexColor('#f9fafb')
TEXT_MUTED = colors.HexColor('#9ca3af')
TEXT_SUBTLE = colors.HexColor('#6b7280')

COLOR_INDIGO = colors.HexColor('#6366f1')
COLOR_PURPLE = colors.HexColor('#a855f7')
COLOR_PINK = colors.HexColor('#ec4899')
COLOR_CYAN = colors.HexColor('#06b6d4')
COLOR_EMERALD = colors.HexColor('#10b981')
COLOR_AMBER = colors.HexColor('#f59e0b')
COLOR_ROSE = colors.HexColor('#f43f5e')

AUTHORS = "Shubh Shetgaonkar (25BCE2878)  •  Riddhi Kotowar (25CBE2554)  •  Ashmeetha Carol Noronha (25BDS0162)"

def wrap_text_lines(c, text, max_width, font_name='Helvetica', font_size=10, hanging_indent=0):
    """Splits text into wrapped lines that strictly fit within max_width points."""
    words = text.split()
    if not words:
        return []
    lines = []
    current_line = []
    for word in words:
        test_line = current_line + [word]
        is_first = (len(lines) == 0)
        avail = max_width if is_first else (max_width - hanging_indent)
        w = c.stringWidth(' '.join(test_line), font_name, font_size)
        if w <= avail or not current_line:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_wrapped_text(c, text, x, y, max_width, line_height=14, font_name='Helvetica', font_size=10, fill_color=TEXT_WHITE, hanging_indent=12):
    """
    Draws text wrapped strictly within max_width.
    Hanging indent is applied to lines 2+ if there is a bullet or number.
    Returns the new y position.
    """
    lines = wrap_text_lines(c, text, max_width, font_name, font_size, hanging_indent)
    c.setFont(font_name, font_size)
    c.setFillColor(fill_color)
    for i, line in enumerate(lines):
        lx = x if i == 0 else (x + hanging_indent)
        c.drawString(lx, y, line)
        y -= line_height
    return y

def draw_slide_base(c, slide_num, total_slides, category, title, subtitle):
    """Draws consistent background, header, category pill, and footer on every slide."""
    # Background
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # Top accent bar
    c.setFillColor(COLOR_INDIGO)
    c.rect(0, PAGE_HEIGHT - 6, PAGE_WIDTH, 6, fill=1, stroke=0)

    # Category Pill
    c.setFillColor(colors.HexColor('#1e1b4b'))
    c.setStrokeColor(COLOR_INDIGO)
    c.setLineWidth(1)
    c.roundRect(50, PAGE_HEIGHT - 48, 220, 24, 12, fill=1, stroke=1)
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(62, PAGE_HEIGHT - 38, category.upper())

    # Title
    c.setFillColor(TEXT_WHITE)
    c.setFont('Helvetica-Bold', 22)
    c.drawString(50, PAGE_HEIGHT - 82, title)

    # Subtitle
    c.setFillColor(TEXT_MUTED)
    c.setFont('Helvetica', 12)
    c.drawString(50, PAGE_HEIGHT - 104, subtitle)

    # Header Divider Line
    c.setStrokeColor(CARD_BORDER)
    c.setLineWidth(1)
    c.line(50, PAGE_HEIGHT - 116, PAGE_WIDTH - 50, PAGE_HEIGHT - 116)

    # Footer
    c.setStrokeColor(CARD_BORDER)
    c.line(50, 42, PAGE_WIDTH - 50, 42)

    c.setFillColor(TEXT_SUBTLE)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(50, 26, "AUDIOMENTAL")
    c.setFont('Helvetica', 9)
    c.drawString(135, 26, f"•   Probability & Statistics Course Project   •   {AUTHORS}")

    # Slide Counter
    c.drawRightString(PAGE_WIDTH - 50, 26, f"Slide {slide_num} of {total_slides}")

def draw_card(c, x, y, w, h, title=None, badge=None, badge_color=COLOR_INDIGO):
    """Draws a styled container card."""
    c.setFillColor(CARD_BG)
    c.setStrokeColor(CARD_BORDER)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)

    if title:
        c.setFillColor(TEXT_WHITE)
        c.setFont('Helvetica-Bold', 13)
        c.drawString(x + 18, y + h - 28, title)

    if badge:
        c.setFillColor(CARD_INNER)
        c.setStrokeColor(badge_color)
        c.setLineWidth(1)
        bw = len(badge) * 7 + 16
        c.roundRect(x + w - bw - 16, y + h - 32, bw, 20, 10, fill=1, stroke=1)
        c.setFillColor(badge_color)
        c.setFont('Helvetica-Bold', 9)
        c.drawRightString(x + w - 24, y + h - 24, badge)

def draw_formula_box(c, x, y, w, h, formula_text, label="Mathematical Definition"):
    """
    Draws a highlighted formula container.
    Dynamically scales down the font size to guarantee that formulas never overflow
    the box boundaries or page borders regardless of formula length.
    """
    c.setFillColor(colors.HexColor('#0c1322'))
    c.setStrokeColor(colors.HexColor('#2e384d'))
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(x + 14, y + h - 16, label.upper())

    lines = formula_text.split('\n')
    avail_w = w - 30  # 15pt margin on each side for comfortable internal breathing room

    # Auto-scale font size so all lines fit cleanly within the box width
    font_size = 11.0
    for line in lines:
        while font_size > 6.0 and c.stringWidth(line, 'Courier-Bold', font_size) > avail_w:
            font_size -= 0.25

    c.setFillColor(colors.HexColor('#38bdf8'))
    c.setFont('Courier-Bold', font_size)

    if len(lines) == 1:
        # Vertically center single-line formula in the available box area below the label
        vert_y = y + (h - 22) / 2 - (font_size * 0.35) + 3
        c.drawString(x + 15, vert_y, lines[0])
    else:
        # Vertically center multi-line formula
        line_h = font_size * 1.35
        total_text_h = len(lines) * line_h
        start_y = y + (h - 22 + total_text_h) / 2 - (font_size * 0.35)
        for i, line in enumerate(lines):
            c.drawString(x + 15, start_y - (i * line_h), line)

def create_presentation(filename="AudioMental_ProbStats_Presentation.pdf"):
    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    total_slides = 14

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # Ambient Glow decoration
    c.setFillColor(colors.HexColor('#1e1b4b'))
    c.circle(PAGE_WIDTH - 200, PAGE_HEIGHT - 180, 240, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#172554'))
    c.circle(200, 150, 220, fill=1, stroke=0)

    # Accent Top Line
    c.setFillColor(COLOR_INDIGO)
    c.rect(0, PAGE_HEIGHT - 8, PAGE_WIDTH, 8, fill=1, stroke=0)

    # Project Pill
    c.setFillColor(colors.HexColor('#1e1b4b'))
    c.setStrokeColor(COLOR_CYAN)
    c.setLineWidth(1.5)
    c.roundRect(70, PAGE_HEIGHT - 130, 360, 32, 16, fill=1, stroke=1)
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(90, PAGE_HEIGHT - 117, "🎧  PROBABILITY & STATISTICS COURSE PROJECT")

    # Main Project Title
    c.setFillColor(TEXT_WHITE)
    c.setFont('Helvetica-Bold', 40)
    c.drawString(70, PAGE_HEIGHT - 195, "AudioMental")

    c.setFont('Helvetica-Bold', 24)
    c.setFillColor(COLOR_INDIGO)
    c.drawString(70, PAGE_HEIGHT - 235, "Statistical & Inferential Modeling of Music Genre Preferences")
    c.setFillColor(TEXT_MUTED)
    c.drawString(70, PAGE_HEIGHT - 268, "on Psychological Well-Being (Anxiety, Depression, Insomnia & OCD)")

    # Horizontal Rule
    c.setStrokeColor(CARD_BORDER)
    c.setLineWidth(1.5)
    c.line(70, PAGE_HEIGHT - 295, PAGE_WIDTH - 70, PAGE_HEIGHT - 295)

    # Authors Box (Left) - ROLES REMOVED AS REQUESTED
    draw_card(c, 70, 75, 480, 200, "Project Research Authors")
    authors_data = [
        ("Shubh Shetgaonkar", "25BCE2878"),
        ("Riddhi Kotowar", "25CBE2554"),
        ("Ashmeetha Carol Noronha", "25BDS0162")
    ]
    curr_y = 215
    for name, reg in authors_data:
        c.setFillColor(CARD_INNER)
        c.setStrokeColor(CARD_BORDER)
        c.roundRect(85, curr_y - 12, 450, 38, 6, fill=1, stroke=1)

        c.setFillColor(TEXT_WHITE)
        c.setFont('Helvetica-Bold', 13)
        c.drawString(102, curr_y + 2, name)

        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 11.5)
        c.drawString(330, curr_y + 2, f"Reg. No: {reg}")
        curr_y -= 48

    # Metadata & Dataset Box (Right) - Text strictly wrapped inside card
    draw_card(c, 580, 75, 500, 200, "Course Context & Dataset Specifications")
    meta_info = [
        ("Course:", "Probability & Statistics (Class Review & Evaluation)"),
        ("Dataset:", "Kaggle Music & Mental Health Survey (MxMH)"),
        ("Sample Size:", "N = 735 Validated Survey Respondents"),
        ("Variables:", "33 Evaluated Features (Mental Health Scales 0-10, Habits, Genres)"),
        ("Core Methods:", "Continuous Gaussian PDF, Bivariate OLS, Welch's t-Test, Chi-Square, Binomial"),
        ("Deliverables:", "Live Interactive Dashboard + Offline Standalone + Slide Deck + PDF")
    ]
    my = 226
    for lbl, val in meta_info:
        c.setFillColor(COLOR_INDIGO)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(600, my, lbl)
        my = draw_wrapped_text(c, val, 705, my, 355, line_height=12.5, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)
        my -= 3

    c.showPage()

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & RESEARCH OBJECTIVES
    # =========================================================================
    draw_slide_base(c, 2, total_slides, "Executive Summary", 
                    "Research Motivation & Scientific Objectives", 
                    "Investigating whether subjective musical taste has statistically measurable links with clinical mental health scores.")

    col_w = (PAGE_WIDTH - 100 - 40) / 3

    # Card 1: Core Problem Statement
    draw_card(c, 50, 140, col_w, 360, "1. Problem Formulation", "RQ1 & RQ2", COLOR_ROSE)
    cy = 455
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(68, cy, "Primary Research Questions:")
    cy -= 18

    rqs = [
        "• Does daily music listening duration correlate linearly with self-reported anxiety severity?",
        "• Do workplace listeners experience lower psychological strain than non-workplace listeners?",
        "• Does preference for intense genres (e.g., Metal, Rock) associate with higher incidence of clinical anxiety or depression?"
    ]
    for rq in rqs:
        cy = draw_wrapped_text(c, rq, 68, cy, col_w - 36, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=12)
        cy -= 5

    cy -= 4
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(68, cy, "Scientific Importance:")
    cy -= 18
    cy = draw_wrapped_text(c, "Music therapy is widely cited, but quantitative probabilistic foundations across large-sample real-world surveys remain under-analyzed.", 
                           68, cy, col_w - 36, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_MUTED, hanging_indent=0)

    # Card 2: Probability & Stats Methodology
    draw_card(c, 50 + col_w + 20, 140, col_w, 360, "2. Statistical Framework", "Curriculum", COLOR_INDIGO)
    cy = 455
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(68 + col_w + 20, cy, "Curriculum Topic Alignments:")
    cy -= 18

    curric = [
        "1. Exploratory Location & Dispersion: Sample mean, variance, IQR, Tukey outlier fences.",
        "2. Continuous Modeling: Normal distribution fitting and empirical density overlays.",
        "3. Bivariate Association: Pearson product-moment vs. Spearman rank correlation.",
        "4. Parametric Modeling: Ordinary Least Squares (OLS) bivariate regression.",
        "5. Two-Sample Testing: Welch unequal-variance t-test with Satterthwaite df.",
        "6. Contingency Analysis: Pearson Chi-Square (χ²) test of independence.",
        "7. Discrete Modeling: Binomial PMF & Bayes conditional probability theorem."
    ]
    for cur in curric:
        cy = draw_wrapped_text(c, cur, 68 + col_w + 20, cy, col_w - 36, line_height=12.5, font_name='Helvetica', font_size=9, fill_color=TEXT_WHITE, hanging_indent=13)
        cy -= 3

    # Card 3: Key Analytical Findings
    draw_card(c, 50 + (col_w + 20) * 2, 140, col_w, 360, "3. Summary of Findings", "Empirical", COLOR_EMERALD)
    cy = 455
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(68 + (col_w + 20) * 2, cy, "Key Empirical Takeaways:")
    cy -= 18

    takeaways = [
        "• Weak Linear Trend: Pearson r = 0.0497 (p = 0.1787). Listening hours do not linearly dictate anxiety.",
        "• Monotonic Rank Trend: Spearman ρ = 0.0941 (p = 0.0107*). Indicates subtle monotonic rank association.",
        "• Workplace Invariance: Welch t = -0.9791 (p = 0.3285). Listening while working does not significantly alter anxiety.",
        "• Genre Independence: χ² = 6.9182 (df = 6, p = 0.3285). Genre preference is independent of high anxiety.",
        "• Positive Solace: 73.7% survey-wide report music improves their psychological state."
    ]
    for tk in takeaways:
        cy = draw_wrapped_text(c, tk, 68 + (col_w + 20) * 2, cy, col_w - 36, line_height=12.5, font_name='Helvetica', font_size=9, fill_color=TEXT_WHITE, hanging_indent=12)
        cy -= 4

    # Bottom Callout Box
    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_INDIGO)
    c.roundRect(50, 60, PAGE_WIDTH - 100, 65, 8, fill=1, stroke=1)
    c.setFillColor(COLOR_AMBER)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(70, 102, "💡 SCIENTIFIC TAKEAWAY FOR COURSE REVIEW:")
    draw_wrapped_text(c, "Self-reported emotional solace does NOT translate into disparate baseline mental health severities. Statistical tests confirm that listeners of all genres share comparable psychological distributions.", 
                      70, 84, PAGE_WIDTH - 140, line_height=14, font_name='Helvetica', font_size=10, fill_color=TEXT_WHITE, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 3: DATASET ANATOMY & DATA PREPROCESSING
    # =========================================================================
    draw_slide_base(c, 3, total_slides, "Data Pipeline", 
                    "Dataset Anatomy & Robust Preprocessing Pipeline", 
                    "Transformation of raw survey records into structured, distribution-ready statistical vectors.")

    draw_card(c, 50, 70, 480, 430, "Survey Data Cleaning & Filtering Protocol", "ETL Pipeline")
    etl_steps = [
        ("Raw Ingestion:", "736 survey submissions collected across diverse international demographics."),
        ("Validation & Dropping:", "Removed row with missing primary genre / unparseable numeric bounds (Final N = 735)."),
        ("Continuous Bounds:", "Daily listening hours truncated and validated against physical day boundaries (0 - 24 hrs)."),
        ("Discrete Likert Scales:", "Anxiety, Depression, Insomnia, OCD scored integer discrete [0, 10]."),
        ("Nominal Categorical:", "Primary Genre (16 discrete classes: Rock, Pop, Metal, Classical, etc.)."),
        ("Binary Dichotomy:", "Listen while working? [Yes (n=578, 78.6%), No (n=154, 21.0%), Unknown (n=3)]."),
        ("Perceived Solace:", "Music Effects [Improve (n=542, 73.7%), No Effect (n=169, 23.0%), Worsen (n=17, 2.3%)]."),
        ("Format Parity:", "Simultaneously serialized into JSON for web runtime and CSV for base R statistical verification.")
    ]
    ey = 450
    for title, desc in etl_steps:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawString(68, ey, title)
        ey = draw_wrapped_text(c, desc, 210, ey, 305, line_height=12.5, font_name='Helvetica', font_size=9, fill_color=TEXT_WHITE, hanging_indent=0)
        ey -= 4

    # Right Column: Global Benchmark Table
    draw_card(c, 550, 70, 550, 430, "Global Empirical Summary Metrics (N = 735)", "Parameters")
    table_headers = ["Metric Variable", "Sample Mean (x̄)", "Sample SD (s)", "Median", "IQR [Q1, Q3]"]
    ty = 450
    c.setFillColor(colors.HexColor('#2e384d'))
    c.rect(570, ty - 6, 510, 24, fill=1, stroke=0)
    c.setFillColor(COLOR_INDIGO)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(580, ty + 2, table_headers[0])
    c.drawString(720, ty + 2, table_headers[1])
    c.drawString(830, ty + 2, table_headers[2])
    c.drawString(930, ty + 2, table_headers[3])
    c.drawString(1000, ty + 2, table_headers[4])

    rows = [
        ("Anxiety Score (0-10)", "5.83", "2.79", "6.0", "[4.0, 8.0] (4.0)"),
        ("Depression Score (0-10)", "4.80", "3.03", "5.0", "[2.0, 7.0] (5.0)"),
        ("Insomnia Score (0-10)", "3.74", "3.09", "3.0", "[1.0, 6.0] (5.0)"),
        ("OCD Score (0-10)", "2.63", "2.85", "2.0", "[0.0, 4.0] (4.0)"),
        ("Daily Listening Hours", "3.71 hrs", "3.03", "3.0 hrs", "[2.0, 5.0] (3.0)"),
        ("Participant Age", "25.2 yrs", "12.05", "21.0 yrs", "[18.0, 28.0] (10.0)")
    ]
    r_y = ty - 32
    for r in rows:
        c.setFillColor(TEXT_WHITE)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawString(580, r_y, r[0])
        c.setFont('Helvetica', 9.5)
        c.drawString(720, r_y, r[1])
        c.drawString(830, r_y, r[2])
        c.drawString(930, r_y, r[3])
        c.drawString(1000, r_y, r[4])
        c.setStrokeColor(CARD_BORDER)
        c.line(570, r_y - 6, 1080, r_y - 6)
        r_y -= 28

    draw_formula_box(c, 570, 95, 510, 55, 
                     "s = sqrt( (1 / (n - 1)) * sum( (x_i - mean(x))^2 ) )", 
                     "Sample Standard Deviation (Bessel-Corrected)")

    c.showPage()

    # =========================================================================
    # SLIDE 4: DESCRIPTIVE STATISTICS & FIVE-NUMBER SUMMARY
    # =========================================================================
    draw_slide_base(c, 4, total_slides, "Descriptive Statistics", 
                    "Location, Dispersion & Five-Number Summary Analysis", 
                    "Evaluating central tendency and non-parametric spread across psychological dimensions.")

    col_w2 = (PAGE_WIDTH - 100 - 20) / 2

    draw_card(c, 50, 70, col_w2, 430, "Theoretical Formulas & Foundations", "Theory")
    draw_formula_box(c, 70, 395, col_w2 - 40, 50, 
                     "x_bar = (1 / n) * sum(x_i, i=1..n)", "Sample Mean (First Central Moment)")
    draw_formula_box(c, 70, 335, col_w2 - 40, 50, 
                     "s^2 = (1 / (n - 1)) * sum( (x_i - x_bar)^2 )", "Sample Variance (Bessel's Correction)")
    draw_formula_box(c, 70, 275, col_w2 - 40, 50, 
                     "IQR = Q3 - Q1   |   Whiskers: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]", "Tukey's Interquartile Range & Outlier Fences")

    theory_bullets = [
        "• Robustness Considerations: Means and variances are susceptible to extreme values (e.g. participant reporting 24h listening).",
        "• Median & IQR Resilience: The median (Q2) remains resilient to skewed tails, making it ideal for discrete 0-10 Likert scales.",
        "• Outlier Classification: Any observation outside [Q1 - 1.5 IQR, Q3 + 1.5 IQR] is isolated as an outlier in our interactive boxplots.",
        "• Implementation in AudioMental: Live boxplots feature an interactive Jitter toggle that renders each participant dot overlaid on top of quartiles."
    ]
    by = 240
    for b in theory_bullets:
        by = draw_wrapped_text(c, b, 70, by, col_w2 - 40, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_MUTED, hanging_indent=12)
        by -= 6

    # Right Card: Working vs Non-Working Comparison Boxplot Data
    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Two-Sample Boxplot Quartiles: Work vs Non-Work", "Application")
    c.setFillColor(TEXT_WHITE)
    c.setFont('Helvetica', 10.5)
    c.drawString(70 + col_w2 + 20, 445, "Comparison of Anxiety Scores grouped by 'Listens while working':")

    sub_headers = ["Statistic", "Listens While Working (YES)", "Does NOT Listen (NO)"]
    sy = 410
    c.setFillColor(colors.HexColor('#2e384d'))
    c.rect(70 + col_w2 + 20, sy - 6, col_w2 - 40, 22, fill=1, stroke=0)
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(80 + col_w2 + 20, sy + 2, sub_headers[0])
    c.drawString(220 + col_w2 + 20, sy + 2, sub_headers[1])
    c.drawString(390 + col_w2 + 20, sy + 2, sub_headers[2])

    comp_rows = [
        ("Sample Size (n)", "578 participants (78.6%)", "154 participants (21.0%)"),
        ("Sample Mean (x̄)", "5.88", "5.62"),
        ("Sample Std Dev (s)", "2.76", "2.90"),
        ("Minimum (Min)", "0.0", "0.0"),
        ("First Quartile (Q1)", "4.0", "3.0"),
        ("Median (Q2)", "6.0", "6.0 (Identical)"),
        ("Third Quartile (Q3)", "8.0", "8.0 (Identical)"),
        ("Maximum (Max)", "10.0", "10.0"),
        ("Interquartile Range", "IQR = 4.0", "IQR = 5.0")
    ]
    r_y2 = sy - 28
    for r in comp_rows:
        c.setFillColor(TEXT_WHITE)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawString(80 + col_w2 + 20, r_y2, r[0])
        c.setFont('Helvetica', 9.5)
        c.drawString(220 + col_w2 + 20, r_y2, r[1])
        c.drawString(390 + col_w2 + 20, r_y2, r[2])
        c.setStrokeColor(CARD_BORDER)
        c.line(70 + col_w2 + 20, r_y2 - 6, 70 + col_w2 + 20 + col_w2 - 40, r_y2 - 6)
        r_y2 -= 24

    c.setFillColor(COLOR_EMERALD)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(70 + col_w2 + 20, 114, "Statistical Finding:")
    draw_wrapped_text(c, "Both cohorts exhibit identical median scores of 6.0 and matching Q3 boundaries. Workplace listening neither elevates nor depresses clinical anxiety distributions.",
                      70 + col_w2 + 20, 96, col_w2 - 40, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_MUTED, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 5: CONTINUOUS PROBABILITY: GAUSSIAN MODELING
    # =========================================================================
    draw_slide_base(c, 5, total_slides, "Continuous Probability", 
                    "Continuous Probability Density Modeling (Gaussian Fit)", 
                    "Superimposing theoretical Normal distributions N(μ, σ²) onto discrete empirical histograms.")

    draw_card(c, 50, 70, col_w2, 430, "Theoretical Normal Density & Scaling", "Mathematical Model")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "f(x; mu, sigma) = (1 / (sigma * sqrt(2*pi))) * exp( -((x - mu)^2) / (2*sigma^2) )", 
                     "Gaussian Probability Density Function")
    draw_formula_box(c, 70, 320, col_w2 - 40, 55, 
                     "h(x) = N * Delta_x * f(x; mu, sigma)", 
                     "Discrete Histogram Frequency Scaling Equation")

    g_points = [
        "• Dimensionality: Anxiety, Depression, Insomnia, and OCD are recorded on 0-10 discrete scales, while daily listening is a continuous non-negative real.",
        "• Binning Protocol: In AudioMental's interactive Studio, users can vary the bin count k in [5, 20]. The step width Delta_x = (x_max - x_min) / k.",
        "• Scaled Density Curve: Multiplying the PDF f(x) by N * Delta_x aligns the continuous curve area directly with discrete bar count frequencies.",
        "• Goodness of Visual Fit: Anxiety exhibits a slight negative skew with a mode at 6-7, while OCD shows a strong right skew (peak at 0-1)."
    ]
    gy = 280
    for p in g_points:
        gy = draw_wrapped_text(c, p, 70, gy, col_w2 - 40, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_MUTED, hanging_indent=12)
        gy -= 6

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Interactive Histogram Studio Capabilities", "Live Feature")
    features = [
        ("Parametric Bin Slider:", "Dynamically re-aggregates 735 observations from 5 to 20 bins in real time."),
        ("Normal Curve Toggle:", "Computes live sample mean and standard deviation, overlaying glowing SVG Gaussian curves."),
        ("Mean & Median Lines:", "Draws vertical reference lines: cyan dashed line for sample mean, amber for sample median."),
        ("Hover Crosshair Inspector:", "Hovering over any bin displays exact interval [a, b), absolute frequency, and percentage share."),
        ("Full Dimension Switching:", "Seamlessly toggles between Anxiety, Depression, Insomnia, OCD, and Listening Hours.")
    ]
    fy = 445
    for title, desc in features:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70 + col_w2 + 20, fy, title)
        fy -= 14
        fy = draw_wrapped_text(c, desc, 70 + col_w2 + 20, fy, col_w2 - 40, line_height=12.5, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)
        fy -= 6

    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_EMERALD)
    c.roundRect(70 + col_w2 + 20, 95, col_w2 - 40, 70, 8, fill=1, stroke=1)
    c.setFillColor(COLOR_EMERALD)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(85 + col_w2 + 20, 145, "📥 Crisp Vector SVG Export Engine:")
    draw_wrapped_text(c, "Users can click 'Export SVG' to download mathematically precise vector graphics directly into research reports and course slide decks without pixelation.",
                      85 + col_w2 + 20, 128, col_w2 - 70, line_height=13, font_name='Helvetica', font_size=9, fill_color=TEXT_WHITE, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 6: BIVARIATE CORRELATION: PEARSON VS SPEARMAN
    # =========================================================================
    draw_slide_base(c, 6, total_slides, "Bivariate Analysis", 
                    "Correlation Analysis: Pearson Linear vs. Spearman Rank", 
                    "Evaluating monotonic vs linear dependency between daily music listening hours and anxiety.")

    draw_card(c, 50, 70, col_w2, 430, "Pearson Product-Moment Correlation (r)", "Parametric")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "r = Cov(X,Y) / (s_X * s_Y) = sum((x_i - x_bar)(y_i - y_bar)) / sqrt(sum(dx^2)*sum(dy^2))", 
                     "Pearson Correlation Coefficient")

    c.setFillColor(TEXT_WHITE)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(70, 360, "Empirical Finding: r = +0.0497 (t = 1.35, p = 0.1787)")

    p_facts = [
        "• Hypothesis: H0: rho = 0 (No linear correlation) vs H1: rho != 0",
        "• Critical Value: For df = 733 and alpha = 0.05, critical t = 1.963",
        "• Decision: t = 1.35 < 1.963, p-value = 0.1787 > 0.05",
        "• Statistical Verdict: Fail to Reject H0. There is no statistically significant linear relationship between hours spent listening to music and anxiety.",
        "• Coefficient of Determination: R^2 = r^2 = 0.0025. Only 0.25% of the total variance in anxiety scores can be explained by daily listening duration."
    ]
    py = 330
    for pf in p_facts:
        py = draw_wrapped_text(c, pf, 70, py, col_w2 - 40, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_MUTED, hanging_indent=12)
        py -= 5

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Spearman Rank-Order Correlation (rho)", "Non-Parametric")
    draw_formula_box(c, 70 + col_w2 + 20, 390, col_w2 - 40, 55, 
                     "rho = 1 - ( 6 * sum(d_i^2) ) / ( n * (n^2 - 1) )", 
                     "Spearman Monotonic Rank-Order Formulation")

    c.setFillColor(COLOR_EMERALD)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(70 + col_w2 + 20, 360, "Empirical Finding: rho = +0.0941 (p = 0.0107 *)")

    s_facts = [
        "• Hypothesis: H0: No monotonic association between ranks.",
        "• Decision: p-value = 0.0107 < alpha = 0.05. Reject H0.",
        "• Statistical Verdict: Significant positive monotonic trend detected.",
        "• Key Academic Rigor - Why does Spearman detect significance while Pearson fails?",
        "  1. Robust to Ties & Non-Normality: The 0-10 anxiety scale has heavy discrete ties.",
        "  2. Non-Linear Monotonicity: Higher listening hours weakly accompany higher rank orders of anxiety, without obeying a strict straight-line proportional increment."
    ]
    sy = 330
    for sf in s_facts:
        is_highlight = sf.startswith("• Key")
        color = COLOR_AMBER if is_highlight else TEXT_MUTED
        font = 'Helvetica-Bold' if is_highlight else 'Helvetica'
        sy = draw_wrapped_text(c, sf, 70 + col_w2 + 20, sy, col_w2 - 40, line_height=12.5, font_name=font, font_size=9.5, fill_color=color, hanging_indent=12)
        sy -= 4

    c.showPage()

    # =========================================================================
    # SLIDE 7: ORDINARY LEAST SQUARES (OLS) REGRESSION
    # =========================================================================
    draw_slide_base(c, 7, total_slides, "Regression Modeling", 
                    "Ordinary Least Squares (OLS) Bivariate Regression", 
                    "Quantifying the linear predictor model between listening duration and psychological distress.")

    draw_card(c, 50, 70, col_w2, 430, "Mathematical Formulation & Parameter Estimation", "OLS Derivation")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "y_hat = beta_0 + beta_1 * x", "Simple Linear Regression Model")
    draw_formula_box(c, 70, 320, col_w2 - 40, 55, 
                     "beta_1 = Cov(X,Y) / Var(X)   |   beta_0 = y_bar - beta_1 * x_bar", "OLS Normal Equation Parameter Estimators")

    ols_steps = [
        ("Slope (beta_1):", "beta_1 = 0.0458. For every additional hour of music listened daily, predicted anxiety rises by just 0.046 points."),
        ("Intercept (beta_0):", "beta_0 = 5.6698. The baseline predicted anxiety score for an individual listening to zero music hours."),
        ("Fitted Model:", "Anxiety_Hat = 5.6698 + 0.0458 * (Hours)"),
        ("ANOVA F-Statistic:", "F(1, 733) = 1.815, p-value = 0.1787. Overall model regression is not statistically significant."),
        ("Residual Variance:", "Residual Standard Error: s_e = 2.788 on 733 degrees of freedom.")
    ]
    oy = 285
    for title, desc in ols_steps:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70, oy, title)
        oy = draw_wrapped_text(c, desc, 195, oy, col_w2 - 165, line_height=12.5, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)
        oy -= 6

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Interactive Scatter Studio & Participant Inspector", "Application")
    insp_features = [
        ("N=735 Circle Rendering:", "Renders all 735 surveyed participants as interactive vector circles with customizable opacity & size."),
        ("Per-Participant Inspection:", "Hovering over any dot displays their Participant ID, Age, Daily Hours, Genre, Workplace status, and Perceived Effect."),
        ("Real-Time Genre Subsetting:", "Filter by Rock, Pop, Metal, Classical, etc. Live OLS recalculates slope, intercept, and r instantly."),
        ("Regression Line Overlay:", "Renders the glowing OLS linear equation badge with interactive toggles for visual assessment.")
    ]
    iy = 445
    for title, desc in insp_features:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70 + col_w2 + 20, iy, title)
        iy -= 14
        iy = draw_wrapped_text(c, desc, 70 + col_w2 + 20, iy, col_w2 - 40, line_height=12.5, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)
        iy -= 6

    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_AMBER)
    c.roundRect(70 + col_w2 + 20, 95, col_w2 - 40, 80, 8, fill=1, stroke=1)
    c.setFillColor(COLOR_AMBER)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(85 + col_w2 + 20, 155, "⚠️ Practical Interpretation for Course Defense:")
    draw_wrapped_text(c, "While pop culture often assumes excessive music consumption reflects depressive states, OLS modeling proves that daily listening duration explains less than 0.3% of anxiety. Individual psychological state is dictated by factors far beyond daily listening hours.",
                      85 + col_w2 + 20, 138, col_w2 - 70, line_height=12.5, font_name='Helvetica', font_size=9, fill_color=TEXT_WHITE, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 8: TWO-SAMPLE HYPOTHESIS TESTING: WELCH'S T-TEST
    # =========================================================================
    draw_slide_base(c, 8, total_slides, "Hypothesis Testing", 
                    "Two-Sample Welch's t-Test & Confidence Intervals", 
                    "Testing whether listening while working causes statistically significant shifts in anxiety.")

    draw_card(c, 50, 70, col_w2, 430, "Hypothesis Formulation & Welch-Satterthwaite", "Formulation")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "H0: mu_work = mu_nowork   vs.   H1: mu_work != mu_nowork", "Two-Tailed Hypothesis Formulation")
    draw_formula_box(c, 70, 320, col_w2 - 40, 55, 
                     "t = (x_bar1 - x_bar2) / sqrt( s1^2 / n1 + s2^2 / n2 )", "Welch's Two-Sample t-Statistic")
    draw_formula_box(c, 70, 250, col_w2 - 40, 55, 
                     "df = (s1^2/n1 + s2^2/n2)^2 / [ (s1^2/n1)^2/(n1-1) + (s2^2/n2)^2/(n2-1) ]", "Welch-Satterthwaite Effective Degrees of Freedom")

    hyps = [
        "• Group 1 (Works to Music): n1 = 578, x_bar1 = 5.88, s1 = 2.76",
        "• Group 2 (No Music at Work): n2 = 154, x_bar2 = 5.62, s2 = 2.90",
        "• Welch's Degrees of Freedom: df = 230.6 (Robust to unequal variances)",
        "• Test Statistic Result: t = -0.9791"
    ]
    hy = 215
    for h in hyps:
        c.setFillColor(TEXT_WHITE)
        c.setFont('Helvetica', 9.5)
        c.drawString(70, hy, h)
        hy -= 22

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Decision Boundaries & 95% Confidence Intervals", "Decision")
    d_points = [
        ("Significance Threshold:", "alpha = 0.05 (Two-Tailed Rejection Boundary: alpha/2 = 0.025 per tail)"),
        ("Critical Values:", "t_critical = +/- 1.970"),
        ("Observed Test Stat:", "t = -0.9791 falls comfortably inside acceptance region [-1.970, +1.970]."),
        ("p-Value:", "p = 0.3285 > 0.05. High probability of observing this data under H0."),
        ("Statistical Decision:", "FAIL TO REJECT NULL HYPOTHESIS (H0)."),
        ("Cohen's d Effect Size:", "d = (x_bar1 - x_bar2) / s_pooled = 0.09 (Negligible effect size < 0.20).")
    ]
    dy = 445
    for title, desc in d_points:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70 + col_w2 + 20, dy, title)
        dy -= 14
        color = COLOR_EMERALD if title.startswith("Statistical") else TEXT_WHITE
        font = 'Helvetica-Bold' if title.startswith("Statistical") else 'Helvetica'
        dy = draw_wrapped_text(c, desc, 70 + col_w2 + 20, dy, col_w2 - 40, line_height=12.5, font_name=font, font_size=9.5, fill_color=color, hanging_indent=0)
        dy -= 6

    draw_formula_box(c, 70 + col_w2 + 20, 95, col_w2 - 40, 60, 
                     "95% CI for (mu1 - mu2) = [-0.772, +0.260]", 
                     "95% Population Difference Confidence Interval")

    c.showPage()

    # =========================================================================
    # SLIDE 9: CONTINGENCY & CHI-SQUARE TEST OF INDEPENDENCE
    # =========================================================================
    draw_slide_base(c, 9, total_slides, "Categorical Analysis", 
                    "Contingency Tables & Chi-Square (χ²) Independence Test", 
                    "Evaluating whether primary music genre preference associates with high clinical anxiety severity.")

    draw_card(c, 50, 70, col_w2, 430, "Chi-Square Test Formulation & Contingency Table", "Independence")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "H0: Genre Preference and Anxiety Severity are Independent", "Null Hypothesis Statement")
    draw_formula_box(c, 70, 320, col_w2 - 40, 55, 
                     "chi^2 = sum_i sum_j ( (O_ij - E_ij)^2 / E_ij )", "Pearson's Chi-Square Test Statistic")
    draw_formula_box(c, 70, 250, col_w2 - 40, 55, 
                     "E_ij = (Row_i * Col_j) / N", "Expected Cell Frequencies under Independence")

    c_points = [
        "• Contingency Matrix: 7 Genres (Classical, EDM, Metal, Pop, Rock, Video Game, Other) x 2 Anxiety Tiers (High >= 6 vs Normal < 6).",
        "• Total Sample N = 735 respondents across contingency cells.",
        "• Assumption Verification: All expected cell frequencies E_ij > 5, satisfying Cochran's rule for valid Chi-square asymptotic approximation."
    ]
    cy2 = 215
    for cp in c_points:
        cy2 = draw_wrapped_text(c, cp, 70, cy2, col_w2 - 40, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_MUTED, hanging_indent=12)
        cy2 -= 6

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Test Results & Cramer's V Effect Size", "Findings")
    chi_results = [
        ("Chi-Square Statistic:", "X^2 = 6.9182"),
        ("Degrees of Freedom:", "df = (r - 1) * (c - 1) = (7 - 1) * (2 - 1) = 6"),
        ("p-Value:", "p = 0.3285 > 0.05"),
        ("Statistical Verdict:", "FAIL TO REJECT NULL HYPOTHESIS (H0). Music genre and high anxiety classification are statistically independent."),
        ("Cramer's V Effect Size:", "V = sqrt( chi^2 / (n * min(r-1, c-1)) ) = sqrt( 6.918 / 735 ) = 0.097"),
        ("Magnitude:", "Cramer's V = 0.097 represents a negligible association (< 0.10).")
    ]
    ry = 445
    for title, desc in chi_results:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70 + col_w2 + 20, ry, title)
        ry -= 14
        color = COLOR_EMERALD if title.startswith("Statistical") else TEXT_WHITE
        font = 'Helvetica-Bold' if title.startswith("Statistical") else 'Helvetica'
        ry = draw_wrapped_text(c, desc, 70 + col_w2 + 20, ry, col_w2 - 40, line_height=12.5, font_name=font, font_size=9.5, fill_color=color, hanging_indent=0)
        ry -= 6

    draw_card(c, 70 + col_w2 + 20, 95, col_w2 - 40, 65, "Academic Meaning for Teacher Review")
    draw_wrapped_text(c, "Debunks the common cultural assumption that listeners of heavier genres (e.g., Metal, Rock) possess disproportionately higher clinical anxiety rates.",
                      85 + col_w2 + 20, 130, col_w2 - 70, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 10: DISCRETE PROBABILITY: BINOMIAL DISTRIBUTION MODELING
    # =========================================================================
    draw_slide_base(c, 10, total_slides, "Discrete Probability", 
                    "Discrete Probability: Binomial Distribution PMF & CDF", 
                    "Modeling random variable X ~ Bin(n, p) for clinical risk forecasting in survey cohorts.")

    draw_card(c, 50, 70, col_w2, 430, "Binomial Model Formulation & Moments", "PMF & Moments")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "P(X = k) = C(n, k) * p^k * (1 - p)^(n - k)", "Binomial Probability Mass Function (PMF)")
    draw_formula_box(c, 70, 320, col_w2 - 40, 55, 
                     "E[X] = n * p   |   Var(X) = n * p * (1 - p)   |   sigma = sqrt(Var(X))", "Expected Value, Variance & Standard Deviation")

    b_facts = [
        "• Random Variable Definition: X = Number of high-anxiety respondents (score >= 6) in a random sample of size n.",
        "• Empirical Parameter Estimation: Base sample proportion p_hat = 443 / 735 = 0.6027 (60.27%).",
        "• Baseline Scenario (n = 10 trials):",
        "  - Expected Value: E[X] = 10 * 0.6027 = 6.03 respondents",
        "  - Variance: Var(X) = 10 * 0.6027 * (1 - 0.6027) = 2.395",
        "  - Standard Deviation: sigma = sqrt(2.395) = 1.548",
        "• Modal Probability: Peak probability occurs at k = 6 with P(X = 6) = 0.2508 (25.08%).",
        "• Extreme Event Improbability: P(X = 0) = (1 - 0.6027)^10 = 0.000088 (< 0.01%)."
    ]
    by3 = 285
    for bf in b_facts:
        is_bold = bf.startswith("• Random") or bf.startswith("• Empirical")
        color = TEXT_WHITE if is_bold else TEXT_MUTED
        font = 'Helvetica-Bold' if is_bold else 'Helvetica'
        by3 = draw_wrapped_text(c, bf, 70, by3, col_w2 - 40, line_height=12.5, font_name=font, font_size=9.5, fill_color=color, hanging_indent=12)
        by3 -= 3

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Interactive PMF Calculator & Cumulative Bounds", "Live Feature")
    calc_points = [
        ("Dynamic Trials Slider (n in [5, 30]):", "Allows users to simulate classroom sample sizes from n=5 to n=30 dynamically."),
        ("Success Probability Slider (p):", "Permits adjusting base rate from 5% to 95% to model custom sub-populations."),
        ("Target Threshold Slider (k):", "Highlights target bin k in neon purple while computing both PMF P(X=k) and CDF P(X <= k)."),
        ("Live Normal Approximation:", "For large n * p >= 10, the Binomial converges towards Gaussian distribution via the Central Limit Theorem (CLT).")
    ]
    cay = 445
    for title, desc in calc_points:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70 + col_w2 + 20, cay, title)
        cay -= 14
        cay = draw_wrapped_text(c, desc, 70 + col_w2 + 20, cay, col_w2 - 40, line_height=12.5, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)
        cay -= 6

    draw_formula_box(c, 70 + col_w2 + 20, 95, col_w2 - 40, 70, 
                     "Cumulative CDF: P(X <= 6) = sum( C(10,i) * p^i * (1-p)^(10-i), i=0..6 ) = 60.9%", 
                     "Cumulative Probability Formulation")

    c.showPage()

    # =========================================================================
    # SLIDE 11: BAYESIAN PROBABILITY & CONDITIONAL LIKELIHOOD
    # =========================================================================
    draw_slide_base(c, 11, total_slides, "Conditional Probability", 
                    "Bayesian Probability & Conditional Likelihood Modeling", 
                    "Updating prior probabilities to evaluate genre-conditional anxiety risk: P(High Anxiety | Genre).")

    draw_card(c, 50, 70, col_w2, 430, "Bayes' Law & Prior-to-Posterior Updating", "Bayes Formulation")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "P(A | B) = [ P(B | A) * P(A) ] / P(B)", "Bayes' Theorem Formulation")
    draw_formula_box(c, 70, 320, col_w2 - 40, 55, 
                     "P(B) = P(B | A)*P(A) + P(B | A^c)*P(A^c)", "Law of Total Probability")

    b_text = [
        "• Event A: Participant reports High Anxiety (Score >= 6). Global Prior P(A) = 0.6027.",
        "• Event B: Participant's favorite music genre is Genre G.",
        "• Posterior P(A | B): The updated conditional probability that a listener reports high anxiety given their primary genre.",
        "• Bayes Factor / Relative Risk: Ratio of posterior to prior: RR = P(A | B) / P(A)."
    ]
    by4 = 280
    for bt in b_text:
        by4 = draw_wrapped_text(c, bt, 70, by4, col_w2 - 40, line_height=13, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=12)
        by4 -= 5

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Ranked Conditional Probabilities Across Genres", "Ranked Likelihood")
    c_subheaders = ["Genre (Class)", "n", "P(High Anxiety | Genre)", "Relative Risk (vs 60.3%)"]
    csy = 445
    c.setFillColor(colors.HexColor('#2e384d'))
    c.rect(70 + col_w2 + 20, csy - 6, col_w2 - 40, 22, fill=1, stroke=0)
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(80 + col_w2 + 20, csy + 2, c_subheaders[0])
    c.drawString(200 + col_w2 + 20, csy + 2, c_subheaders[1])
    c.drawString(250 + col_w2 + 20, csy + 2, c_subheaders[2])
    c.drawString(390 + col_w2 + 20, csy + 2, c_subheaders[3])

    cond_rows = [
        ("Folk", "30", "76.7%", "+27.3% (Highest Risk)"),
        ("Lofi", "10", "70.0%", "+16.1%"),
        ("Pop", "114", "66.7%", "+10.7%"),
        ("Rock", "188", "64.4%", "+6.8%"),
        ("Metal", "88", "61.4%", "+1.9%"),
        ("Survey Baseline", "735", "60.3%", "1.00 (Prior Baseline)"),
        ("Classical", "53", "56.6%", "-6.1%"),
        ("Video Game Music", "44", "54.5%", "-9.6%"),
        ("Latin", "3", "33.3%", "-44.8% (Lowest Sample)")
    ]
    cry = csy - 26
    for cr in cond_rows:
        is_base = "Baseline" in cr[0]
        c.setFillColor(COLOR_AMBER if is_base else TEXT_WHITE)
        c.setFont('Helvetica-Bold' if is_base else 'Helvetica', 9)
        c.drawString(80 + col_w2 + 20, cry, cr[0])
        c.drawString(200 + col_w2 + 20, cry, cr[1])
        c.drawString(250 + col_w2 + 20, cry, cr[2])
        c.drawString(390 + col_w2 + 20, cry, cr[3])
        c.setStrokeColor(CARD_BORDER)
        c.line(70 + col_w2 + 20, cry - 5, 70 + col_w2 + 20 + col_w2 - 40, cry - 5)
        cry -= 22

    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_CYAN)
    c.roundRect(70 + col_w2 + 20, 95, col_w2 - 40, 70, 8, fill=1, stroke=1)
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(85 + col_w2 + 20, 145, "Important Bayes Reasoning for Teacher Defense:")
    draw_wrapped_text(c, "While Folk has the highest conditional rate (76.7%), its small sample size (n=30) means Rock (n=188, 64.4%) contributes far more absolute high-anxiety listeners.",
                      85 + col_w2 + 20, 130, col_w2 - 70, line_height=12.5, font_name='Helvetica', font_size=9, fill_color=TEXT_MUTED, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 12: HIGH-PERFORMANCE UI & VISUAL ENGINE
    # =========================================================================
    draw_slide_base(c, 12, total_slides, "Software Engineering", 
                    "Interactive Mathematical Visualizer & UI Architecture", 
                    "How AudioMental translates complex statistical theory into responsive, GPU-accelerated visualizations.")

    draw_card(c, 50, 70, col_w2, 430, "Fluid 60fps Shape Morphing & Animation Math", "Interpolation")
    draw_formula_box(c, 70, 390, col_w2 - 40, 55, 
                     "ease(t) = 1 - (1 - t)^3   |   x(t) = x_start + (x_target - x_start) * ease(t)", 
                     "Cubic Ease-Out Tweening Function")
    draw_formula_box(c, 70, 320, col_w2 - 40, 55, 
                     "x_i = cx + r_i * cos(theta_i)   |   y_i = cy - r_i * sin(theta_i)", 
                     "Polar-to-Cartesian Radar Projection Math")

    ui_points = [
        ("Continuous Polar Morphing:", "When switching between genres (e.g. Gospel to Rock), the 4-axis radar polygon vertices do not teleport—they fluidly interpolate coordinates frame-by-frame over 480ms."),
        ("Donut Arc Trigonometry:", "Circumference C = 2*pi*r. Stroke dash-arrays and dash-offsets glide continuously across mental health improvement tiers."),
        ("Rolling Odometer Numbers:", "KPI values (means, sample size, hours) smoothly roll up from 0 using requestAnimationFrame eased counters.")
    ]
    uy = 285
    for title, desc in ui_points:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70, uy, title)
        uy -= 14
        uy = draw_wrapped_text(c, desc, 70, uy, col_w2 - 40, line_height=12.5, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)
        uy -= 6

    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "System Architecture & Offline Reliability", "Architecture")
    arch_points = [
        ("Zero External Dependencies:", "Built entirely with native HTML5, Vanilla JavaScript, and SVG. Requires zero CDN script downloads, operating reliably in air-gapped sandboxes."),
        ("Dual Distribution Models:", "Serves both a live HTTP server on port 8080 and a fully self-contained offline artifact HTML file with inlined data."),
        ("Silky Tab-to-Tab Transitions:", "Features crossfading .view-panel states that glide out (-8px) and glide in (+14px) smoothly when navigating between 6 primary view tabs."),
        ("Slow Staggered Leaderboards:", "Leaderboard bars expand from 0% with staggered delays (0.85s ease with index * 45ms offset), creating an aesthetic race-to-rank visual.")
    ]
    ay = 445
    for title, desc in arch_points:
        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70 + col_w2 + 20, ay, title)
        ay -= 14
        ay = draw_wrapped_text(c, desc, 70 + col_w2 + 20, ay, col_w2 - 40, line_height=12.5, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)
        ay -= 6

    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_EMERALD)
    c.roundRect(70 + col_w2 + 20, 95, col_w2 - 40, 65, 8, fill=1, stroke=1)
    c.setFillColor(COLOR_EMERALD)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(85 + col_w2 + 20, 140, "Interactive Graph Studio Modal:")
    draw_wrapped_text(c, "Clicking any graph across the application opens a 2-column studio with live parameter controls (bins, alpha, OLS toggles, sample sizes, and vector SVG exports).",
                      85 + col_w2 + 20, 124, col_w2 - 70, line_height=12.5, font_name='Helvetica', font_size=9, fill_color=TEXT_MUTED, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 13: COMPREHENSIVE FINDINGS MATRIX
    # =========================================================================
    draw_slide_base(c, 13, total_slides, "Summary of Findings", 
                    "Comprehensive Statistical Hypothesis Testing Matrix", 
                    "Consolidated empirical verification across all primary research questions and statistical tests.")

    draw_card(c, 50, 70, PAGE_WIDTH - 100, 430, "Probability & Statistics Hypothesis Verification Matrix", "Summary")
    
    m_headers = ["Statistical Method", "Null Hypothesis (H0)", "Test Statistic", "p-Value", "Decision (alpha=0.05)", "Academic Conclusion"]
    my = 450
    c.setFillColor(colors.HexColor('#2e384d'))
    c.rect(70, my - 6, PAGE_WIDTH - 140, 24, fill=1, stroke=0)
    c.setFillColor(COLOR_CYAN)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(80, my + 2, m_headers[0])
    c.drawString(250, my + 2, m_headers[1])
    c.drawString(450, my + 2, m_headers[2])
    c.drawString(590, my + 2, m_headers[3])
    c.drawString(680, my + 2, m_headers[4])
    c.drawString(850, my + 2, m_headers[5])

    matrix_rows = [
        ("Welch's Two-Sample t-Test", "mu_work = mu_nowork", "t = -0.9791 (df=230.6)", "0.3285", "Fail to Reject H0", "Workplace listening does not alter anxiety."),
        ("Chi-Square Independence", "Genre & Anxiety Independent", "chi^2 = 6.9182 (df=6)", "0.3285", "Fail to Reject H0", "Music genre preference is independent of anxiety."),
        ("Pearson Correlation", "rho = 0 (Linear correlation)", "r = +0.0497 (t=1.35)", "0.1787", "Fail to Reject H0", "Listening hours do not linearly dictate anxiety."),
        ("Spearman Rank Correlation", "rho_s = 0 (Monotonic trend)", "rho = +0.0941", "0.0107 *", "Reject H0", "Weak positive monotonic rank association exists."),
        ("Binomial PMF Model", "p = 0.50 (Chance majority)", "z = 5.57 (p_hat=0.603)", "< 0.0001 ***", "Reject H0", "Statistically significant majority report anxiety >= 6."),
        ("One-Way ANOVA", "mu_1 = mu_2 = ... = mu_k", "F = 1.34 (df=15, 719)", "0.1712", "Fail to Reject H0", "Mean anxiety does not differ significantly across genres.")
    ]
    m_y = my - 34
    for mr in matrix_rows:
        is_sig = "Reject H0" in mr[4] and "Fail" not in mr[4]
        c.setFillColor(COLOR_CYAN if is_sig else TEXT_WHITE)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawString(80, m_y, mr[0])
        c.setFont('Helvetica', 9)
        c.setFillColor(TEXT_MUTED)
        c.drawString(250, m_y, mr[1])
        c.drawString(450, m_y, mr[2])
        c.drawString(590, m_y, mr[3])
        c.setFillColor(COLOR_EMERALD if is_sig else COLOR_AMBER)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(680, m_y, mr[4])
        c.setFillColor(TEXT_WHITE)
        c.setFont('Helvetica', 9)
        c.drawString(850, m_y, mr[5])

        c.setStrokeColor(CARD_BORDER)
        c.line(70, m_y - 8, PAGE_WIDTH - 70, m_y - 8)
        m_y -= 38

    # Final Summary banner
    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_INDIGO)
    c.roundRect(70, 90, PAGE_WIDTH - 140, 80, 8, fill=1, stroke=1)
    c.setFillColor(COLOR_AMBER)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(90, 145, "🎓 Core Conclusion for Probability & Statistics Review:")
    draw_wrapped_text(c, "Our statistical investigation demonstrates that subjective musical preferences act as a therapeutic coping mechanism (73.7% reported improvement), but baseline anxiety and depression distributions remain statistically invariant across genres. Music is a shared universal outlet rather than a clinical differentiator.",
                      90, 126, PAGE_WIDTH - 180, line_height=14, font_name='Helvetica', font_size=9.5, fill_color=TEXT_WHITE, hanging_indent=0)

    c.showPage()

    # =========================================================================
    # SLIDE 14: AUTHORS, REPOSITORY ACCESS & COURSE SUBMISSION
    # =========================================================================
    draw_slide_base(c, 14, total_slides, "Course Submission", 
                    "Project Authors, Deliverables & Repository Access", 
                    "Final submission details for Probability & Statistics Course Evaluation.")

    # Left Card: Authors (ROLES REMOVED)
    draw_card(c, 50, 70, col_w2, 430, "Project Authors & Student Identification", "Authors")
    c.setFillColor(TEXT_MUTED)
    c.setFont('Helvetica', 10)
    c.drawString(70, 445, "University Probability and Statistics Class Review")

    team_members = [
        ("Shubh Shetgaonkar", "25BCE2878"),
        ("Riddhi Kotowar", "25CBE2554"),
        ("Ashmeetha Carol Noronha", "25BDS0162")
    ]
    ty4 = 405
    for name, reg in team_members:
        c.setFillColor(CARD_INNER)
        c.setStrokeColor(CARD_BORDER)
        c.roundRect(70, ty4 - 14, col_w2 - 40, 52, 8, fill=1, stroke=1)

        c.setFillColor(TEXT_WHITE)
        c.setFont('Helvetica-Bold', 13)
        c.drawString(88, ty4 + 14, name)

        c.setFillColor(COLOR_CYAN)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(88, ty4 - 4, f"Registration No: {reg}")

        ty4 -= 68

    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_INDIGO)
    c.roundRect(70, 100, col_w2 - 40, 75, 8, fill=1, stroke=1)
    c.setFillColor(COLOR_INDIGO)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(85, 155, "Course Context:")
    c.setFillColor(TEXT_WHITE)
    c.setFont('Helvetica', 9.5)
    c.drawString(85, 138, "Subject: Probability & Statistics (Course Evaluation)")
    c.drawString(85, 122, "Project: AudioMental (MxMH Dataset Empirical Analysis)")

    # Right Card: Project Links & Access
    draw_card(c, 50 + col_w2 + 20, 70, col_w2, 430, "Project Repository & Inspection Deliverables", "Deliverables")
    links_info = [
        ("Interactive Web Dashboard:", "http://localhost:8080 (Served via Python HTTP Server)"),
        ("Standalone Offline Dashboard:", "genre_stats_dashboard.html (Zero external dependencies)"),
        ("Course Presentation Deck:", "presentation.html (Interactive HTML slide deck with Print-to-PDF)"),
        ("Course Presentation PDF:", "AudioMental_ProbStats_Presentation.pdf (Widescreen 16:9 PDF)"),
        ("Base Dataset:", "Data/mxmh_survey_results.csv (N = 735 cleaned entries)"),
        ("Verification Scripts:", "additional_analysis.R & web_dashboard/prepare_data.py")
    ]
    ly = 445
    for label, link in links_info:
        c.setFillColor(COLOR_INDIGO)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(70 + col_w2 + 20, ly, label)
        ly = draw_wrapped_text(c, link, 70 + col_w2 + 20, ly - 14, col_w2 - 40, line_height=12, font_name='Courier-Bold', font_size=9, fill_color=TEXT_WHITE, hanging_indent=0)
        ly -= 8

    # Thank you note
    c.setFillColor(CARD_INNER)
    c.setStrokeColor(COLOR_CYAN)
    c.roundRect(70 + col_w2 + 20, 95, col_w2 - 40, 75, 8, fill=1, stroke=1)
    c.setFillColor(TEXT_WHITE)
    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(50 + col_w2 + 20 + (col_w2 - 40) / 2 + 20, 142, "Thank You!")
    c.setFillColor(TEXT_MUTED)
    c.setFont('Helvetica', 10)
    c.drawCentredString(50 + col_w2 + 20 + (col_w2 - 40) / 2 + 20, 120, "Questions & Discussion Open for Course Evaluation")

    c.showPage()
    c.save()
    print(f"Successfully generated {filename} ({total_slides} slides, 16:9 widescreen)!")

if __name__ == "__main__":
    create_presentation()
