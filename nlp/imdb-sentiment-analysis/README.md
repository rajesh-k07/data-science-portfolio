# Sentiment Analysis on IMDB Movie Reviews

## About Dataset
"labeledTrainData" — a labeled, tab-delimited dataset of 25,000 IMDB movie reviews. Binary sentiment: 1 = positive, 0 = negative.

**Dataset link:** https://www.kaggle.com/competitions/word2vec-nlp-tutorial/data?select=labeledTrainData.tsv.zip

## Data Preparation
- Removed HTML tags (`<br />`) from review text.
- Lowercased, removed punctuation, tokenized, removed stopwords, applied Porter stemming.
- Encoded cleaned text as Bag of Words, then weighted with TF-IDF.
- Train/test split (80/20, stratified) done before TF-IDF fitting — fit_transform on train only, transform only on test, to avoid data leakage.

## Model 1: Logistic Regression
**Results:** Accuracy = 88.72% · Recall = 0.90 · F1 = 0.89 (both classes)

Identifies sentiment correctly in nearly 9 out of 10 reviews, with identical F1-scores across both classes — balanced, no bias toward either sentiment.

## Model 2: Random Forest
**Results:** Accuracy = 84.54% · Precision/Recall = 0.84–0.85 · F1 = 0.85 (both classes)

Consistent across both classes, but scored below Logistic Regression on this dataset.

## Conclusion
Logistic Regression outperformed Random Forest on this TF-IDF feature set (88.72% vs. 84.54% accuracy) and was the stronger model for this task.

## Tools
`Python` `scikit-learn` `NLTK` — Bag of Words, TF-IDF, Logistic Regression, Random Forest

## Files in this folder
- `Sentiment_Analysis_IMDB_Movie_Reviews.ipynb` — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
