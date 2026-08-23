# Enhancing US Travel Review Insights through Multi-Sources

## About Project
Combined multiple data sources — Google review activity, U.S. population statistics, holiday calendars, and air-quality data — into a single master dataset, to explore how environmental conditions, seasonal variations, holidays, and urban characteristics influence user activity and review behavior across major U.S. cities.

This project is about pulling data from different sources, cleaning it, merging it into a single SQL database, and building visualizations for analysis.

## Data Sources
- **Google Review Ratings** (`df_google_review_ratings.csv`) — main dataset. UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/485/travel+review+ratings
- **US State/City Population** (`df_us_state_city_population.csv`) — scraped from Wikipedia HTML pages.
- **US Holidays 2025** (`df_us_holiday_api.csv`) — from api-ninjas.com.
- **US City Air Quality Index** (`df_us_aqi_api.csv`) — from api-ninjas.com.

Each source was cleaned and prepared in its own separate `.ipynb` file, then run and loaded into this notebook (`%run`).

## Data Preparation
- Replaced "Santa Monica" with "Los Angeles" in the Google review city column, since Santa Monica wasn't present in the other API datasets.
- Loaded all four cleaned CSVs into a SQLite database (`term5_db`), one table per source.
- Merged all four tables into a single combined table (`tbl_all`): joined Google reviews to population data and AQI data on city, and left-joined to the holiday table on date (marking non-matches as "No_Holiday").

## Visualizations
- **Average Ratings of Places by City on Non-Holidays** — reveals how visitors rate everyday experiences without the unusual surges in crowd levels that holidays often create.
- **Total Food Places Reviews by Season** — count of reviews for four major food categories (restaurants, pubs/bars, burger–pizza shops, juice bars), aggregated by season.
- **Total Reviews per Month** — converts daily review dates into monthly totals to see trends on a broader timescale.
- **Weekend vs Weekday and Holiday vs Non-Holiday Reviews** — pie charts comparing review activity between weekends/weekdays and holiday/non-holiday periods.
- **Number of Reviews by City and Air Quality Index** — dual-axis chart combining a bar chart of total reviews per city with a line chart of average AQI in those cities, showing how environmental conditions coexist with user activity.

## Ethical Considerations
The ethical considerations primarily involve ensuring data privacy and maintaining integrity in downloading the Google review rating dataset, fetching and handling the API data, and using the population data from Wikipedia for project work. All three data sources are publicly available.

Transparency was maintained by documenting all cleaning steps, loading data into tables, merging into one table, ensuring reproducibility, and avoiding transformations that could distort the purpose of the analysis.

## Tools
`Python` `pandas` `SQLite` `BeautifulSoup` `requests` `matplotlib` — Data Integration, Web Scraping, API Integration, Data Visualization

## Files in this folder
- `Enhancing_US_Travel_Review_MultiSource.ipynb` — final notebook, loads and merges all sources
- Source-cleaning notebooks (`google_review_ratings.ipynb`, `US_state_city_population.ipynb`, `US_aqi_api.ipynb`)

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
