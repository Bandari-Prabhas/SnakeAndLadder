import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Live Dashboard", page_icon="🎯", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(139, 92, 246, 0.4);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def load_logs(log_file='logs/honeypot.log'):
    """Load logs from file"""
    events = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
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
    <h1 style='color: #a78bfa; font-size: 2.5em;'>🎯 Live Threat Dashboard</h1>
    <p style='color: #9ca3af;'>Real-time monitoring of attack patterns and threats</p>
</div>
""", unsafe_allow_html=True)

# Load data
df = load_logs()

# Real-time stats
col1, col2, col3, col4, col5 = st.columns(5)

if not df.empty:
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #ef4444; margin: 0;'>🔥 Live Attacks</h3>
            <h2 style='margin: 10px 0;'>{}</h2>
            <p style='color: #9ca3af; margin: 0;'>Total Events</p>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        unique_ips = df['source_ip'].nunique() if 'source_ip' in df.columns else 0
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #3b82f6; margin: 0;'>🌐 Source IPs</h3>
            <h2 style='margin: 10px 0;'>{}</h2>
            <p style='color: #9ca3af; margin: 0;'>Unique Addresses</p>
        </div>
        """.format(unique_ips), unsafe_allow_html=True)
    
    with col3:
        if 'timestamp' in df.columns:
            last_hour = datetime.now() - timedelta(hours=1)
            recent = len(df[df['timestamp'] > last_hour])
        else:
            recent = 0
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #f59e0b; margin: 0;'>⏰ Last Hour</h3>
            <h2 style='margin: 10px 0;'>{}</h2>
            <p style='color: #9ca3af; margin: 0;'>Recent Attacks</p>
        </div>
        """.format(recent), unsafe_allow_html=True)
    
    with col4:
        attack_types = df['type'].nunique() if 'type' in df.columns else 0
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #8b5cf6; margin: 0;'>🎯 Attack Types</h3>
            <h2 style='margin: 10px 0;'>{}</h2>
            <p style='color: #9ca3af; margin: 0;'>Different Methods</p>
        </div>
        """.format(attack_types), unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #10b981; margin: 0;'>🛡️ Block Rate</h3>
            <h2 style='margin: 10px 0;'>100%</h2>
            <p style='color: #9ca3af; margin: 0;'>Success Rate</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Attack Timeline (Last 24 Hours)")
    if not df.empty and 'timestamp' in df.columns:
        # Prepare timeline data
        df['hour'] = df['timestamp'].dt.floor('H')
        timeline = df.groupby('hour').size().reset_index(name='attacks')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timeline['hour'],
            y=timeline['attacks'],
            mode='lines+markers',
            name='Attacks',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(size=8, color='#a78bfa'),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.2)'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e5e7eb'),
            xaxis=dict(showgrid=True, gridcolor='rgba(75, 85, 99, 0.3)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(75, 85, 99, 0.3)'),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data available yet")

with col2:
    st.markdown("### 🔍 Attack Type Distribution")
    if not df.empty and 'type' in df.columns:
        type_counts = df['type'].value_counts()
        
        colors = ['#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6', '#10b981']
        
        fig = go.Figure(data=[go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont=dict(color='white', size=12)
        )])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e5e7eb'),
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No attack type data available yet")

# Top Attackers
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Top Usernames Attempted")
    if not df.empty and 'username' in df.columns:
        top_users = df['username'].value_counts().head(10)
        
        fig = go.Figure(go.Bar(
            y=top_users.index,
            x=top_users.values,
            orientation='h',
            marker=dict(color='#3b82f6', line=dict(color='#1e40af', width=1))
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e5e7eb'),
            xaxis=dict(showgrid=True, gridcolor='rgba(75, 85, 99, 0.3)'),
            yaxis=dict(showgrid=False),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No username data available yet")

with col2:
    st.markdown("### 🔑 Top Passwords Attempted")
    if not df.empty and 'password' in df.columns:
        top_pass = df['password'].value_counts().head(10)
        
        fig = go.Figure(go.Bar(
            y=top_pass.index,
            x=top_pass.values,
            orientation='h',
            marker=dict(color='#f59e0b', line=dict(color='#b45309', width=1))
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e5e7eb'),
            xaxis=dict(showgrid=True, gridcolor='rgba(75, 85, 99, 0.3)'),
            yaxis=dict(showgrid=False),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No password data available yet")

# Recent attacks table
st.markdown("### 🚨 Live Attack Feed")
if not df.empty:
    recent_df = df.tail(20).sort_values('timestamp', ascending=False)
    
    # Format for display
    display_df = pd.DataFrame({
        'Time': recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S') if 'timestamp' in recent_df.columns else 'N/A',
        'Source IP': recent_df['source_ip'] if 'source_ip' in recent_df.columns else 'N/A',
        'Type': recent_df['type'] if 'type' in recent_df.columns else 'N/A',
        'Username': recent_df['username'] if 'username' in recent_df.columns else 'N/A',
        'Status': '🛡️ BLOCKED'
    })
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
else:
    st.info("No attack data available. Start the honeypot to see live attacks.")

# Auto refresh
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()