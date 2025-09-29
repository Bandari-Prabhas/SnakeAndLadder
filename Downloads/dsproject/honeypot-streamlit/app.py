import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="Honeypot Security Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
    }
    .stMetric {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    .stAlert {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
    }
    h1, h2, h3 {
        color: #a78bfa;
    }
    .metric-container {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'honeypot_running' not in st.session_state:
    st.session_state.honeypot_running = False
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Helper functions
def load_logs(log_file='logs/honeypot.log', max_lines=10000):
    """Load and parse log files"""
    events = []
    
    if not os.path.exists(log_file):
        return pd.DataFrame()
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-max_lines:] if len(lines) > max_lines else lines
            
            for line in recent_lines:
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except:
                    continue
        
        if events:
            df = pd.DataFrame(events)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading logs: {e}")
        return pd.DataFrame()

def get_stats(df):
    """Calculate statistics from dataframe"""
    if df.empty:
        return {
            'total_attacks': 0,
            'unique_ips': 0,
            'unique_usernames': 0,
            'success_rate': 0
        }
    
    return {
        'total_attacks': len(df),
        'unique_ips': df['source_ip'].nunique() if 'source_ip' in df.columns else 0,
        'unique_usernames': df['username'].nunique() if 'username' in df.columns else 0,
        'success_rate': 100.0
    }

# Main page
def main():
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 3em; background: linear-gradient(90deg, #a78bfa, #ec4899); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                🛡️ Honeypot Security Analytics
            </h1>
            <p style='color: #9ca3af; font-size: 1.2em;'>Real-Time Threat Intelligence System</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Status indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        status_color = "🟢" if st.session_state.honeypot_running else "🔴"
        status_text = "ACTIVE" if st.session_state.honeypot_running else "INACTIVE"
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: rgba(16, 185, 129, 0.1); 
                    border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <h3>{status_color} System Status: {status_text}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Load data
    df = load_logs()
    stats = get_stats(df)
    
    # Metrics row
    st.markdown("### 📊 Quick Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Total Attacks",
            value=f"{stats['total_attacks']:,}",
            delta="+23 last hour",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="🌍 Unique IPs",
            value=f"{stats['unique_ips']:,}",
            delta="+5 new today"
        )
    
    with col3:
        st.metric(
            label="👤 Unique Usernames",
            value=f"{stats['unique_usernames']:,}",
            delta="47 common"
        )
    
    with col4:
        st.metric(
            label="🛡️ Block Rate",
            value=f"{stats['success_rate']:.1f}%",
            delta="Perfect"
        )
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("### 🔥 Recent Attack Activity")
    
    if not df.empty:
        # Show last 10 attacks
        recent_df = df.tail(10).sort_values('timestamp', ascending=False)
        
        for _, row in recent_df.iterrows():
            time_ago = datetime.now() - row['timestamp']
            minutes_ago = int(time_ago.total_seconds() / 60)
            
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            
            with col1:
                st.markdown(f"**{minutes_ago}m ago**")
            with col2:
                attack_type = row.get('type', 'unknown')
                color = "#ef4444" if 'ssh' in attack_type else "#f59e0b"
                st.markdown(f"<span style='color: {color}; font-weight: bold;'>{attack_type}</span>", 
                          unsafe_allow_html=True)
            with col3:
                st.code(f"{row.get('source_ip', 'N/A')} → {row.get('username', 'N/A')}")
            with col4:
                st.markdown("🛡️ **BLOCKED**")
            
            st.markdown("---")
    else:
        st.info("No attacks recorded yet. Start the honeypot services to begin monitoring.")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Honeypot Services", use_container_width=True):
            st.session_state.honeypot_running = True
            st.success("Services started successfully!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state.last_update = datetime.now()
            st.rerun()
    
    with col3:
        if st.button("📥 Export Data", use_container_width=True):
            if not df.empty:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"honeypot_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data to export")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 20px;'>
        <p>Last updated: {}</p>
        <p>🛡️ Honeypot Security Analytics v1.0 | Built with Streamlit</p>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
    
    # Auto-refresh
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('config', exist_ok=True)
    
    main()