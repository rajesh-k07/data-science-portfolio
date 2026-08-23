# Women's E-Commerce Sentiment Analysis and Product Rating

## About Project
Online retailers receive thousands of customer reviews, and analyzing these reviews manually is inefficient and time consuming. Retailers need an automated process that can quickly understand customer sentiment and predict product performance.

I built multiple models on this dataset, but the two selected for deployment are:
- **Logistic Regression** for customer review text analysis (predicting Recommended IND)
- **Light Gradient Boosted (LightGBM) Regressor** for predicting customer ratings

## About Dataset
"Women's E-Commerce Clothing Reviews" dataset from Kaggle — 23,486 individual customer entries, each with ten feature variables pairing the shopper's raw review text with metadata such as age and product category.

**Dataset link:** https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews/data

## Data Preparation
- Dropped `Unnamed: 0` index column, `Division Name`, `Department Name`, `Class Name`.
- Dropped rows with missing `Review Text`; filled missing `Title` with "Unknown".
- Age outliers (108, via IQR) not removed — Age isn't used in the sentiment model.
- Cleaned `Review Text`: lowercased, removed punctuation, tokenized, removed stopwords, Porter stemming.
- Vectorized with `TfidfVectorizer` (ngram_range=(1,2)), then reduced with Chi2 (k=25000) and NMF (300 components).
- Train/test split (80/20) done before fit_transform to avoid data leakage, stratified on `Recommended IND`.

## Model 1: Logistic Regression (Review Text Sentiment)
Predicts `Recommended IND` from TF-IDF + Chi2-selected review text features, with `class_weight='balanced'` to handle the imbalanced target.

**Results:** Accuracy = 85.60% · Recall (Class 0) = 0.82 · Precision (Class 0) = 0.57

Selected over Random Forest (88% accuracy but only 61% recall on "Not Recommended") since catching dissatisfied customers matters more than raw accuracy here.

## Model 2: Light Gradient Boosted Regressor (Product Rating)
Rating (1–5) predicted as a continuous value instead of a class, using 300 NMF topics + Age + Positive Feedback Count + Recommended IND.

**Results:** R² = 0.69 · MAE = 0.46 (beat Random Forest's R² = 0.67)

**Top contributors:** Age, Recommended IND, Positive Feedback Count, and Topics 250 and 52.

## Tools
`Python` `scikit-learn` `LightGBM` `NLTK` — TF-IDF, Chi2 Feature Selection, NMF, Logistic Regression, LightGBM Regression

## Files in this folder
- `Woman_Sentiment_Analysis_ProductRating.ipynb` — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
