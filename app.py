import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.subplots as sp
from datetime import datetime, timedelta
from db_setup import SessionLocal, AnomalyData, CostData, UptimeData
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import time

st.set_page_config(
    page_title="FlexGuard Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ FlexGuard Dashboard")

session = SessionLocal()

with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    
    st.subheader("📅 Date Range Filter")
    end_date = datetime.now().date()
    start_date = (datetime.now() - timedelta(days=7)).date()
    
    date_range = st.date_input(
        "Select Date Range",
        value=(start_date, end_date),
        max_value=end_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = start_date
    
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    st.subheader("🚨 Alert Thresholds")
    anomaly_threshold = st.slider(
        "Anomaly Alert Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Alert when anomaly intensity exceeds this threshold"
    )
    
    uptime_threshold = st.slider(
        "Minimum Uptime %",
        min_value=0.0,
        max_value=100.0,
        value=95.0,
        step=1.0,
        help="Alert when uptime falls below this threshold"
    )
    
    st.subheader("🔄 Auto-Refresh")
    auto_refresh = st.checkbox("Enable Auto-Refresh", value=False)
    refresh_interval = 10
    if auto_refresh:
        refresh_interval = st.slider(
            "Refresh Interval (seconds)",
            min_value=5,
            max_value=60,
            value=10,
            step=5
        )
    
    st.subheader("📊 Comparative Analysis")
    enable_comparison = st.checkbox("Enable Time Period Comparison", value=False)
    
    if enable_comparison:
        comparison_days = st.slider(
            "Compare with previous days",
            min_value=1,
            max_value=30,
            value=7,
            step=1
        )

anomaly_records = session.query(AnomalyData).filter(
    AnomalyData.timestamp >= start_datetime,
    AnomalyData.timestamp <= end_datetime
).all()

cost_records = session.query(CostData).filter(
    CostData.timestamp >= start_datetime,
    CostData.timestamp <= end_datetime
).all()

uptime_records = session.query(UptimeData).filter(
    UptimeData.timestamp >= start_datetime,
    UptimeData.timestamp <= end_datetime
).all()

if anomaly_records:
    latest_date = max([r.timestamp for r in anomaly_records])
    latest_anomalies = [r for r in anomaly_records if r.timestamp == latest_date]
    
    heatmap_data = np.zeros((10, 10))
    for record in latest_anomalies:
        heatmap_data[record.y_coord, record.x_coord] = record.intensity
else:
    heatmap_data = np.random.rand(10, 10)

if cost_records:
    cost_df = pd.DataFrame([{
        'component': r.component,
        'savings_percent': r.savings_percent,
        'timestamp': r.timestamp
    } for r in cost_records])
    
    cost_avg = cost_df.groupby('component')['savings_percent'].mean().reset_index()
    components = cost_avg['component'].tolist()
    cost_savings = cost_avg['savings_percent'].tolist()
else:
    components = [f"Component {i}" for i in range(1, 6)]
    cost_savings = np.random.uniform(5, 25, size=5).tolist()

if uptime_records:
    uptime_df = pd.DataFrame([{
        'timestamp': r.timestamp,
        'uptime_percent': r.uptime_percent
    } for r in uptime_records])
    uptime_df = uptime_df.sort_values('timestamp')
    uptime_data = uptime_df['uptime_percent'].tolist()
    uptime_timestamps = uptime_df['timestamp'].tolist()
else:
    uptime_data = np.random.uniform(90, 100, size=10).tolist()
    uptime_timestamps = list(range(1, 11))

if enable_comparison:
    comp_start = start_datetime - timedelta(days=comparison_days)
    comp_end = end_datetime - timedelta(days=comparison_days)
    
    comp_uptime = session.query(UptimeData).filter(
        UptimeData.timestamp >= comp_start,
        UptimeData.timestamp <= comp_end
    ).all()
    
    if comp_uptime:
        comp_uptime_df = pd.DataFrame([{
            'timestamp': r.timestamp,
            'uptime_percent': r.uptime_percent
        } for r in comp_uptime])
        comp_uptime_df = comp_uptime_df.sort_values('timestamp')
        comp_uptime_df['shifted_timestamp'] = comp_uptime_df['timestamp'] + timedelta(days=comparison_days)
        comp_uptime_data = comp_uptime_df['uptime_percent'].tolist()
        comp_uptime_timestamps = comp_uptime_df['shifted_timestamp'].tolist()

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

anomaly_alerts = np.sum(heatmap_data > anomaly_threshold)

alert_coords_x = []
alert_coords_y = []
for i in range(10):
    for j in range(10):
        if heatmap_data[i, j] > anomaly_threshold:
            alert_coords_x.append(j)
            alert_coords_y.append(i)

if alert_coords_x:
    fig.add_trace(
        go.Scatter(
            x=alert_coords_x,
            y=alert_coords_y,
            mode='markers',
            marker=dict(
                symbol='x',
                size=12,
                color='red',
                line=dict(color='white', width=2)
            ),
            name='Alert Threshold Exceeded',
            hovertemplate="ALERT at X:%{x}, Y:%{y}<extra></extra>",
            showlegend=False
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
        x=uptime_timestamps if uptime_records else list(range(1, len(uptime_data)+1)),
        y=uptime_data,
        mode='lines+markers',
        name="Current Period Uptime %",
        line=dict(color='cyan', width=3),
        hovertemplate="Time: %{x}<br>Uptime: %{y:.1f}%<extra></extra>"
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=uptime_timestamps if uptime_records else list(range(1, len(uptime_data)+1)),
        y=[uptime_threshold] * len(uptime_data),
        mode='lines',
        name=f"Alert Threshold ({uptime_threshold}%)",
        line=dict(color='red', width=2, dash='dash'),
        hovertemplate=f"Threshold: {uptime_threshold}%<extra></extra>"
    ),
    row=2, col=1
)

if enable_comparison and comp_uptime:
    fig.add_trace(
        go.Scatter(
            x=comp_uptime_timestamps,
            y=comp_uptime_data,
            mode='lines+markers',
            name=f"Previous Period (-{comparison_days}d)",
            line=dict(color='orange', width=2, dash='dot'),
            hovertemplate="Time: %{x}<br>Uptime: %{y:.1f}%<extra></extra>"
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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚨 Anomaly Alerts",
        f"{anomaly_alerts} cells",
        delta=f"Threshold: {anomaly_threshold}",
        delta_color="inverse"
    )

with col2:
    avg_cost_savings = np.mean(cost_savings) if cost_savings else 0
    st.metric(
        "💰 Avg Cost Savings",
        f"{avg_cost_savings:.1f}%",
        delta="Across all components"
    )

with col3:
    avg_uptime = np.mean(uptime_data) if uptime_data else 0
    uptime_alerts = sum(1 for u in uptime_data if u < uptime_threshold)
    st.metric(
        "⚡ Avg Uptime",
        f"{avg_uptime:.1f}%",
        delta=f"{uptime_alerts} alerts" if uptime_alerts > 0 else "No alerts",
        delta_color="inverse" if uptime_alerts > 0 else "normal"
    )

st.subheader("📥 Data Export")

col1, col2 = st.columns(2)

with col1:
    export_df = pd.DataFrame({
        'Metric': ['Anomaly Alerts', 'Avg Cost Savings', 'Avg Uptime', 'Uptime Alerts'],
        'Value': [
            f"{anomaly_alerts} cells",
            f"{avg_cost_savings:.1f}%",
            f"{avg_uptime:.1f}%",
            f"{uptime_alerts}"
        ]
    })
    
    csv_buffer = BytesIO()
    export_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    st.download_button(
        label="📄 Download CSV Report",
        data=csv_buffer,
        file_name=f"flexguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col2:
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph(f"FlexGuard Dashboard Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    data = [['Metric', 'Value']] + [[row['Metric'], row['Value']] for _, row in export_df.iterrows()]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    
    doc.build(elements)
    pdf_buffer.seek(0)
    
    st.download_button(
        label="📑 Download PDF Report",
        data=pdf_buffer,
        file_name=f"flexguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )

session.close()

if auto_refresh:
    if 'last_refresh_time' not in st.session_state:
        st.session_state.last_refresh_time = time.time()
    
    time_since_refresh = time.time() - st.session_state.last_refresh_time
    
    if time_since_refresh >= refresh_interval:
        st.session_state.last_refresh_time = time.time()
        st.rerun()
