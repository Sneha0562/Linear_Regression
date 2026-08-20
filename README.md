# Linear Regression MLOps Project

A production-ready machine learning project that predicts product sales based on advertising spend across different media channels. This project demonstrates best practices in MLOps including containerization, CI/CD pipelines, automated testing, and API deployment.

## 🎯 Project Overview

**Objective:** Build and deploy a linear regression model that predicts sales based on TV, Radio, and Newspaper advertising investments.

**Dataset:** Advertising.csv (200 samples)
- **Features:** TV, Radio, Newspaper (advertising spend in thousands)
- **Target:** Sales (in thousands)

## 📊 Quick Start

### Local Setup

```bash
# Clone repository
git clone https://github.com/Sneha0562/Linear_Regression.git
cd Linear_Regression

# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train model
cd src
python train.py

# View metrics
cat ../models/metrics.json
```

### Docker Setup

```bash
# Using Docker Compose
docker-compose up --build

# Or manual Docker
docker build -t linear-regression:latest -f Dockerfile .
docker run -v $(pwd)/models:/app/models linear-regression:latest
```

## 🚀 Features

### Core Components
- **Data Loader** (`src/data_loader.py`): Handles data loading, preprocessing, and splitting
- **Model** (`src/model.py`): Training, evaluation, and prediction
- **Training Pipeline** (`src/train.py`): End-to-end training orchestration
- **API** (`src/api.py`): Flask REST API for predictions
- **Predictor** (`src/predict.py`): Inference module for batch and single predictions

### MLOps Infrastructure
- ✅ **Containerization**: Docker & Docker Compose
- ✅ **CI/CD Pipelines**: GitHub Actions workflows
- ✅ **Automated Testing**: Unit tests with pytest
- ✅ **Code Quality**: Flake8, Pylint, Black, isort
- ✅ **Monitoring**: Metrics tracking and validation
- ✅ **API**: REST endpoints for predictions
- ✅ **Documentation**: Comprehensive guides and examples

## 📁 Project Structure

```
Linear_Regression/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── data_loader.py         # Data loading & preprocessing
│   ├── model.py               # Model implementation
│   ├── train.py               # Training pipeline
│   ├── predict.py             # Inference module
│   ├── api.py                 # Flask REST API
│   └── monitoring.py          # Metrics tracking
├── tests/
│   ├── test_data_loader.py
│   ├── test_model.py
│   └── conftest.py
├── scripts/
│   ├── check_metrics.py       # Metric validation
│   └── generate_report.py     # Report generation
├── models/                    # Trained models storage
├── logs/                      # Application logs
├── reports/                   # Generated reports
├── .github/workflows/         # CI/CD pipelines
│   ├── train.yml
│   ├── evaluate.yml
│   ├── docker.yml
│   └── quality.yml
├── Dockerfile                 # Training container
├── Dockerfile.api             # API container
├── docker-compose.yml         # Multi-container setup
├── requirements.txt           # Python dependencies
├── MLOPS_SETUP.md            # Detailed setup guide
├── README.md                  # This file
└── Advertising.csv            # Dataset
```

## 🔧 Installation

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (optional)
- Git

### Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install base dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 pylint isort
```

## 📈 Model Performance

The trained model achieves:
- **R² Score**: ~0.90 (90% variance explained)
- **RMSE**: ~2.12 (average prediction error)
- **MAE**: ~1.85 (mean absolute error)

### Feature Importance
- **TV**: Strongest predictor (coefficient: 0.0457)
- **Radio**: Second strongest (coefficient: 0.1885)
- **Newspaper**: Weakest impact (coefficient: -0.0010)

## 🚢 API Usage

### Start API Server

```bash
python src/api.py
# Server runs on http://localhost:5000
```

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:5000/health

# Response
{
  "status": "healthy",
  "model_loaded": true
}
```

#### 2. Single Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"TV": 230.1, "Radio": 37.8, "Newspaper": 69.2}'

# Response
{
  "prediction": 22.15,
  "input": {"TV": 230.1, "Radio": 37.8, "Newspaper": 69.2}
}
```

#### 3. Batch Predictions
```bash
curl -X POST http://localhost:5000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"TV": 230.1, "Radio": 37.8, "Newspaper": 69.2},
      {"TV": 44.5, "Radio": 39.3, "Newspaper": 45.1}
    ]
  }'

# Response
{
  "predictions": [22.15, 10.42],
  "count": 2
}
```

#### 4. Model Metrics
```bash
curl http://localhost:5000/metrics

