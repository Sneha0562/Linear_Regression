"""Main training script."""
import os
import json
import logging
from data_loader import DataLoader
from model import LinearRegressionModel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main training function."""
    # Configuration
    data_path = os.environ.get('DATA_PATH', '../Advertising.csv')
    model_path = os.environ.get('MODEL_PATH', '../models/model.pkl')
    metrics_path = os.environ.get('METRICS_PATH', '../models/metrics.json')
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    logger.info("Starting training pipeline...")
    
    # Load and preprocess data
    logger.info(f"Loading data from {data_path}")
    data_loader = DataLoader(data_path)
    data_loader.load_data()
    X_train, X_test, y_train, y_test = data_loader.preprocess()
    
    logger.info(f"Training set size: {len(X_train)}")
    logger.info(f"Test set size: {len(X_test)}")
    
    # Train model
    logger.info("Initializing model...")
    model = LinearRegressionModel()
    model.train(X_train, y_train)
    
    # Evaluate model
    logger.info("Evaluating model...")
    metrics = model.evaluate(X_test, y_test)
    
    # Log metrics
    logger.info("=" * 50)
    logger.info("MODEL EVALUATION METRICS")
    logger.info("=" * 50)
    for metric_name, metric_value in metrics.items():
        logger.info(f"{metric_name}: {metric_value:.4f}")
    logger.info("=" * 50)
    
    # Get feature coefficients
    feature_names = data_loader.get_feature_names()
    coefficients = model.get_coefficients(feature_names)
    logger.info("Feature Coefficients:")
    for feature, coef in coefficients.items():
        logger.info(f"  {feature}: {coef:.4f}")
    
    # Save model
    logger.info(f"Saving model to {model_path}")
    model.save(model_path)
    
    # Save metrics
    metrics['coefficients'] = coefficients
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Metrics saved to {metrics_path}")
    
    logger.info("Training pipeline completed successfully!")
    return metrics


if __name__ == "__main__":
    main()
