# Time Series Modeling on US Retail Sales

## Data Preparation
- Dataframe was in Wide Format where months are the columns. Converted to Long Format (every row a single point in time and a sales value) using `pd.melt`.
- Combined Year and Month columns into a new "Date" column.
- Sorted by Date, reset index, dropped NaN values.
- Kept only Date and Sales columns.

## About the Data
Almost 30 years of US retail history (1992–2021). A consistent upward trend shows a growing economy over 30 years, with an increase in sales at the end of the year from holiday shopping in November and December.

Sharp dip in sales during 2008 to 2010 — the financial crisis and recession, taking 3 years for sales to recover. Sharp drop in early 2020 during COVID-19 and lockdowns, then sales shot up faster in 2021 once vaccines became available.

## Train/Test Split
Time Series Modeling requires data in a chronological sequence, so shuffling was avoided.

- **Train:** through June 2020
- **Test:** July 2020 – June 2021

## Model: SARIMA
SARIMA not only looks at the immediate neighbors (like predicting Feb based on Jan), but also has a seasonal component that checks the same month in previous years (predicting Dec 2020 based on Dec 2019).

Needs two sets of parameters: (p, d, q) for the general trend and (P, D, Q, s) for the seasonal pattern — for retail data, s is always 12.

Starting parameters: (p, d, q) = (1, 1, 1), (P, D, Q, s) = (1, 1, 1, 12). Forecast from the last known date (June 2020) for 12 steps.

## Results
**RMSE: 59,307.28**

On average, the monthly sales prediction is off by 59,307.28. The model score looks affected by extreme historical events, such as the 2008 Financial Crisis and the 2020 COVID pandemic.

## Tools
`Python` `statsmodels` `pandas` — SARIMAX, Time Series Forecasting

## Files in this folder
- `Time_Series_Model_Retail_Sales.ipynb` — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
