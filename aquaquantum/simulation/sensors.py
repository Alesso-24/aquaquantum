"""
Módulo: sensors.py
Genera datos realistas de sensores para la red hídrica de Puebla.
Incluye series temporales de demanda, lecturas de presión y parámetros de calidad.
"""

import random
import math
from datetime import datetime, timedelta


def generar_datos_sensores(n_sensores: int = 6, estado: str = "normal", semilla: int = None) -> list:
    """
    Genera lecturas de presión normalizadas para N sensores de la red.

    Args:
        n_sensores: Número de sensores (equivale a zonas monitoreadas).
        estado:     'normal', 'fuga_leve', 'fuga_critica', 'contaminacion'
        semilla:    Semilla para reproducibilidad (None = aleatorio).

    Returns:
        Lista de floats [0, 1] representando presión normalizada por sensor.
    """
    if semilla is not None:
        random.seed(semilla)

    lecturas = []
    for i in range(n_sensores):
        if estado == "normal":
            # Presión normal: centrada en 0.5 con poca variación
            base = random.uniform(0.40, 0.60)
        elif estado == "fuga_leve":
            # Una o dos zonas con presión baja (fuga pequeña)
            if i < 2:
                base = random.uniform(0.15, 0.30)  # zona con fuga
            else:
                base = random.uniform(0.38, 0.55)
        elif estado == "fuga_critica":
            # Múltiples zonas con presión muy baja
            if i < n_sensores // 2:
                base = random.uniform(0.05, 0.20)  # colapso de presión
            else:
                base = random.uniform(0.25, 0.45)
        elif estado == "contaminacion":
            # Presión normal pero con patrón irregular (ruido)
            base = random.uniform(0.35, 0.65)
            base += random.uniform(-0.15, 0.15) * (1 if i % 2 == 0 else -1)
            base = max(0.05, min(0.95, base))
        else:
            base = random.uniform(0.30, 0.70)

        lecturas.append(round(base, 4))

    return lecturas


def generar_parametros_calidad(estado: str = "normal") -> dict:
    """
    Genera parámetros de calidad del agua según el estado de la red.

    Returns:
        Diccionario con pH, turbidez, cloro residual y coliformes.
    """
    if estado == "normal":
        return {
            'ph':             round(random.uniform(6.8, 7.8), 2),
            'turbidez_ntu':   round(random.uniform(0.5, 3.0), 2),
            'cloro_mg_l':     round(random.uniform(0.4, 1.2), 2),
            'coliformes_nmp': round(random.uniform(0.0, 1.0), 1),
        }
    elif estado == "contaminacion":
        return {
            'ph':             round(random.uniform(5.5, 6.3), 2),
            'turbidez_ntu':   round(random.uniform(8.0, 25.0), 2),
            'cloro_mg_l':     round(random.uniform(0.0, 0.15), 2),
            'coliformes_nmp': round(random.uniform(10.0, 200.0), 1),
        }
    else:
        return {
            'ph':             round(random.uniform(6.0, 8.5), 2),
            'turbidez_ntu':   round(random.uniform(1.0, 10.0), 2),
            'cloro_mg_l':     round(random.uniform(0.1, 2.0), 2),
            'coliformes_nmp': round(random.uniform(0.0, 15.0), 1),
        }


def generar_serie_temporal_demanda(horas: int = 24, base_m3h: float = 2500.0) -> list:
    """
    Genera una serie temporal de demanda hídrica para un día completo.

    Simula los patrones reales de consumo en una ciudad mexicana:
    - Pico matutino: 6–9h
    - Valle al mediodía
    - Segundo pico: 18–21h
    - Mínimo nocturno: 0–5h

    Args:
        horas:     Número de horas a simular.
        base_m3h:  Demanda base en m³/hora.

    Returns:
        Lista de dicts con hora, demanda real, predicción cuántica y error.
    """
    serie = []
    for h in range(horas):
        # Patrón de demanda horaria (función de dos picos)
        factor_pico1 = math.exp(-((h - 7.5) ** 2) / 8)   # Pico AM: 7:30h
        factor_pico2 = math.exp(-((h - 19.0) ** 2) / 6)  # Pico PM: 19:00h
        factor_noche = 0.25 if 0 <= h < 5 else 0.0

        factor_total = 0.30 + 0.70 * max(factor_pico1, factor_pico2) + factor_noche
        demanda_real = base_m3h * factor_total * (1 + random.uniform(-0.08, 0.08))

        # Predicción cuántica: ligeramente más precisa que la clásica
        error_cuantico  = demanda_real * random.uniform(-0.04, 0.04)
        error_clasico   = demanda_real * random.uniform(-0.10, 0.10)

        serie.append({
            'hora':               h,
            'hora_str':           f"{h:02d}:00",
            'demanda_real_m3h':   round(demanda_real, 1),
            'prediccion_cuantica': round(demanda_real + error_cuantico, 1),
            'prediccion_clasica':  round(demanda_real + error_clasico, 1),
            'error_cuantico_pct': round(abs(error_cuantico / demanda_real) * 100, 2),
            'error_clasico_pct':  round(abs(error_clasico / demanda_real) * 100, 2),
        })

    return serie


def generar_features_hora(hora: int, temperatura_c: float = 22.0, lluvia_mm: float = 0.0) -> dict:
    """
    Genera el diccionario de características para predecir la demanda de una hora dada.
    """
    from datetime import date
    dia_semana = date.today().weekday()  # 0=lunes, 6=domingo
    return {
        'hora':            hora,
        'temperatura_c':   temperatura_c,
        'dia_semana':      dia_semana,
        'densidad_pob':    0.6,  # Puebla: densidad media-alta
        'lluvia_mm':       lluvia_mm,
    }
