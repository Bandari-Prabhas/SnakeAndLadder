from flask import Flask, request, render_template_string, jsonify
import json
import logging
from datetime import datetime
import hashlib
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_attack(attack_data):
    """Log attack to file"""
    os.makedirs('logs', exist_ok=True)
    with open('logs/honeypot.log', 'a') as f:
        f.write(json.dumps(attack_data) + '\n')

# Fake login page HTML with modern design
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Login - Admin Panel</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .login-container {
            background: white;
            padding: 50px 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: white;
            margin-bottom: 15px;
        }
        
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .input-group {
            margin-bottom: 25px;
            position: relative;
        }
        
        .input-group label {
            display: block;
            color: #555;
            margin-bottom: 8px;
            font-weight: 500;
            font-size: 14px;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .input-group input::placeholder {
            color: #999;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            border: 1px solid #fcc;
            animation: shake 0.5s ease;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .footer {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 30px;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .checkbox-group input {
            margin-right: 8px;
        }
        
        .checkbox-group label {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <div class="logo-icon">🔒</div>
            <h2>System Login</h2>
            <p class="subtitle">Enter your credentials to continue</p>
        </div>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form action="/login" method="POST">
            <div class="input-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Enter your username" required>
            </div>
            
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>
            
            <div class="checkbox-group">
                <input type="checkbox" id="remember" name="remember">
                <label for="remember">Remember me</label>
            </div>
            
            <button type="submit">Sign In</button>
        </form>
        
        <div class="footer">
            <p>© 2025 System Administration Panel</p>
            <p>Secure Access Portal v2.0</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve fake login page"""
    # Log the visit
    attack_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": "http_visit",
        "source_ip": request.remote_addr,
        "path": request.path,
        "method": request.method,
        "user_agent": request.headers.get('User-Agent'),
        "referer": request.headers.get('Referer', 'direct')
    }
    log_attack(attack_data)
    logging.info(f"Visit from {request.remote_addr} to {request.path}")
    
    return render_template_string(LOGIN_PAGE, error=None)

@app.route('/login', methods=['POST'])
def login():
    """Handle login attempts"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Log login attempt
    attack_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": "http_attack",
        "attack_type": "login_attempt",
        "source_ip": request.remote_addr,
        "username": username,
        "password": password,
        "password_hash": hashlib.sha256(password.encode()).hexdigest(),
        "user_agent": request.headers.get('User-Agent'),
        "referer": request.headers.get('Referer'),
        "method": request.method
    }
    log_attack(attack_data)
    logging.warning(f"Login attempt from {request.remote_addr} - User: {username}, Pass: {password}")
    
    # Always return error
    return render_template_string(LOGIN_PAGE, error="Invalid username or password. Please try again.")

@app.route('/admin')
@app.route('/administrator')
@app.route('/wp-admin')
@app.route('/phpmyadmin')
@app.route('/.env')
@app.route('/config')
@app.route('/backup')
@app.route('/database')
def common_paths():
    """Catch common scanning paths"""
    attack_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": "http_attack",
        "attack_type": "path_scanning",
        "source_ip": request.remote_addr,
        "path": request.path,
        "method": request.method,
        "user_agent": request.headers.get('User-Agent'),
        "query_string": request.query_string.decode()
    }
    log_attack(attack_data)
    logging.warning(f"Path scanning from {request.remote_addr} - Path: {request.path}")
    
    return "404 Not Found", 404

@app.route('/<path:path>')
def catch_all(path):
    """Catch all other requests"""
    attack_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": "http_attack",
        "attack_type": "unknown_path",
        "source_ip": request.remote_addr,
        "path": f"/{path}",
        "method": request.method,
        "user_agent": request.headers.get('User-Agent'),
        "query_string": request.query_string.decode()
    }
    log_attack(attack_data)
    logging.info(f"Unknown path from {request.remote_addr}: /{path}")
    
    return "404 Not Found", 404

@app.errorhandler(404)
def not_found(error):
    return "404 Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    return "500 Internal Server Error", 500

if __name__ == '__main__':
    print("=" * 60)
    print("HTTP HONEYPOT SERVICE")
    print("=" * 60)
    print("[+] Starting HTTP Honeypot on port 8080")
    print("[+] Access at: http://localhost:8080")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)