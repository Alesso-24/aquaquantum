import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_probability_distribution(probabilities):
    """
    Genera un gráfico de barras para la distribución de probabilidades cuánticas.
    """
    df_probs = pd.DataFrame(
        {'Estado Cuántico': list(probabilities.keys()),
         'Probabilidad': list(probabilities.values())}
    )
    # Ordenar para una visualización consistente
    df_probs['Estado Cuántico'] = pd.Categorical(
        df_probs['Estado Cuántico'],
        categories=['00', '01', '10', '11'],
        ordered=True
    )
    df_probs = df_probs.sort_values('Estado Cuántico')

    fig = px.bar(
        df_probs,
        x='Estado Cuántico',
        y='Probabilidad',
        color='Probabilidad',
        color_continuous_scale=px.colors.sequential.Plasma,
        title='Distribución de Probabilidades de Estados Cuánticos Finales',
        labels={'Probabilidad': 'Probabilidad de Medición (%)'},
        text_auto='.1%',
        height=400
    )
    fig.update_layout(
        xaxis_title="Estados Medidos",
        yaxis_title="Probabilidad",
        yaxis_tickformat=".0%", # Formato de porcentaje en el eje Y
        coloraxis_colorbar=dict(
            title="Probabilidad",
            tickformat=".0%",
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=200,
        )
    )
    fig.update_traces(marker_line_width=1, marker_line_color='black')
    return fig

def create_gauge_chart(value, title, max_value=1.0, threshold=0.6, high_threshold=0.8):
    """
    Crea un gráfico tipo medidor para métricas clave.
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, threshold], 'color': 'lightgreen'},
                {'range': [threshold, high_threshold], 'color': 'yellow'},
                {'range': [high_threshold, max_value], 'color': 'red'}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': threshold}}))

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
    return fig
