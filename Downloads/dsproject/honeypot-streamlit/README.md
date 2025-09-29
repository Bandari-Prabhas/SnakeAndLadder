# 🛡️ Honeypot Security Analytics System

A comprehensive cybersecurity project that uses honeypots to attract, monitor, and analyze cyber attacks in real-time with beautiful interactive visualizations using Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This project implements a **honeypot security analytics system** that:

- Deploys fake SSH and HTTP services to attract attackers
- Logs all intrusion attempts with detailed information
- Provides real-time analytics and visualizations
- Tracks attack patterns, credentials, and geographic origins
- Demonstrates practical cybersecurity concepts for learning

## ✨ Features

### 🔥 Honeypot Services

- **SSH Honeypot**: Fake SSH server that logs login attempts
- **HTTP Honeypot**: Fake admin login page that captures credentials
- Automatic logging of usernames, passwords, IPs, and timestamps

### 📊 Analytics Dashboard

- **Real-time monitoring** with auto-refresh
- **Interactive visualizations** using Plotly
- **Geographic mapping** of attack sources
- **Attack pattern analysis** (temporal, credential, behavioral)
- **Statistical summaries** and reports

### 🎨 Modern UI

- Beautiful gradient design with dark theme
- Responsive layout that works on all devices
- Interactive charts and graphs
- Live attack feed with real-time updates

### 🛠️ Additional Features

- Attack simulation for testing
- Data export (CSV, JSON)
- Configurable settings
- Log rotation and management
- Service control panel

## 🏗️ Architecture

```
┌─────────────────┐
│   Attackers     │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Honeypots│
    │ SSH/HTTP │
    └────┬─────┘
         │
    ┌────▼─────┐
    │   Logs   │
    │  JSON    │
    └────┬─────┘
         │
    ┌────▼─────┐
    │ Streamlit│
    │Dashboard │
    └──────────┘
```

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum
- Linux/Mac/Windows

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/honeypot-analytics.git
cd honeypot-analytics
```

### Step 2: Create Project Structure

```bash
mkdir -p logs data config honeypot scripts pages utils assets
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
streamlit==1.31.0
pandas==2.1.4
numpy==1.26.3
plotly==5.18.0
paramiko==3.4.0
flask==3.0.0
requests==2.31.0
psutil==5.9.7
```

## 🚀 Quick Start

### Option 1: Manual Start (Recommended for Learning)

**Terminal 1 - SSH Honeypot:**

```bash
python honeypot/ssh_honeypot.py
```

**Terminal 2 - HTTP Honeypot:**

```bash
python honeypot/http_honeypot.py
```

**Terminal 3 - Streamlit Dashboard:**

```bash
streamlit run app.py
```

### Option 2: Automated Start

```bash
python scripts/start_services.py
```

### Access the Dashboard

Open your browser and navigate to:

```
http://localhost:8501
```

## 📖 Usage

### 1. Start the System

Run the services as described in Quick Start.

### 2. Generate Test Data

Open a new terminal and run:

```bash
python scripts/simulate_attacks.py
```

Select option 5 for a full simulation.

### 3. Monitor Attacks

The Streamlit dashboard will automatically update with:

- Live attack statistics
- Real-time charts and graphs
- Geographic distribution
- Attack logs

### 4. Test the Honeypots

**Test SSH Honeypot:**

```bash
ssh root@localhost -p 2222
# Try password: admin123
```

**Test HTTP Honeypot:**
Open browser: `http://localhost:8080`
Try login: admin / password

### 5. Analyze Data

Navigate through the dashboard pages:

- **Home**: Overview and quick stats
- **Live Dashboard**: Real-time monitoring
- **Analytics**: Deep dive into patterns
- **Geographic Map**: Attack origins
- **Settings**: Configure system

## 📁 Project Structure

```
honeypot-streamlit/
│
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration
│
├── honeypot/
│   ├── __init__.py
│   ├── ssh_honeypot.py        # SSH service
│   └── http_honeypot.py       # HTTP service
│
├── pages/
│   ├── 1_🎯_Live_Dashboard.py  # Real-time monitoring
│   ├── 2_📊_Analytics.py       # Deep analytics
│   ├── 3_🌍_Geographic_Map.py  # Geographic viz
│   └── 4_⚙️_Settings.py        # System settings
│
├── scripts/
│   ├── simulate_attacks.py    # Attack simulator
│   └── start_services.py      # Service manager
│
├── logs/
│   ├── honeypot.log           # Main log file
│   └── attacks.log            # Attack logs
│
└── data/
    └── geo_cache.json         # Cached data
```

## 🖼️ Screenshots

### Main Dashboard

Real-time statistics and attack feed

### Analytics Page

Deep dive into attack patterns with interactive charts

### Geographic Map

World map showing attack origins

### Settings Panel

Configure honeypot services and system parameters

## ⚙️ Configuration

Edit `config/settings.py` to customize:

```python
# Ports
SSH_PORT = 2222
HTTP_PORT = 8080

# Logging
LOG_LEVEL = 'INFO'
MAX_LOG_SIZE_MB = 100

# Security
ENABLE_GEOBLOCKING = False
ALERT_THRESHOLD = 50
```

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :2222
# Kill process
sudo kill -9 <PID>
```

### Permission Denied

```bash
# Give execute permission
chmod +x scripts/*.py
```

### Missing Packages

```bash
pip install --upgrade -r requirements.txt
```

### SSH Connection Refused

Check if SSH honeypot is running:

```bash
ps aux | grep ssh_honeypot
```

## 📚 Learning Outcomes

This project teaches:

- **Cybersecurity Fundamentals**: Understanding attack patterns
- **Honeypot Technology**: How to deploy and monitor traps
- **Log Analysis**: Processing and analyzing security logs
- **Data Visualization**: Creating meaningful security dashboards
- **Python Programming**: Network programming, async operations
- **Real-world Security**: Practical threat intelligence

## 🎓 Use Cases

- **Educational**: Learn cybersecurity concepts
- **Research**: Study attack patterns and trends
- **Portfolio**: Showcase unique data science project
- **Security Testing**: Test network security measures
- **Threat Intelligence**: Gather real attack data

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Use it:

- On your own systems or with explicit permission
- In isolated/sandboxed environments
- For learning and research purposes

**Do not**:

- Deploy on production systems
- Use for illegal activities
- Expose to the internet without proper security

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

For questions or support:

- Open an issue on GitHub
- Email: your.email@example.com

## 🙏 Acknowledgments

- Built with Streamlit
- Uses Paramiko for SSH
- Flask for HTTP honeypot
- Plotly for visualizations

---

**Made with for cybersecurity education**

🛡️ Stay secure! 🛡️
