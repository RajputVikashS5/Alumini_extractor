#!/bin/bash
# Shell script to launch Streamlit UI on macOS/Linux

echo ""
echo "======================================================"
echo "   Alumni Data Extractor - Web UI Launcher"
echo "======================================================"
echo ""

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "[OK] Virtual environment activated"
    echo ""
else
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python -m venv venv"
    exit 1
fi

# Check if streamlit is installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] Streamlit not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Launch Streamlit
echo "Starting Streamlit application..."
echo "The web interface will open at: http://localhost:8501"
echo ""

python -m streamlit run ui/app.py --logger.level=info --client.showErrorDetails=true
