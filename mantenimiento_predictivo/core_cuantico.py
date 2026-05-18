# Archivo: core_cuantico.py
import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def analizar_anomalia_cuantica(datos_sensores):
    """
    Recibe 4 datos de vibración, los codifica en 2 qubits usando
    compuertas de rotación (Rx, Ry) y mide la probabilidad de colapso.
    """
    # 2 Qubits, 2 Bits clásicos
    qc = QuantumCircuit(2, 2)

    # 1. Codificación de los datos físicos al mundo cuántico
    qc.rx(datos_sensores[0] * math.pi, 0)
    qc.rx(datos_sensores[1] * math.pi, 1)

    # 2. Entrelazamiento (La magia cuántica: conectamos el destino de ambos sensores)
    qc.cx(0, 1)

    # 3. Aplicamos el resto de los datos
    qc.ry(datos_sensores[2] * math.pi, 0)
    qc.ry(datos_sensores[3] * math.pi, 1)

    # Medimos
    qc.measure([0, 1], [0, 1])

    # Simulamos
    simulador = AerSimulator()
    circuito_compilado = transpile(qc, simulador)
    trabajo = simulador.run(circuito_compilado, shots=1000)
    conteos = trabajo.result().get_counts()

    # Calculamos el "Riesgo de Falla" basado en cuántas veces colapsó en '11'
    riesgo = conteos.get("11", 0) / 1000.0

    return riesgo, qc.draw("text")
