# National Database of Childcare Prices

## About the Data
National Database of Childcare Prices dataset (U.S. Department of Labor, Women's Bureau, 2008–2018).

Rows: 34,567 · Columns: 227 · Years: 2008–2018 · States: 51 · Counties: 1,879

Missing values in price columns are expected — not all counties reported data every year, so no NaN values were deleted.

## Data Preparation
- Derived variables: annual infant center-based care cost (weekly × 52), infant care cost as % of median household income, gender pay gap within counties.
- Key columns selected for the story: childcare prices by age group and setting, median household/female/male earnings, female labor force participation rate, population.

## Design Decisions
A data storytelling project — 18 unique charts in Python and R, distributed with no repeats across a slide deck (data-literate executives), a video (general public), and an infographic (medium complexity), assigned by chart complexity.

- **Color:** tomato, gray, and blue variants highlight key insights so they're immediately visible; consistent color strategy across all charts builds a visual vocabulary.
- **Text:** every chart title is an insight, not a label — leads with the conclusion; titles left-aligned for "Z" scanning.
- **Alignment/Spacing:** minimal grid lines, no top/right spine borders, value labels on or beside bars.
- **Sizing:** 8–10 inches wide, readable on screen and in print.
- **Gestalt principles:** proximity groups related labels near data; similarity via consistent color; contrast makes data pop against white backgrounds; bolded action titles, lighter subtitles, gray source footnotes.

## Charts
- Banner Chart — median weekly infant center-based care is $134.50
- Line Chart — +27.7% in 10 years, childcare costs rising faster than wages
- Pie Chart — only 0.2% of counties have affordable childcare (≤7% of income)
- Horizontal Stacked Bar — 66% of low-income counties spend >15% of income on infant care alone
- Heatmap — by 2018, NY and NH exceeded $200/week for infant care
- Difference Chart — women earned $2,102 more, but childcare cost $1,714 more, in 10 years
- Baseline Chart — childcare costs rose 27% since 2008, male earnings grew just 2.5%
- Scatter Chart — by 2018 single mothers spent 33% of income on childcare, 5x the HHS threshold
- Waffle/Square Pie Chart — 4 out of 5 counties spend >10% of household income on infant care
- Line Chart — childcare costs climbed from $121/week (2008) to $154/week (2018)
- Histogram — most counties charge $100–$200/week, some as high as $470/week
- Barbell Chart — infant center care costs $1,768/year more than home-based care
- Stacked Area Chart — total weekly childcare burden reached $419 by 2018, up $84 from 2008
- Donut Chart — 99.8% of counties cannot afford childcare by federal standards (2018)
- Slope Chart — single mothers' childcare spending rose from 29.2% to 33.2% of income (2008–2018)
- Stream Chart — every age group got more expensive every year; infant care rose $33/week since 2008
- Horizontal Bar Chart — DC infant care costs $303/week, $15,786/year for one child
- GeoMap — West Coast states (MA, CA, NY, WA) have the highest weekly childcare bills; Southern/Midwestern states pay significantly less

## Tools
`Python` `R` `matplotlib` `seaborn` — Data Storytelling, Data Visualization

## Files in this folder
- `National_Database_Childcare_Benefits.ipynb` — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
