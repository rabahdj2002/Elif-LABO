import subprocess
import os
import sys
from pathlib import Path

def launch():
    # Use the venv python to run streamlit
    # command: streamlit run elif_web_app.py
    
    app_file = Path("elif_web_app.py").absolute()
    
    if not app_file.exists():
        print(f"Error: {app_file} not found.")
        return

    # Add src to PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path("src").absolute())
    
    print("🚀 Launching ELIF V1 Dashboard...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_file)], env=env)

if __name__ == "__main__":
    launch()
