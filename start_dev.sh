#!/bin/bash

# LearnPilot Development Environment Setup and Startup Script
# Using uv for package management

set -e

echo "🚀 Starting LearnPilot Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv is not installed. Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
fi

# Check uv version
echo -e "${BLUE}📦 Using uv version: $(uv --version)${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📁 Creating virtual environment with uv...${NC}"
    uv venv --python 3.10
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies with uv
echo -e "${YELLOW}📥 Installing dependencies with uv...${NC}"
uv pip install -e ".[dev,docs,test]"

# Set environment variables
export PYTHONPATH=.:$PYTHONPATH

# Create necessary directories
echo -e "${YELLOW}📂 Creating necessary directories...${NC}"
mkdir -p user_data/papers
mkdir -p user_data/outputs
mkdir -p logs
mkdir -p uploads
mkdir -p src/learn_pilot/web/static

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Creating .env template file...${NC}"
    cat > .env << EOF
# LearnPilot Configuration
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///learnpilot.db

# Authentication
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=43200

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/learnpilot.log

# AI Configuration
DEFAULT_MODEL=gpt-4o-mini
MAX_TOKENS=4000
TEMPERATURE=0.7

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=pdf,md,txt
EOF
    echo -e "${RED}🔑 Please edit .env file and add your API keys!${NC}"
fi

# Initialize database
echo -e "${YELLOW}🗄️  Initializing database...${NC}"
python -c "
from src.learn_pilot.database import init_database
init_database()
print('✅ Database initialized successfully!')
"

# Run pre-commit install if available
if command -v pre-commit &> /dev/null; then
    echo -e "${YELLOW}🔧 Installing pre-commit hooks...${NC}"
    pre-commit install
fi

# Check if dependencies are working
echo -e "${YELLOW}🧪 Testing core dependencies...${NC}"
python -c "
try:
    import fastapi
    import sqlalchemy
    import openai
    print('✅ Core dependencies loaded successfully!')
except ImportError as e:
    print(f'❌ Dependency error: {e}')
    exit(1)
"

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Check if port 8000 is available
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. Finding alternative port...${NC}"
    PORT=8001
    while check_port $PORT; do
        PORT=$((PORT + 1))
    done
    echo -e "${BLUE}🌐 Using port $PORT instead${NC}"
else
    PORT=8000
fi

echo -e "${GREEN}✅ Development environment ready!${NC}"
echo -e "${BLUE}🌐 Starting web server on http://localhost:$PORT${NC}"
echo -e "${BLUE}📖 API documentation will be available at http://localhost:$PORT/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Set Python path and start the development server
export PYTHONPATH="/home/bin.liang/Documents/03-open-source/LearnPilot/src:$PYTHONPATH"
cd /home/bin.liang/Documents/03-open-source/LearnPilot
uvicorn src.learn_pilot.web.main:app --host 0.0.0.0 --port $PORT --reload --reload-dir src --log-level info