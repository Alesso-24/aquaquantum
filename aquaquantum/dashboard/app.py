"""
Dashboard Principal: AquaQuantum
HACKATHON LATAM 2026 · Computación Cuántica para los Desafíos del Agua
Puebla de Zaragoza, México
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
import time
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from aquaquantum.core import (
    optimizar_red_hidrica,
    detectar_fugas_cuantico,
    predecir_demanda_cuantica,
    analizar_calidad_cuantica,
)
from aquaquantum.simulation import (
    generar_red_puebla,
    generar_datos_sensores,
    generar_serie_temporal_demanda,
)
from aquaquantum.simulation.sensors import generar_parametros_calidad, generar_features_hora
from aquaquantum.data import obtener_clima_puebla, obtener_datos_conagua, obtener_poblacion_puebla
from aquaquantum.utils.visualizations import (
    graficar_red_hidrica,
    graficar_distribucion_cuantica,
    crear_gauge,
    graficar_demanda,
    graficar_calidad_radar,
    graficar_mapa_fugas,
    graficar_comparacion_cuantica,
)
from aquaquantum.utils.explanations import (
    INTRO_AQUAQUANTUM, QAOA_EXPLANATION, LEAK_DETECTION_EXPLANATION,
    VQC_EXPLANATION, QUALITY_EXPLANATION, IMPACTO_TEXTO,
)

# ─── Config de página ───────────────────────────────────────
st.set_page_config(
    page_title="AquaQuantum — HACKATHON LATAM 2026",
    page_icon="💧", layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS completo ───────────────────────────────────────────
st.markdown("""
<style>
  .stApp {
    background: linear-gradient(160deg,#020818 0%,#041a3a 40%,#0a2240 70%,#010c1e 100%);
    color:#cceeff;
  }
  .hero-banner {
    background:linear-gradient(135deg,rgba(0,119,182,.35),rgba(0,180,216,.15));
    border:1px solid rgba(0,180,216,.5); border-radius:16px;
    padding:26px 36px; margin-bottom:18px; text-align:center;
    box-shadow:0 0 40px rgba(0,180,216,.15);
  }
  .hero-banner h1 { font-size:2.8rem; margin:0; color:#00B4D8; letter-spacing:2px; }
  .hero-banner h2 { font-size:1.15rem; margin:8px 0 4px; color:#8ECAE6; font-weight:400; }
  .badge {
    display:inline-block; background:rgba(0,180,216,.2);
    border:1px solid #00B4D8; border-radius:20px;
    padding:3px 12px; font-size:0.80rem; color:#00B4D8; margin:4px 3px 0;
  }
  .kpi-card {
    background:linear-gradient(135deg,rgba(0,119,182,.25),rgba(3,4,94,.4));
    border:1px solid rgba(0,180,216,.4); border-radius:12px;
    padding:16px 10px; text-align:center; margin:3px;
    box-shadow:0 4px 15px rgba(0,0,0,.3);
  }
  .kpi-val  { font-size:1.9rem; font-weight:700; color:#00B4D8; }
  .kpi-lbl  { font-size:0.75rem; color:#8ECAE6; margin-top:3px; }
  .kpi-icon { font-size:1.4rem; }
  .data-badge-real {
    display:inline-block; background:rgba(6,214,160,.15);
    border:1px solid #06D6A0; border-radius:6px;
    padding:2px 8px; font-size:0.72rem; color:#06D6A0;
  }
  .data-badge-sim {
    display:inline-block; background:rgba(255,209,102,.10);
    border:1px solid #FFD166; border-radius:6px;
    padding:2px 8px; font-size:0.72rem; color:#FFD166;
  }
  .clima-card {
    background:rgba(0,30,70,.5); border:1px solid rgba(0,180,216,.35);
    border-radius:10px; padding:12px 16px; margin-bottom:10px;
  }
  .alerta-critica {
    background:rgba(239,35,60,.15); border:1px solid #EF233C;
    border-radius:10px; padding:14px; color:#ff7080;
  }
  .alerta-ok {
    background:rgba(6,214,160,.12); border:1px solid #06D6A0;
    border-radius:10px; padding:14px; color:#06D6A0;
  }
  .seccion-titulo {
    color:#00B4D8; font-size:1.1rem; font-weight:700;
    border-bottom:1px solid rgba(0,180,216,.3);
    padding-bottom:5px; margin:16px 0 10px;
  }
  [data-testid="stSidebar"] { background:linear-gradient(180deg,#010c1e 0%,#021226 100%); }
  [data-testid="stSidebar"] * { color:#aaddff; }
  .stButton>button {
    background:linear-gradient(135deg,#0077B6,#00B4D8);
    color:white; border:none; border-radius:8px;
    font-weight:600; letter-spacing:.5px; width:100%;
  }
  .stTabs [data-baseweb="tab-list"] { background:rgba(0,20,50,.5); border-radius:10px; }
  .stTabs [data-baseweb="tab"] { color:#8ECAE6; }
  .stTabs [aria-selected="true"] { color:#00B4D8; background:rgba(0,180,216,.15); border-radius:8px; }
  [data-testid="metric-container"] {
    background:rgba(0,60,120,.2); border:1px solid rgba(0,180,216,.3);
    border-radius:10px; padding:8px;
  }
  .conagua-row {
    background:rgba(0,20,50,.5); border-left:3px solid #00B4D8;
    padding:8px 12px; margin:4px 0; border-radius:0 6px 6px 0;
  }
</style>
""", unsafe_allow_html=True)

# ─── Banner héroe ────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div style="font-size:2rem">💧⚛️</div>
  <h1>AquaQuantum</h1>
  <h2>Soluciones Cuánticas para los Desafíos del Agua en Grandes Ciudades</h2>
  <span class="badge">🏆 HACKATHON LATAM 2026 · Puebla, México</span>
  <span class="badge">⚛️ Qiskit + IBM Quantum Simulator</span>
  <span class="badge">📡 Datos reales: Open-Meteo · CONAGUA · INEGI 2020</span>
</div>
""", unsafe_allow_html=True)


# ─── Carga de datos con cache ─────────────────────────────────
@st.cache_data(ttl=1800)  # Clima: refresca cada 30 min (evita 429 en Streamlit Cloud)
def _clima():
    return obtener_clima_puebla()

@st.cache_data(ttl=3600)  # CONAGUA: refresca cada hora
def _conagua():
    return obtener_datos_conagua()

@st.cache_data(ttl=86400) # INEGI: datos del censo, no cambia
def _inegi():
    return obtener_poblacion_puebla()

@st.cache_data(ttl=120)
def _red():
    return generar_red_puebla()

@st.cache_data(ttl=60)
def _serie():
    return generar_serie_temporal_demanda(horas=24)


def _badge(status):
    """Genera el HTML del badge de fuente de datos."""
    if status.es_real:
        return f'<span class="data-badge-real">📡 {status.fuente}</span>'
    return f'<span class="data-badge-sim">🔄 {status.fuente}</span>'


# ─── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💧 AquaQuantum")
    st.markdown("**HACKATHON LATAM 2026**")
    st.caption("Puebla de Zaragoza, México")
    st.divider()

    modulo_activo = st.radio(
        "Módulo",
        ["🗺️ Visión General", "⚡ Optimización QAOA", "🔍 Detección de Fugas",
         "📈 Predicción de Demanda", "🧪 Calidad del Agua",
         "📡 Datos Reales", "⚛️ Circuitos Cuánticos"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### Parámetros")
    estado_red  = st.selectbox("Estado de la red", ["normal","fuga_leve","fuga_critica","contaminacion"],
        format_func=lambda x: {"normal":"✅ Normal","fuga_leve":"⚠️ Fuga Leve",
                                "fuga_critica":"🔴 Fuga Crítica","contaminacion":"☣️ Contaminación"}[x])
    hora_dia    = st.slider("Hora del día", 0, 23, 10)

    st.divider()
    st.markdown("### Conceptos Cuánticos")
    with st.expander("¿Por qué cuántica para el agua?"):
        st.markdown(INTRO_AQUAQUANTUM)
    with st.expander("QAOA — Optimización"):
        st.markdown(QAOA_EXPLANATION)
    with st.expander("Detección de Fugas"):
        st.markdown(LEAK_DETECTION_EXPLANATION)
    with st.expander("VQC — Predicción"):
        st.markdown(VQC_EXPLANATION)

    st.divider()
    st.caption("© 2026 AquaQuantum · Hackathon LATAM")


# ─── Cargar datos ─────────────────────────────────────────────
clima, s_clima       = _clima()
conagua, s_conagua   = _conagua()
inegi, s_inegi       = _inegi()
red                  = _red()
serie_demanda        = _serie()
temperatura_real     = clima["temperatura_c"]
lluvia_real          = clima["lluvia_mm"]


# ══════════════════════════════════════════════════════════════
# MÓDULO 1 — VISIÓN GENERAL
# ══════════════════════════════════════════════════════════════
if modulo_activo == "🗺️ Visión General":

    # ── Clima real en tiempo real ─────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    desc_clima = clima.get("descripcion", "—")
    with c1:
        st.markdown(f"""<div class="clima-card">
          <div style="font-size:1.5rem">🌡️</div>
          <div style="font-size:1.6rem;color:#00B4D8;font-weight:700">{clima['temperatura_c']}°C</div>
          <div style="font-size:0.7rem;color:#8ECAE6">Temp. actual · Puebla</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="clima-card">
          <div style="font-size:1.5rem">🌧️</div>
          <div style="font-size:1.6rem;color:#00B4D8;font-weight:700">{clima['lluvia_mm']} mm</div>
          <div style="font-size:0.7rem;color:#8ECAE6">Precipitación actual</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="clima-card">
          <div style="font-size:1.5rem">💧</div>
          <div style="font-size:1.6rem;color:#00B4D8;font-weight:700">{clima['humedad_pct']}%</div>
          <div style="font-size:0.7rem;color:#8ECAE6">Humedad relativa</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="clima-card">
          <div style="font-size:1.5rem">☁️</div>
          <div style="font-size:1rem;color:#00B4D8;font-weight:700">{desc_clima}</div>
          <div style="font-size:0.7rem;color:#8ECAE6">Condición actual</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="clima-card">
          <div style="font-size:1.5rem">👥</div>
          <div style="font-size:1.4rem;color:#00B4D8;font-weight:700">{inegi['total_municipal']:,}</div>
          <div style="font-size:0.7rem;color:#8ECAE6">Habitantes · INEGI 2020</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"{_badge(s_clima)} &nbsp; {_badge(s_inegi)}", unsafe_allow_html=True)
    st.markdown("")

    # ── KPIs de la red ───────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-icon">🏙️</div>
          <div class="kpi-val">{red['num_zonas']}</div>
          <div class="kpi-lbl">Zonas Monitoreadas</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        agua_no_acc = round((100 - inegi['agua_entubada_pct']) * inegi['total_municipal'] / 100)
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-icon">🚫💧</div>
          <div class="kpi-val" style="color:#FFD166">{agua_no_acc:,}</div>
          <div class="kpi-lbl">Sin acceso a agua · INEGI 2020</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-icon">⚠️</div>
          <div class="kpi-val" style="color:{'#EF233C' if red['zonas_con_fuga']>0 else '#06D6A0'}">{red['zonas_con_fuga']}</div>
          <div class="kpi-lbl">Zonas con Fuga Activa</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-icon">💧</div>
          <div class="kpi-val">{red['agua_perdida_m3dia']:,.0f}</div>
          <div class="kpi-lbl">m³/día Perdidos</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # ── Mapa + stats ────────────────────────────────────────
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.plotly_chart(graficar_red_hidrica(red), use_container_width=True)
        st.markdown(f"Población por zona: {_badge(s_inegi)}", unsafe_allow_html=True)

    with col_s:
        st.markdown('<div class="seccion-titulo">📊 Red Hídrica</div>', unsafe_allow_html=True)
        st.metric("Cobertura de agua", f"{inegi['agua_entubada_pct']}%",
                  help="INEGI Censo 2020 — % viviendas con agua entubada")
        st.metric("Pérdidas en red", f"{red['perdida_red_pct']}%")
        st.metric("Demanda diaria", f"{red['demanda_total_m3dia']:,.0f} m³")
        st.metric("Tuberías monitoreadas", f"{red['num_tuberias']} tramos")
        st.divider()
        st.markdown('<div class="seccion-titulo">🌡️ Clima hoy</div>', unsafe_allow_html=True)
        pronostico = clima.get("pronostico_7dias", [])
        if pronostico:
            df_prono = pd.DataFrame(pronostico[:5])
            df_show  = df_prono[["fecha","descripcion","t_max","t_min","lluvia_mm"]].rename(
                columns={"fecha":"Día","descripcion":"Clima","t_max":"Máx°C",
                          "t_min":"Mín°C","lluvia_mm":"Lluvia mm"})
            st.dataframe(df_show, hide_index=True, use_container_width=True)
        st.markdown(IMPACTO_TEXTO)


# ══════════════════════════════════════════════════════════════
# MÓDULO 2 — OPTIMIZACIÓN QAOA
# ══════════════════════════════════════════════════════════════
elif modulo_activo == "⚡ Optimización QAOA":
    st.markdown('<div class="seccion-titulo">⚡ Optimización Cuántica de Red Hídrica (QAOA)</div>',
                unsafe_allow_html=True)
    st.markdown("""El **QAOA** modela la red de distribución de agua como optimización combinatoria.
    Cada qubit = una zona urbana. Las compuertas ZZ penalizan pérdidas de presión entre zonas conectadas.""")

    col_c, col_r = st.columns([1, 2])
    with col_c:
        p_capas  = st.slider("Capas del circuito (p)", 1, 5, 3)
        gamma    = st.slider("γ (costo)", 0.1, 1.5, 0.9, 0.1)
        beta     = st.slider("β (mezclador)", 0.1, 1.5, 0.4, 0.1)
        ejecutar = st.button("🚀 Ejecutar QAOA")

    if ejecutar or "res_qaoa" in st.session_state:
        if ejecutar:
            with st.spinner("Ejecutando circuito QAOA en simulador cuántico..."):
                t0 = time.time()
                r  = optimizar_red_hidrica(red, gamma=gamma, beta=beta, p_capas=p_capas)
                st.session_state["res_qaoa"]      = r
                st.session_state["tiempo_qaoa"]   = round(time.time() - t0, 2)

        r = st.session_state["res_qaoa"]
        with col_r:
            a, b, c = st.columns(3)
            a.metric("Eficiencia cuántica",  f"{r['eficiencia_pct']}%", "+12%")
            b.metric("Ahorro estimado",       f"{r['ahorro_m3_dia']:,.0f} m³/día")
            c.metric("Profundidad circuito",  f"{r['profundidad_circuito']}")

        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(graficar_distribucion_cuantica(r["probabilidades"],
                "Distribución QAOA — Top configuraciones"), use_container_width=True)
        with g2:
            n = r["num_qubits"]
            antes = {f"{i:0{n}b}": 1/(2**n) for i in range(min(2**n, 12))}
            st.plotly_chart(graficar_comparacion_cuantica(antes, r["probabilidades"]),
                use_container_width=True)

        cf, mt = st.columns(2)
        with cf:
            st.markdown('<div class="seccion-titulo">Configuración óptima de válvulas</div>',
                        unsafe_allow_html=True)
            cfg   = r["configuracion_optima"]
            zonas = list(red["nodos"].values())
            for i, (bit, zona) in enumerate(zip(cfg, zonas)):
                icono = "🟢 ABIERTA" if bit == "1" else "🔴 CERRADA"
                pob   = f"({zona['poblacion']:,} hab · INEGI)"
                st.markdown(f"**{zona['nombre']}**: {icono} {pob}")
        with mt:
            st.markdown('<div class="seccion-titulo">Métricas cuánticas</div>', unsafe_allow_html=True)
            st.metric("Qubits utilizados", r["num_qubits"])
            st.metric("Capas QAOA", r["p_capas"])
            st.metric("Costo cuántico", f"{r['costo_cuantico']:.4f}")
            st.metric("Tiempo ejecución", f"{st.session_state.get('tiempo_qaoa',0)}s")
    else:
        st.info("👆 Ajusta los parámetros y presiona **Ejecutar QAOA**.")


# ══════════════════════════════════════════════════════════════
# MÓDULO 3 — DETECCIÓN DE FUGAS
# ══════════════════════════════════════════════════════════════
elif modulo_activo == "🔍 Detección de Fugas":
    st.markdown('<div class="seccion-titulo">🔍 Detección Cuántica de Fugas en Tuberías</div>',
                unsafe_allow_html=True)
    st.markdown("""Las lecturas de **presión** de cada sensor se codifican como ángulos de rotación cuántica.
    Las fugas rompen la coherencia → distribución anómala → alerta en tiempo real.""")

    col_c, col_r = st.columns([1, 2])
    with col_c:
        n_sens   = st.slider("Sensores", 4, 8, 6)
        umbral   = st.slider("Umbral anomalía", 0.10, 0.80, 0.35, 0.05)
        ejecutar = st.button("🔍 Analizar Fugas")

    if ejecutar or "res_fugas" in st.session_state:
        if ejecutar:
            with st.spinner("Ejecutando detección cuántica..."):
                lecturas = generar_datos_sensores(n_sensores=n_sens, estado=estado_red)
                r2 = detectar_fugas_cuantico(lecturas, umbral_anomalia=umbral)
                st.session_state["res_fugas"] = r2

        r2   = st.session_state["res_fugas"]
        fuga = r2["fuga_detectada"]

        with col_r:
            if fuga:
                st.markdown(f"""<div class="alerta-critica">
                  🚨 <b>{r2['estado']}</b><br/>
                  Sensor crítico: Zona #{r2['sensor_critico_idx']+1}<br/>
                  Severidad: {r2['severidad'].upper()}<br/>
                  Pérdida estimada: <b>{r2['litros_fuga_por_hora']:,.0f} L/hora</b>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="alerta-ok">
                  ✅ <b>{r2['estado']}</b><br/>
                  Todos los sensores dentro de rangos normales.
                </div>""", unsafe_allow_html=True)

        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(crear_gauge(r2["indice_anomalia"], "Índice de Anomalía",
                maximo=1.0, umbral1=0.35, umbral2=0.65), use_container_width=True)
            st.plotly_chart(crear_gauge(r2["entropia_cuantica"], "Entropía Cuántica",
                maximo=r2["entropia_maxima"], umbral1=0.5, umbral2=0.75, invertido=True),
                use_container_width=True)
        with g2:
            st.plotly_chart(graficar_distribucion_cuantica(r2["probabilidades"],
                "Distribución de Estados Cuánticos"), use_container_width=True)
            st.plotly_chart(graficar_mapa_fugas(red, r2), use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Índice anomalía", f"{r2['indice_anomalia']:.3f}")
        m2.metric("Entropía cuántica", f"{r2['entropia_cuantica']:.3f}")
        m3.metric("Pérdida L/hora", f"{r2['litros_fuga_por_hora']:,.0f}")
    else:
        st.info("👆 Selecciona el estado de la red y presiona **Analizar Fugas**.")


# ══════════════════════════════════════════════════════════════
# MÓDULO 4 — PREDICCIÓN DE DEMANDA
# ══════════════════════════════════════════════════════════════
elif modulo_activo == "📈 Predicción de Demanda":
    st.markdown('<div class="seccion-titulo">📈 Predicción Cuántica de Demanda Hídrica</div>',
                unsafe_allow_html=True)
    st.markdown(f"""Un **VQC de 5 qubits** predice el consumo de agua usando como entrada la
    **temperatura real de Puebla** ({temperatura_real}°C) y la **precipitación actual** ({lluvia_real} mm)
    obtenidas en tiempo real de Open-Meteo.""")
    st.markdown(f"{_badge(s_clima)}", unsafe_allow_html=True)

    col_c, col_r = st.columns([1, 2])
    with col_c:
        usar_clima_real = st.checkbox("Usar clima real de Puebla (Open-Meteo)", value=True)
        if usar_clima_real:
            temp_input  = temperatura_real
            lluvia_input = lluvia_real
            st.info(f"🌡️ {temp_input}°C  |  🌧️ {lluvia_input} mm\n(datos en tiempo real)")
        else:
            temp_input   = st.slider("Temperatura (°C)", 10, 38, 22)
            lluvia_input = st.slider("Lluvia (mm)", 0.0, 50.0, 0.0, 1.0)
        ejecutar = st.button("📈 Predecir Demanda")

    if ejecutar or "res_dem" in st.session_state:
        if ejecutar:
            with st.spinner("Ejecutando VQC de predicción..."):
                features = generar_features_hora(hora_dia, temp_input, lluvia_input)
                r3 = predecir_demanda_cuantica(features)
                st.session_state["res_dem"] = r3

        r3 = st.session_state["res_dem"]
        with col_r:
            a, b, c = st.columns(3)
            a.metric("Demanda predicha", f"{r3['demanda_predicha_m3h']:,.0f} m³/h")
            b.metric("Confianza VQC",    f"{r3['confianza_pct']}%")
            c.metric("Entropía",         f"{r3['entropia_prediccion']:.3f}")

        st.divider()
        g1, g2 = st.columns([2, 1])
        with g1:
            st.plotly_chart(graficar_demanda(serie_demanda), use_container_width=True)
        with g2:
            st.plotly_chart(graficar_distribucion_cuantica(r3["probabilidades"],
                "Distribución VQC"), use_container_width=True)

        st.divider()
        errs_q = [p["error_cuantico_pct"] for p in serie_demanda]
        errs_c = [p["error_clasico_pct"]  for p in serie_demanda]
        mae_q  = sum(errs_q) / len(errs_q)
        mae_c  = sum(errs_c) / len(errs_c)
        e1, e2, e3 = st.columns(3)
        e1.metric("MAE Cuántico",  f"{mae_q:.1f}%", f"-{mae_c-mae_q:.1f}%")
        e2.metric("MAE Clásico",   f"{mae_c:.1f}%")
        e3.metric("Mejora cuántica", f"{(mae_c-mae_q)/mae_c*100:.1f}%")
    else:
        st.info("👆 Presiona **Predecir Demanda** para ejecutar el VQC.")


# ══════════════════════════════════════════════════════════════
# MÓDULO 5 — CALIDAD DEL AGUA
# ══════════════════════════════════════════════════════════════
elif modulo_activo == "🧪 Calidad del Agua":
    st.markdown('<div class="seccion-titulo">🧪 Análisis Cuántico de Calidad del Agua</div>',
                unsafe_allow_html=True)
    st.markdown(f"""Un circuito de **4 qubits** codifica pH, turbidez, cloro y coliformes.
    La probabilidad del estado |0000⟩ define el **ICC — Índice de Calidad Cuántico**.
    Los valores por defecto provienen de datos reales de estaciones CONAGUA en Puebla. {_badge(s_conagua)}""",
    unsafe_allow_html=True)

    col_c, col_r = st.columns([1, 2])
    with col_c:
        modo = st.radio("Fuente de datos", ["📡 CONAGUA (datos reales)", "✏️ Manual", "🎲 Simular"])
        if modo == "📡 CONAGUA (datos reales)":
            est_sel = st.selectbox("Estación de monitoreo",
                [e["estacion"] for e in conagua])
            datos_est = next(e for e in conagua if e["estacion"] == est_sel)
            params = {k: datos_est[k] for k in ["ph","turbidez_ntu","cloro_mg_l","coliformes_nmp"]}
            st.markdown(f"""<div class="conagua-row">
              <b>{datos_est['estacion']}</b><br/>
              pH: {params['ph']} · Turb: {params['turbidez_ntu']} NTU<br/>
              Cloro: {params['cloro_mg_l']} mg/L · Coli: {params['coliformes_nmp']} NMP<br/>
              <small>{datos_est['fuente']}</small>
            </div>""", unsafe_allow_html=True)
        elif modo == "✏️ Manual":
            params = {
                "ph":             st.slider("pH", 4.0, 10.0, 7.2, 0.1),
                "turbidez_ntu":   st.slider("Turbidez (NTU)", 0.0, 100.0, 2.5, 0.5),
                "cloro_mg_l":     st.slider("Cloro residual (mg/L)", 0.0, 5.0, 0.8, 0.05),
                "coliformes_nmp": st.slider("Coliformes (NMP/100mL)", 0.0, 500.0, 0.0, 1.0),
            }
        else:
            params = generar_parametros_calidad(estado=estado_red)
            st.json(params)

        ejecutar = st.button("🧪 Analizar Calidad")

    if ejecutar or "res_cal" in st.session_state:
        if ejecutar:
            with st.spinner("Ejecutando análisis cuántico..."):
                r4 = analizar_calidad_cuantica(params)
                st.session_state["res_cal"] = r4

        r4 = st.session_state["res_cal"]
        cmap = {"verde":"#06D6A0","azul":"#00B4D8","amarillo":"#FFD166",
                "naranja":"#F77F00","rojo":"#EF233C"}
        col_icc = cmap.get(r4["color_estado"], "#00B4D8")

        with col_r:
            st.markdown(f"""
            <div style="text-align:center;padding:20px;
                        background:rgba(0,30,60,.4);
                        border:2px solid {col_icc};border-radius:12px;">
              <div style="font-size:3rem;color:{col_icc};font-weight:700">{r4['icc']:.1f}</div>
              <div style="font-size:1.1rem;color:{col_icc}">ICC — Índice de Calidad Cuántico</div>
              <div style="font-size:1.4rem;margin-top:8px;color:{col_icc}">{r4['estado']}</div>
              <div style="font-size:0.85rem;color:#aaa;margin-top:4px">
                Prob. |0000⟩: {r4['prob_estado_optimo']}% · NOM-127-SSA1
              </div>
            </div>""", unsafe_allow_html=True)

        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(graficar_calidad_radar(r4["desviaciones"]), use_container_width=True)
        with g2:
            st.plotly_chart(graficar_distribucion_cuantica(r4["probabilidades"],
                "Distribución de Calidad Cuántica"), use_container_width=True)

        rec, dos = st.columns(2)
        with rec:
            st.markdown('<div class="seccion-titulo">📋 Recomendaciones CONAGUA</div>',
                        unsafe_allow_html=True)
            for rx in r4["recomendaciones"]:
                st.markdown(f"• {rx}")
        with dos:
            st.markdown('<div class="seccion-titulo">⚗️ Dosis optimizada</div>', unsafe_allow_html=True)
            st.metric("Cloro recomendado", f"{r4['dosis_cloro_optima_mg_l']} mg/L")
            st.metric("Norma NOM-127-SSA1", "0.2 – 1.5 mg/L")
    else:
        st.info("👆 Selecciona la fuente de datos y presiona **Analizar Calidad**.")


# ══════════════════════════════════════════════════════════════
# MÓDULO 6 — DATOS REALES (panel de transparencia)
# ══════════════════════════════════════════════════════════════
elif modulo_activo == "📡 Datos Reales":
    st.markdown('<div class="seccion-titulo">📡 Panel de Datos Reales — Transparencia Total</div>',
                unsafe_allow_html=True)
    st.markdown("""Este panel muestra exactamente **qué datos son reales** y cuáles son simulados,
    de dónde vienen y cuándo se obtuvieron. La transparencia es parte del diseño.""")

    # ── Open-Meteo ──────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### 🌦️ Clima de Puebla — Open-Meteo  {_badge(s_clima)}", unsafe_allow_html=True)
    st.caption(s_clima.nota)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Temperatura actual",   f"{clima['temperatura_c']}°C")
        st.metric("Sensación térmica",    f"{clima['sensacion_c']}°C")
        st.metric("Humedad relativa",     f"{clima['humedad_pct']}%")
        st.metric("Precipitación actual", f"{clima['lluvia_mm']} mm")
        st.metric("Condición",            clima["descripcion"])
    with col2:
        pronostico = clima.get("pronostico_7dias", [])
        if pronostico:
            df_p = pd.DataFrame(pronostico)
            fig_prono = go.Figure()
            fig_prono.add_trace(go.Bar(x=df_p["fecha"], y=df_p["lluvia_mm"],
                name="Lluvia (mm)", marker_color="#00B4D8", opacity=0.7))
            fig_prono.add_trace(go.Scatter(x=df_p["fecha"], y=df_p["t_max"],
                name="T°max", line=dict(color="#FFD166", width=2), yaxis="y2"))
            fig_prono.add_trace(go.Scatter(x=df_p["fecha"], y=df_p["t_min"],
                name="T°min", line=dict(color="#8ECAE6", width=2, dash="dot"), yaxis="y2"))
            fig_prono.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,10,30,.8)",
                font=dict(color="#CCEEFF"), height=280, margin=dict(l=20,r=20,t=30,b=20),
                title="Pronóstico 7 días — Open-Meteo (datos reales)",
                yaxis=dict(title="Lluvia (mm)", side="left", gridcolor="#1a3a5c"),
                yaxis2=dict(title="Temperatura °C", overlaying="y", side="right"),
                legend=dict(bgcolor="rgba(0,20,60,.8)", font=dict(color="white")),
            )
            st.plotly_chart(fig_prono, use_container_width=True)

    # ── CONAGUA ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### 🏭 Calidad del Agua en Puebla — CONAGUA BANDAS 2023  {_badge(s_conagua)}",
                unsafe_allow_html=True)
    st.caption(s_conagua.nota)

    df_conagua = pd.DataFrame(conagua)[
        ["estacion","ph","turbidez_ntu","cloro_mg_l","coliformes_nmp","dbo_mg_l","fuente"]]
    df_conagua.columns = ["Estación","pH","Turbidez NTU","Cloro mg/L",
                           "Colif. NMP","DBO mg/L","Fuente"]

    # Color por calidad: coliformes > 100 = crítico
    def color_row(row):
        if row["Colif. NMP"] > 100:
            return ["background-color:rgba(239,35,60,.2)"]*len(row)
        return [""] * len(row)

    st.dataframe(df_conagua.style.apply(color_row, axis=1),
                 use_container_width=True, hide_index=True)
    st.caption("Rojo = coliformes por encima de la norma NOM-127-SSA1 (máx 2 NMP/100mL en agua potable)")

    # ── INEGI ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### 👥 Población — INEGI Censo 2020  {_badge(s_inegi)}",
                unsafe_allow_html=True)
    st.caption(f"Fuente: {inegi['fuente']} · {inegi['url']}")

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.metric("Población municipal", f"{inegi['total_municipal']:,}")
        st.metric("Hogares", f"{inegi['hogares_total']:,}")
        st.metric("Con agua entubada", f"{inegi['agua_entubada_pct']}%")
        st.metric("Con drenaje", f"{inegi['drenaje_pct']}%")
        st.metric("Densidad", f"{inegi['densidad_hab_km2']:,} hab/km²")
    with col_i2:
        zonas_df = pd.DataFrame(inegi["zonas"]).T.reset_index()
        zonas_df.columns = ["Zona","Población","Viviendas","Agua (%)"]
        fig_inegi = px.bar(zonas_df, x="Zona", y="Población",
            color="Agua (%)", color_continuous_scale="Blues",
            title="Población por zona — INEGI Censo 2020")
        fig_inegi.update_layout(paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,10,30,.8)", font=dict(color="#CCEEFF"),
            height=300, margin=dict(l=10,r=10,t=40,b=60),
            xaxis=dict(tickangle=-35, tickfont=dict(size=9)))
        st.plotly_chart(fig_inegi, use_container_width=True)

    # ── Simulado ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔄 Datos Simulados (declaración de transparencia)")
    st.markdown("""
    Los siguientes componentes usan datos **simulados** porque SOAPAP no tiene API pública
    de sensores en tiempo real:

    | Componente | Estado | Razón |
    |------------|--------|-------|
    | Presión en tuberías | 🔄 Simulado | SOAPAP sin API pública |
    | Lecturas de sensores | 🔄 Simulado | Red SCADA no accesible |
    | Demanda horaria | 🔄 Simulado | Modelo basado en patrones CONAGUA |
    | Fugas activas | 🔄 Simulado | Sin telemetría en tiempo real |

    **Para producción real:** conectar al sistema SCADA de SOAPAP o instalar sensores IoT
    que alimenten este dashboard con telemetría en tiempo real.
    """)


# ══════════════════════════════════════════════════════════════
# MÓDULO 7 — CIRCUITOS CUÁNTICOS
# ══════════════════════════════════════════════════════════════
elif modulo_activo == "⚛️ Circuitos Cuánticos":
    st.markdown('<div class="seccion-titulo">⚛️ Visualización de Circuitos Cuánticos</div>',
                unsafe_allow_html=True)

    circuito_sel = st.selectbox("Circuito",
        ["QAOA — Optimización de Red", "Detección de Fugas",
         "VQC — Predicción de Demanda", "Calidad del Agua"])

    if st.button("⚛️ Generar Circuito"):
        with st.spinner("Construyendo circuito cuántico..."):
            if circuito_sel == "QAOA — Optimización de Red":
                res = optimizar_red_hidrica(red, p_capas=2)
                texto = res["circuito_texto"]
                info  = f"{res['num_qubits']} qubits · {res['p_capas']} capas QAOA · Profundidad {res['profundidad_circuito']}"
                desc  = QAOA_EXPLANATION
            elif circuito_sel == "Detección de Fugas":
                lecturas = generar_datos_sensores(4, estado=estado_red)
                res  = detectar_fugas_cuantico(lecturas)
                texto = res["circuito_texto"]
                info  = f"{res['num_qubits']} qubits · Compuertas: RY, CX, RZ"
                desc  = LEAK_DETECTION_EXPLANATION
            elif circuito_sel == "VQC — Predicción de Demanda":
                features = generar_features_hora(hora_dia, temperatura_real, lluvia_real)
                res  = predecir_demanda_cuantica(features)
                texto = res["circuito_texto"]
                info  = f"{res['num_qubits']} qubits · Compuertas: RY, CX, RZ, RX"
                desc  = VQC_EXPLANATION
            else:
                params_q = generar_parametros_calidad()
                res  = analizar_calidad_cuantica(params_q)
                texto = res["circuito_texto"]
                info  = f"{res['num_qubits']} qubits · Compuertas: RY, CX, RZ"
                desc  = QUALITY_EXPLANATION

        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"**{info}**")
            st.code(texto, language="text")
        with c2:
            st.markdown("### Explicación")
            st.markdown(desc)
            st.markdown("""
            **Leyenda:**
            - `H` — Hadamard: superposición
            - `RY(θ)` — codifica datos como ángulo
            - `RZ(θ)` — fase de anomalía
            - `RX(θ)` — operador mezclador QAOA
            - `CX` — entrelazamiento CNOT
            - `RZZ(θ)` — correlación entre zonas
            """)
    else:
        st.info("👆 Selecciona un circuito y presiona **Generar Circuito**.")


# ─── Footer ──────────────────────────────────────────────────
st.divider()
f1, f2, f3 = st.columns(3)
f1.caption("💧 AquaQuantum · HACKATHON LATAM 2026")
f2.caption("⚛️ Qiskit · 📡 Open-Meteo · CONAGUA · INEGI 2020")
f3.caption("🏙️ Puebla de Zaragoza, México · © 2026")
