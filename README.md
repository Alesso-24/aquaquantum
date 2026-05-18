# 🚀 Proyecto de Mantenimiento Predictivo Cuántico (Q-PdM) - Edición Hackathon

## ✨ ¡Preséntalo con Orgullo en tu Hackathon!

Este proyecto demuestra una aplicación innovadora del Mantenimiento Predictivo (PdM) tradicional al integrarlo con la Computación Cuántica. Está diseñado para impresionar en un hackathon, mostrando no solo un dashboard interactivo sino también una arquitectura de microservicios con una API robusta y una explicación clara de los conceptos cuánticos.

### Características Destacadas:
-   **Análisis Cuántico de Anomalías**: Utiliza un circuito cuántico de 2 qubits con entrelazamiento y mapeo de características para detectar patrones de anomalías en datos de sensores de vibración.
-   **Métricas Cuánticas Avanzadas**: Calcula un "Índice de Riesgo Cuántico" y una "Entropía Cuántica de Anomalía" para una detección más sofisticada.
-   **Dashboard Interactivo (Streamlit)**: Una interfaz de usuario moderna y responsiva que permite simular estados del motor (normal/anómalo) y visualizar los resultados, incluyendo distribuciones de probabilidad cuántica y diagramas de circuito.
-   **API RESTful (FastAPI)**: Expone la lógica de análisis cuántico como un servicio web, permitiendo que otras aplicaciones se conecten y utilicen la inteligencia cuántica. Ideal para una arquitectura modular o para integrar con sistemas existentes.
-   **Explicaciones Integradas**: Incluye una sección de "Conceptos Cuánticos" para que cualquier jurado o público pueda entender los fundamentos detrás de la magia.

## 🛠️ Configuración del Entorno

Asegúrate de tener Python 3.9+ instalado.

1.  **Clona este repositorio (o descarga los archivos):**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd <nombre_de_la_carpeta_del_proyecto>
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    **En Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
    **En macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Cómo Ejecutar el Proyecto

Este proyecto consta de dos componentes principales: la API de FastAPI y el Dashboard de Streamlit. Puedes ejecutarlos de forma independiente o conjunta.

### 1. Iniciar la API de Análisis Cuántico (FastAPI)

Esta API sirve la lógica cuántica como un servicio REST. ¡Es lo que hace que tu proyecto sea "interconectado"!

```bash
uvicorn mantenimiento_predictivo.api:app --reload --host 0.0.0.0 --port 8000
```
-   `--reload`: La API se reiniciará automáticamente al guardar cambios en el código.
-   `--host 0.0.0.0`: Hace que la API sea accesible desde tu red local (útil para pruebas).
-   `--port 8000`: Se ejecutará en el puerto 8000.

Una vez iniciada, puedes acceder a la documentación interactiva de la API en tu navegador:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Iniciar el Dashboard Interactivo (Streamlit)

Este es el frontend visual de tu aplicación, donde los usuarios pueden interactuar con la simulación y ver los resultados.

```bash
streamlit run mantenimiento_predictivo\dashboard.py
```

Una vez iniciado, el dashboard se abrirá automáticamente en tu navegador:
👉 [http://localhost:8501](http://localhost:8501)

#### Modo de Operación del Dashboard:
-   **Con la API (Recomendado para el Hackathon)**: Asegúrate de que la API de FastAPI esté corriendo (Paso 1). En el dashboard, marca la casilla "Usar API para el análisis cuántico". Esto mostrará cómo tu dashboard se comunica con tu microservicio cuántico.
-   **Directo**: Si la API no está corriendo o si desmarcas la casilla, el dashboard ejecutará el análisis cuántico directamente en el mismo proceso.

## 💡 ¿Cómo "Vender" este Proyecto en un Hackathon?

1.  **Impacto Innovador**: Destaca cómo la computación cuántica se aplica a un problema industrial real (mantenimiento predictivo), una de las áreas más prometedoras para esta tecnología emergente.
2.  **Detección Superior**: Explica que el entrelazamiento y los feature maps cuánticos pueden revelar patrones de anomalía más sutiles y complejos que los algoritmos clásicos.
3.  **Arquitectura Modular**: Enfatiza la separación entre la lógica de análisis cuántico (API) y la interfaz de usuario (dashboard), mostrando un diseño escalable y listo para producción.
4.  **Experiencia de Usuario**: Muestra la facilidad de uso del dashboard, las visualizaciones claras y las explicaciones integradas que hacen que la computación cuántica sea comprensible para una audiencia no técnica.
5.  **Potencial de Futuro**: Habla sobre cómo esto podría evolucionar hacia una solución híbrida (clásico-cuántico), integrándose con datos en tiempo real de fábricas inteligentes.

---
© 2026 Mantenimiento Predictivo Cuántico - Desarrollado con pasión para el Hackathon.
