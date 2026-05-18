from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .core_cuantico import analizar_anomalia_cuantica
from .sensores import leer_vibracion_motor # Para simular si es necesario

app = FastAPI(
    title="API de Mantenimiento Predictivo Cuántico",
    description="API REST para analizar anomalías en maquinaria usando computación cuántica.",
    version="1.0.0",
)

class SensorData(BaseModel):
    datos_sensores: List[float] # Esperamos una lista de 4 flotantes

class SimulationRequest(BaseModel):
    estado_motor: str = "normal" # "normal" o "anomalo"

@app.get("/", summary="Estado de la API", tags=["General"])
async def read_root():
    return {"message": "API de Mantenimiento Predictivo Cuántico funcionando. Visita /docs para la documentación."}

@app.post("/analyze_quantum", response_model=dict, summary="Analizar anomalía con circuito cuántico", tags=["Análisis Cuántico"])
async def analyze_quantum_data(data: SensorData):
    """
    Recibe una lista de 4 valores de sensores y ejecuta el análisis cuántico.
    Devuelve el índice de riesgo, la entropía de anomalía, el dibujo del circuito
    y la distribución de probabilidades.
    """
    if len(data.datos_sensores) != 4:
        raise HTTPException(status_code=400, detail="Se requieren exactamente 4 valores de sensores.")
    
    try:
        riesgo, entropia_anomalia, dibujo_circuito, probabilidades = analizar_anomalia_cuantica(data.datos_sensores)
        return {
            "riesgo": riesgo,
            "entropia_anomalia": entropia_anomalia,
            "dibujo_circuito": dibujo_circuito,
            "probabilidades": probabilidades
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis cuántico: {str(e)}")

@app.post("/simulate_and_analyze", response_model=dict, summary="Simular datos y analizar anomalía", tags=["Análisis Cuántico"])
async def simulate_and_analyze(request: SimulationRequest):
    """
    Simula lecturas de sensores basadas en un estado de motor ("normal" o "anomalo")
    y luego ejecuta el análisis cuántico sobre esos datos.
    """
    estado = request.estado_motor.lower()
    if estado not in ["normal", "anomalo"]:
        raise HTTPException(status_code=400, detail="El estado del motor debe ser 'normal' o 'anomalo'.")
    
    datos_simulados = leer_vibracion_motor(estado)
    
    try:
        riesgo, entropia_anomalia, dibujo_circuito, probabilidades = analizar_anomalia_cuantica(datos_simulados)
        return {
            "datos_sensores_simulados": datos_simulados,
            "riesgo": riesgo,
            "entropia_anomalia": entropia_anomalia,
            "dibujo_circuito": dibujo_circuito,
            "probabilidades": probabilidades
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis cuántico: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
