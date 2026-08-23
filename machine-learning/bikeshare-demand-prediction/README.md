
# Capital Bikeshare: Predicting Bike Sharing Demand

## About Project
Capital bike-sharing system is a new-generation bike rental system in which membership, rental, and return are automated. The efficient management of bicycle availability across docking stations across a city is very important to maintain bike demand and reduce operating costs. The Capital Bikeshare system in Washington, D.C., serves thousands of trips daily, and its operational efficiency depends on accurately anticipating bike demand.

I used a **supervised learning model** to predict target features and an **unsupervised learning model** to discover the usage pattern and clustering.

## About Dataset
Dataset is from the UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset). The dataset captures hourly bike rental activity from the Capital Bikeshare system in Washington, D.C., for the years 2011 and 2012. It contains 17,379 hourly records with 17 features covering temporal, environmental, and user-type information.

hour.csv.csv has hourly data, and day.csv has day level data.

Target "cnt": count of total rental bikes including both casual and registered.

## Data Preparation
- Used only `hour.csv` for modeling — `day.csv` is fully derivable from `hour.csv` (grouped/summed by date), so it's redundant.
- Dropped `atemp` (near-duplicate of `temp`, correlation 0.99).
- Dropped `season` (high multicollinearity with `mnth`, correlation 0.83).
- Created `cnt_sqrt` (square root transform of `cnt`) to reduce skew for K-Means, used in place of `cnt`.
- Created `demand_level` (Low / Medium / High / Very High) using quartile cutoffs on `cnt`, used as the classifier target.
- No missing values, no duplicates, and no outliers removed from `cnt` — high values are important for predicting demand on busy days.

## Model 1: Random Forest Regressor (predicts cnt)
Features used: `mnth`, `yr`, `hr`, `holiday`, `weekday`, `workingday`, `weathersit`, `temp`, `hum`, `windspeed`. No one-hot encoding was needed since Random Forest splits on raw integer codes and doesn't require scaling. Hyperparameters were tuned with GridSearchCV (5-fold CV, scoring on negative RMSE).

**Results:** RMSE = 43.29 · MAE = 25.27 · R² = 0.9408 — the model explains approximately 94.08% of the variability in bike demand (cnt), with predictions typically off by about 43 rentals.

**Top features:** `hr` (Hour of day) is the most important feature (importance = 0.61) — the model relies on time-of-day more than anything else. `temp` is second (0.14), followed by `yr` (0.08), `workingday` (0.06), and humidity (0.03).

## Model 2: Random Forest Classifier (predicts demand_level)
Same features as the regressor, with `demand_level` as the target and a stratified train/test split to preserve class balance. GridSearchCV was scored on `f1_macro`, which treats all four classes equally since the classes are balanced.

**Results:** Test Accuracy = 84.3% — well above the 25% random-guessing baseline for a balanced four-class problem. Low demand was predicted most reliably (F1 = 0.93), followed by Very High (F1 = 0.89). `hr` is again the top feature (importance = 0.48).

## Model 3: K-Means Clustering (usage pattern discovery)
Features: `hr`, `mnth`, `weekday`, `temp`, `hum`, `windspeed`, `cnt_sqrt` (scaled), plus one-hot encoded `holiday`, `workingday`, `weathersit`.

Elbow and silhouette analysis were used to choose k — clusters = 2 had the highest silhouette value, so k = 2 was selected.

- **Cluster 0** (n = 7,362): low-demand / off-peak — average hour 5.66am, cooler temperatures, mean rental count of 60/hour.
- **Cluster 1** (n = 10,017): high-demand / active hours — average hour 3:52pm (commute window), warmer temperatures, mean rental count of 284/hour.

**Fowlkes–Mallows Index** (clusters vs. demand_level) = 0.54 — K-Means independently discovered a meaningful low-vs-high demand grouping without ever seeing the demand_level labels.

## Conclusion
The Random Forest Regressor explained ~94% of the variability in hourly bike demand (R² = 0.9408), driven primarily by hour of day, temperature, and year. The Random Forest Classifier reached 84.3% accuracy predicting demand_level. K-Means (k=2) independently separated an off-peak/low-demand group from an active/high-demand group (FMI = 0.54), supporting data-driven bike rebalancing across demand periods.

## Tools
`Python` `scikit-learn` `pandas` — Random Forest Regression, Random Forest Classification, K-Means Clustering, GridSearchCV, PCA

## Files in this folder
- `Predicting_Bike_Sharing_Demand.ipynb` — full analysis and code
---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
