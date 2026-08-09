
# Predictive Modeling Using Bank Marketing Dataset

## About Project
The Bank Marketing team calls customers to encourage them to subscribe to a term
deposit. They do not want to call all new and old customers without any insight —
it will cost them a lot of money and time. The objective of this project is to
optimize the bank's telemarketing efforts for term deposit subscriptions.

My primary machine learning model is a **supervised classification learning
model** to predict whether a customer will subscribe to a term deposit, helping
identify which features most strongly influence customer decisions. I also
trained an **unsupervised clustering model** to create customer segments, so the
bank can prioritize higher-performing segments and use lower-cost channels for
the rest.

## About Dataset
UCI Machine Learning Repository — nearly 45,000 direct marketing phone contacts
made by a Portuguese bank. Target "y": has the client subscribed a term deposit?
(binary: "yes","no")

**Citation:** Moro, S., Cortez, P., & Rita. P. (2012, Feb 13). *Bank marketing*. 
UCI irvine machine learning repository. https://archive.ics.uci.edu/dataset/222/bank+marketing

## Data Cleaning
- Dropped 'poutcome' and 'duration' columns
- Dropped rows where 'job' is 'unknown'
- Handled outliers: balance > 15000, campaign > 10, previous > 60
- Created a new binary feature pdays_connect (0 = New Customer, 1 = Returning Customer)

## Random Forest Classifier
I tried multiple models, but I am proposing the Random Forest classifier because
it offers the strongest balance between efficiency and opportunity, achieving an
F1-score of 0.44 and an AUC of 0.7760. It has a per-call success rate, precision =
40%, while still capturing nearly half of all potential subscribers. This
performance is primarily driven by customer balance, age, and specific timing
factors, such as the day of the call.

Balance and age are the most important input features for term deposit
subscriptions. The model also relies on timing and engagement patterns, such as
the specific day of the call and the history of previous bank interactions, to
distinguish potential subscribers.

**Results:** Accuracy = 85.85% · F1-score (class "yes") = 0.44 · AUC-ROC = 0.7760 ·
Precision = 0.40 · Recall = 0.48

Bank can achieve a 40% success rate per call, identifying nearly half of all
potential subscribers while avoiding 90% of uninterested customers.

## KMeans Clustering
Using K-Means clustering, I am creating a customer segment so the bank can
prioritize segments during telemarketing campaigns to increase conversion rates
and reduce marketing costs, and target the lower-performing segment using
alternative low-cost channels.

Silhouette score was used to pick the optimal number of clusters — clusters = 2
had the highest positive value.

Cluster label 0 is the more responsive segment, with approximately 15.5% of
customers subscribing compared to 10.3% in Cluster 1 — 1.5x higher chance to
subscribe. Fowlkes–Mallows Index = 0.6859, indicating strong similarity between
how K-Means grouped customers and how they actually responded. PCA visualization
confirms the two segments are meaningfully distinct.

## Conclusion
Random Forest achieved an accuracy of 85.85% and the highest F1-score (0.44) for
the positive class, driven primarily by customer balance, age, and call timing.
The K-Means model identified Cluster 0 as the more responsive segment (15.5% vs.
10.3% subscription rate), letting the bank focus resources on higher-conversion
customers.

## Tools
`Python` `scikit-learn` `pandas` — Random Forest Classification, K-Means
Clustering, GridSearchCV, Feature Engineering, PCA

## Files in this folder
- `Predictive_Modeling_Bank_Marketing.ipynb` — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
