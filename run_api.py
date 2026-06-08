"""
Lanzador de la API FastAPI AquaQuantum
Ejecutar: python run_api.py
"""
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "uvicorn",
                    "aquaquantum.api.main:app",
                    "--reload", "--host", "0.0.0.0", "--port", "8000"], check=True)