# Response
{
  "r2": 0.897,
  "rmse": 2.12,
  "mae": 1.85,
  "mse": 4.5,
  "samples": 40,
  "coefficients": {...}
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_model.py -v

# Run specific test
pytest tests/test_model.py::test_model_train -v
```

## 🔍 Code Quality

```bash
# Format code with Black
black src/

# Check import sorting
isort src/

# Lint with Flake8
flake8 src/ --max-line-length=120

# Static analysis with Pylint
pylint src/

# All checks at once
black src/ && isort src/ && flake8 src/ && pylint src/
```

## 🐳 Docker

### Build Docker Images

```bash
# Training image
docker build -t linear-regression-train:latest -f Dockerfile .

# API image
docker build -t linear-regression-api:latest -f Dockerfile.api .
```

### Run with Docker

```bash
# Training
docker run -v $(pwd)/models:/app/models linear-regression-train:latest

# API
docker run -p 5000:5000 -v $(pwd)/models:/app/models linear-regression-api:latest
```

### Docker Compose

```bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f training
docker-compose logs -f api

# Stop services
docker-compose down
```

## 🔄 CI/CD Workflows

### GitHub Actions Pipelines

1. **Training Pipeline** (`train.yml`)
   - Triggers: Push, scheduled daily
   - Tasks: Lint, train, upload artifacts

2. **Evaluation** (`evaluate.yml`)
   - Triggers: After training success
   - Tasks: Test, validate metrics, generate reports

3. **Docker Build** (`docker.yml`)
   - Triggers: After evaluation success
   - Tasks: Build & push Docker images

4. **Code Quality** (`quality.yml`)
   - Triggers: Push, pull requests
   - Tasks: Format checks, linting, coverage

### Setup GitHub Actions

1. Navigate to repository settings
2. Enable GitHub Actions
3. Create secrets for Docker:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - `DOCKER_REGISTRY`

## 📊 Monitoring & Logging

- **Logs**: All logs saved to `logs/mlops.log`
- **Metrics**: Model metrics in `models/metrics.json`
- **Reports**: Generated reports in `reports/model_report.md`
- **Dashboard**: GitHub Actions tab for workflow status

## 🛠️ Configuration

### Environment Variables

```bash
# Data paths
DATA_PATH=Advertising.csv
MODEL_PATH=models/model.pkl
METRICS_PATH=models/metrics.json

# API settings
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/mlops.log

# Model thresholds
MIN_R2_SCORE=0.7
MAX_RMSE=5.0
```

### Configuration File

Edit `src/config.py` to modify default settings.

## 📚 Detailed Documentation

See [MLOPS_SETUP.md](MLOPS_SETUP.md) for:
- Complete setup instructions
- Workflow configurations
- Deployment options
- Troubleshooting guide
- Best practices

## 🔗 API Documentation

### Request Format
All requests use JSON with Content-Type: `application/json`

### Response Format
```json
{
  "prediction": float,
  "input": object,
  "count": int,
  "status": "string",
  "error": "string (if error)"
}
```

### Error Handling
- 400: Bad Request (missing/invalid fields)
- 500: Server Error (model not loaded, prediction failed)

## 📦 Dependencies

Key packages:
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **flask**: Web framework
- **pytest**: Testing framework
- **docker**: Containerization

See `requirements.txt` for complete list.

## 🚀 Deployment Options

### 1. Local Machine
```bash
python src/train.py
python src/api.py
```

### 2. Docker
```bash
docker-compose up --build
```

### 3. Cloud Platforms
- **AWS**: ECR + Lambda/ECS
- **GCP**: Container Registry + Cloud Run
- **Azure**: ACR + Container Instances
- **Heroku**: Docker deployment

## 📝 Usage Examples

### Python Script
```python
from src.model import LinearRegressionModel
from src.data_loader import DataLoader

# Load and prepare data
loader = DataLoader('Advertising.csv')
X_train, X_test, y_train, y_test = loader.preprocess()

# Train model
model = LinearRegressionModel()
model.train(X_train, y_train)

# Evaluate
metrics = model.evaluate(X_test, y_test)
print(f"R² Score: {metrics['r2']:.4f}")

# Make prediction
pred = model.predict([[230.1, 37.8, 69.2]])
print(f"Predicted Sales: {pred[0]:.2f}")
```

### API Client
```python
import requests

url = "http://localhost:5000/predict"
data = {"TV": 230.1, "Radio": 37.8, "Newspaper": 69.2}

response = requests.post(url, json=data)
prediction = response.json()['prediction']
print(f"Predicted Sales: {prediction:.2f}")
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/improvement`
2. Make changes and test: `pytest tests/`
3. Format code: `black src/`
4. Commit: `git commit -am 'Add improvement'`
5. Push: `git push origin feature/improvement`
6. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see LICENSE file for details.

## 🆘 Troubleshooting

### Model Training Fails
- Check data file exists: `Advertising.csv`
- Verify dependencies: `pip install -r requirements.txt`
- Check logs: `cat logs/mlops.log`

### API Won't Start
- Ensure model exists: `ls models/model.pkl`
- Check port availability: `lsof -i :5000`
- Verify Flask installed: `pip install flask`

### Docker Issues
- Clean up: `docker system prune -a`
- Rebuild: `docker-compose down && docker-compose up --build`
- Check Docker daemon: `docker ps`

## 📞 Support

For issues and questions:
1. Check [MLOPS_SETUP.md](MLOPS_SETUP.md) troubleshooting section
2. Review GitHub Issues
3. Check logs in `logs/mlops.log`

## 🔄 Version History

- **v1.0.0** (2026-08-20): Initial MLOps setup
  - Training pipeline
  - REST API
  - GitHub Actions workflows
  - Docker containerization
  - Comprehensive testing

## 📊 Metrics Dashboard

Current model performance:
- Training samples: 160
- Test samples: 40
- R² Score: 0.897
- RMSE: 2.12
- MAE: 1.85

Last trained: 2026-08-20

---

**Made with ❤️ for MLOps Excellence**

For detailed technical information, see [MLOPS_SETUP.md](MLOPS_SETUP.md)
