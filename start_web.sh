#!/bin/bash

# LearnPilot Web Interface Startup Script

echo "🚀 Starting LearnPilot Web Interface..."

# Set environment variables
export PYTHONPATH=.:$PYTHONPATH

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p user_data/papers
mkdir -p user_data/outputs
mkdir -p src/learn_pilot/web/static

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please create one with your OPENAI_API_KEY"
    echo "Example: echo 'OPENAI_API_KEY=your_key_here' > .env"
fi

# Start the web server
echo "🌐 Starting web server on http://localhost:8000"
cd src/learn_pilot/web
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload