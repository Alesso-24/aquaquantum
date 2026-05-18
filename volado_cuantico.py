# 1. Importaciones modernas de Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

print("Iniciando el motor cuántico moderno...\n")

# 2. Creamos el circuito: 1 Qubit y 1 Bit clásico
qc = QuantumCircuit(1, 1)

# Aplicamos la compuerta Hadamard (H) para el 50/50
qc.h(0)

# Medimos
qc.measure(0, 0)

# 3. Configuramos el simulador con la nueva sintaxis
simulador = AerSimulator()

# En las versiones nuevas, IBM exige "transpilar" (compilar) el circuito
# antes de enviarlo al simulador o a la máquina real
circuito_compilado = transpile(qc, simulador)

# 4. Ejecutamos el circuito 10,000 veces
print("Lanzando la moneda cuántica 10,000 veces...")
trabajo = simulador.run(circuito_compilado, shots=10000)
resultado = trabajo.result()
conteos = resultado.get_counts()

# 5. Imprimimos resultados
print("\n--- RESULTADOS DEL VOLADO ---")
print(f"Caras (0): {conteos.get('0', 0)}")
print(f"Cruces (1): {conteos.get('1', 0)}")

print("\n--- DIBUJO DEL CIRCUITO ---")
print(qc.draw("text"))
