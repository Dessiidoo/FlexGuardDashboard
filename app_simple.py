import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.subplots as sp

st.set_page_config(
    page_title="FlexGuard Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ FlexGuard Dashboard - Test")

heatmap_data = np.random.rand(10, 10)
uptime_data = np.random.uniform(90, 100, size=10)
components = [f"Component {i}" for i in range(1, 6)]
cost_savings = np.random.uniform(5, 25, size=5)

fig = sp.make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "heatmap"}, {"type": "bar"}],
           [{"colspan": 2, "type": "scatter"}, None]],
    subplot_titles=("FlexGuard: Detection Heatmap",
                    "FlexGuard: Cost Insights",
                    "FlexGuard: Reliability / System Uptime")
)

fig.add_trace(
    go.Heatmap(
        z=heatmap_data,
        colorscale='Viridis',
        colorbar=dict(title="Anomaly Intensity"),
        hovertemplate="X:%{x}, Y:%{y}, Value:%{z}<extra></extra>"
    ),
    row=1, col=1
)

fig.add_trace(
    go.Bar(
        x=components,
        y=cost_savings,
        name="Cost Savings %",
        marker_color='gold',
        hovertemplate="%{x}: %{y:.1f}% savings<extra></extra>"
    ),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(
        x=list(range(1, 11)),
        y=uptime_data,
        mode='lines+markers',
        name="Uptime %",
        line=dict(color='cyan', width=3),
        hovertemplate="Step %{x}: %{y:.1f}% uptime<extra></extra>"
    ),
    row=2, col=1
)

fig.update_layout(
    title="FlexGuard Dashboard",
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white', size=12),
    height=700,
    showlegend=True,
    margin=dict(t=100, l=50, r=50, b=50)
)

st.plotly_chart(fig, use_container_width=True)

st.success("✅ Dashboard loaded successfully!")
