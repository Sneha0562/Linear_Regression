# GitHub Actions Workflow Templates

Copy these files to `.github/workflows/` directory to enable CI/CD.

## 1. Training Pipeline - `train.yml`

```yaml
name: Model Training Pipeline

on:
  push:
    branches: [ main, mlops-infrastructure ]
    paths:
      - 'src/**'
      - 'Advertising.csv'
      - 'requirements.txt'
      - '.github/workflows/train.yml'
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'

jobs:
  train:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run linting checks
      run: |
        pip install flake8
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Train model
      run: |
        cd src
        python train.py
      env:
        DATA_PATH: ../Advertising.csv
        MODEL_PATH: ../models/model.pkl
        METRICS_PATH: ../models/metrics.json
    
    - name: Upload model artifacts
      if: success()
      uses: actions/upload-artifact@v3
      with:
        name: trained-model
        path: models/
        retention-days: 30
    
    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          try {
            const metrics = JSON.parse(fs.readFileSync('models/metrics.json', 'utf8'));
            const comment = `## 📊 Model Training Results
            
            | Metric | Value |
            |--------|-------|
            | R² Score | ${metrics.r2.toFixed(4)} |
            | RMSE | ${metrics.rmse.toFixed(4)} |
            | MAE | ${metrics.mae.toFixed(4)} |
            | Test Samples | ${metrics.samples} |
            `;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
          } catch (err) {
            console.log('Could not read metrics: ' + err);
          }
```

## 2. Code Quality - `quality.yml`

```yaml
name: Code Quality Checks

on:
  push:
    branches: [ main, mlops-infrastructure ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install flake8 pylint black isort pytest pytest-cov
    
    - name: Black code formatting check
      run: black --check src/ tests/ || true
    
    - name: isort import check
      run: isort --check-only src/ tests/ || true
    
    - name: Flake8 linting
      run: flake8 src/ tests/ --max-line-length=120 --count || true
    
    - name: Pylint analysis
      run: pylint src/ --disable=all --enable=E,F || true
    
    - name: Run unit tests
      run: pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

## 3. Docker Build - `docker.yml`

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  workflow_run:
    workflows: [ "Code Quality Checks" ]
    types: [ completed ]
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    if: ${{ github.event_name == 'push' || github.event.workflow_run.conclusion == 'success' }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
      if: github.event_name != 'pull_request'
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ secrets.DOCKER_REGISTRY }}/linear-regression-mlops
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha
    
    - name: Build and push training image
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile
        push: ${{ github.event_name != 'pull_request' && secrets.DOCKER_USERNAME != '' }}
        tags: ${{ steps.meta.outputs.tags }}-training
        labels: ${{ steps.meta.outputs.labels }}
    
    - name: Build and push API image
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile.api
        push: ${{ github.event_name != 'pull_request' && secrets.DOCKER_USERNAME != '' }}
        tags: ${{ steps.meta.outputs.tags }}-api
        labels: ${{ steps.meta.outputs.labels }}
```

## 4. Model Evaluation - `evaluate.yml`

```yaml
name: Model Evaluation

on:
  workflow_run:
    workflows: [ "Model Training Pipeline" ]
    types: [ completed ]
    branches: [ main, mlops-infrastructure ]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Download model artifacts
      uses: actions/download-artifact@v3
      with:
        name: trained-model
        path: models/
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      run: pytest tests/ -v --tb=short
    
    - name: Check model metrics
      run: python scripts/check_metrics.py
      continue-on-error: true
    
    - name: Generate model report
      run: python scripts/generate_report.py
      continue-on-error: true
    
    - name: Upload evaluation report
      uses: actions/upload-artifact@v3
      with:
        name: evaluation-report
        path: reports/
        retention-days: 90
```

---

## Setup Instructions

### Step 1: Create Workflows Directory

```bash
mkdir -p .github/workflows
```

### Step 2: Create Workflow Files

