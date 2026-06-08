"""
Módulo: optimizer.py
Algoritmo QAOA (Quantum Approximate Optimization Algorithm) adaptado para
optimizar la distribución de agua en redes urbanas.

El problema se modela como una variante del Max-Cut: dadas las zonas de la ciudad
conectadas por tuberías, encontrar la configuración óptima de válvulas para
minimizar pérdidas y maximizar cobertura.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from collections import Counter


def _calcular_costo_configuracion(config: str, conexiones: list) -> float:
    """Evalúa el costo de una configuración de válvulas para la red hídrica."""
    bits = [int(b) for b in config]
    costo = 0.0
    for conn in conexiones:
        i, j = conn['origen_idx'], conn['destino_idx']
        if i < len(bits) and j < len(bits):
            # Zonas en estados opuestos = corte óptimo (diferencia de presión controlada)
            if bits[i] != bits[j]:
                costo += conn['peso']
    return costo


def optimizar_red_hidrica(red_ciudad: dict, gamma: float = 0.9, beta: float = 0.4, p_capas: int = 3) -> dict:
    """
    Aplica QAOA para encontrar la configuración óptima de válvulas en la red hídrica.

    Args:
        red_ciudad: Diccionario con nodos y conexiones de la red urbana.
        gamma:      Parámetro del operador de costo (0–1).
        beta:       Parámetro del operador mezclador (0–1).
        p_capas:    Profundidad del circuito QAOA (más capas = mejor aproximación).

    Returns:
        Diccionario con configuración óptima, probabilidades, métricas y circuito.
    """
    zonas = list(red_ciudad['nodos'].keys())
    n = len(zonas)
    conexiones = red_ciudad.get('conexiones', [])

    qc = QuantumCircuit(n, n)

    # --- Inicialización: superposición uniforme ---
    qc.h(range(n))

    # --- Capas QAOA ---
    for capa in range(p_capas):
        # Escala los ángulos progresivamente por capa
        g = gamma * np.pi * (capa + 1) / p_capas
        b = beta  * np.pi * (capa + 1) / p_capas

        # Operador de costo: compuertas ZZ entre zonas conectadas por tuberías
        for conn in conexiones:
            i, j = conn['origen_idx'], conn['destino_idx']
            if i < n and j < n:
                qc.rzz(2.0 * g * conn['peso'], i, j)

        qc.barrier()

        # Operador mezclador: rotaciones RX para explorar el espacio de soluciones
        for i in range(n):
            qc.rx(2.0 * b, i)

        qc.barrier()

    # --- Medición ---
    qc.measure(range(n), range(n))

    # --- Simulación cuántica ---
    simulador = AerSimulator()
    compilado  = transpile(qc, simulador)
    resultado  = simulador.run(compilado, shots=4096).result()
    conteos    = resultado.get_counts()

    total = 4096
    probs = {k: v / total for k, v in conteos.items()}

    # --- Evaluar la mejor configuración ---
    mejor_config = max(conteos, key=lambda cfg: _calcular_costo_configuracion(cfg, conexiones))
    mejor_costo  = _calcular_costo_configuracion(mejor_config, conexiones)
    costo_max    = sum(c['peso'] for c in conexiones) if conexiones else 1

    # Métricas de impacto
    zonas_balanceadas  = sum(int(b) for b in mejor_config)
    eficiencia         = mejor_costo / costo_max if costo_max > 0 else 0
    ahorro_estimado_m3 = eficiencia * red_ciudad.get('consumo_diario_m3', 50000) * 0.30

    return {
        'configuracion_optima':  mejor_config,
        'probabilidades':        dict(sorted(probs.items(), key=lambda x: -x[1])[:12]),
        'zonas_abiertas':        zonas_balanceadas,
        'zonas_totales':         n,
        'eficiencia_pct':        round(eficiencia * 100, 2),
        'ahorro_m3_dia':         round(ahorro_estimado_m3, 0),
        'costo_cuantico':        round(mejor_costo, 4),
        'circuito_texto':        str(qc.draw('text')),
        'profundidad_circuito':  qc.depth(),
        'num_qubits':            n,
        'p_capas':               p_capas,
    }
