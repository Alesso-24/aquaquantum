# Archivo: motor_cuantico.py
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def generar_clave_cuantica(num_qubits):
    """
    Crea un circuito, aplica superposición a todos los qubits
    y colapsa el estado para generar entropía real.
    """
    # Creamos el circuito con 'n' qubits y 'n' bits clásicos
    qc = QuantumCircuit(num_qubits, num_qubits)

    # Aplicamos la compuerta Hadamard a cada qubit para el 50/50
    for i in range(num_qubits):
        qc.h(i)

    # Medimos todos los qubits
    qc.measure(range(num_qubits), range(num_qubits))

    # Simulamos
    simulador = AerSimulator()
    circuito_compilado = transpile(qc, simulador)
    trabajo = simulador.run(circuito_compilado, shots=1)

    # Extraemos el único resultado generado
    resultado = trabajo.result()
    conteos = resultado.get_counts()

    # Devolvemos la cadena binaria (ej. '10110010')
    return list(conteos.keys())[0]
