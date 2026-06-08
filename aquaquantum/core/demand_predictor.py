"""
Módulo: demand_predictor.py
Predicción cuántica de demanda hídrica usando Circuitos Cuánticos Variacionales (VQC).

Las características (hora, temperatura, día de semana, densidad poblacional) se
codifican como ángulos de rotación en un circuito ansatz. El circuito produce una
distribución cuya media ponderada representa la demanda predicha.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def _normalizar_features(features: dict) -> list:
    """Normaliza las características de entrada al rango [0, 1]."""
    hora         = features.get('hora', 12) / 23.0
    temperatura  = (features.get('temperatura_c', 22) - 5) / 40.0
    dia_semana   = features.get('dia_semana', 3) / 6.0   # 0=lunes … 6=domingo
    densidad     = min(features.get('densidad_pob', 0.5), 1.0)
    lluvia       = features.get('lluvia_mm', 0) / 50.0
    return [hora, temperatura, dia_semana, densidad, min(lluvia, 1.0)]


def predecir_demanda_cuantica(features: dict, demanda_base_m3h: float = 2500.0) -> dict:
    """
    Predice la demanda hídrica horaria usando un VQC de 5 qubits.

    Args:
        features:          Diccionario con hora, temperatura_c, dia_semana,
                           densidad_pob (0–1), lluvia_mm.
        demanda_base_m3h:  Demanda de referencia en m³/hora para escalar la predicción.

    Returns:
        Diccionario con demanda predicha, confianza, distribución cuántica y circuito.
    """
    x = _normalizar_features(features)
    n = len(x)  # 5 qubits

    qc = QuantumCircuit(n, n)

    # --- Capa 1: Codificación de características ---
    for i, xi in enumerate(x):
        qc.ry(xi * np.pi, i)  # Codificación en amplitud

    # --- Entrelazamiento: captura correlaciones entre features ---
    for i in range(n - 1):
        qc.cx(i, i + 1)
    qc.cx(n - 1, 0)  # Cierre del anillo

    # --- Capa 2: Rotaciones paramétricas (ansatz) ---
    # Parámetros fijos que codifican el "aprendizaje" del modelo
    thetas = [np.pi * (xi + 0.5) * 0.7 for xi in x]
    for i, theta in enumerate(thetas):
        qc.rz(theta, i)
        qc.ry(theta * 0.6, i)

    # --- Capa 3: Segundo entrelazamiento para profundidad ---
    for i in range(0, n - 1, 2):
        qc.cx(i, i + 1)

    # --- Rotaciones finales para mayor expresividad ---
    for i, xi in enumerate(x):
        qc.rx(xi * np.pi * 0.8, i)

    qc.measure(range(n), range(n))

    # --- Simulación ---
    simulador = AerSimulator()
    compilado  = transpile(qc, simulador)
    resultado  = simulador.run(compilado, shots=4096).result()
    conteos    = resultado.get_counts()

    total = 4096
    probs = {k: v / total for k, v in conteos.items()}

    # --- Decodificación: la predicción es la expectativa ponderada ---
    # Los estados con más 1s → mayor demanda
    expectativa = 0.0
    for estado, prob in probs.items():
        fraccion_unos = estado.count('1') / n
        expectativa  += fraccion_unos * prob

    # Escalar al rango de demanda real
    # expectativa en [0,1]: 0=mín demanda, 1=máx demanda
    factor_hora = 1.0 + 0.5 * np.sin((features.get('hora', 12) - 7) * np.pi / 12)
    demanda_m3h = demanda_base_m3h * expectativa * 2.5 * max(factor_hora, 0.3)

    # Confianza: inversamente proporcional a la entropía
    entropia = -sum(p * np.log2(p) for p in probs.values() if p > 0)
    confianza = max(0, 1 - entropia / np.log2(2 ** n))

    return {
        'demanda_predicha_m3h':   round(demanda_m3h, 1),
        'demanda_base_m3h':       demanda_base_m3h,
        'expectativa_cuantica':   round(expectativa, 4),
        'confianza_pct':          round(confianza * 100, 1),
        'entropia_prediccion':    round(entropia, 4),
        'probabilidades':         dict(sorted(probs.items(), key=lambda x: -x[1])[:10]),
        'features_normalizadas':  x,
        'features_originales':    features,
        'circuito_texto':         str(qc.draw('text')),
        'num_qubits':             n,
    }
