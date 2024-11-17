# server.py
from flask import Flask, request, jsonify
from routes import user_routes
"""
import tensorflow as tf
from PIL import Image
import numpy as np
from google.cloud import storage
import os
import uuid
"""

app = Flask(__name__)
app.register_blueprint(user_routes)
"""
model = tf.keras.models.load_model("model.h5")

class_labels = ["Healthy", "Disease A", "Disease B", "Disease C"]

storage_client = storage.Client()

def preprocess_image(image_path): 

    #Preprocess the input image to match the model's expected input size.

    target_size = (224, 224)  # Update based on your model's input size
    image = Image.open(image_path).convert("RGB")  # Ensure image is RGB
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    return np.expand_dims(image_array, axis=0)  # Add batch dimension
    
# Function to upload image to GCS bucket
def upload_image_to_bucket(bucket_name, source_file_path, destination_blob_name):

    #Upload a file to a Google Cloud Storage bucket.

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)
        return f"gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        raise Exception(f"Failed to upload image to bucket: {str(e)}")

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():

    #Handle image upload, prediction, and storage in GCS.

    try:
        # Check if an image file is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        # Save the uploaded image temporarily
        image_file = request.files['image']
        temp_image_path = os.path.join("temp", f"{uuid.uuid4()}.jpg")
        os.makedirs("temp", exist_ok=True)
        image_file.save(temp_image_path)

        # Preprocess the image
        image_data = preprocess_image(temp_image_path)

        # Make a prediction
        predictions = model.predict(image_data)
        predicted_class = class_labels[np.argmax(predictions)]

        # Upload the image to GCS
        bucket_name = "your-gcs-bucket-name"  # Replace with your bucket name
        destination_blob_name = f"uploads/{uuid.uuid4()}.jpg"  # Generate a unique filename
        gcs_uri = upload_image_to_bucket(bucket_name, temp_image_path, destination_blob_name)

        # Remove the temporary image file
        os.remove(temp_image_path)

        # Return the prediction and image storage location
        return jsonify({
            "prediction": predicted_class,
            "image_uri": gcs_uri
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""

if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)