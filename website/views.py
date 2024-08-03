from flask import Flask, render_template, request, Blueprint
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pickle
import joblib
import tensorflow as tf
import numpy as np
import pandas as pd


views = Blueprint('views', __name__)


# Load preprocessor and model
preprocessor = joblib.load('preprocessor.pkl')
model = pickle.load(open("rf_bags_model.pkl", "rb"))
resnet_model = tf.keras.models.load_model('resnet_model.h5')

# Function to load and preprocess images
def load_and_preprocess_image(filename):
    img = tf.keras.preprocessing.image.load_img(filename, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)
    return img_array

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Save the uploaded file
            uploaded_file.save(uploaded_file.filename)
            
            # Load and preprocess the uploaded image
            example_img_array = np.array(load_and_preprocess_image(uploaded_file.filename))

            # Extract image features
            example_image_features = resnet_model.predict(np.expand_dims(example_img_array, axis=0))

            # Get the form data
            brand = request.form['brand']
            model1 = request.form['model']
            condition = request.form['condition']
            material = request.form['material']
            color = request.form['color']

            # Create structured data from form data
            example_structured_data = pd.DataFrame({
                'Brand': [brand],
                'Model': [model1],
                'Condition': [condition],
                'Material': [material],
                'Color': [color]
            })

            # Transform the structured data
            example_structured_data_transformed = preprocessor.transform(example_structured_data)
            example_structured_data_dense = example_structured_data_transformed.toarray()

            # Combine the image features with the structured data
            X_combined_ex = np.concatenate((example_image_features.reshape(1, -1), example_structured_data_dense), axis=1)

            # Make predictions
            y_pred2 = model.predict(X_combined_ex)
            predicted_price = y_pred2[0]

            return render_template('result.html', predicted_price=predicted_price)

    # If GET request or file not uploaded, render the form
    return render_template('index.html')

    

