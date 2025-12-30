# ============================================
# SENTINEL Project - Environment Setup Script
# PowerShell script for Windows
# ============================================

Write-Host "🛡️ SENTINEL Project - Environment Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python version
Write-Host "📌 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green

# Check if Python version is 3.11+
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
        Write-Host "❌ Python 3.11+ required. Current: $pythonVersion" -ForegroundColor Red
        exit 1
    }
}

# Check Docker
Write-Host "`n📌 Checking Docker..." -ForegroundColor Yellow
docker --version 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Docker not found. MLOps stack will not be available." -ForegroundColor Yellow
    $installDocker = Read-Host "Install Docker Desktop? (y/n)"
    if ($installDocker -eq "y") {
        Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
        exit 0
    }
} else {
    Write-Host "✅ Docker is installed" -ForegroundColor Green
}

# Create virtual environment
Write-Host "`n📌 Creating Python virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️ Virtual environment already exists. Recreating..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Activate virtual environment
Write-Host "`n📌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host "`n📌 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to upgrade pip" -ForegroundColor Red
    exit 1
}
Write-Host "✅ pip upgraded" -ForegroundColor Green

# Install PyTorch (CUDA-enabled for RTX 3060)
Write-Host "`n📌 Installing PyTorch with CUDA support..." -ForegroundColor Yellow
Write-Host "   (This may take a few minutes...)" -ForegroundColor Gray
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ CUDA installation failed. Installing CPU version..." -ForegroundColor Yellow
    pip install torch torchvision torchaudio
}
Write-Host "✅ PyTorch installed" -ForegroundColor Green

# Install quantitative research requirements
Write-Host "`n📌 Installing quantitative research libraries..." -ForegroundColor Yellow
Write-Host "   (This will take 5-10 minutes...)" -ForegroundColor Gray
pip install -r requirements-quant.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install requirements" -ForegroundColor Red
    exit 1
}
Write-Host "✅ All Python packages installed" -ForegroundColor Green

# Install Ollama
Write-Host "`n📌 Checking Ollama..." -ForegroundColor Yellow
ollama --version 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Ollama not found." -ForegroundColor Yellow
    $installOllama = Read-Host "Install Ollama? (y/n)"
    if ($installOllama -eq "y") {
        Write-Host "Downloading Ollama..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri "https://ollama.ai/download/OllamaSetup.exe" -OutFile "OllamaSetup.exe"
        Write-Host "Please run OllamaSetup.exe to install Ollama" -ForegroundColor Cyan
        Start-Process "OllamaSetup.exe"
    }
} else {
    Write-Host "✅ Ollama is installed" -ForegroundColor Green
    
    # Pull Llama 3.1 model
    Write-Host "`n📌 Pulling Llama 3.1 8B model..." -ForegroundColor Yellow
    Write-Host "   (This will download ~4.7GB, may take 10-15 minutes...)" -ForegroundColor Gray
    ollama pull llama3.1:8b-instruct-q4_K_M
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Llama 3.1 model downloaded" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Failed to download model. You can do this later with: ollama pull llama3.1:8b-instruct-q4_K_M" -ForegroundColor Yellow
    }
}

# Create directory structure
Write-Host "`n📌 Creating project directory structure..." -ForegroundColor Yellow
$directories = @(
    "data/raw",
    "data/processed",
    "data/features",
    "research/notebooks",
    "research/experiments",
    "research/results",
    "backend/services",
    "backend/models",
    "backend/routers",
    "backend/tests",
    "monitoring/grafana/dashboards",
    "monitoring/grafana/datasources",
    "mlruns",
    "mlartifacts"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✅ Directory structure created" -ForegroundColor Green

# Create .env file
Write-Host "`n📌 Creating .env configuration..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    @"
# SENTINEL Project Environment Variables

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=sentinel-experiments

# Database Configuration
DATABASE_URL=postgresql://sentinel:sentinel123@localhost:5432/sentinel

# Redis Configuration
REDIS_URL=redis://:redis123@localhost:6379/0

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_TOKEN=sentinel-token-123

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b-instruct-q4_K_M

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
API_WORKERS=4

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ .env file created" -ForegroundColor Green
} else {
    Write-Host "⚠️ .env file already exists. Skipping..." -ForegroundColor Yellow
}

# Create init-db.sql script
Write-Host "`n📌 Creating database initialization script..." -ForegroundColor Yellow
if (!(Test-Path "scripts")) {
    New-Item -ItemType Directory -Path "scripts" -Force | Out-Null
}

@"
-- Create MLflow database
CREATE DATABASE mlflow;

-- Create user for MLflow
CREATE USER mlflow WITH PASSWORD 'mlflow123';
GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;

-- Grant permissions
\c mlflow
GRANT ALL ON SCHEMA public TO mlflow;
"@ | Out-File -FilePath "scripts/init-db.sql" -Encoding UTF8
Write-Host "✅ Database script created" -ForegroundColor Green

# Start Docker containers
Write-Host "`n📌 Starting MLOps infrastructure..." -ForegroundColor Yellow
docker --version 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    $startDocker = Read-Host "Start Docker containers now? (y/n)"
    if ($startDocker -eq "y") {
        Write-Host "Starting containers..." -ForegroundColor Cyan
        docker-compose -f docker-compose.mlops.yml up -d
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker containers started" -ForegroundColor Green
            Write-Host "`n📊 Access services at:" -ForegroundColor Cyan
            Write-Host "   - MLflow UI: http://localhost:5000" -ForegroundColor White
            Write-Host "   - Grafana: http://localhost:3001 (admin/admin123)" -ForegroundColor White
            Write-Host "   - Prometheus: http://localhost:9090" -ForegroundColor White
            Write-Host "   - Jupyter Lab: http://localhost:8888 (token: sentinel123)" -ForegroundColor White
            Write-Host "   - MinIO: http://localhost:9001 (minio/minio123)" -ForegroundColor White
        } else {
            Write-Host "⚠️ Failed to start containers" -ForegroundColor Yellow
        }
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Activate environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   2. Start Ollama: ollama serve" -ForegroundColor White
Write-Host "   3. Test installation: python -c 'import mlflow; print(mlflow.__version__)'" -ForegroundColor White
Write-Host "   4. Start development: jupyter lab" -ForegroundColor White
Write-Host "`n🎯 Happy researching!" -ForegroundColor Cyan
