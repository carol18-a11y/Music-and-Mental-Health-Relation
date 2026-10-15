

# 1. SETUP AND LOAD DATA

setwd("C:/projects/MusicMentalHealth")

output_dir <- "outputs/R_analysis"
table_dir <- file.path(output_dir, "tables")
plot_dir <- file.path(output_dir, "plots")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(plot_dir, recursive = TRUE, showWarnings = FALSE)

df <- read.csv(
  "data/mxmh_survey_results.csv",
  stringsAsFactors = FALSE,
  na.strings = c("", "NA")
)

cat("\n========== DATA VALIDATION ==========\n")
cat("Original rows:", nrow(df), "\n")
cat("Columns:", ncol(df), "\n")

missing_values <- colSums(is.na(df))
print(missing_values[missing_values > 0])

# Select the variables needed for the main analysis.
required_variables <- c(
  "Age", "Hours.per.day", "Anxiety", "Depression",
  "Insomnia", "OCD", "Fav.genre"
)

analysis_data <- df[
  complete.cases(df[, required_variables]),
]

cat("Rows after cleaning:", nrow(analysis_data), "\n")

write.csv(
  data.frame(
    Original_Rows = nrow(df),
    Columns = ncol(df),
    Rows_After_Cleaning = nrow(analysis_data)
  ),
  file.path(table_dir, "validation.csv"),
  row.names = FALSE
)


# 2. DESCRIPTIVE STATISTICS

cat("\n========== DESCRIPTIVE STATISTICS ==========\n")

variables <- c(
  "Age", "Hours.per.day", "Anxiety",
  "Depression", "Insomnia", "OCD"
)

descriptive_stats <- data.frame()

for (variable in variables) {
  x <- analysis_data[[variable]]
  
  descriptive_stats <- rbind(
    descriptive_stats,
    data.frame(
      Variable = variable,
      Count = length(x),
      Mean = mean(x),
      Median = median(x),
      Variance = var(x),
      Standard_Deviation = sd(x),
      Minimum = min(x),
      Maximum = max(x)
    )
  )
}

print(descriptive_stats, digits = 4)

write.csv(
  descriptive_stats,
  file.path(table_dir, "descriptive_statistics.csv"),
  row.names = FALSE
)


# 3. PROBABILITY OF HIGH ANXIETY
cat("\n========== BASIC PROBABILITY ==========\n")

# Define high anxiety as a score of 6 or above.
analysis_data$AnxietyGroup <- ifelse(
  analysis_data$Anxiety >= 6,
  "High anxiety",
  "Not high anxiety"
)

high_count <- sum(analysis_data$Anxiety >= 6)
total_count <- nrow(analysis_data)
p_high <- high_count / total_count

cat("High-anxiety respondents:", high_count, "\n")
cat("Total respondents:", total_count, "\n")
cat("P(high anxiety):", round(p_high, 4), "\n")

probability_results <- data.frame(
  Event = c("High anxiety", "Not high anxiety"),
  Count = c(high_count, total_count - high_count),
  Probability = c(p_high, 1 - p_high)
)

write.csv(
  probability_results,
  file.path(table_dir, "basic_probability.csv"),
  row.names = FALSE
)


# 4. CONDITIONAL PROBABILITY BY MUSIC GENRE

cat("\n========== CONDITIONAL PROBABILITY ==========\n")

genre_results <- aggregate(
  Anxiety >= 6 ~ Fav.genre,
  data = analysis_data,
  FUN = mean
)

names(genre_results) <- c("Genre", "P_High_Anxiety")

genre_counts <- as.data.frame(
  table(analysis_data$Fav.genre),
  stringsAsFactors = FALSE
)

names(genre_counts) <- c("Genre", "Count")

conditional_probability <- merge(
  genre_counts,
  genre_results,
  by = "Genre"
)

conditional_probability <- conditional_probability[
  order(-conditional_probability$P_High_Anxiety),
]

print(conditional_probability, row.names = FALSE)

write.csv(
  conditional_probability,
  file.path(table_dir, "conditional_probability.csv"),
  row.names = FALSE
)

highest_genre <- conditional_probability[1, ]

cat(
  "\nHighest conditional probability:",
  highest_genre$Genre,
  "=",
  round(highest_genre$P_High_Anxiety, 3),
  "\n"
)


# 5. BAYES' THEOREM

cat("\n========== BAYES THEOREM ==========\n")

genre_bayes <- c("Rock", "Pop", "Metal")

for (genre in genre_bayes) {
  genre_total <- sum(analysis_data$Fav.genre == genre)
  high_in_genre <- sum(
    analysis_data$Fav.genre == genre &
      analysis_data$Anxiety >= 6
  )
  
  if (genre_total > 0 && high_count > 0) {
    posterior <- high_in_genre / high_count
    
    cat(
      "P(", genre, "| high anxiety) =",
      round(posterior, 4), "\n"
    )
  }
}

