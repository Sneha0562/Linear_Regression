"""Model training and evaluation module."""
import pickle
import json
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinearRegressionModel:
    """Linear Regression model wrapper."""
    
    def __init__(self):
        """Initialize model."""
        self.model = LinearRegression()
        self.is_trained = False
        self.metrics = {}
    
    def train(self, X_train, y_train):
        """Train the model.
        
        Args:
            X_train: Training features
            y_train: Training target
        """
        logger.info("Training model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("Model training completed")
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set.
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        y_pred = self.model.predict(X_test)
        
        self.metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'samples': len(y_test)
        }
        
        logger.info(f"Evaluation metrics: {self.metrics}")
        return self.metrics
    
    def predict(self, X):
        """Make predictions.
        
        Args:
            X: Features for prediction
            
        Returns:
            Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        return self.model.predict(X)
    
    def save(self, filepath):
        """Save model to file.
        
        Args:
            filepath: Path to save model
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath):
        """Load model from file.
        
        Args:
            filepath: Path to saved model
        """
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True
        logger.info(f"Model loaded from {filepath}")
    
    def get_coefficients(self, feature_names):
        """Get model coefficients with feature names.
        
        Args:
            feature_names: List of feature names
            
        Returns:
            Dictionary with feature names and coefficients
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        coefficients = dict(zip(feature_names, self.model.coef_))
        coefficients['intercept'] = self.model.intercept_
        return coefficients
