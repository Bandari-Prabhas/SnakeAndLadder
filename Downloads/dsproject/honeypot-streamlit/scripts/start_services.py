#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import signal

def print_banner():
    """Print startup banner"""
    print("\n" + "="*70)
    print(" "*20 + "HONEYPOT SERVICE MANAGER")
    print("="*70)
    print(" [+] Starting Honeypot Security Analytics System")
    print("="*70 + "\n")

def check_dependencies():
    """Check if required packages are installed"""
    print("[*] Checking dependencies...")
    
    required_packages = ['paramiko', 'flask', 'streamlit', 'pandas', 'plotly']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        print("[!] Install with: pip install " + " ".join(missing))
        return False
    
    print("[+] All dependencies satisfied\n")
    return True

def create_directories():
    """Create necessary directories"""
    print("[*] Creating directories...")
    
    directories = ['logs', 'data', 'config', 'honeypot', 'scripts', 'pages', 'utils']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}/")
    
    print("[+] Directories ready\n")

def start_ssh_honeypot():
    """Start SSH honeypot service"""
    print("[*] Starting SSH Honeypot on port 2222...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, 'honeypot/ssh_honeypot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)
        
        if process.poll() is None:
            print("[+] SSH Honeypot started (PID: {})".format(process.pid))
            return process
        else:
            print("[!] SSH Honeypot failed to start")
            return None
    except Exception as e:
        print(f"[!] Error starting SSH honeypot: {e}")
        return None

def start_http_honeypot():
    """Start HTTP honeypot service"""
    print("[*] Starting HTTP Honeypot on port 8080...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, 'honeypot/http_honeypot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)
        
        if process.poll() is None:
            print("[+] HTTP Honeypot started (PID: {})".format(process.pid))
            return process
        else:
            print("[!] HTTP Honeypot failed to start")
            return None
    except Exception as e:
        print(f"[!] Error starting HTTP honeypot: {e}")
        return None

def start_streamlit():
    """Start Streamlit dashboard"""
    print("[*] Starting Streamlit Dashboard on port 8501...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'streamlit', 'run', 'app.py', 
             '--server.port=8501', '--server.headless=true'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)
        
        if process.poll() is None:
            print("[+] Streamlit Dashboard started (PID: {})".format(process.pid))
            return process
        else:
            print("[!] Streamlit failed to start")
            return None
    except Exception as e:
        print(f"[!] Error starting Streamlit: {e}")
        return None

def main():
    """Main service manager"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Store process handles
    processes = []
    
    try:
        # Start services
        print("\n" + "-"*70)
        print("STARTING SERVICES")
        print("-"*70 + "\n")
        
        ssh_process = start_ssh_honeypot()
        if ssh_process:
            processes.append(('SSH Honeypot', ssh_process))
        
        time.sleep(1)
        
        http_process = start_http_honeypot()
        if http_process:
            processes.append(('HTTP Honeypot', http_process))
        
        time.sleep(1)
        
        streamlit_process = start_streamlit()
        if streamlit_process:
            processes.append(('Streamlit', streamlit_process))
        
        # Display status
        print("\n" + "="*70)
        print(" "*25 + "ALL SERVICES RUNNING")
        print("="*70)
        print("\n📊 Access Points:")
        print("  • Streamlit Dashboard: http://localhost:8501")
        print("  • HTTP Honeypot:       http://localhost:8080")
        print("  • SSH Honeypot:        ssh root@localhost -p 2222")
        print("\n📁 Log Files:")
        print("  • Main Log:            logs/honeypot.log")
        print("  • Attack Log:          logs/attacks.log")
        print("\n⚠️  Press Ctrl+C to stop all services")
        print("="*70 + "\n")
        
        # Keep running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            for name, process in processes:
                if process.poll() is not None:
                    print(f"[!] {name} stopped unexpectedly")
        
    except KeyboardInterrupt:
        print("\n\n[*] Shutting down services...")
        
        for name, process in processes:
            print(f"[*] Stopping {name}...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print(f"[+] {name} stopped")
            except subprocess.TimeoutExpired:
                print(f"[!] Force killing {name}...")
                process.kill()
        
        print("\n[+] All services stopped")
        print("="*70 + "\n")
    
    except Exception as e:
        print(f"\n[!] Error: {e}")
        
        # Cleanup
        for name, process in processes:
            try:
                process.terminate()
            except:
                pass

if __name__ == "__main__":
    main()