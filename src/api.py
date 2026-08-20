"""Flask API for model predictions."""
from flask import Flask, request, jsonify
import os
import logging
from predict import Predictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load model
model_path = os.environ.get('MODEL_PATH', './models/model.pkl')
try:
    predictor = Predictor(model_path)
    logger.info(f"Model loaded successfully from {model_path}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    predictor = None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint.
    
    Expected JSON:
    {
        "TV": float,
        "Radio": float,
        "Newspaper": float
    }
    """
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['TV', 'Radio', 'Newspaper']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': f'Missing required fields: {required_fields}'
            }), 400
        
        # Make prediction
        prediction = predictor.predict(data)
        
        return jsonify({
            'prediction': prediction,
            'input': data
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Batch prediction endpoint.
    
    Expected JSON:
    {
        "data": [
            {"TV": float, "Radio": float, "Newspaper": float},
            ...
        ]
    }
    """
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if 'data' not in data:
            return jsonify({'error': 'Missing "data" field'}), 400
        
        import pandas as pd
        df = pd.DataFrame(data['data'])
        predictions = predictor.predict_batch(df)
        
        return jsonify({
            'predictions': predictions.tolist(),
            'count': len(predictions)
        }), 200
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/metrics', methods=['GET'])
def metrics():
    """Get model metrics."""
    try:
        import json
        metrics_path = './models/metrics.json'
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
