#!/usr/bin/env python
"""
Launcher script for Streamlit UI
Run this script to start the web interface
"""
import subprocess
import sys
import os

def launch_ui():
    """Launch the Streamlit web UI"""
    app_path = os.path.join(os.path.dirname(__file__), 'ui/app.py')
    
    print("=" * 60)
    print("Starting Alumni Data Extractor - Web UI")
    print("=" * 60)
    print(f"\nLaunching Streamlit app: {app_path}")
    print("\nThe web interface will open in your default browser.")
    print("If it doesn't open automatically, visit: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Launch Streamlit with the app
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", app_path,
        "--logger.level=info",
        "--client.showErrorDetails=true"
    ])

if __name__ == "__main__":
    try:
        launch_ui()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
