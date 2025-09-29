import paramiko
import socket
import threading
import json
import logging
from datetime import datetime
import hashlib
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SSHHoneypot(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event_log = []
        
    def check_auth_password(self, username, password):
        """Log password authentication attempts"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "ssh_attack",
            "source_ip": self.client_ip,
            "username": username,
            "password": password,
            "password_hash": hashlib.sha256(password.encode()).hexdigest(),
            "auth_method": "password",
            "success": False
        }
        self.log_event(event)
        logging.warning(f"SSH login attempt from {self.client_ip} - User: {username}, Pass: {password}")
        return paramiko.AUTH_FAILED
    
    def check_auth_publickey(self, username, key):
        """Log public key authentication attempts"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "ssh_attack",
            "source_ip": self.client_ip,
            "username": username,
            "auth_method": "publickey",
            "key_type": key.get_name(),
            "key_fingerprint": hashlib.md5(key.asbytes()).hexdigest(),
            "success": False
        }
        self.log_event(event)
        logging.warning(f"SSH pubkey attempt from {self.client_ip} - User: {username}")
        return paramiko.AUTH_FAILED
    
    def get_allowed_auths(self, username):
        """Return allowed authentication methods"""
        return "password,publickey"
    
    def check_channel_request(self, kind, chanid):
        """Handle channel requests"""
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_channel_shell_request(self, channel):
        """Handle shell requests"""
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        """Handle PTY requests"""
        return True
    
    def log_event(self, event):
        """Write event to log file"""
        os.makedirs('logs', exist_ok=True)
        with open('logs/honeypot.log', 'a') as f:
            f.write(json.dumps(event) + '\n')

def generate_host_key():
    """Generate RSA host key for SSH server"""
    try:
        return paramiko.RSAKey.generate(2048)
    except Exception as e:
        logging.error(f"Error generating host key: {e}")
        # Create a simple key file if generation fails
        key = paramiko.RSAKey.generate(1024)
        return key

def handle_connection(client_socket, client_addr):
    """Handle incoming SSH connection"""
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(generate_host_key())
        
        server = SSHHoneypot(client_addr[0])
        transport.start_server(server=server)
        
        channel = transport.accept(20)
        if channel is None:
            logging.info(f"No channel from {client_addr[0]}")
            return
        
        logging.info(f"Channel established from {client_addr[0]}")
        
        # Send fake welcome message
        welcome_msg = b"Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.0-56-generic x86_64)\r\n\r\n"
        welcome_msg += b"Last login: " + datetime.now().strftime("%a %b %d %H:%M:%S %Y").encode() + b" from 192.168.1.1\r\n"
        welcome_msg += b"$ "
        
        channel.send(welcome_msg)
        
        # Keep connection alive and log commands
        channel.settimeout(30)
        command_buffer = b""
        
        try:
            while True:
                data = channel.recv(1024)
                if not data:
                    break
                
                command_buffer += data
                
                # Log command if Enter is pressed
                if b'\r' in data or b'\n' in data:
                    command = command_buffer.decode('utf-8', errors='ignore').strip()
                    if command:
                        event = {
                            "timestamp": datetime.utcnow().isoformat(),
                            "type": "ssh_command",
                            "source_ip": client_addr[0],
                            "command": command
                        }
                        with open('logs/honeypot.log', 'a') as f:
                            f.write(json.dumps(event) + '\n')
                        logging.info(f"Command from {client_addr[0]}: {command}")
                    
                    command_buffer = b""
                    channel.send(b"-bash: " + data + b": command not found\r\n$ ")
                
        except socket.timeout:
            logging.info(f"Connection timeout from {client_addr[0]}")
        except Exception as e:
            logging.error(f"Error in channel communication: {e}")
            
    except Exception as e:
        logging.error(f"Error handling connection from {client_addr}: {e}")
    finally:
        try:
            transport.close()
        except:
            pass

def start_ssh_honeypot(host='0.0.0.0', port=2222):
    """Start SSH honeypot server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(100)
        
        logging.info(f"SSH Honeypot started on {host}:{port}")
        print(f"[+] SSH Honeypot listening on {host}:{port}")
        
        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                logging.info(f"Connection from {client_addr[0]}:{client_addr[1]}")
                print(f"[*] Connection from {client_addr[0]}:{client_addr[1]}")
                
                client_thread = threading.Thread(
                    target=handle_connection,
                    args=(client_socket, client_addr),
                    daemon=True
                )
                client_thread.start()
                
            except KeyboardInterrupt:
                logging.info("Shutting down SSH honeypot...")
                print("\n[-] Shutting down SSH honeypot...")
                break
            except Exception as e:
                logging.error(f"Error accepting connection: {e}")
                
    except Exception as e:
        logging.error(f"Failed to start SSH honeypot: {e}")
        print(f"[!] Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    print("=" * 60)
    print("SSH HONEYPOT SERVICE")
    print("=" * 60)
    start_ssh_honeypot()