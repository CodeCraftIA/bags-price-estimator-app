import pandas as pd
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import pickle
from xgboost import XGBClassifier

# Load the dataset
df = pd.read_excel("dior_Soldbags.xlsx")

# Define paths to images
image_folder = "dior_images"  # Assuming the folder containing images is named 'dior_images'

# Function to load and preprocess images
def load_and_preprocess_image(filename):
    #img_path = os.path.join(image_folder, filename)
    img = tf.keras.preprocessing.image.load_img(filename, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)
    return img_array

# Load pre-trained ResNet50 model for image feature extraction
resnet_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Extract image features
image_features = np.array([load_and_preprocess_image(os.path.join(image_folder, filename)) for filename in df['Filename']])
image_features = resnet_model.predict(image_features)

# Define categorical features
categorical_features = ['Brand', 'Model', 'Condition', 'Material', 'Color']

# Define preprocessing steps for structured data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features),
    ])

# Train-test split
X_structured = preprocessor.fit_transform(df)

# Convert sparse matrix to dense array
X_structured_dense = X_structured.toarray()

# Combine the image features with the structured data
X_combined = np.concatenate((image_features.reshape(image_features.shape[0], -1), X_structured_dense), axis=1)

# Remove euro symbol and commas, and convert to float
y = df['Sold at/Selling price'].str.replace('€', '').str.replace(',', '.').astype(float)

X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# Train a regression model
model = RandomForestRegressor(max_depth=5, n_estimators=500, n_jobs=-1 , random_state=42, verbose=2)
model.fit(X_combined, y)

#model = XGBClassifier(learning_rate=0.1, max_depth=5, n_estimators=100, random_state=42, verbose=1)
#model.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='mae')


# Save the model using pickle
file_name = "rf_bags_model.pkl"
pickle.dump(model, open(file_name, "wb"))

# Make predictions
y_pred = model.predict(X_test)

# Calculate mean absolute error
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)
r2 = r2_score(y_test, y_pred)
print("R2 score:", r2)



'''
# Function to predict price given image and optional structured data
def predict_bag_price(image_filename, structured_data=None):
    img_features = load_and_preprocess_image(image_filename)
    img_features = resnet_model.predict(np.expand_dims(img_features, axis=0))
    if structured_data is None:
        structured_data = np.zeros((1, X_structured.shape[1]))  # Fill with zeros if no structured data provided
    X_combined = np.concatenate([img_features, structured_data], axis=1)
    return model.predict(X_combined)[0]

# Example usage
image_filename = "example_bag.png"  # Example bag image filename

structured_data = preprocessor.transform(pd.DataFrame({'Brand': ['Dior'], 'Model': ['Tote'], 'Condition': [''], 'Material': [''], 'Color': ['']}))  # Example structured data
predicted_price = predict_bag_price(image_filename, structured_data)
print("Predicted price:", predicted_price)
'''


# Define the example image path
example_image_path = "example_bag.png"
'''
# Load and preprocess the example image
example_img = tf.keras.preprocessing.image.load_img(os.path.join(image_folder, example_image_path), target_size=(224, 224))
example_img_array = tf.keras.preprocessing.image.img_to_array(example_img)
example_img_array = tf.keras.applications.resnet.preprocess_input(example_img_array)
'''
example_img_array = np.array(load_and_preprocess_image(example_image_path))

# Extract image features
example_image_features = resnet_model.predict(np.expand_dims(example_img_array, axis=0))

# Define the structured data for the example
example_structured_data = pd.DataFrame({
    'Brand': ['Dior'],
    'Model': ['Lady Dior'],
    'Condition': ['New'],
    'Material': ['Leather'],
    'Color': ['Black']
})

# Transform the structured data for the example
example_structured_data_transformed = preprocessor.transform(example_structured_data)

# Convert sparse matrix to dense array for the example
example_structured_data_dense = example_structured_data_transformed.toarray()

# Combine the image features with the structured data for the example
X_combined_ex = np.concatenate((example_image_features.reshape(1, -1), example_structured_data_dense), axis=1)

# Make predictions
y_pred2 = model.predict(X_combined_ex)
print("Predicted Price for the Example Bag:", y_pred2)

