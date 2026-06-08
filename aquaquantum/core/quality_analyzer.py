"""
Módulo: quality_analyzer.py
Análisis cuántico de calidad del agua y optimización de tratamiento.

Usa un circuito de 4 qubits para codificar parámetros de calidad del agua
(pH, turbidez, cloro residual, coliformes) y obtener un índice de calidad
cuántico junto con recomendaciones de tratamiento.
"""

import numpy as np
import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# Rangos óptimos de calidad del agua potable (norma NOM-127-SSA1)
RANGOS_OPTIMOS = {
    'ph':              (6.5, 8.5),
    'turbidez_ntu':    (0.0, 5.0),
    'cloro_mg_l':      (0.2, 1.5),
    'coliformes_nmp':  (0.0, 2.0),
}


def _normalizar_parametro(valor: float, rango_optimo: tuple, rango_maximo: tuple) -> float:
    """
    Normaliza un parámetro de calidad a [0, 1].
    0 = dentro del rango óptimo (excelente), 1 = fuera del rango (crítico).
    """
    lo, hi = rango_optimo
    max_lo, max_hi = rango_maximo
    if lo <= valor <= hi:
        return 0.0  # óptimo
    elif valor < lo:
        return (lo - valor) / (lo - max_lo + 1e-9)
    else:
        return (valor - hi) / (max_hi - hi + 1e-9)


def analizar_calidad_cuantica(parametros: dict) -> dict:
    """
    Analiza la calidad del agua con un circuito cuántico de 4 qubits.

    Args:
        parametros: Diccionario con:
            - ph:             Valor de pH (ideal: 6.5–8.5)
            - turbidez_ntu:   Turbidez en NTU (ideal: <5)
            - cloro_mg_l:     Cloro residual en mg/L (ideal: 0.2–1.5)
            - coliformes_nmp: Coliformes en NMP/100mL (ideal: 0)

    Returns:
        Diccionario con índice de calidad, estado, recomendaciones y circuito.
    """
    ph              = parametros.get('ph', 7.0)
    turbidez        = parametros.get('turbidez_ntu', 2.0)
    cloro           = parametros.get('cloro_mg_l', 0.8)
    coliformes      = parametros.get('coliformes_nmp', 0.0)

    # Desviaciones normalizadas respecto al rango óptimo [0=óptimo, 1=crítico]
    dev_ph          = _normalizar_parametro(ph,         (6.5, 8.5),  (4.0, 11.0))
    dev_turbidez    = _normalizar_parametro(turbidez,   (0.0, 5.0),  (0.0, 200.0))
    dev_cloro       = _normalizar_parametro(cloro,      (0.2, 1.5),  (0.0, 5.0))
    dev_coliformes  = _normalizar_parametro(coliformes, (0.0, 2.0),  (0.0, 1000.0))

    desviaciones = [dev_ph, dev_turbidez, dev_cloro, dev_coliformes]
    n = len(desviaciones)

    qc = QuantumCircuit(n, n)

    # --- Codificación: mayor desviación → mayor ángulo → más probabilidad de |1⟩ ---
    for i, dev in enumerate(desviaciones):
        angulo = dev * np.pi
        qc.ry(angulo, i)

    # --- Entrelazamiento: los parámetros de calidad están correlacionados ---
    qc.cx(0, 1)  # pH ↔ turbidez
    qc.cx(2, 3)  # cloro ↔ coliformes
    qc.cx(1, 2)  # turbidez ↔ cloro

    # --- Segunda capa de rotaciones para amplificar señales críticas ---
    for i, dev in enumerate(desviaciones):
        if dev > 0.5:  # Parámetro fuera del rango → rotación adicional
            qc.rz(dev * np.pi * 0.5, i)

    qc.measure(range(n), range(n))

    # --- Simulación ---
    simulador = AerSimulator()
    compilado  = transpile(qc, simulador)
    resultado  = simulador.run(compilado, shots=4096).result()
    conteos    = resultado.get_counts()

    total = 4096
    probs = {k: v / total for k, v in conteos.items()}

    # --- Índice de calidad cuántico (ICC) ---
    # Probabilidad del estado |0000⟩ representa calidad perfecta
    prob_optima = probs.get('0000', 0.0)
    icc = prob_optima * 100  # 0–100: 100 = agua perfecta

    # Puntaje adicional ponderado por parámetro
    pesos = [0.25, 0.30, 0.25, 0.20]  # turbidez pesa más
    score_clasico = sum((1 - dev) * w for dev, w in zip(desviaciones, pesos)) * 100
    icc_final = (icc * 0.6 + score_clasico * 0.4)

    # --- Clasificación ---
    if icc_final >= 90:
        estado, color = "EXCELENTE", "verde"
    elif icc_final >= 75:
        estado, color = "BUENA", "azul"
    elif icc_final >= 55:
        estado, color = "ACEPTABLE", "amarillo"
    elif icc_final >= 30:
        estado, color = "DEFICIENTE", "naranja"
    else:
        estado, color = "NO APTA", "rojo"

    # --- Recomendaciones de tratamiento ---
    recomendaciones = []
    if dev_ph > 0.1:
        recomendaciones.append(f"Ajustar pH: agregar {'cal viva' if ph < 6.5 else 'CO₂'} — desviación {dev_ph*100:.0f}%")
    if dev_turbidez > 0.1:
        recomendaciones.append(f"Aumentar coagulación/floculación — turbidez {turbidez:.1f} NTU")
    if dev_cloro > 0.1:
        recomendaciones.append(f"{'Cloración adicional' if cloro < 0.2 else 'Reducir cloración'} — cloro {cloro:.2f} mg/L")
    if dev_coliformes > 0.05:
        recomendaciones.append(f"Desinfección urgente — coliformes {coliformes:.1f} NMP/100mL")
    if not recomendaciones:
        recomendaciones.append("Agua en condiciones óptimas. Mantener proceso actual.")

    # Dosis óptima de cloro recomendada (regresión cuántica simplificada)
    dosis_cloro = max(0.2, min(2.0, 0.8 + dev_turbidez * 1.2 + dev_coliformes * 0.8))

    return {
        'icc':                    round(icc_final, 1),
        'estado':                 estado,
        'color_estado':           color,
        'probabilidades':         dict(sorted(probs.items(), key=lambda x: -x[1])[:8]),
        'prob_estado_optimo':     round(prob_optima * 100, 1),
        'desviaciones':           {
            'ph':         round(dev_ph, 3),
            'turbidez':   round(dev_turbidez, 3),
            'cloro':      round(dev_cloro, 3),
            'coliformes': round(dev_coliformes, 3),
        },
        'parametros_entrada':     parametros,
        'recomendaciones':        recomendaciones,
        'dosis_cloro_optima_mg_l': round(dosis_cloro, 2),
        'circuito_texto':         str(qc.draw('text')),
        'num_qubits':             n,
    }
