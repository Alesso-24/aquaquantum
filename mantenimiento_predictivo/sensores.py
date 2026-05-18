# Archivo: sensores.py
import random


def leer_vibracion_motor(estado="normal"):
    """
    Simula la lectura de 4 sensores de vibración en una maquinaria rotativa.
    Devuelve valores normalizados entre 0 y 1.
    """
    if estado == "normal":
        # Vibración baja, funcionamiento óptimo
        return [random.uniform(0.1, 0.4) for _ in range(4)]
    else:
        # Anomalía detectada, vibración errática
        return [random.uniform(0.5, 0.9) for _ in range(4)]
