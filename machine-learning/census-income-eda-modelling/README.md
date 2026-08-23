# Census Income Dataset - EDA and Modeling

Census Income Database (1994, extraction by Barry Becker) — 48,842 instances, mix of continuous and discrete features (train=32,561, test=16,281), merged into one dataset. Income is the target value (whether a person earns more than $50K or not in a year)

**Dataset link:** https://archive.ics.uci.edu/dataset/20/census+income

## Data Cleaning and Preparation
- Removed "?" values, dropped NaN/None values, dropped duplicates.
- Replaced "United-States" with "US" in native_country; grouped rare categories in native_country, race, and occupation into "Non-US"/"Others".
- Created `capital_diff` (capital_gain − capital_loss).
- Age outliers were removed.
- Created `work_time_category` (part_time / full_time / over_time) from hours_per_week.

## Exploratory Data Analysis
- **Univariate Analysis:** summary statistics, and distribution/frequency of individual features.
- **Bivariate Analysis:** relationships between pairs of features — e.g., age vs. education_num by income and sex (scatterplot).
- **Scaling and Normalization:** Min-Max scaling (range 0.01–1, since log normalization needs positive values) — doesn't change the shape of the distribution. Log and Square Root normalization applied to squeeze outliers (log for age, hours_per_week; sqrt for fnlwgt, capital_gain, capital_loss, capital_diff) — no big improvement was seen, so Min-Max scaling was used going forward.
- **Covariance:** calculated on raw (unscaled) data, since covariance is not standardized and its magnitude depends on the units of the variables.
- **Pearson correlation coefficient:** calculated on the scaled dataframe. All correlations are well below 0.6, so no real multicollinearity.
- **Spearman correlation coefficient:** calculated on label-encoded categorical features (rank-based, less sensitive to outliers). Most correlations are near 0 (categorical features largely independent),- except relationship vs. sex (-0.62) — a strong inverse relationship, since "Husband" strongly links to "Male" and "Wife" to "Female".

## t-Test
H₀: average age is the same for <=50K and >50K earners. H₁: average age differs between the two groups.

**Result:** T-value = -54.29, p-value ≈ 0 — reject the null hypothesis. There's very strong evidence that average age differs between income groups.

## One-Way ANOVA
Tests whether average age differs significantly across work time categories (part_time, full_time, over_time).

**Result:** F = 475.72, p < 0.000001 — reject the null hypothesis; at least one group's mean age is different.

R² = 0.0207; Only ~2.07% of the variance in the dependent variable is explained by the group differences.

## Linear Regression
Predicts age based on work-related, demographic, and income features.

**Results:** R² = 0.429 · RMSE = 0.1188 · Intercept = 0.4859

The model explains about 42.9% of the variance in age. The dataset is more suited to classification or clustering than to precisely predicting age.

## Logistic Regression (Classification)
Classifies whether an individual earns >50K or <=50K yearly.

**Results:** Accuracy = 84.17% · Precision = 0.80 · Recall = 0.75 · F1 = 0.77 · AUC = 0.90 · Average Precision = 0.76

The model strongly predicts low-income individuals but struggles more with high-income detection, mainly due to class imbalance (~75% <=50K vs. 25% >50K).

## K-Means Clustering
Separates the dataset into two clusters (k=2, matching the number of sex categories) based on age, education_num, and marital_status — without using the actual sex labels. 

Sex is only used afterward, for Fowlkes–Mallows evaluation.

**Result:** Fowlkes–Mallows Index = 0.6052 — clusters are doing better than random grouping. PCA (PC1 + PC2) preserves about 80.5% of the variance from the original multi-dimensional dataset.

## Tools
`Python` `scikit-learn` `scipy` `pandas` — Linear Regression, Logistic Regression, K-Means, PCA, t-Test, One-Way ANOVA, Pearson/Spearman Correlation

## Files in this folder
- `census_income_eda_models.ipynb` — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
