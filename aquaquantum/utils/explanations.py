"""
Módulo: explanations.py
Textos explicativos sobre computación cuántica aplicada al agua, en español.
"""

INTRO_AQUAQUANTUM = """
## ¿Por qué Computación Cuántica para el Agua?

Las ciudades latinoamericanas pierden entre **30–50% del agua potable** por fugas,
mala planificación y sistemas de monitoreo obsoletos. Los algoritmos clásicos
fallan ante la complejidad de optimizar cientos de tuberías simultáneamente.

**AquaQuantum** resuelve esto usando qubits que pueden evaluar miles de
configuraciones en paralelo gracias a la superposición cuántica.
"""

QAOA_EXPLANATION = """
### ¿Qué es QAOA?

El **Quantum Approximate Optimization Algorithm** combina dos operadores alternados:

1. **Operador de costo** (ZZ): "penaliza" las configuraciones de válvulas que
   causan pérdidas de presión entre zonas conectadas.
2. **Operador mezclador** (RX): permite al circuito "explorar" combinaciones
   de apertura/cierre de válvulas.

Después de P capas, el estado cuántico más probable corresponde a la
**configuración óptima de distribución de agua**.
"""

LEAK_DETECTION_EXPLANATION = """
### Detección Cuántica de Fugas

El circuito codifica la presión de cada sensor como un **ángulo de rotación**.
Presiones normales producen **interferencia constructiva** (distribución uniforme).
Una fuga rompe ese equilibrio → **interferencia destructiva** → distribución anómala.

La **Entropía de Shannon** mide el caos de la distribución:
- Entropía alta → sistema equilibrado → operación normal
- Entropía baja con picos anómalos → **fuga detectada**
"""

VQC_EXPLANATION = """
### Predicción con VQC (Variational Quantum Circuit)

El circuito variacional aprende los patrones de consumo de agua:
- **Hora del día**, temperatura, densidad poblacional → ángulos de rotación
- **Capas de entrelazamiento** → correlaciones entre variables
- **Expectativa cuántica** → demanda predicha en m³/hora

Los VQC son el equivalente cuántico de las redes neuronales, pero con
ventajas de expresividad exponencial en el espacio de características.
"""

QUALITY_EXPLANATION = """
### Análisis Cuántico de Calidad

4 parámetros críticos del agua (pH, turbidez, cloro, coliformes) se codifican
en 4 qubits. El circuito detecta desviaciones de los rangos óptimos (NOM-127-SSA1).

- **Estado |0000⟩** = agua perfecta en todos los parámetros
- **Estados con |1⟩** = parámetro fuera de rango
- La probabilidad de |0000⟩ define el **Índice de Calidad Cuántico (ICC)**
"""

IMPACTO_TEXTO = """
### Impacto Esperado para Puebla

| Métrica | Sin AquaQuantum | Con AquaQuantum |
|---------|----------------|-----------------|
| Pérdidas en red | 35% | < 12% |
| Detección de fugas | 72h promedio | < 2h |
| Error de predicción | ±15% | ±4% |
| Calidad monitoreo | Manual | Tiempo real |

**Ahorro estimado: 18,000 m³/día** — agua para 72,000 personas adicionales.
"""
