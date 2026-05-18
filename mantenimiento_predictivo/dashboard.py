# Archivo: dashboard.py
import streamlit as st
import pandas as pd
import time
import plotly.express as px
from sensores import leer_vibracion_motor
from core_cuantico import analizar_anomalia_cuantica
from visuals import plot_probability_distribution, create_gauge_chart
from explanations import (
    INTRO_QUANTUM,
    QUBIT_EXPLANATION,
    ENTANGLEMENT_EXPLANATION,
    FEATURE_MAP_EXPLANATION,
    ENTROPY_EXPLANATION,
)

st.set_page_config(page_title="Q-PdM Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.title("🚀 Mantenimiento Predictivo Cuántico (Q-PdM) - Hackathon Edition")
st.write(
    "Un enfoque innovador para la detección de anomalías en maquinaria industrial "
    "utilizando el poder de la computación cuántica."
)
st.divider()

# --- SIDEBAR (Para explicaciones) ---
with st.sidebar:
    st.header("Conceptos Cuánticos ⚛️")
    st.markdown(INTRO_QUANTUM)
    with st.expander("¿Qué es un Qubit?"):
        st.markdown(QUBIT_EXPLANATION)
    with st.expander("Entrelazamiento Cuántico"):
        st.markdown(ENTANGLEMENT_EXPLANATION)
    with st.expander("Mapeo de Características Cuántico"):
        st.markdown(FEATURE_MAP_EXPLANATION)
    with st.expander("Entropía Cuántica de Anomalía"):
        st.markdown(ENTROPY_EXPLANATION)
    st.write("---")
    st.info("Desarrollado para el Hackathon de Mantenimiento Inteligente.")


# --- MAIN CONTENT LAYOUT ---
col_control, col_data_visuals = st.columns([1, 2])

with col_control:
    st.subheader("🎛️ Control de Simulación")
    st.info("Selecciona el estado del motor para simular las lecturas de los sensores.")
    estado_motor_opcion = st.radio(
        "Simular estado físico del motor:",
        ["Normal", "Anomalía (Falla Inminente)"],
        index=0, # Normal por defecto
        help="Elige entre un estado de operación normal o uno anómalo para ver cómo reacciona el algoritmo cuántico."
    )

    if st.button("🚀 Ejecutar Análisis Cuántico", type="primary", use_container_width=True):
        st.session_state['run_analysis'] = True
        st.session_state['estado_motor'] = estado_motor_opcion
    
    if st.button("🔄 Reiniciar Simulación", type="secondary", use_container_width=True):
        if 'run_analysis' in st.session_state:
            del st.session_state['run_analysis']
        st.rerun() # Reinicia la aplicación

# Inicializar estados si no existen
if 'run_analysis' not in st.session_state:
    st.session_state['run_analysis'] = False
    st.session_state['estado_motor'] = "Normal" # Estado inicial por defecto

if st.session_state['run_analysis']:
    with st.spinner("Analizando datos de sensores con algoritmos cuánticos..."):
        # 1. Leer sensores
        datos_sensores = leer_vibracion_motor(
            estado="normal" if st.session_state['estado_motor'] == "Normal" else "anomalo"
        )
        time.sleep(0.5) # Simular latencia de red/procesamiento

        # 2. Procesar en Qiskit
        riesgo, entropia_anomalia, dibujo_circuito, probabilidades = analizar_anomalia_cuantica(datos_sensores)
        
        st.session_state['datos_sensores'] = datos_sensores
        st.session_state['riesgo'] = riesgo
        st.session_state['entropia_anomalia'] = entropia_anomalia
        st.session_state['dibujo_circuito'] = dibujo_circuito
        st.session_state['probabilidades'] = probabilidades

    st.success("✅ Análisis Cuántico Completado. ¡Resultados listos!")

# --- DISPLAY RESULTS ---
with col_data_visuals:
    st.subheader("📊 Resultados del Análisis")

    if st.session_state['run_analysis'] and 'datos_sensores' in st.session_state:
        # Pestañas para organizar la información
        tab1, tab2, tab3 = st.tabs(["Métricas Clave", "Telemetría Clásica", "Topología Cuántica"])

        with tab1:
            st.subheader("Índices de Salud Cuántica")
            metrics_col1, metrics_col2 = st.columns(2)

            with metrics_col1:
                st.plotly_chart(create_gauge_chart(
                    st.session_state['riesgo'],
                    "Índice de Riesgo Cuántico",
                    threshold=0.4,
                    high_threshold=0.7
                ), use_container_width=True)
                riesgo_status = "🔴 CRÍTICO" if st.session_state['riesgo'] > 0.7 else \
                                "🟠 ATENCIÓN" if st.session_state['riesgo'] > 0.4 else "🟢 ÓPTIMO"
                st.markdown(f"<h3 style='text-align: center;'>Estado: {riesgo_status}</h3>", unsafe_allow_html=True)
                
            with metrics_col2:
                # La entropía de Shannon para 4 resultados con 0.25 cada uno es log2(4) = 2
                # Entonces, una entropía alta sería cercana a 2.
                st.plotly_chart(create_gauge_chart(
                    st.session_state['entropia_anomalia'],
                    "Entropía de Anomalía",
                    max_value=2.0, # Log2(4) para 4 estados posibles
                    threshold=1.0,
                    high_threshold=1.5
                ), use_container_width=True)
                entropia_status = "🟡 ALTA" if st.session_state['entropia_anomalia'] > 1.5 else \
                                  "🟠 MEDIA" if st.session_state['entropia_anomalia'] > 1.0 else "🟢 BAJA"
                st.markdown(f"<h3 style='text-align: center;'>Entropía: {entropia_status}</h3>", unsafe_allow_html=True)


            st.divider()
            st.subheader("🔬 Distribución de Probabilidades Cuánticas")
            st.plotly_chart(plot_probability_distribution(st.session_state['probabilidades']), use_container_width=True)
            st.caption("Esta gráfica muestra la probabilidad de medir cada estado cuántico final (00, 01, 10, 11) después de ejecutar el circuito.")

        with tab2:
            st.subheader("Valores Clásicos de los Sensores")
            # Gráfica de los sensores clásicos
            df_sensores = pd.DataFrame(
                [st.session_state['datos_sensores']],
                columns=["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4"]
            )
            fig_classic_sensors = px.bar(
                df_sensores.T,
                x=df_sensores.T.index,
                y=0,
                labels={'0': 'Valor Normalizado', 'index': 'Sensor'},
                title="Lecturas Normalizadas de Sensores de Vibración",
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig_classic_sensors, use_container_width=True)
            st.caption("Valores normalizados (entre 0 y 1) de los 4 sensores de vibración utilizados como entrada al circuito cuántico.")

        with tab3:
            st.subheader("Topología del Circuito Cuántico Generado")
            st.info("Este es el diagrama ASCII del circuito cuántico que se ejecutó. Puedes ver las compuertas de inicialización (H), codificación de datos (RZ), y entrelazamiento (CX).")
            st.code(st.session_state['dibujo_circuito'], language="text")
            st.caption("Cada línea representa un qubit, y las letras son compuertas cuánticas.")

    else:
        st.info("👆 Presiona 'Ejecutar Análisis Cuántico' para iniciar la simulación y ver los resultados.")

st.divider()
st.caption("© 2026 Mantenimiento Predictivo Cuántico - Desarrollado para el Hackathon.")
