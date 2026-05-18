# Archivo: core_cuantico.py
import math
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from collections import Counter

def calcular_entropia_shannon(probabilities):
    """Calcula la entropía de Shannon para una distribución de probabilidades."""
    entropy = 0.0
    for prob in probabilities:
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

def analizar_anomalia_cuantica(datos_sensores):
    """
    Recibe 4 datos de vibración, los codifica en 2 qubits utilizando un mapa de características
    más complejo con entrelazamiento y mide la distribución de probabilidad de los estados finales.
    Calcula un "Índice de Riesgo Cuántico" y la "Entropía Cuántica de Anomalía".
    """
    # 2 Qubits, 2 Bits clásicos
    qc = QuantumCircuit(2, 2)

    # Normalizar los datos de entrada para que estén entre 0 y 1 si no lo están ya
    # Aseguramos que los datos se mapeen a un rango apropiado para las rotaciones
    scaled_data = [d * math.pi for d in datos_sensores]

    # --- Feature Map y Entrelazamiento Mejorado ---
    # Capa de inicialización (opcional, pero ayuda a explorar el espacio)
    qc.h(0)
    qc.h(1)

    # Primera capa de codificación de datos con RZ
    qc.rz(scaled_data[0], 0)
    qc.rz(scaled_data[1], 1)

    # Entrelazamiento (Control-X)
    qc.cx(0, 1)

    # Segunda capa de codificación de datos con RZ (usando los datos restantes)
    qc.rz(scaled_data[2], 0)
    qc.rz(scaled_data[3], 1)
    
    # Otro entrelazamiento para mayor complejidad
    qc.cx(1, 0) # CX invertida para más profundidad

    # Medimos los qubits a los bits clásicos
    qc.measure([0, 1], [0, 1])

    # Simulamos en el simulador Aer
    simulador = AerSimulator()
    circuito_compilado = transpile(qc, simulador)
    trabajo = simulador.run(circuito_compilado, shots=1024) # Aumentamos shots para mejor resolución
    conteos = trabajo.result().get_counts()

    # Asegurar que conteos tenga las 4 claves (00, 01, 10, 11) aunque estén a 0
    full_conteos = Counter({'00': 0, '01': 0, '10': 0, '11': 0})
    full_conteos.update(conteos)
    
    # Convertir conteos a probabilidades
    total_shots = 1024
    probabilities = {k: v / total_shots for k, v in full_conteos.items()}

    # Calculamos el "Índice de Riesgo Cuántico"
    # Puede ser la probabilidad de '11' o una suma ponderada de estados anómalos
    # Para este ejemplo, usaremos una métrica basada en la "desviación" o "energía"
    # Podríamos decir que los estados '10' y '01' también contribuyen al riesgo.
    riesgo = (probabilities.get("11", 0) * 2 + probabilities.get("10", 0) + probabilities.get("01", 0)) / 3.0 # Ponderación
    
    # Calculamos la "Entropía Cuántica de Anomalía"
    # Una entropía más alta puede indicar un estado más "caótico" o anómalo
    prob_values = [probabilities[k] for k in sorted(probabilities.keys())]
    entropia_anomalia = calcular_entropia_shannon(prob_values)

    return riesgo, entropia_anomalia, qc.draw("text"), probabilities
