# Tetouan Power Grid: Forecasting Electricity Consumption

## About Project
This project analyzes 10-minute interval power consumption data from three electrical distribution zones in Tetouan, Morocco. It model and forecast regional electricity demand using supervised regression and time-series methods.

Tetouan's power grid is divided into three distribution zones, each with a different mix of residential and commercial customers. 

## About Dataset
Power Consumption of Tetouan City dataset from the UCI Machine Learning Repository — 52,416 records of power consumption and weather readings recorded every 10 minutes across 2017 for three distribution zones.

**Features:** Temperature (°C), Humidity (%), Wind Speed (m/s), General Diffuse Flows (W/m²), Diffuse Flows (W/m²)

**Targets:** Zone 1, Zone 2, Zone 3 Power Consumption (kW)

**Dataset link:** https://archive.ics.uci.edu/dataset/849/power+consumption+of+tetouan+city

## Data Preparation
- Cleaned inconsistent column name spacing (e.g., double space in "Zone 2  Power Consumption").
- Converted DateTime to datetime type and created new temporal features: hour, day of week, month, and a weekend flag.
- Created two lagged features per zone (consumption 24 hours prior, and a 1-hour trailing rolling average) to capture short-term demand velocity — improved model accuracy.
- No features dropped — no high multicollinearity found among the five weather features, so all were retained.
- No log/sqrt transforms applied.
- No missing values, duplicates, or outlier removal — outliers in solar flow features reflect the normal day/night solar cycle, not data errors.
- Split chronologically (80% train / 20% test) rather than randomly, since a random split would leak future information into training.

## Model 1: t-test (Weekday vs. Weekend Consumption)
Tested whether average consumption differs between weekdays and weekends, per zone.

H₀: No real difference in average consumption between weekdays and weekends.
H₁: There is a genuine difference.

**Result:** p-value < 0.05 for all three zones — reject the null hypothesis. There is a statistically significant difference between weekday and weekend consumption in every zone.

## Model 2: Random Forest Regressor (Multi-Output)
Predicts power consumption across Zone 1, 2, and 3 simultaneously, using weather, calendar, and lagged-consumption features. Chronological 80/20 split; hyperparameters tuned with GridSearchCV (3-fold CV).

**Results:** R² = 0.71–0.79 across the three zones · MAE = 1,401–2,545 kW (average ~1,964 kW off)

Each zone's own recent consumption history is the most important feature in predicting its power consumption.

## Model 3: SARIMA (per zone)
Run independently for each zone on hourly-resampled data (from the original 10-minute intervals), using a seasonal order capturing daily (24-hour) demand cycles, evaluated over a 48-hour forecast horizon.

**Results:** R² = 0.89–0.98 across all three zones — strong short-horizon accuracy.

## Conclusion
Electricity demand across Tetouan's three zones can be forecast with good accuracy. The Random Forest Regressor explains 71–79% of variance in zone-level demand using weather, calendar, and recent-consumption features, and is recommended as the primary model since it's a single unified model across all three zones and incorporates weather for forward-looking planning. SARIMA (89–98% accuracy) serves as a secondary, cross-check model for short-horizon forecasts when weather data is unavailable. Zone 3 shows the highest volatility and warrants extra planning caution.

## Limitations
- Covers only one city and one calendar year (2017) — results may not generalize across years or regions.
- No holiday or facility-specific data to explain irregular demand spikes.

## Tools
`Python` `scikit-learn` `statsmodels` `pandas` — Random Forest Regression (Multi-Output), SARIMA, GridSearchCV, t-test

## Files in this folder
- 'Forecasting_Electricity_Consumption.ipynb' — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
