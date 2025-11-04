#!/bin/bash

echo "🚀 Setting up Synthetic Media Detection Tool..."

# Check if required tools are installed
check_requirements() {
    echo "📋 Checking requirements..."
    
    # Check Java
    if ! command -v java &> /dev/null; then
        echo "❌ Java not found. Please install Java 21."
        exit 1
    fi
    
    java_version=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
    if [ "$java_version" -lt 17 ]; then
        echo "❌ Java version must be 17 or higher. Found: $java_version"
        exit 1
    fi
    echo "✅ Java $java_version found"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 not found. Please install Python 3.10+"
        exit 1
    fi
    echo "✅ Python3 found"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker"
        exit 1
    fi
    echo "✅ Docker found"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose not found. Please install Docker Compose"
        exit 1
    fi
    echo "✅ Docker Compose found"
}

# Create directory structure
create_directories() {
    echo "📁 Creating directory structure..."
    mkdir -p models temp logs
    echo "✅ Directories created"
}

# Download pretrained models
download_models() {
    echo "🤖 Downloading pretrained models..."
    
    # Create Python virtual environment for downloading
    python3 -m venv venv
    source venv/bin/activate
    
    # Install required packages for downloading
    pip install huggingface-hub torch transformers
    
    # Download models
    python3 scripts/download_models.py
    
    deactivate
    echo "✅ Models downloaded"
}

# Build and start services
build_services() {
    echo "🔨 Building Docker services..."
    docker-compose build
    echo "✅ Services built"
    
    echo "🚀 Starting services..."
    docker-compose up -d
    echo "✅ Services started"
}

# Wait for services to be ready
wait_for_services() {
    echo "⏳ Waiting for services to be ready..."
    
    # Wait for ML service
    for i in {1..30}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            echo "✅ ML service is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ ML service failed to start"
            exit 1
        fi
        sleep 2
    done
    
    # Wait for backend service
    for i in {1..30}; do
        if curl -f http://localhost:8080/api/detect/health &> /dev/null; then
            echo "✅ Backend service is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ Backend service failed to start"
            exit 1
        fi
        sleep 2
    done
}

# Run tests
run_tests() {
    echo "🧪 Running tests..."
    python3 scripts/test_api.py
    echo "✅ Tests completed"
}

# Main setup process
main() {
    echo "🎯 Starting setup process..."
    
    check_requirements
    create_directories
    download_models
    build_services
    wait_for_services
    run_tests
    
    echo ""
    echo "🎉 Setup complete!"
    echo ""
    echo "📍 Services are running at:"
    echo "   • Web Interface: http://localhost:8080"
    echo "   • ML API: http://localhost:8000"
    echo "   • API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📝 To stop services: docker-compose down"
    echo "📝 To view logs: docker-compose logs -f"
    echo ""
}

# Run main function
main "$@"