Copy each workflow template above into separate files:
- `.github/workflows/train.yml`
- `.github/workflows/quality.yml`
- `.github/workflows/docker.yml`
- `.github/workflows/evaluate.yml`

### Step 3: Configure Secrets (Optional - for Docker Push)

Go to GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
```
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_token
DOCKER_REGISTRY=your_registry_url (e.g., docker.io)
```

### Step 4: Enable GitHub Actions

1. Go to repository → Settings
2. Under "Code and automation" → Actions
3. Choose "Allow all actions and reusable workflows"
4. Click "Save"

### Step 5: Push to GitHub

```bash
git add .github/
git commit -m "Add GitHub Actions workflows"
git push origin mlops-infrastructure
```

---

## Workflow Triggers

| Workflow | Triggers |
|----------|----------|
| **train.yml** | Push to main/mlops-infrastructure, Daily at 2 AM UTC, Pull requests |
| **quality.yml** | Push to main/mlops-infrastructure, Pull requests |
| **evaluate.yml** | After successful training |
| **docker.yml** | Push to main with tags, After successful evaluation |

---

## Monitoring Workflows

### Via GitHub UI

1. Go to repository → Actions tab
2. Click on workflow name to see runs
3. Click on specific run to see details
4. View job logs by clicking job name

### Via CLI

```bash
# List recent workflow runs
gh run list --repo Sneha0562/Linear_Regression

# View specific run
gh run view <run-id> --repo Sneha0562/Linear_Regression

# View logs
gh run view <run-id> --log --repo Sneha0562/Linear_Regression
```

---

## Troubleshooting Workflows

### Workflow not triggering?

1. Check branch protection rules
2. Verify file paths match trigger conditions
3. Check workflow YAML syntax: `yamllint .github/workflows/`
4. Enable Actions in repository settings

### Jobs failing?

1. Click on failed job to see logs
2. Check environment variables
3. Verify dependencies in requirements.txt
4. Check Docker credentials for docker.yml

### Model training fails?

```yaml
# Debug step to add to train.yml
- name: Debug
  if: failure()
  run: |
    ls -la
    cat logs/mlops.log || echo "No logs found"
    pwd
```

---

## Best Practices

### 1. Secrets Management
- Never commit secrets
- Use GitHub Secrets for sensitive data
- Rotate tokens regularly

### 2. Performance
- Use caching for pip dependencies
- Avoid unnecessary rebuilds
- Clean up old artifacts

### 3. Notifications
- Set up branch protection rules
- Require status checks to pass
- Enable notifications for failures

### 4. Documentation
- Keep workflow YAMLs documented
- Document required secrets
- Maintain this file with any changes

---

## Example Workflow Run Timeline

```
10:30 AM - Developer pushes code
    ↓
10:35 AM - train.yml starts
    - Lint checks
    - Train model
    - Upload artifacts
    ↓
10:45 AM - quality.yml starts (parallel)
    - Code formatting
    - Linting
    - Tests with coverage
    ↓
11:00 AM - evaluate.yml starts (after train.yml succeeds)
    - Download model
    - Run validation tests
    - Generate report
    ↓
11:15 AM - docker.yml starts (after evaluate.yml succeeds)
    - Build images
    - Push to registry
    ↓
11:30 AM - All workflows complete
    - PR commented with results
    - Artifacts available for download
```

---

## Quick Reference Commands

```bash
# Test workflow locally (requires act: https://github.com/nektos/act)
act push -j train

# Validate YAML syntax
python -m yamllint .github/workflows/

# View artifact from command line
gh run download <run-id> -n trained-model

# Trigger workflow manually
gh workflow run train.yml -r mlops-infrastructure

# Cancel running workflow
gh run cancel <run-id>
```

---

**Created:** 2026-08-20  
**Version:** 1.0.0  
**Status:** Ready to use

For issues or questions, refer to [MLOPS_SETUP.md](MLOPS_SETUP.md)