# Posterior probability:
# P(genre | high anxiety) =
# P(high anxiety | genre) * P(genre) / P(high anxiety)


# 6. CONFIDENCE INTERVALS FOR MEANS

cat("\n========== 95% CONFIDENCE INTERVALS ==========\n")

ci_results <- data.frame()

for (variable in c(
  "Anxiety", "Depression", "Insomnia", "OCD"
)) {
  for (group in c("Yes", "No")) {
    
    # Use rows with a recorded response to While working.
    group_data <- analysis_data[
      !is.na(analysis_data$While.working) &
        analysis_data$While.working == group,
    ]
    
    x <- group_data[[variable]]
    x <- x[!is.na(x)]
    
    if (length(x) > 1) {
      ci <- t.test(x, conf.level = 0.95)$conf.int
      
      ci_results <- rbind(
        ci_results,
        data.frame(
          Variable = variable,
          While_Working = group,
          Count = length(x),
          Mean = mean(x),
          CI_Lower = ci[1],
          CI_Upper = ci[2]
        )
      )
    }
  }
}

print(ci_results, digits = 4)

write.csv(
  ci_results,
  file.path(table_dir, "confidence_intervals.csv"),
  row.names = FALSE
)


# 7. CORRELATION: LISTENING HOURS AND ANXIETY
cat("\n========== CORRELATION ==========\n")

cor_data <- analysis_data[
  complete.cases(
    analysis_data[, c("Hours.per.day", "Anxiety")]
  ),
]

pearson_result <- cor.test(
  cor_data$Hours.per.day,
  cor_data$Anxiety,
  method = "pearson"
)

spearman_result <- cor.test(
  cor_data$Hours.per.day,
  cor_data$Anxiety,
  method = "spearman",
  exact = FALSE
)

cat("Pearson correlation:\n")
print(pearson_result)

cat("\nSpearman correlation:\n")
print(spearman_result)

correlation_results <- data.frame(
  Method = c("Pearson", "Spearman"),
  Correlation = c(
    unname(pearson_result$estimate),
    unname(spearman_result$estimate)
  ),
  P_Value = c(
    pearson_result$p.value,
    spearman_result$p.value
  )
)

write.csv(
  correlation_results,
  file.path(table_dir, "correlation_results.csv"),
  row.names = FALSE
)


# 8. WELCH TWO-SAMPLE T-TEST

cat("\n========== T-TEST: ANXIETY BY WHILE WORKING ==========\n")

test_data <- analysis_data[
  !is.na(analysis_data$While.working) &
    analysis_data$While.working %in% c("Yes", "No"),
]

t_test_result <- t.test(
  Anxiety ~ While.working,
  data = test_data,
  var.equal = FALSE
)

print(t_test_result)

cat("H0: Mean anxiety is equal in both groups.\n")
cat("H1: Mean anxiety differs between the groups.\n")
cat("Significance level: 0.05\n")

write.csv(
  data.frame(
    Test = "Welch two-sample t-test",
    T_Statistic = unname(t_test_result$statistic),
    Degrees_of_Freedom = unname(t_test_result$parameter),
    P_Value = t_test_result$p.value,
    CI_Lower = t_test_result$conf.int[1],
    CI_Upper = t_test_result$conf.int[2]
  ),
  file.path(table_dir, "t_test_results.csv"),
  row.names = FALSE
)


# 9. CHI-SQUARE TEST OF INDEPENDENCE
cat("\n========== CHI-SQUARE TEST ==========\n")

# Retain the six most common genres and group the rest as Other.
top_genres <- names(
  sort(table(analysis_data$Fav.genre), decreasing = TRUE)
)[1:min(6, length(unique(analysis_data$Fav.genre)))]

chi_data <- analysis_data
chi_data$Genre_Group <- ifelse(
  chi_data$Fav.genre %in% top_genres,
  chi_data$Fav.genre,
  "Other"
)

chi_table <- table(
  chi_data$Genre_Group,
  chi_data$AnxietyGroup
)

cat("Contingency table:\n")
print(chi_table)

chi_result <- chisq.test(chi_table, correct = FALSE)

cat("\nExpected frequencies:\n")
print(round(chi_result$expected, 2))

if (any(chi_result$expected < 5)) {
  cat(
    "Warning: Some expected counts are below 5. ",
    "Consider combining more categories.\n"
  )
}

cat("\nChi-square test result:\n")
print(chi_result)

cat("H0: Music genre and anxiety group are independent.\n")
cat("H1: Music genre and anxiety group are associated.\n")

