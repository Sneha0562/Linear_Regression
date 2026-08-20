"""Data loading and preprocessing module."""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os


class DataLoader:
    """Handle data loading and preprocessing."""
    
    def __init__(self, data_path):
        """Initialize data loader.
        
        Args:
            data_path: Path to CSV file
        """
        self.data_path = data_path
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
    
    def load_data(self):
        """Load data from CSV file."""
        self.data = pd.read_csv(self.data_path)
        # Drop index column if it exists
        if 'Unnamed: 0' in self.data.columns:
            self.data = self.data.drop('Unnamed: 0', axis=1)
        return self.data
    
    def preprocess(self, test_size=0.2, random_state=42):
        """Preprocess data and split into train/test sets.
        
        Args:
            test_size: Proportion of test set
            random_state: Random seed for reproducibility
        """
        if self.data is None:
            self.load_data()
        
        # Check for missing values
        if self.data.isnull().sum().sum() > 0:
            print("Warning: Missing values detected")
            self.data = self.data.dropna()
        
        # Separate features and target
        X = self.data.drop('Sales', axis=1)
        y = self.data['Sales']
        
        # Split into train and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_feature_names(self):
        """Get feature names."""
        if self.data is None:
            self.load_data()
        return [col for col in self.data.columns if col != 'Sales']
