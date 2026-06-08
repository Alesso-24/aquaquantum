"""
API REST de AquaQuantum — FastAPI
HACKATHON LATAM 2026 · Puebla, México
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from aquaquantum.core import (
    optimizar_red_hidrica,
    detectar_fugas_cuantico,
    predecir_demanda_cuantica,
    analizar_calidad_cuantica,
)
from aquaquantum.simulation import generar_red_puebla, generar_datos_sensores, generar_features_hora

app = FastAPI(
    title="AquaQuantum API",
    description="API de Computación Cuántica para Gestión Hídrica Urbana — HACKATHON LATAM 2026",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# --- Modelos de entrada ---

class SensoresInput(BaseModel):
    lecturas: List[float] = Field(..., description="Lecturas de presión [0–1] por sensor", min_items=2, max_items=12)
    umbral:   float       = Field(0.35, description="Umbral de anomalía para declarar fuga")

class CalidadInput(BaseModel):
    ph:             float = Field(7.0, ge=0, le=14)
    turbidez_ntu:   float = Field(2.0, ge=0)
    cloro_mg_l:     float = Field(0.8, ge=0)
    coliformes_nmp: float = Field(0.0, ge=0)

class DemandaInput(BaseModel):
    hora:          int   = Field(12, ge=0, le=23)
    temperatura_c: float = Field(22.0)
    lluvia_mm:     float = Field(0.0, ge=0)
    dia_semana:    int   = Field(3, ge=0, le=6)

class SimulacionInput(BaseModel):
    estado: str = Field("normal", description="'normal', 'fuga_leve', 'fuga_critica', 'contaminacion'")


# --- Endpoints ---

@app.get("/", tags=["General"])
async def raiz():
    return {"mensaje": "AquaQuantum API activa. Visita /docs para explorar los endpoints."}


@app.get("/red/puebla", tags=["Red Hídrica"])
async def obtener_red_puebla():
    """Retorna el modelo completo de la red hídrica de Puebla."""
    red = generar_red_puebla()
    red.pop('nodos')      # Simplificar respuesta
    red.pop('conexiones')
    return red


@app.post("/analizar/fugas", tags=["Detección de Fugas"])
async def analizar_fugas(data: SensoresInput):
    """Detecta fugas usando interferencia cuántica sobre lecturas de presión."""
    try:
        return detectar_fugas_cuantico(data.lecturas, data.umbral)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analizar/calidad", tags=["Calidad del Agua"])
async def analizar_calidad(data: CalidadInput):
    """Analiza la calidad del agua con un circuito cuántico de 4 qubits."""
    try:
        return analizar_calidad_cuantica(data.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analizar/demanda", tags=["Predicción de Demanda"])
async def analizar_demanda(data: DemandaInput):
    """Predice la demanda hídrica usando un VQC de 5 qubits."""
    try:
        features = data.dict()
        features['densidad_pob'] = 0.6
        return predecir_demanda_cuantica(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simular/fugas", tags=["Simulación"])
async def simular_fugas(data: SimulacionInput):
    """Simula sensores con el estado dado y ejecuta detección cuántica de fugas."""
    try:
        lecturas = generar_datos_sensores(n_sensores=6, estado=data.estado)
        resultado = detectar_fugas_cuantico(lecturas)
        resultado['estado_simulado'] = data.estado
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", tags=["General"])
async def health():
    return {"status": "ok", "version": "1.0.0", "hackathon": "LATAM 2026 Puebla"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
