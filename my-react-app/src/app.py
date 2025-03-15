from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import tensorflow as tf
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import os

 
NLTK_DIR = os.path.join(os.getcwd(), 'nltk_data')
os.makedirs(NLTK_DIR, exist_ok=True)
nltk.data.path.append(NLTK_DIR)

try:
    nltk.download('punkt', download_dir=NLTK_DIR, quiet=True)
    nltk.download('stopwords', download_dir=NLTK_DIR, quiet=True)
    
    # 🔥 Force reload stopwords
    nltk.data.load("tokenizers/punkt/english.pickle")  # Force loading punkt tokenizer
    nltk.data.load("corpora/stopwords.zip")  # Force loading stopwords
    
    STOP_WORDS = set(stopwords.words('english') + list(string.punctuation))
except Exception as e:
    print(f"⚠️ Warning: NLTK resources not fully loaded ({str(e)}), using basic fallback.")
    STOP_WORDS = set(string.punctuation)  # Fallback: Only remove punctuation

 
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

 
model = tf.keras.applications.MobileNetV2(weights="imagenet")

 
def preprocess_image(image):
    try:
        image = cv2.resize(image, (224, 224))  # Resize for model
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        image = image / 255.0  # Normalize
        return image
    except Exception as e:
        return None

# 🔥 IMPROVED SEO DESCRIPTION FUNCTION
def generate_seo_description(text):
    try:
        nltk.data.path.append(NLTK_DIR)  # Ensure correct NLTK path
        words = word_tokenize(text.lower())  # Tokenize text
        keywords = [word for word in words if word not in STOP_WORDS]

        return ", ".join(keywords) if keywords else "No meaningful keywords extracted"
    
    except Exception as e:
        print(f"❌ SEO Generation Failed: {str(e)}")
        return "keywords, image, AI, analysis, prediction, SEO"

 
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running! Use /analyze for image analysis."})

 
@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "Invalid image file"}), 400

        # Process image
        processed_img = preprocess_image(image)
        if processed_img is None:
            return jsonify({"error": "Image processing failed"}), 500

        # Predict features
        predictions = model.predict(processed_img)
        predicted_labels = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        
        description = ", ".join([label[1] for label in predicted_labels])
        seo_description = generate_seo_description(description)

        return jsonify({
            "predictions": description,
            "seo_description": seo_description
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  # Runs on all networks




