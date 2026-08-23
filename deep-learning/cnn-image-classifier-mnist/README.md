# Image Classifier using CNN

A Convolutional Neural Network (CNN) is a deep learning model designed to process data with a grid like topology, mostly images and computer vision. A standard CNN architecture consists of three layers.

The Convolutional Layer learns important image features that can be used for the task at hand, by applying a filter to a particular area of an image. 

Pooling layers typically reduce the dimensionality of the inputs from the previous layers, taking only the most important information from a small area. 

Fully connected layers can be used with something like a softmax activation function to create a classification task.

## About Dataset
MNIST (Modified National Institute of Standards and Technology) — a collection of small, grayscale images representing handwritten digits from 0 through 9. Each observation has two parts: Image (a 28x28 pixel grayscale image, a grid of 784 pixels) and Label (a single integer from 0 to 9 identifying the digit written in the image).

Training Set: 60,000 images · Test Set: 10,000 images

## Data Preparation
- Converting the image into a PyTorch Tensor is a data preprocessing stage in Machine Learning. Used a mean = 0.11 and a standard deviation = 0.31 to standardize the image pixel values.
- Batch Size = 64 — the number of training examples used in one single pass of the model's learning process. Data loaders shuffle both train and test sets.

## Model: CNN (PyTorch)
Architecture:
- **conv1**: takes 1 input channel and creates 32 different filtered versions of the image to find edges and curves.
- **conv2**: takes those results and uses 64 filters to combine those lines into more complex shapes and patterns.
- **ReLU**: the activation function that turns off negative value pixels so that the model only focuses on important features.
- **max_pool2d**: looks at 2x2 pixel squares and only keeps the maximum value, reducing the image size and keeping only important features.
- **Dropout**: 0.25 applied after pooling, 0.5 applied before fc1.
- **fc1 / fc2**: CNNs work in 2D (height and width), but standard classification layers work in 1D, so the output is transitioned from 2D into a 1D array.
- **log_softmax(x, dim=1)**: converts raw scores into log probabilities between 0 and 1.

Trained for 3 epochs — it goes through the entire training dataset 3 times. Device set to Metal Performance Shaders (MPS) to accelerate GPU based training, else CPU.

## Results
CNN Model Accuracy for Image Classifier is 99.23%. This means 99.23% of the test images were correctly classified. Only 77 predictions are wrong out of 10,000 test images. The model is very accurate across all classes, since most numbers are on the diagonal of the confusion matrix — numbers outside the diagonal are the mistakes.

Results show that the CNN Image Classifier model learned the digit patterns correctly and generalizes well to test data.

## Tools
`Python` `PyTorch` `torchvision` — CNN, Conv2D, Max Pooling, Dropout

## Files in this folder
- `Image_Classifier_CNN.ipynb` — full analysis and code

---
Part of [Data Science Portfolio](https://github.com/rajesh-k07/data-science-portfolio/tree/main)

**Main site:** [rajesh-k07.github.io](https://rajesh-k07.github.io)
