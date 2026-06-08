@echo off
chcp 65001 >nul 2>&1

:: Ir siempre al directorio donde está este .bat, sin importar desde dónde se ejecute
cd /d "%~dp0"

cls
echo.
echo  ============================================================
echo   💧  AquaQuantum — HACKATHON LATAM 2026
echo       Puebla de Zaragoza, Mexico
echo  ============================================================
echo.
echo  Directorio: %CD%
echo.

:: ── Verificar Python ────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python no encontrado en el PATH.
    echo  Descargalo en: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
python --version

:: ── Verificar/instalar dependencias directamente ─────────────
echo.
echo  Instalando/verificando dependencias...
echo  (esto puede tardar 1-2 minutos la primera vez)
echo.
pip install -r requirements.txt --quiet --disable-pip-version-check

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Fallo al instalar dependencias. Intentando sin --quiet...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo  [ERROR] No se pudieron instalar las dependencias.
        pause
        exit /b 1
    )
)

echo.
echo  ============================================================
echo   Dashboard listo. Abriendo navegador...
echo   URL: http://localhost:8501
echo   Para detener: presiona Ctrl+C en esta ventana
echo  ============================================================
echo.

:: Abrir navegador después de 4 segundos
start "" cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:8501"

:: ── Lanzar Streamlit ─────────────────────────────────────────
python -m streamlit run aquaquantum\dashboard\app.py --server.port=8501 --browser.gatherUsageStats=false

echo.
echo  El dashboard se ha detenido.
echo.
pause
