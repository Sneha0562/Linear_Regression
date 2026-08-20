# MLOps Infrastructure Setup Guide

## Overview
This guide provides complete MLOps setup for the Linear Regression project, making it production-ready with CI/CD pipelines, containerization, and automated testing.

## Project Structure
```
Linear_Regression/
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # Data loading & preprocessing
│   ├── model.py            # Model training & evaluation
│   ├── train.py            # Training pipeline
│   ├── predict.py          # Inference module
│   ├── api.py              # Flask API
│   ├── config.py           # Configuration management
│   └── monitoring.py       # Metrics tracking
├── tests/
│   ├── test_data_loader.py
│   └── test_model.py
├── scripts/
│   ├── check_metrics.py    # Validate metrics
│   └── generate_report.py  # Generate reports
├── models/                 # Trained models directory
├── logs/                   # Application logs
├── reports/                # Generated reports
├── .github/
│   └── workflows/          # CI/CD pipelines
├── Dockerfile              # Training container
├── Dockerfile.api          # API container
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git
- GitHub account (for Actions)

### 2. Local Development Setup

```bash
# Clone the repository
git clone https://github.com/Sneha0562/Linear_Regression.git
cd Linear_Regression

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov black flake8 pylint
```

### 3. Running the Training Pipeline Locally

```bash
# Navigate to src directory
cd src

# Run training
python train.py

# View metrics
cat ../models/metrics.json
```

### 4. Docker Setup

#### Option A: Docker Compose (Recommended)

```bash
# Build and run all services
docker-compose up --build

# View training logs
docker-compose logs training

# Run API only
docker-compose run api python src/api.py
```

#### Option B: Manual Docker

```bash
# Build training image
docker build -t linear-regression-train:latest -f Dockerfile .

# Run training
docker run -v $(pwd)/models:/app/models linear-regression-train:latest

# Build API image
docker build -t linear-regression-api:latest -f Dockerfile.api .

# Run API
docker run -p 5000:5000 -v $(pwd)/models:/app/models linear-regression-api:latest
```

### 5. Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_model.py -v
```

### 6. Code Quality Checks

```bash
# Format code with Black
black src/

# Check import sorting
isort src/

# Lint with Flake8
flake8 src/ --max-line-length=120

# Static analysis with Pylint
pylint src/
```

## GitHub Actions Workflows

### 1. Training Pipeline Workflow
**File:** `.github/workflows/train.yml`

Triggers on:
- Push to `main` or `mlops-infrastructure` branch
- Changes in `src/`, `Advertising.csv`, or `requirements.txt`
- Daily schedule (2 AM UTC)

Actions:
- Install dependencies
- Run linting
- Train model
- Upload artifacts
- Comment on PR with results

### 2. Model Evaluation Workflow
**File:** `.github/workflows/evaluate.yml`

Triggers after successful training

Actions:
- Download trained model
- Run unit tests
- Validate metrics against thresholds
- Generate evaluation report

### 3. Docker Build & Push Workflow
**File:** `.github/workflows/docker.yml`

Triggers after successful evaluation

Actions:
- Build Docker images
- Push to registry
- Tag with version/branch

### 4. Code Quality Workflow
**File:** `.github/workflows/quality.yml`

Triggers on push and pull requests

Actions:
- Format checking (Black, isort)
- Linting (Flake8)
- Code analysis (Pylint)
- Unit tests with coverage
- Upload to Codecov

## API Usage

### Start the API

```bash
python src/api.py
```

### Endpoints

#### Health Check
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### Single Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "TV": 230.1,
    "Radio": 37.8,
    "Newspaper": 69.2
  }'
```

Response:
```json
{
  "prediction": 22.15,
  "input": {
    "TV": 230.1,
    "Radio": 37.8,
    "Newspaper": 69.2
  }
}
```

#### Batch Predictions
```bash
curl -X POST http://localhost:5000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"TV": 230.1, "Radio": 37.8, "Newspaper": 69.2},
      {"TV": 44.5, "Radio": 39.3, "Newspaper": 45.1}
    ]
  }'
```

#### Get Metrics
```bash
curl http://localhost:5000/metrics
```

## Environment Variables

```bash
# Data and model paths
DATA_PATH=Advertising.csv
MODEL_PATH=models/model.pkl
METRICS_PATH=models/metrics.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/mlops.log

# Model Thresholds
MIN_R2_SCORE=0.7
MAX_RMSE=5.0
```

## Creating GitHub Actions Workflows

Create these files in `.github/workflows/`:

### 1. train.yml
See the workflow YAML content provided in the push_files call above.

### 2. evaluate.yml
Runs after training to validate model performance.

### 3. docker.yml
Builds and pushes Docker images on successful evaluation.

### 4. quality.yml
Runs code quality checks on every push/PR.

## Model Metrics

The training pipeline produces:
- **R² Score**: Proportion of variance explained (0-1, higher is better)
- **RMSE**: Root Mean Squared Error (lower is better)
- **MAE**: Mean Absolute Error (lower is better)
- **Coefficients**: Feature importance values

Example metrics.json:
```json
{
  "mse": 4.5,
  "rmse": 2.12,
  "mae": 1.85,
  "r2": 0.897,
  "samples": 40,
  "coefficients": {
    "TV": 0.0457,
    "Radio": 0.1885,
    "Newspaper": -0.0010,
    "intercept": 2.9389
  }
}
```

## Deployment Options

### Option 1: Docker Hub
1. Set GitHub Secrets:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - `DOCKER_REGISTRY`

2. Push workflow will automatically build and push images

### Option 2: Kubernetes
Deploy using the provided docker-compose configuration as basis

### Option 3: Cloud Platforms
- AWS: Use ECR + Lambda/ECS
- GCP: Use Container Registry + Cloud Run
- Azure: Use ACR + Container Instances

## Monitoring & Logging

- All logs saved to `logs/mlops.log`
- Metrics tracked in `models/metrics.json`
- Reports generated in `reports/model_report.md`
- GitHub Actions logs available in Actions tab

## Best Practices

1. **Versioning**: Tag releases in git for model versions
2. **Data**: Keep Advertising.csv in version control
3. **Models**: Store trained models in artifacts/releases
4. **Testing**: Always run tests before deployment
5. **Monitoring**: Check metrics thresholds regularly
6. **Documentation**: Keep MLOPS_SETUP.md updated

## Troubleshooting

### Model training fails
- Check data file exists at specified path
- Verify Python dependencies installed: `pip install -r requirements.txt`
- Check logs: `cat logs/mlops.log`

### API won't start
- Ensure model file exists at MODEL_PATH
- Check port 5000 is available
- Verify Flask installed: `pip install flask`

### Docker build fails
- Ensure Dockerfile and requirements.txt exist
- Check Docker is running: `docker ps`
- Clean and rebuild: `docker-compose down && docker-compose up --build`

### GitHub Actions won't run
- Verify branch protection rules allow Actions
- Check workflow YAML syntax
- Ensure secrets are configured for Docker push

## Next Steps

1. Push code to GitHub
2. Create GitHub Secrets for Docker
3. Create `.github/workflows/` files
4. Enable GitHub Actions in repository settings
5. Monitor first pipeline run
6. Integrate with deployment platform

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Last Updated:** 2026-08-20
**Author:** MLOps Infrastructure Setup
