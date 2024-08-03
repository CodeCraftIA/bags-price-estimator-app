# bags-price-estimator-app
This project shows how to scrape sold bags from vestiairecollective using selenium, use the images and their specs to train a model to predict a price, and using flask and the model we create the web app.

# Data Scraping
The first step involves scraping data about Dior bags from a specified website. This data includes details like brand, model, condition, material, color, and selling price. Additionally, images of the bags are also downloaded. 

# Create the model
The second step involves training a machine learning model using the scraped data. This includes preprocessing the structured data, extracting features from images, and training a regression model to predict the prices.

# Libraries Used:
joblib
pandas
numpy
tensorflow
sklearn
xgboost
pickle

# Process:
Load the scraped data and images.
Preprocess the structured data using ColumnTransformer and Pipeline.
Extract features from images using a pre-trained ResNet50 model.
Combine the image features with the structured data.
Train a RandomForestRegressor model on the combined features.
Save the trained model and the preprocessor.

# Flask Application
The third step is to create a Flask web application that allows users to upload an image of a Dior bag and input its details to predict its price.
