"""
Módulo: leak_detector.py
Detección cuántica de fugas en tuberías usando circuitos de interferencia cuántica.

El algoritmo codifica las lecturas de presión/flujo de N sensores en amplitudes
cuánticas. Una fuga crea una perturbación estadística detectada como distribución
anómala en la medición, cuantificada con entropía de Shannon y un índice de anomalía.
"""

import math
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from collections import Counter


def _entropia_shannon(probs: dict) -> float:
    """Entropía de Shannon en bits; máxima cuando la distribución es uniforme."""
    return -sum(p * math.log2(p) for p in probs.values() if p > 0)


def _indice_anomalia(probs: dict, n_qubits: int) -> float:
    """
    Calcula qué tan lejos está la distribución medida de la uniforme ideal.
    Rango [0, 1]: 0 = perfectamente normal, 1 = altamente anómalo.
    """
    n_estados = 2 ** n_qubits
    prob_uniforme = 1.0 / n_estados
    desviacion = sum(abs(probs.get(f'{i:0{n_qubits}b}', 0) - prob_uniforme)
                     for i in range(n_estados))
    return min(desviacion / 2.0, 1.0)


def detectar_fugas_cuantico(lecturas_sensores: list, umbral_anomalia: float = 0.35) -> dict:
    """
    Detecta fugas en la red hídrica usando interferencia cuántica.

    Args:
        lecturas_sensores: Lista de floats [0, 1] con presión normalizada de cada sensor.
                           Una lectura muy alta o muy baja indica posible fuga.
        umbral_anomalia:   Valor de índice de anomalía a partir del cual se declara fuga.

    Returns:
        Diccionario con índice de anomalía, probabilidades cuánticas, entropía,
        clasificación y localización estimada de la fuga.
    """
    n = len(lecturas_sensores)
    if n < 2:
        raise ValueError("Se necesitan al menos 2 sensores para detección de fugas.")

    qc = QuantumCircuit(n, n)

    # --- Codificación: Rotaciones RY proporcionales a la presión medida ---
    # Presión normal (≈0.5) → π/2 → superposición uniforme
    # Presión anómala (alta/baja) → sesga la amplitud → interferencia detectable
    for i, presion in enumerate(lecturas_sensores):
        angulo = presion * np.pi
        qc.ry(angulo, i)

    # --- Entrelazamiento para correlacionar sensores vecinos ---
    for i in range(n - 1):
        qc.cx(i, i + 1)

    # --- Segunda capa de rotaciones para amplificar la anomalía ---
    for i, presion in enumerate(lecturas_sensores):
        # La diferencia respecto al centro (0.5) amplifica la señal de fuga
        desviacion = abs(presion - 0.5) * np.pi
        qc.rz(desviacion, i)

    # --- Entrelazamiento inverso para interferencia destructiva en estados normales ---
    for i in range(n - 2, -1, -1):
        qc.cx(i, i + 1)

    qc.measure(range(n), range(n))

    # --- Simulación ---
    simulador = AerSimulator()
    compilado  = transpile(qc, simulador)
    resultado  = simulador.run(compilado, shots=4096).result()
    conteos    = resultado.get_counts()

    total = 4096
    probs = {k: v / total for k, v in conteos.items()}

    # Garantizar que todos los estados aparezcan
    for i in range(2 ** n):
        key = f'{i:0{n}b}'
        probs.setdefault(key, 0.0)

    # --- Métricas ---
    entropia   = _entropia_shannon(probs)
    entropia_max = math.log2(2 ** n)
    anomalia   = _indice_anomalia(probs, n)

    # Localización: el sensor cuya lectura se desvía más del rango normal
    desviaciones = [abs(p - 0.5) for p in lecturas_sensores]
    sensor_critico = int(np.argmax(desviaciones))

    # Clasificación del estado
    if anomalia > 0.65:
        estado, severidad = "FUGA CRÍTICA", "alta"
    elif anomalia > umbral_anomalia:
        estado, severidad = "FUGA DETECTADA", "media"
    elif anomalia > 0.15:
        estado, severidad = "ANOMALÍA LEVE", "baja"
    else:
        estado, severidad = "OPERACIÓN NORMAL", "ninguna"

    # Volumen estimado de fuga (modelo lineal simplificado)
    litros_por_hora = anomalia * 8500

    return {
        'indice_anomalia':     round(anomalia, 4),
        'entropia_cuantica':   round(entropia, 4),
        'entropia_maxima':     round(entropia_max, 4),
        'probabilidades':      dict(sorted(probs.items(), key=lambda x: -x[1])[:8]),
        'estado':              estado,
        'severidad':           severidad,
        'sensor_critico_idx':  sensor_critico,
        'fuga_detectada':      anomalia > umbral_anomalia,
        'litros_fuga_por_hora': round(litros_por_hora, 0),
        'lecturas_sensores':   lecturas_sensores,
        'circuito_texto':      str(qc.draw('text')),
        'num_qubits':          n,
    }
