# Punto de entrada para Streamlit Community Cloud.
# Streamlit Cloud ejecuta este archivo desde la raíz del repositorio.
# Pasamos __file__ correcto al contexto para que las rutas relativas de app.py funcionen.

import sys, os

ROOT     = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.join(ROOT, "aquaquantum", "dashboard", "app.py")

sys.path.insert(0, ROOT)

with open(APP_PATH, encoding="utf-8") as f:
    exec(compile(f.read(), APP_PATH, "exec"), {"__file__": APP_PATH, "__name__": "__main__"})
