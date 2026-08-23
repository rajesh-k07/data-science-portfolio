# Statistical Significance Testing

One-way and two-way ANOVA tests evaluating statistical significance across grouped data.

## About Dataset
`travel_insurance.csv` — 63,326 rows, 11 columns, including Agency, Gender, Net Sales, Duration, Destination, and Claim.

## One-Way ANOVA: Net Sales ~ Agency
Agency is the factor and Net Sales is the dependent variable. `aov()` uses Type-I sum of squares, since in One-Way ANOVA all Types I, II, and III give the same result.

**Results:** F = 186.4, p < 2×10⁻¹⁶ — statistically highly significant. AIC = 206230.2

The differences in mean Net Sales across the 14 agencies are far larger than we would expect by chance, so we can confidently reject the null hypothesis of equal means.

## Two-Way ANOVA: Net Sales ~ Agency * Gender
Agency and Gender are the factors and Net Sales is the dependent variable. Checked whether observations were balanced or unbalanced — cell counts varied across Agency × Gender, so the design is unbalanced, and Type-III sum of squares was used (via `Anova()` with sum-to-zero contrasts).

**Results:**
- Agency (main effect): F = 181.41, p < 2.2×10⁻¹⁶ — highly significant
- Gender (main effect): F = 0.055, p = 0.8143 — not significant
- Agency×Gender (interaction): F = 2.345, p = 0.0040 — significant
- AIC = 206218.5

## AIC Comparison
Two-way ANOVA is preferred (lower AIC). Since the two-way AIC is lower by about 11.7 points, that's a substantial improvement.

AIC (Akaike Information Criterion) is a metric for comparing statistical models on the basis of both their goodness of fit and their complexity.

## Tools
`R` `tidyverse` `car` `e1071` — One-Way ANOVA, Two-Way ANOVA, Type-III Sum of Squares, AIC

## Files in this folder
- `statistical_significance_testing.Rmd` — source code
- **`statistical_significance_testing.md` — rendered version with output (view this for results)**

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
