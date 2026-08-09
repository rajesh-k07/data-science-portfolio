# Data Science Portfolio

Portfolio of data science projects- machine learning, NLP, deep learning, time
series, and statistical analysis covering academic and independent work.

🔗 **Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)

Each project below has its own folder with a notebook and a project-specific
README summarizing the problem, approach, and results.

## Machine Learning

- **[Predictive Modeling Using Bank Marketing Dataset](machine-learning/bank-marketing-predictive-modeling/)**
  A supervised classification model predicting customer subscription to term
  deposits, identifying key features driving customer decisions and campaign
  effectiveness. Paired with an unsupervised clustering model that segments
  customers, enabling prioritization of high-conversion groups and cheaper
  channels for low-performing segments.
  `Python` `scikit-learn` `Classification` `Clustering` `Feature Analysis`

- **[Census Income Dataset - EDA and Modeling](machine-learning/census-income-eda-modeling/)**
  A logistic regression model classifying individuals as earning
  above or below $50K annually. K-Means clustering segments the population into
  two groups based on age, education, income, and marital status, without
  relying on sex as a label, and regression predicting age from work-related, demographic, and income features.
  `Python` `scikit-learn` `Regression` `Logistic Regression` `K-Means` `EDA`

- **[Capital Bikeshare: Predicting Bike Sharing Demand](machine-learning/bikeshare-demand-prediction/)**
  A Random Forest Regression model predicting rental counts, and a Random
  Forest Classifier categorizing demand into distinct levels based on usage
  and environmental features. K-Means clustering identifies usage patterns and
  segments demand behavior across different conditions.
  `Python` `scikit-learn` `Random Forest` `K-Means`

## NLP

- **[Women's E-Commerce Sentiment Analysis and Product Rating](nlp/ecommerce-sentiment-analysis/)**
  A supervised classification model predicting whether a customer would recommend a
  product based on review text and customer metadata, identifying high-risk
  products and key drivers of dissatisfaction. A secondary regression model
  predicts product ratings from review text and customer features.
  `Python` `NLP` `Sentiment Analysis` `Classification` `Regression`

- **[Sentiment Analysis on IMDB Movie Reviews](nlp/imdb-sentiment-analysis/)**
  Text preprocessing and a sentiment classification model on the labeled IMDB
  movie review dataset (25,000 reviews), predicting binary sentiment positive or
  negative from raw review text with emphasis on cleaning unstructured text to
  improve model accuracy and generalizability.
  `Python` `NLP` `Text Preprocessing` `Sentiment Classification`

## Deep Learning

- **[Image Classifier using CNN](deep-learning/cnn-image-classifier-mnist/)**
  A CNN (Convolutional Neural Network) model in PyTorch classifying handwritten digits
  (0-9) from the MNIST dataset, using convolutional layers to extract image features
  and achieving accurate digit recognition on 28x28 grayscale images through iterative
  tuning of the network architecture. `Python` `PyTorch` `CNNs` `Computer Vision`

## Time Series

- **[Time Series Modeling on US Retail Sales](time-series/retail-sales-time-series-sarima/)**
  A SARIMA (Seasonal AutoRegressive Integrated Moving Average) model forecasting
  US retail sales, with trend (p, d, q) and seasonal (P, D, Q, s=12) parameters
  tuned for monthly forecast accuracy.
  `Python` `Time Series` `SARIMA` `statsmodels`

## Data Visualization

- **[National Database of Childcare Prices](data-visualization/childcare-prices-financial-planning/)**
  Exploring a national childcare pricing dataset to discover trends in childcare affordability across
  regions and demographics, using storytelling with data techniques to make findings accessible to
  non-technical audiences. Built visualizations in both Python and R to support financial
  planning insights around childcare benefits.
  `Python` `R` `Data Visualization` `Data Storytelling`

- **[Enhancing US Travel Review Insights](data-visualization/us-travel-review-insights/)**
  Multiple data sources merged into a unified database for deeper analysis of US travel
  trends and customer sentiment, with visualizations improving the ability to compare review patterns.
  `Python` `SQL` `Data Integration` `Data Visualization`

## Statistics / R

- **[Feature Scaling and Transformation](statistics-r/feature-scaling-transformation/)**
  Feature scaling techniques include min-max scaling, square root, and log transformations,
  exploring how different transformations affect data distribution and downstream statistical analysis.
  `R` `Feature Scaling` `Data Transformation`

- **[Statistical Significance Testing](statistics-r/statistical-significance-testing/)**
  One-way and two-way ANOVA tests evaluating statistical significance across
  grouped data.
  `R` `ANOVA` `Statistical Analysis`

---

*More projects will be added over time.*

Feel free to reach out via the contact links on my [main site](https://rajesh-k07.github.io).
