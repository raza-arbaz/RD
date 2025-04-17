from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np
import pandas as pd

# Load the trained Keras model
model = load_model('model.h5')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect all form input values and cast to float
        features = [float(request.form.get(feat)) for feat in request.form]
        input_array = np.array([features])

        # Get prediction (assuming binary classification)
        prediction = model.predict(input_array)[0][0]  # model.predict returns [[0.123]]

        # Convert to binary: threshold = 0.5
        result = 'Attack Detected 🚨' if prediction >= 0.5 else 'Safe ✅'
        return render_template('index.html', result=result)
    except Exception as e:
        return render_template('index.html', result=f"Error: {e}")

import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

