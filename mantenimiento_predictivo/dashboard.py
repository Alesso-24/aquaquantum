# Archivo: dashboard.py
import streamlit as st
import pandas as pd
import time
from sensores import leer_vibracion_motor
from core_cuantico import analizar_anomalia_cuantica

st.set_page_config(page_title="Q-PdM Dashboard", layout="wide")

st.title("⚙️ Mantenimiento Predictivo Cuántico (Q-PdM)")
st.write(
    "Análisis de anomalías en maquinaria rotativa mediante entrelazamiento de Qubits."
)
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Control de Maquinaria")
    estado_motor = st.radio(
        "Simular estado físico del motor:", ["Normal", "Falla Inminente"]
    )

    if st.button("Ejecutar Escaneo Cuántico", type="primary"):
        with st.spinner("Leyendo sensores y transpilando circuito..."):
            time.sleep(1)  # Simular latencia de red

            # 1. Leer sensores
            datos = leer_vibracion_motor(
                estado="normal" if estado_motor == "Normal" else "anomalo"
            )

            # 2. Procesar en Qiskit
            riesgo, dibujo_circuito = analizar_anomalia_cuantica(datos)

            # 3. Mostrar resultados
            st.success("Escaneo completado.")

            st.metric(
                label="Índice de Riesgo Cuántico",
                value=f"{riesgo * 100:.1f}%",
                delta="Crítico" if riesgo > 0.4 else "Óptimo",
                delta_color="inverse",
            )

with col2:
    st.subheader("Telemetría y Topología")
    if "datos" in locals():
        # Gráfica de los sensores clásicos
        df_sensores = pd.DataFrame(
            [datos], columns=["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4"]
        )
        st.bar_chart(df_sensores.T)

        # Mostrar el circuito generado dinámicamente
        st.text("Topología del Circuito Cuántico Generado:")
        st.code(dibujo_circuito, language="text")
    else:
        st.info("Presiona el botón para iniciar la simulación.")
