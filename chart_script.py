import plotly.graph_objects as go
import pandas as pd

# Data from the provided JSON
data = {
    "setores": [
        {"nome": "Administrativo", "economia_kwh_mes": 4500},
        {"nome": "Engenharia", "economia_kwh_mes": 3600},
        {"nome": "Produção", "economia_kwh_mes": 6000},
        {"nome": "Vendas", "economia_kwh_mes": 3240},
        {"nome": "Suporte", "economia_kwh_mes": 4390}
    ]
}

# Extract data for plotting
setores = [item["nome"] for item in data["setores"]]
economia = [item["economia_kwh_mes"] for item in data["setores"]]

# Brand colors in order
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Create bar chart
fig = go.Figure(data=[
    go.Bar(
        x=setores,
        y=economia,
        marker_color=colors,
        text=[f'{val/1000:.1f}k' for val in economia],
        textposition='auto',
        textfont=dict(color='white', size=14)
    )
])

# Update layout
fig.update_layout(
    title='Potencial Economia Energética por Setor',
    xaxis_title='Setores',
    yaxis_title='Economia (kWh/mês)',
    showlegend=False
)

# Update y-axis to show values in thousands
fig.update_yaxes(
    tickformat='.0f',
    ticksuffix='',
    title='Economia (kWh/mês)'
)

# Update traces
fig.update_traces(cliponaxis=False)

# Save both PNG and SVG
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

fig.show()