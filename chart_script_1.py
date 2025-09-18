import pandas as pd
import plotly.graph_objects as go

# Data from the provided JSON
data = {
    "previsao_7_dias": [
        {"dia": "Segunda", "consumo_atual": 1400, "consumo_otimizado": 1100},
        {"dia": "Terça", "consumo_atual": 1450, "consumo_otimizado": 1150},
        {"dia": "Quarta", "consumo_atual": 1380, "consumo_otimizado": 1080},
        {"dia": "Quinta", "consumo_atual": 1420, "consumo_otimizado": 1120},
        {"dia": "Sexta", "consumo_atual": 1500, "consumo_otimizado": 1200},
        {"dia": "Sábado", "consumo_atual": 900, "consumo_otimizado": 700},
        {"dia": "Domingo", "consumo_atual": 800, "consumo_otimizado": 600}
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data["previsao_7_dias"])

# Create the line chart
fig = go.Figure()

# Add Current Consumption line (yellow)
fig.add_trace(go.Scatter(
    x=df['dia'],
    y=df['consumo_atual'],
    mode='lines+markers',
    name='Consumo Atual',
    line=dict(color='#D2BA4C', width=3),
    marker=dict(size=8)
))

# Add Optimized Consumption line (green)
fig.add_trace(go.Scatter(
    x=df['dia'],
    y=df['consumo_otimizado'],
    mode='lines+markers',
    name='Consumo Otimiz.',
    line=dict(color='#2E8B57', width=3),
    marker=dict(size=8)
))

# Update layout
fig.update_layout(
    title='Previsão Consumo Energético - 7 Dias',
    xaxis_title='Dias',
    yaxis_title='Consumo (kWh)',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update traces and axes
fig.update_traces(cliponaxis=False)
fig.update_yaxes(tickformat='.0f')

# Save the chart as both PNG and SVG
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

print("Chart saved successfully as chart.png and chart.svg")