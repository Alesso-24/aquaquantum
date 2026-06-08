"""
Lanzador del Dashboard AquaQuantum
Ejecutar: python run_dashboard.py
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    dashboard_path = os.path.join(os.path.dirname(__file__), "aquaquantum", "dashboard", "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path,
                    "--server.port=8501", "--server.headless=false"], check=True)
