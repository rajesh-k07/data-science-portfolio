# Feature Scaling and Transformation

Feature scaling techniques include min-max scaling, square root, and log transformations, exploring how different
transformations affect data distribution and downstream statistical analysis. This is about scaling and fixing skewness.

## About Dataset
`vgchartz-2024.csv` — video game sales data (total_sales, na_sales, jp_sales, pal_sales, other_sales, critic_score). High positive skewness in the sales columns, negative skewness for critic_score.

## Scaling
Min-max scaled to range 0.01–1 (not 0–1), since the log method needs strictly positive values. In scaling, we are changing the range of our data — skewness stays the same after min-max scaling.

## Fixing Skewness
- **Log method** — applied to total_sales, na_sales, jp_sales, pal_sales.
- **Square root method** — applied to other_sales.

In Normalization, we are changing the shape of the distribution of our data. Compared before/after using histograms.

**Improved Skewness.** It is not perfect yet, but it is still better than raw data.

## Tools
`R` `tidyverse` `e1071` `ggplot2` `gridExtra`

## Files in this folder
- `feature_scaling_transformation.Rmd`

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
