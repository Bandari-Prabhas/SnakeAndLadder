import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from collections import Counter

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

def load_logs():
    events = []
    if os.path.exists('logs/honeypot.log'):
        with open('logs/honeypot.log', 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line.strip()))
                except:
                    continue
    
    if events:
        df = pd.DataFrame(events)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()

# Header
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='color: #a78bfa; font-size: 2.5em;'>📊 Deep Analytics</h1>
    <p style='color: #9ca3af;'>Comprehensive analysis of attack patterns and trends</p>
</div>
""", unsafe_allow_html=True)

df = load_logs()

if df.empty:
    st.warning("⚠️ No data available for analysis. Start the honeypot services first.")
    st.stop()

# Time range selector
st.markdown("### ⏰ Analysis Time Range")
col1, col2, col3 = st.columns(3)

with col1:
    time_range = st.selectbox(
        "Select Time Range",
        ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last Week", "All Time"]
    )

# Filter data based on time range
now = datetime.now()
if time_range == "Last Hour":
    df = df[df['timestamp'] > now - timedelta(hours=1)]
elif time_range == "Last 6 Hours":
    df = df[df['timestamp'] > now - timedelta(hours=6)]
elif time_range == "Last 24 Hours":
    df = df[df['timestamp'] > now - timedelta(days=1)]
elif time_range == "Last Week":
    df = df[df['timestamp'] > now - timedelta(weeks=1)]

# Key metrics
st.markdown("---")
st.markdown("### 📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_attacks = len(df)
    st.metric("Total Attacks", f"{total_attacks:,}")

with col2:
    unique_ips = df['source_ip'].nunique() if 'source_ip' in df.columns else 0
    st.metric("Unique Sources", f"{unique_ips:,}")

with col3:
    if 'username' in df.columns:
        unique_users = df['username'].nunique()
    else:
        unique_users = 0
    st.metric("Username Attempts", f"{unique_users:,}")

with col4:
    avg_per_hour = total_attacks / max(1, (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600) if not df.empty and 'timestamp' in df.columns else 0
    st.metric("Avg Attacks/Hour", f"{avg_per_hour:.1f}")

st.markdown("---")

# Advanced Analytics
tab1, tab2, tab3, tab4 = st.tabs(["⏰ Temporal Analysis", "👤 Credential Analysis", "🎯 Attack Patterns", "📋 Statistical Summary"])

with tab1:
    st.markdown("#### 📅 Attack Distribution Over Time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly distribution
        if 'timestamp' in df.columns:
            df['hour'] = df['timestamp'].dt.hour
            hourly_dist = df.groupby('hour').size().reset_index(name='count')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=hourly_dist['hour'],
                y=hourly_dist['count'],
                marker=dict(
                    color=hourly_dist['count'],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=hourly_dist['count'],
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Attacks by Hour of Day",
                xaxis_title="Hour",
                yaxis_title="Number of Attacks",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e5e7eb'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Daily distribution
        if 'timestamp' in df.columns:
            df['date'] = df['timestamp'].dt.date
            daily_dist = df.groupby('date').size().reset_index(name='count')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_dist['date'],
                y=daily_dist['count'],
                mode='lines+markers',
                line=dict(color='#8b5cf6', width=3),
                marker=dict(size=10, color='#a78bfa'),
                fill='tozeroy',
                fillcolor='rgba(139, 92, 246, 0.3)'
            ))
            
            fig.update_layout(
                title="Attacks by Day",
                xaxis_title="Date",
                yaxis_title="Number of Attacks",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e5e7eb'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
# Heatmap
st.markdown("#### 🔥 Attack Intensity Heatmap")
if 'timestamp' in df.columns:
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['hour_of_day'] = df['timestamp'].dt.hour
    
    # Build pivot table
    heatmap_data = df.pivot_table(
        index='day_of_week',
        columns='hour_of_day',
        values='source_ip',  # or just count rows
        aggfunc='count',
        fill_value=0
    )
    
    # Ensure correct day order
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = heatmap_data.reindex(days_order)

    fig = px.imshow(
        heatmap_data.values,
        labels=dict(x="Hour of Day", y="Day of Week", color="Attacks"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        title="Heatmap of Attack Intensity",
        xaxis=dict(side="top"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
