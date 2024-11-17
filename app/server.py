# server.py
from flask import Flask, request, jsonify
from routes import user_routes
"""
import tensorflow as tf
from PIL import Image
"""
import numpy as np


app = Flask(__name__)
app.register_blueprint(user_routes)
"""
model = tf.keras.models.load_model("model.h5")

class_labels = ["Healthy", "Disease A", "Disease B", "Disease C"]
def preprocess_image(image_path):

    #Preprocess the input image to match the model's expected input size.

    target_size = (224, 224)  # Update based on your model's input size
    image = Image.open(image_path).convert("RGB")  # Ensure image is RGB
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    return np.expand_dims(image_array, axis=0)  # Add batch dimension
    
@app.route('/predict', methods=['POST'])
def predict():

    #Handle image upload and return predictions.

    try:
        # Check if an image file is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        # Save the uploaded image
        image_file = request.files['image']
        image_path = os.path.join("temp_image.jpg")  # Temporary path to save the file
        image_file.save(image_path)

        # Preprocess the image
        image_data = preprocess_image(image_path)

        # Make predictions
        predictions = model.predict(image_data)
        predicted_class = class_labels[np.argmax(predictions)]

        # Remove the temporary image file
        os.remove(image_path)

        # Return the prediction
        return jsonify({"prediction": predicted_class}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""

if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)