write.csv(
  as.data.frame.matrix(chi_table),
  file.path(table_dir, "chi_square_contingency_table.csv")
)

write.csv(
  data.frame(
    Test = "Chi-square test of independence",
    Chi_Square = unname(chi_result$statistic),
    Degrees_of_Freedom = unname(chi_result$parameter),
    P_Value = chi_result$p.value
  ),
  file.path(table_dir, "chi_square_results.csv"),
  row.names = FALSE
)


# 10. BINOMIAL PROBABILITY DISTRIBUTION


cat("\n========== BINOMIAL DISTRIBUTION ==========\n")

# Hypothetical sample of 10 respondents.
# Estimated probability of high anxiety = p_high.
n <- 10

binomial_results <- data.frame(
  High_Anxiety_Count = 0:n,
  Probability = dbinom(0:n, size = n, prob = p_high)
)

print(binomial_results, digits = 4)

write.csv(
  binomial_results,
  file.path(table_dir, "binomial_distribution.csv"),
  row.names = FALSE
)


# 11. GENERATE AND SAVE GRAPHS

# Graph 1: Anxiety score histogram
png(
  file.path(plot_dir, "anxiety_histogram.png"),
  width = 1000, height = 700
)

hist(
  analysis_data$Anxiety,
  breaks = seq(-0.5, 10.5, by = 1),
  main = "Distribution of Anxiety Scores",
  xlab = "Anxiety Score",
  ylab = "Number of Respondents",
  col = "lightblue",
  border = "black"
)

dev.off()


# Graph 2: Conditional probability by genre
png(
  file.path(plot_dir, "conditional_probability_genre.png"),
  width = 1200, height = 800
)

par(mar = c(10, 5, 4, 2))

barplot(
  conditional_probability$P_High_Anxiety,
  names.arg = conditional_probability$Genre,
  las = 2,
  main = "Probability of High Anxiety by Music Genre",
  xlab = "",
  ylab = "P(High Anxiety | Genre)",
  ylim = c(0, 1),
  col = "skyblue"
)

dev.off()


# Graph 3: Listening hours vs anxiety
png(
  file.path(plot_dir, "hours_vs_anxiety.png"),
  width = 1000, height = 700
)

plot(
  cor_data$Hours.per.day,
  cor_data$Anxiety,
  main = "Music Listening Hours vs Anxiety",
  xlab = "Hours of Music per Day",
  ylab = "Anxiety Score",
  pch = 19,
  col = "steelblue"
)

abline(
  lm(Anxiety ~ Hours.per.day, data = cor_data),
  lwd = 2
)

dev.off()


# Graph 4: Binomial distribution
png(
  file.path(plot_dir, "binomial_distribution.png"),
  width = 1000, height = 700
)

barplot(
  binomial_results$Probability,
  names.arg = binomial_results$High_Anxiety_Count,
  main = "Binomial Distribution: High Anxiety in 10 Respondents",
  xlab = "Number with High Anxiety",
  ylab = "Probability",
  col = "lightgreen",
  border = "black"
)

dev.off()


# Graph 5: Anxiety by listening while working
png(
  file.path(plot_dir, "anxiety_by_working.png"),
  width = 1000, height = 700
)

boxplot(
  Anxiety ~ While.working,
  data = test_data,
  main = "Anxiety Scores by Listening While Working",
  xlab = "Listen While Working?",
  ylab = "Anxiety Score",
  col = c("lightblue", "lightgreen")
)

dev.off()


# Graph 6: Genre and anxiety group contingency table
png(
  file.path(plot_dir, "genre_anxiety_stacked_bar.png"),
  width = 1200, height = 800
)

barplot(
  t(chi_table),
  beside = FALSE,
  legend.text = TRUE,
  main = "Anxiety Group by Music Genre",
  xlab = "Music Genre",
  ylab = "Number of Respondents",
  col = c("lightblue", "salmon"),
  las = 2
)

dev.off()


# 12. FINAL SUMMARY


cat("\n========== FINAL SUMMARY ==========\n")
cat("Rows after cleaning:", nrow(analysis_data), "\n")
cat("P(high anxiety):", round(p_high, 3), "\n")
cat(
  "Highest genre probability:",
  highest_genre$Genre,
  "=",
  round(highest_genre$P_High_Anxiety, 3),
  "\n"
)

cat(
  "Pearson correlation:",
  round(unname(pearson_result$estimate), 3),
  "\n"
)

cat(
  "T-test p-value:",
  signif(t_test_result$p.value, 4),
  "\n"
)

cat(
  "Chi-square p-value:",
  signif(chi_result$p.value, 4),
  "\n"
)

cat("\nAnalysis complete.\n")
cat("Tables saved in:", table_dir, "\n")
cat("Graphs saved in:", plot_dir, "\n")

