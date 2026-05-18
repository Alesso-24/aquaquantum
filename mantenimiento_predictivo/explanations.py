
INTRO_QUANTUM = """
### ¿Qué es el Mantenimiento Predictivo Cuántico (Q-PdM)?

El Q-PdM combina la **computación cuántica** con el mantenimiento predictivo tradicional. En lugar de solo procesar datos de sensores con algoritmos clásicos, utilizamos principios de la mecánica cuántica (como la superposición y el entrelazamiento) para analizar patrones complejos en los datos de vibración y detectar anomalías de manera más sofisticada.

Esto nos permite:
-   Identificar signos tempranos de falla que podrían ser difíciles de ver con métodos clásicos.
-   Procesar información de una manera que explota las correlaciones no-clásicas entre los sensores.
"""

QUBIT_EXPLANATION = """
### Qubits: El Bit Cuántico
A diferencia de los bits clásicos (0 o 1), un **qubit** puede existir como 0, 1, o una **superposición** de ambos simultáneamente. Esto significa que puede ser 0 y 1 a la vez, con ciertas probabilidades para cada estado. Esta capacidad es fundamental para el procesamiento cuántico.
"""

ENTANGLEMENT_EXPLANATION = """
### Entrelazamiento Cuántico: La Conexión Mágica
El **entrelazamiento** es un fenómeno donde dos o más qubits se conectan de tal manera que el estado de uno no puede describirse independientemente del estado de los otros, incluso si están físicamente separados. En nuestro sistema, usamos el entrelazamiento para crear correlaciones profundas entre los datos de diferentes sensores, permitiendo que la "salud" de un sensor influya en la interpretación de otro de manera cuántica. Una compuerta CNOT (Control-NOT) es un operador clave para crear entrelazamiento.
"""

FEATURE_MAP_EXPLANATION = """
### Mapeo de Características Cuántico (Quantum Feature Map)
Un "Feature Map" cuántico es una técnica para codificar datos clásicos (como las lecturas de sensores de vibración) en un espacio de características de alta dimensión dentro de un circuito cuántico. Esto se hace aplicando una secuencia de compuertas cuánticas (como las rotaciones Ry y Rz) que transforman los datos de entrada en estados cuánticos específicos. El objetivo es que las anomalías, que podrían ser difíciles de distinguir en el espacio clásico, sean más evidentes una vez transformadas en el espacio cuántico, haciéndolas más fáciles de detectar por el circuito.
"""

ENTROPY_EXPLANATION = """
### Entropía Cuántica de Anomalía
La **Entropía de Shannon** es una medida de la incertidumbre o "sorpresa" en una distribución de probabilidades.
En el contexto cuántico, la entropía de la distribución de probabilidades de los estados finales (por ejemplo, '00', '01', '10', '11') nos indica cuán "mezclado" o "uniforme" es el resultado de nuestro circuito cuántico.

-   **Baja Entropía:** Si el sistema colapsa consistentemente a uno o pocos estados (p. ej., casi siempre '00'), significa que el sistema se comporta de manera predecible, lo que podría indicar un estado normal.
-   **Alta Entropía:** Si el sistema colapsa a una mezcla más uniforme de estados (p. ej., probabilidades similares para '00', '01', '10', '11'), sugiere un comportamiento más "caótico" o impredecible, lo que podría ser una señal de anomalía o fallo.

Esta métrica complementa el Índice de Riesgo Cuántico, proporcionando una perspectiva diferente sobre la complejidad del estado del sistema.
"""
