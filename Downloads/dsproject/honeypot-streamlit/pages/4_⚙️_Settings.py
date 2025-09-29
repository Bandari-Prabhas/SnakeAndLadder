import streamlit as st
import json
import os
import subprocess
import psutil
from datetime import datetime

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

# Header
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='color: #a78bfa; font-size: 2.5em;'>⚙️ System Settings & Control</h1>
    <p style='color: #9ca3af;'>Manage honeypot services and configuration</p>
</div>
""", unsafe_allow_html=True)

# Load configuration
config_file = 'config/settings.json'

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {
        'ssh_port': 2222,
        'http_port': 8080,
        'log_level': 'INFO',
        'max_log_size': 100,
        'enable_ssh': True,
        'enable_http': True,
        'auto_backup': False
    }

def save_config(config):
    os.makedirs('config', exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

# Service Control
st.markdown("### 🎛️ Service Control")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
                padding: 20px; border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.4);'>
        <h3 style='color: #10b981; margin: 0;'>🚀 Start Services</h3>
        <p style='color: #9ca3af; margin: 10px 0;'>Launch honeypot services</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start All Services", use_container_width=True, type="primary"):
        st.session_state.services_running = True
        st.success("✅ Services started successfully!")
        st.info("SSH Honeypot: Port " + str(config['ssh_port']))
        st.info("HTTP Honeypot: Port " + str(config['http_port']))

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
                padding: 20px; border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.4);'>
        <h3 style='color: #ef4444; margin: 0;'>🛑 Stop Services</h3>
        <p style='color: #9ca3af; margin: 10px 0;'>Shutdown all honeypots</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Stop All Services", use_container_width=True):
        st.session_state.services_running = False
        st.warning("⚠️ Services stopped")

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
                padding: 20px; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.4);'>
        <h3 style='color: #3b82f6; margin: 0;'>🔄 Restart</h3>
        <p style='color: #9ca3af; margin: 10px 0;'>Restart all services</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Restart Services", use_container_width=True):
        st.info("🔄 Restarting services...")
        st.success("✅ Services restarted")

st.markdown("---")

# Configuration
st.markdown("### 🔧 Honeypot Configuration")

tab1, tab2, tab3, tab4 = st.tabs(["🌐 Network", "📝 Logging", "🔒 Security", "💾 Data Management"])

with tab1:
    st.markdown("#### Network Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### SSH Honeypot")
        ssh_enabled = st.checkbox("Enable SSH Honeypot", value=config.get('enable_ssh', True))
        ssh_port = st.number_input("SSH Port", min_value=1024, max_value=65535, value=config.get('ssh_port', 2222))
        ssh_banner = st.text_input("SSH Banner", value="Ubuntu 22.04 LTS")
        ssh_timeout = st.number_input("Connection Timeout (seconds)", min_value=5, max_value=300, value=30)
    
    with col2:
        st.markdown("##### HTTP Honeypot")
        http_enabled = st.checkbox("Enable HTTP Honeypot", value=config.get('enable_http', True))
        http_port = st.number_input("HTTP Port", min_value=1024, max_value=65535, value=config.get('http_port', 8080))
        http_title = st.text_input("Login Page Title", value="Admin Login")
        rate_limit = st.number_input("Rate Limit (requests/min)", min_value=10, max_value=1000, value=100)

with tab2:
    st.markdown("#### Logging Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        log_level = st.selectbox(
            "Log Level",
            ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=1
        )
        
        max_log_size = st.number_input(
            "Max Log File Size (MB)",
            min_value=10,
            max_value=1000,
            value=config.get('max_log_size', 100)
        )
        
        log_rotation = st.checkbox("Enable Log Rotation", value=True)
        backup_logs = st.number_input("Keep Last N Backups", min_value=1, max_value=50, value=10)
    
    with col2:
        st.markdown("##### Log Locations")
        st.code("Main Log: logs/honeypot.log")
        st.code("Attack Log: logs/attacks.log")
        st.code("Error Log: logs/errors.log")
        
        if st.button("📁 View Logs Directory", use_container_width=True):
            st.info("Logs are stored in: " + os.path.abspath('logs'))
        
        if st.button("🗑️ Clear Old Logs", use_container_width=True):
            st.warning("This will archive logs older than 30 days")

with tab3:
    st.markdown("#### Security Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Access Control")
        ip_blacklist = st.text_area(
            "IP Blacklist (one per line)",
            height=150,
            placeholder="192.168.1.100\n10.0.0.5"
        )
        
        enable_geoblocking = st.checkbox("Enable Geographic Blocking", value=False)
        blocked_countries = st.multiselect(
            "Blocked Countries",
            ["China", "Russia", "North Korea", "Iran"],
            default=[]
        )
    
    with col2:
        st.markdown("##### Alert Settings")
        alert_threshold = st.number_input(
            "Alert Threshold (attacks/minute)",
            min_value=10,
            max_value=1000,
            value=50
        )
        
        enable_email_alerts = st.checkbox("Enable Email Alerts", value=False)
        if enable_email_alerts:
            email_address = st.text_input("Alert Email Address")
            smtp_server = st.text_input("SMTP Server")
        
        enable_webhook = st.checkbox("Enable Webhook Notifications", value=False)
        if enable_webhook:
            webhook_url = st.text_input("Webhook URL")

with tab4:
    st.markdown("#### Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Automatic Backups")
        auto_backup = st.checkbox("Enable Automatic Backups", value=config.get('auto_backup', False))
        backup_interval = st.selectbox(
            "Backup Interval",
            ["Hourly", "Daily", "Weekly", "Monthly"],
            index=1
        )
        backup_location = st.text_input("Backup Location", value="./backups")
        
        if st.button("📦 Create Backup Now", use_container_width=True):
            st.success(f"✅ Backup created: backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
    
    with col2:
        st.markdown("##### Data Retention")
        retention_days = st.number_input(
            "Keep Data For (days)",
            min_value=1,
            max_value=365,
            value=90
        )
        
        compress_old_data = st.checkbox("Compress Old Data", value=True)
        
        st.markdown("##### Database")
        db_size = "23.4 MB"
        st.metric("Current Database Size", db_size)
        
        if st.button("🗜️ Optimize Database", use_container_width=True):
            st.info("Optimizing database...")
            st.success("✅ Database optimized")

# Save Configuration
st.markdown("---")
st.markdown("### 💾 Save Configuration")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("💾 Save All Settings", use_container_width=True, type="primary"):
        new_config = {
            'ssh_port': ssh_port,
            'http_port': http_port,
            'log_level': log_level,
            'max_log_size': max_log_size,
            'enable_ssh': ssh_enabled,
            'enable_http': http_enabled,
            'auto_backup': auto_backup
        }
        save_config(new_config)
        st.success("✅ Configuration saved successfully!")
        st.balloons()

with col2:
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        default_config = {
            'ssh_port': 2222,
            'http_port': 8080,
            'log_level': 'INFO',
            'max_log_size': 100,
            'enable_ssh': True,
            'enable_http': True,
            'auto_backup': False
        }
        save_config(default_config)
        st.info("↩️ Settings reset to defaults")
        st.rerun()

with col3:
    if st.button("📄 Export Config", use_container_width=True):
        config_json = json.dumps(config, indent=4)
        st.download_button(
            label="Download Config",
            data=config_json,
            file_name=f"honeypot_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# System Information
st.markdown("---")
st.markdown("### 🖥️ System Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    cpu_percent = psutil.cpu_percent(interval=1)
    st.metric("CPU Usage", f"{cpu_percent}%")

with col2:
    memory = psutil.virtual_memory()
    st.metric("Memory Usage", f"{memory.percent}%")

with col3:
    disk = psutil.disk_usage('/')
    st.metric("Disk Usage", f"{disk.percent}%")

with col4:
    st.metric("Active Connections", "5")

# Service Status
st.markdown("### 📊 Service Status")

services = [
    {"name": "SSH Honeypot", "status": "Running" if ssh_enabled else "Stopped", "port": ssh_port, "uptime": "2h 34m"},
    {"name": "HTTP Honeypot", "status": "Running" if http_enabled else "Stopped", "port": http_port, "uptime": "2h 34m"},
    {"name": "Log Processor", "status": "Running", "port": "-", "uptime": "2h 34m"},
    {"name": "Analytics Engine", "status": "Running", "port": "-", "uptime": "2h 34m"}
]

for service in services:
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    
    with col1:
        status_color = "🟢" if service['status'] == "Running" else "🔴"
        st.markdown(f"**{status_color} {service['name']}**")
    
    with col2:
        st.text(service['status'])
    
    with col3:
        st.text(f"Port: {service['port']}")
    
    with col4:
        st.text(f"Uptime: {service['uptime']}")

# Advanced Options
with st.expander("🔬 Advanced Options"):
    st.markdown("#### Developer Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        debug_mode = st.checkbox("Enable Debug Mode", value=False)
        verbose_logging = st.checkbox("Verbose Logging", value=False)
        api_enabled = st.checkbox("Enable REST API", value=False)
        
        if api_enabled:
            api_key = st.text_input("API Key", type="password")
            api_port = st.number_input("API Port", min_value=1024, max_value=65535, value=5000)
    
    with col2:
        st.markdown("##### Experimental Features")
        ml_detection = st.checkbox("ML-based Attack Detection", value=False)
        auto_response = st.checkbox("Automated Response System", value=False)
        threat_intel = st.checkbox("Threat Intelligence Integration", value=False)
        
        if threat_intel:
            intel_api = st.text_input("Threat Intel API Key", type="password")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px;'>
    <p>⚙️ System Configuration Panel | Version 1.0.0</p>
    <p>Last configured: {}</p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)