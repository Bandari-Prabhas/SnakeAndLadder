"""
Configuration settings for Honeypot Security Analytics System
"""

# Network Configuration
SSH_PORT = 2222
HTTP_PORT = 8080
STREAMLIT_PORT = 8501

# Host Configuration
SSH_HOST = '0.0.0.0'
HTTP_HOST = '0.0.0.0'

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_DIR = 'logs'
MAIN_LOG_FILE = 'logs/honeypot.log'
ATTACK_LOG_FILE = 'logs/attacks.log'
ERROR_LOG_FILE = 'logs/errors.log'

# Log Rotation
MAX_LOG_SIZE_MB = 100
BACKUP_COUNT = 10

# SSH Honeypot Configuration
SSH_BANNER = "Ubuntu 22.04.1 LTS"
SSH_TIMEOUT = 30
SSH_MAX_CONNECTIONS = 100

# HTTP Honeypot Configuration
HTTP_TITLE = "System Login"
HTTP_SUBTITLE = "Admin Panel"
HTTP_RATE_LIMIT = 100  # requests per minute

# Data Retention
DATA_RETENTION_DAYS = 90
COMPRESS_OLD_DATA = True

# Security Settings
ENABLE_GEOBLOCKING = False
BLOCKED_COUNTRIES = []
IP_BLACKLIST = []

# Alert Configuration
ALERT_THRESHOLD = 50  # attacks per minute
ENABLE_EMAIL_ALERTS = False
EMAIL_ADDRESS = ""
SMTP_SERVER = ""
SMTP_PORT = 587

# Webhook Configuration
ENABLE_WEBHOOK = False
WEBHOOK_URL = ""

# Database Configuration
DB_TYPE = "json"  # json or sqlite
DB_PATH = "data/honeypot.db"

# Backup Configuration
AUTO_BACKUP = False
BACKUP_INTERVAL = "daily"  # hourly, daily, weekly, monthly
BACKUP_DIR = "backups"

# Analytics Configuration
MAX_DISPLAY_RECORDS = 10000
REFRESH_INTERVAL_SECONDS = 5

# GeoIP Configuration
GEOIP_ENABLED = False
GEOIP_DATABASE = "data/GeoLite2-City.mmdb"

# Experimental Features
ML_DETECTION = False
AUTO_RESPONSE = False
THREAT_INTEL_INTEGRATION = False

# UI Configuration
THEME = "dark"
CHART_COLOR_SCHEME = ["#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6", "#10b981"]

# Service Control
ENABLE_SSH_HONEYPOT = True
ENABLE_HTTP_HONEYPOT = True

# Debug Settings
DEBUG_MODE = False
VERBOSE_LOGGING = False