"""Prediction module."""
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)


class Predictor:
    """Handle model predictions."""
    
    def __init__(self, model_path, scaler_path=None):
        """Initialize predictor.
        
        Args:
            model_path: Path to trained model
            scaler_path: Path to scaler (optional)
        """
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        self.scaler = StandardScaler()
        if scaler_path:
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
    
    def predict(self, features):
        """Make prediction.
        
        Args:
            features: Input features (dict or array-like)
            
        Returns:
            Prediction value
        """
        if isinstance(features, dict):
            # Convert dict to array in correct order
            feature_order = ['TV', 'Radio', 'Newspaper']
            features_array = np.array([[features.get(f, 0) for f in feature_order]])
        else:
            features_array = np.array(features).reshape(1, -1)
        
        features_scaled = self.scaler.transform(features_array)
        prediction = self.model.predict(features_scaled)[0]
        return float(prediction)
    
    def predict_batch(self, df):
        """Make batch predictions.
        
        Args:
            df: DataFrame with features
            
        Returns:
            Array of predictions
        """
        features_scaled = self.scaler.transform(df)
        predictions = self.model.predict(features_scaled)
        return predictions
