"""
Módulo: visualizations.py
Funciones de visualización con Plotly para el dashboard AquaQuantum.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# Paleta de colores del proyecto
COLORS = {
    'azul_agua':    '#00B4D8',
    'azul_oscuro':  '#0077B6',
    'azul_prof':    '#03045E',
    'verde':        '#06D6A0',
    'amarillo':     '#FFD166',
    'rojo':         '#EF233C',
    'naranja':      '#F77F00',
    'blanco':       '#FFFFFF',
    'gris':         '#8ECAE6',
}

LAYOUT_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,10,30,0.8)',
    font=dict(color='#CCEEFF', family='Arial'),
    margin=dict(l=20, r=20, t=50, b=20),
)


def graficar_red_hidrica(red: dict) -> go.Figure:
    """Mapa interactivo de la red hídrica con estado de nodos y tuberías."""
    nodos = red['nodos']
    conexiones = red['conexiones']

    # Trazar tuberías (edges)
    edge_x, edge_y, edge_colors = [], [], []
    for conn in conexiones:
        i, j = conn['origen_idx'], conn['destino_idx']
        edge_x += [nodos[i]['lon'], nodos[j]['lon'], None]
        edge_y += [nodos[i]['lat'], nodos[j]['lat'], None]

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon=edge_x, lat=edge_y,
        mode='lines',
        line=dict(width=2, color=COLORS['azul_agua']),
        opacity=0.6,
        name='Tuberías',
        hoverinfo='skip',
    ))

    # Nodos coloreados por estado (fuga / normal)
    for idx, nodo in nodos.items():
        color  = COLORS['rojo'] if nodo['tiene_fuga'] else COLORS['verde']
        simbolo = 'triangle-up' if nodo['tiene_fuga'] else 'circle'
        fig.add_trace(go.Scattergeo(
            lon=[nodo['lon']], lat=[nodo['lat']],
            mode='markers+text',
            marker=dict(size=14, color=color, symbol=simbolo, line=dict(width=2, color='white')),
            text=[nodo['nombre'][:12]],
            textposition='top center',
            textfont=dict(size=9, color='white'),
            name=nodo['nombre'],
            hovertemplate=(
                f"<b>{nodo['nombre']}</b><br>"
                f"Población: {nodo['poblacion']:,}<br>"
                f"Presión: {nodo['presion_bar']} bar<br>"
                f"Cobertura: {nodo['cobertura_pct']}%<br>"
                f"Estado: {'⚠️ FUGA' if nodo['tiene_fuga'] else '✅ Normal'}<extra></extra>"
            ),
            showlegend=False,
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        title='Red Hídrica Urbana — Puebla de Zaragoza',
        geo=dict(
            scope='north america',
            center=dict(lat=19.043, lon=-98.198),
            projection_scale=200,
            showland=True, landcolor='#0D1B2A',
            showocean=True, oceancolor='#03045E',
            showlakes=True, lakecolor='#00B4D8',
            showcountries=True, countrycolor='#333',
        ),
        height=420,
    )
    return fig


def graficar_distribucion_cuantica(probabilidades: dict, titulo: str = "Distribución de Estados Cuánticos") -> go.Figure:
    """Gráfica de barras de la distribución de probabilidades del circuito cuántico."""
    estados = sorted(probabilidades.keys())
    probs   = [probabilidades[e] * 100 for e in estados]
    colores = [COLORS['rojo'] if p == max(probs) else COLORS['azul_agua'] for p in probs]

    fig = go.Figure(go.Bar(
        x=estados, y=probs,
        marker_color=colores,
        marker_line=dict(color='white', width=1),
        text=[f"{p:.1f}%" for p in probs],
        textposition='outside',
        textfont=dict(color='white', size=10),
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=titulo,
        xaxis=dict(title='Estado Cuántico', tickfont=dict(color='white'), gridcolor='#1a3a5c'),
        yaxis=dict(title='Probabilidad (%)', tickfont=dict(color='white'), gridcolor='#1a3a5c'),
        height=320,
    )
    return fig


def crear_gauge(valor: float, titulo: str, maximo: float = 1.0,
                umbral1: float = 0.4, umbral2: float = 0.7,
                invertido: bool = False) -> go.Figure:
    """Medidor semicircular estilo cockpit para métricas clave."""
    if invertido:
        # Para ICC (calidad): más alto = mejor
        pasos = [
            {'range': [0, umbral1 * maximo], 'color': '#EF233C'},
            {'range': [umbral1 * maximo, umbral2 * maximo], 'color': '#FFD166'},
            {'range': [umbral2 * maximo, maximo], 'color': '#06D6A0'},
        ]
    else:
        pasos = [
            {'range': [0, umbral1 * maximo], 'color': '#06D6A0'},
            {'range': [umbral1 * maximo, umbral2 * maximo], 'color': '#FFD166'},
            {'range': [umbral2 * maximo, maximo], 'color': '#EF233C'},
        ]

    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=valor,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': titulo, 'font': {'size': 14, 'color': 'white'}},
        number={'font': {'color': COLORS['azul_agua'], 'size': 28}},
        gauge={
            'axis': {'range': [0, maximo], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
            'bar':  {'color': COLORS['azul_agua'], 'thickness': 0.25},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 2, 'bordercolor': '#1a3a5c',
            'steps': pasos,
            'threshold': {
                'line': {'color': 'white', 'width': 3},
                'thickness': 0.8,
                'value': umbral1 * maximo,
            },
        },
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'),
                      height=230, margin=dict(l=20, r=20, t=50, b=10))
    return fig


def graficar_demanda(serie: list) -> go.Figure:
    """Serie temporal de demanda hídrica: real vs predicción cuántica vs clásica."""
    horas     = [p['hora_str'] for p in serie]
    real      = [p['demanda_real_m3h'] for p in serie]
    cuantica  = [p['prediccion_cuantica'] for p in serie]
    clasica   = [p['prediccion_clasica'] for p in serie]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=horas, y=real,     name='Demanda Real',
                             line=dict(color=COLORS['blanco'], width=2.5)))
    fig.add_trace(go.Scatter(x=horas, y=cuantica, name='Predicción Cuántica',
                             line=dict(color=COLORS['azul_agua'], width=2, dash='dot')))
    fig.add_trace(go.Scatter(x=horas, y=clasica,  name='Predicción Clásica',
                             line=dict(color=COLORS['gris'], width=1.5, dash='dash')))

    fig.update_layout(
        **LAYOUT_BASE,
        title='Predicción de Demanda Hídrica — 24 horas',
        xaxis=dict(title='Hora', tickfont=dict(color='white'), gridcolor='#1a3a5c'),
        yaxis=dict(title='m³/hora', tickfont=dict(color='white'), gridcolor='#1a3a5c'),
        legend=dict(bgcolor='rgba(0,20,60,0.8)', bordercolor='#00B4D8', font=dict(color='white')),
        height=340,
    )
    return fig


def graficar_calidad_radar(desviaciones: dict) -> go.Figure:
    """Gráfica de radar para parámetros de calidad del agua."""
    categorias = ['pH', 'Turbidez', 'Cloro Residual', 'Coliformes']
    valores_mal  = [desviaciones.get('ph', 0) * 100,
                    desviaciones.get('turbidez', 0) * 100,
                    desviaciones.get('cloro', 0) * 100,
                    desviaciones.get('coliformes', 0) * 100]
    valores_bien = [100 - v for v in valores_mal]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores_bien + [valores_bien[0]],
        theta=categorias + [categorias[0]],
        fill='toself', name='Calidad Actual',
        line_color=COLORS['azul_agua'],
        fillcolor='rgba(0,180,216,0.25)',
    ))
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100, 100],
        theta=categorias + [categorias[0]],
        fill='toself', name='Óptimo',
        line_color=COLORS['verde'],
        fillcolor='rgba(6,214,160,0.10)',
        line_dash='dot',
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        polar=dict(
            radialaxis=dict(range=[0, 100], tickfont=dict(color='white'), gridcolor='#1a3a5c'),
            angularaxis=dict(tickfont=dict(color='white'), gridcolor='#1a3a5c'),
            bgcolor='rgba(0,10,30,0.8)',
        ),
        title='Parámetros de Calidad del Agua',
        legend=dict(bgcolor='rgba(0,20,60,0.8)', font=dict(color='white')),
        height=340,
    )
    return fig


def graficar_mapa_fugas(red: dict, resultado_fugas: dict) -> go.Figure:
    """Mapa de calor de anomalías por zona."""
    nodos = red['nodos']
    lecturas = resultado_fugas.get('lecturas_sensores', [])
    sensor_critico = resultado_fugas.get('sensor_critico_idx', 0)

    nombres, presiones, colores, tamanios = [], [], [], []
    for i, (idx, nodo) in enumerate(nodos.items()):
        nombres.append(nodo['nombre'])
        presion = lecturas[i] if i < len(lecturas) else nodo['presion_bar']
        presiones.append(round(presion, 3))
        if i == sensor_critico and resultado_fugas.get('fuga_detectada'):
            colores.append(COLORS['rojo'])
            tamanios.append(25)
        elif presion < 0.25:
            colores.append(COLORS['naranja'])
            tamanios.append(18)
        else:
            colores.append(COLORS['azul_agua'])
            tamanios.append(12)

    fig = go.Figure(go.Bar(
        x=nombres, y=presiones,
        marker_color=colores,
        marker_line=dict(color='white', width=0.5),
        text=[f"{p:.2f}" for p in presiones],
        textposition='outside',
        textfont=dict(color='white', size=9),
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title='Presión por Zona (barras rojas = posible fuga)',
        xaxis=dict(title='Zona', tickangle=-30, tickfont=dict(color='white', size=9),
                   gridcolor='#1a3a5c'),
        yaxis=dict(title='Presión Normalizada', tickfont=dict(color='white'),
                   gridcolor='#1a3a5c', range=[0, 1.1]),
        height=320,
    )
    return fig


def graficar_comparacion_cuantica(probabilidades_antes: dict, probabilidades_despues: dict) -> go.Figure:
    """Compara la distribución cuántica antes y después de la optimización."""
    estados = sorted(set(list(probabilidades_antes.keys()) + list(probabilidades_despues.keys())))
    antes   = [probabilidades_antes.get(e, 0) * 100 for e in estados]
    despues = [probabilidades_despues.get(e, 0) * 100 for e in estados]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=estados, y=antes,   name='Sin Optimizar',
                         marker_color=COLORS['gris'], opacity=0.7))
    fig.add_trace(go.Bar(x=estados, y=despues, name='Optimizado (QAOA)',
                         marker_color=COLORS['azul_agua']))

    fig.update_layout(
        **LAYOUT_BASE,
        title='Distribución Cuántica: Antes vs Después de QAOA',
        barmode='group',
        xaxis=dict(title='Estado Cuántico', tickfont=dict(color='white'), gridcolor='#1a3a5c'),
        yaxis=dict(title='Probabilidad (%)', tickfont=dict(color='white'), gridcolor='#1a3a5c'),
        legend=dict(bgcolor='rgba(0,20,60,0.8)', font=dict(color='white')),
        height=320,
    )
    return fig
