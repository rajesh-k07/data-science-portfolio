
<!-- Note: this file renders to statistical_significance_testing.md — view that file for charts and output -->

### Include libraries

``` r
library(tidyverse)
library(e1071)
library(ggradar)
library(car)
```

### load travel_insurance.csv file

``` r
# sample file is saved in current directory.
options(width = 100) 
travel_data= readr::read_csv('travel_insurance.csv', col_names=TRUE)

# Dataframe concise summary
glimpse(travel_data)
```

    ## Rows: 63,326
    ## Columns: 11
    ## $ Agency                 <chr> "CBH", "CBH", "CWT", "CWT", "CWT", "JZI", "CWT", "CWT", "CWT", "CWT…
    ## $ `Agency Type`          <chr> "Travel Agency", "Travel Agency", "Travel Agency", "Travel Agency",…
    ## $ `Distribution Channel` <chr> "Offline", "Offline", "Online", "Online", "Online", "Online", "Onli…
    ## $ `Product Name`         <chr> "Comprehensive Plan", "Comprehensive Plan", "Rental Vehicle Excess …
    ## $ Claim                  <chr> "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "…
    ## $ Duration               <dbl> 186, 186, 65, 60, 79, 66, 47, 63, 57, 186, 33, 1, 53, 5, 39, 6, 48,…
    ## $ Destination            <chr> "MALAYSIA", "MALAYSIA", "AUSTRALIA", "AUSTRALIA", "ITALY", "UNITED …
    ## $ `Net Sales`            <dbl> -29.00, -29.00, -49.50, -39.60, -19.80, -121.00, -39.60, -108.90, -…
    ## $ `Commision (in value)` <dbl> 9.57, 9.57, 29.70, 23.76, 11.88, 42.35, 23.76, 65.34, 11.88, 59.40,…
    ## $ Gender                 <chr> "F", "F", NA, NA, NA, "F", NA, NA, NA, NA, NA, "M", "F", NA, NA, NA…
    ## $ Age                    <dbl> 81, 71, 32, 32, 41, 44, 32, 29, 44, 37, 118, 47, 48, 64, 36, 53, 43…

### One‑Way ANOVA: Net Sales ~ Agency

We are going to create One-Way ANOVA for Net Sales and Agency.

Agency is the factor and Net Sales is the dependent variable.

aov() uses Type-I of sum of squares, ***since in One-Way ANOVA all
Types-I, II, and III will give the same result.***

``` r
# dropping NAs and keeping only relevant columns
travel_data_aov <- na.omit( travel_data[, c("Agency", "Gender", "Net Sales")] )

# Rename columns so we do not need backticks.
names(travel_data_aov)[names(travel_data_aov) == "Net Sales"] <- "Net_Sales"

# Ensure grouping variables are factors
travel_data_aov$Agency <- factor(travel_data_aov$Agency)
travel_data_aov$Gender <- factor(travel_data_aov$Gender)


# One‑way ANOVA: Net_Sales ~ Agency
oneway_aov <- aov(formula = Net_Sales ~ Agency, data = travel_data_aov)

# Compute AIC for one-way ANOVA
oneway_lm <- lm(Net_Sales ~ Agency, data = travel_data_aov)
oneway_aic <- AIC(oneway_lm)

oneway_aov_txt <- capture.output(summary(oneway_aov))

# Show the one-way ANOVA result and AIC
cat("One‑way ANOVA: Net_Sales ~ Agency \n\n", paste(oneway_aov_txt, collapse = "\n"))
```

    ## One‑way ANOVA: Net_Sales ~ Agency 
    ## 
    ##                 Df   Sum Sq Mean Sq F value Pr(>F)    
    ## Agency         13 11683703  898746   186.4 <2e-16 ***
    ## Residuals   18205 87767963    4821                   
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
cat("One‑way model AIC:", oneway_aic)
```

    ## One‑way model AIC: 206230.2

F value (F‑statistic) = 186.4 and Pr(\>F) (P‑value)=\<2×10⁻¹⁶ are
statistically highly significant.

**The differences in mean Net Sales across the 14 agencies are far
larger than we would expect by chance, so we can confidently reject the
null hypothesis of equal means.**

### Two‑way ANOVA: Net Sales ~ Agency \* Gender

We are going to create Two-Way ANOVA for Net Sales, Agency and Gender .

Agency and Gender are the factors and Net Sales is the dependent
variable.

***We will check if observations in subjects are balanced or
unbalanced.***

``` r
# Cross‑tabulate Agency by Gender
observation_counts <- table(Agency = travel_data_aov$Agency, Gender = travel_data_aov$Gender)
print(observation_counts)
```

    ##       Gender
    ## Agency    F    M
    ##    ADM   16   17
    ##    ART   96  230
    ##    C2B 4594 3673
    ##    CBH   71   30
    ##    CCR  143   50
    ##    CSR   64   22
    ##    CWT    3    2
    ##    JWT  238  494
    ##    JZI 2560 3706
    ##    KML  192  200
    ##    LWC  382  307
    ##    RAB  145  360
    ##    TST  319  207
    ##    TTW   49   49

***Two‑way design is UnBalanced, here cell counts are vary, so we will
use Type-III of sum of squares.***

``` r
# Set sum-to-zero contrasts
options(contrasts = c("contr.sum", "contr.poly"))

# Fit the linear model (not aov) with contr.sum for factors
twoway_lm <- lm( Net_Sales ~ Agency * Gender, data = travel_data_aov)

# Two‑way ANOVA using Type-III: Net Sales ~ Agency * Gender
Anova(twoway_lm, type = "III") 
```

    ## Anova Table (Type III tests)
    ## 
    ## Response: Net_Sales
    ##                 Sum Sq    Df  F value    Pr(>F)    
    ## (Intercept)    1540310     1 319.9440 < 2.2e-16 ***
    ## Agency        11353578    13 181.4075 < 2.2e-16 ***
    ## Gender             266     1   0.0552  0.814255    
    ## Agency:Gender   146770    13   2.3451  0.004028 ** 
    ## Residuals     87577129 18191                       
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
# Compute AIC for two-way ANOVA
twoway_aic <- AIC(twoway_lm)
cat("Two‑way model AIC:", twoway_aic, "\n\n")
```

    ## Two‑way model AIC: 206218.5

Agency (main effect): F=181.41, p\<2.2×10⁻¹⁶ is highly significant.

Gender (main effect): F=0.055, p=0.8143 is not significant.

Agency×Gender (interaction): F=2.345, p=0.0040 significant.

***Intercept: The baseline mean Net_Sales (when all factors are at their
reference level) is significantly different from zero (F=319.94,
p\<2.2×10⁻¹⁶)***

### AIC Comparison

``` r
if (oneway_aic < twoway_aic) {
  cat("One‑way ANOVA is preferred (lower AIC).\n")
} else if (twoway_aic < oneway_aic) {
  cat("Two‑way ANOVA is preferred (lower AIC).\n")
} else {
  cat("AICs are identical; both models are equally supported.\n")
}
```

    ## Two‑way ANOVA is preferred (lower AIC).

Since the two‑way AIC is lower by about 11.7 points, that’s a
substantial improvement.

The Akaike Information Criterion (AIC) is a metric for comparing
statistical models on the basis of both their goodness of fit and their
complexity.
