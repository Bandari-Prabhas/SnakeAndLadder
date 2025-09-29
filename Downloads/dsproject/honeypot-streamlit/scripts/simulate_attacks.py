import paramiko
import requests
import time
import random
from datetime import datetime

# Common username/password combinations used by attackers
USERNAMES = ['root', 'admin', 'user', 'test', 'ubuntu', 'pi', 'guest', 'administrator', 'postgres', 'mysql']
PASSWORDS = ['123456', 'password', 'admin', 'root', '12345678', 'qwerty', '123456789', 'letmein', 'password123', '1234567890']

def print_banner():
    """Print attack simulation banner"""
    print("\n" + "="*70)
    print(" "*20 + "HONEYPOT ATTACK SIMULATOR")
    print("="*70)
    print(" [+] This script simulates various attack patterns")
    print(" [+] All attempts will be logged by the honeypot")
    print("="*70 + "\n")

def simulate_ssh_attacks(host='localhost', port=2222, count=20):
    """Simulate SSH brute force attacks"""
    print(f"\n[*] Simulating {count} SSH brute force attacks...")
    print("-" * 70)
    
    success = 0
    failed = 0
    
    for i in range(count):
        username = random.choice(USERNAMES)
        password = random.choice(PASSWORDS)
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            print(f"[{i+1}/{count}] Attempting SSH: {username}:{password} → {host}:{port}", end=" ")
            
            client.connect(
                host, 
                port=port, 
                username=username, 
                password=password, 
                timeout=5,
                allow_agent=False,
                look_for_keys=False
            )
            
            print("✓ SUCCESS")
            success += 1
            client.close()
            
        except paramiko.AuthenticationException:
            print("✗ FAILED (Auth)")
            failed += 1
        except paramiko.SSHException as e:
            print(f"✗ FAILED (SSH Error)")
            failed += 1
        except Exception as e:
            print(f"✗ FAILED (Connection)")
            failed += 1
        
        # Random delay between attempts
        time.sleep(random.uniform(0.5, 2.0))
    
    print("-" * 70)
    print(f"[+] SSH Simulation Complete: {success} success, {failed} failed")

def simulate_http_attacks(url='http://localhost:8080', count=20):
    """Simulate HTTP login attacks"""
    print(f"\n[*] Simulating {count} HTTP login attacks...")
    print("-" * 70)
    
    success = 0
    failed = 0
    
    for i in range(count):
        username = random.choice(USERNAMES)
        password = random.choice(PASSWORDS)
        
        try:
            print(f"[{i+1}/{count}] HTTP Login: {username}:{password} → {url}", end=" ")
            
            response = requests.post(
                f"{url}/login",
                data={'username': username, 'password': password},
                timeout=5,
                allow_redirects=False
            )
            
            if response.status_code == 200:
                if "Invalid" in response.text or "error" in response.text.lower():
                    print("✗ BLOCKED")
                    failed += 1
                else:
                    print("✓ SUCCESS")
                    success += 1
            else:
                print(f"✗ FAILED ({response.status_code})")
                failed += 1
                
        except requests.exceptions.ConnectionError:
            print("✗ FAILED (Connection)")
            failed += 1
        except requests.exceptions.Timeout:
            print("✗ FAILED (Timeout)")
            failed += 1
        except Exception as e:
            print(f"✗ FAILED (Error)")
            failed += 1
        
        time.sleep(random.uniform(0.5, 2.0))
    
    print("-" * 70)
    print(f"[+] HTTP Simulation Complete: {success} success, {failed} failed")

def simulate_path_scanning(url='http://localhost:8080', count=15):
    """Simulate path scanning attempts"""
    print(f"\n[*] Simulating {count} path scanning attempts...")
    print("-" * 70)
    
    common_paths = [
        '/admin', '/administrator', '/wp-admin', '/phpmyadmin',
        '/.env', '/config', '/backup', '/database', '/api',
        '/phpinfo.php', '/info.php', '/test.php', '/shell.php',
        '/uploads', '/files', '/data'
    ]
    
    for i in range(count):
        path = random.choice(common_paths)
        
        try:
            print(f"[{i+1}/{count}] Scanning: {url}{path}", end=" ")
            
            response = requests.get(
                f"{url}{path}",
                timeout=5,
                allow_redirects=False
            )
            
            print(f"→ {response.status_code}")
            
        except Exception as e:
            print("✗ FAILED")
        
        time.sleep(random.uniform(0.3, 1.5))
    
    print("-" * 70)
    print(f"[+] Path Scanning Complete")

def simulate_user_agent_variations(url='http://localhost:8080', count=10):
    """Simulate attacks with different user agents"""
    print(f"\n[*] Simulating {count} attacks with varied user agents...")
    print("-" * 70)
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'curl/7.68.0',
        'python-requests/2.28.0',
        'Wget/1.20.3',
        'Go-http-client/1.1',
        'Java/11.0.1',
        'Nmap Scripting Engine',
        'sqlmap/1.6',
        'nikto/2.1.6',
        'masscan/1.0'
    ]
    
    for i in range(count):
        username = random.choice(USERNAMES)
        password = random.choice(PASSWORDS)
        user_agent = random.choice(user_agents)
        
        try:
            print(f"[{i+1}/{count}] UA: {user_agent[:40]}...", end=" ")
            
            response = requests.post(
                f"{url}/login",
                data={'username': username, 'password': password},
                headers={'User-Agent': user_agent},
                timeout=5
            )
            
            print(f"→ {response.status_code}")
            
        except Exception as e:
            print("✗ FAILED")
        
        time.sleep(random.uniform(0.5, 2.0))
    
    print("-" * 70)
    print(f"[+] User Agent Variation Complete")

def main():
    """Main simulation function"""
    print_banner()
    
    print("\nSelect attack simulation type:")
    print("1. SSH Brute Force (20 attempts)")
    print("2. HTTP Login Attacks (20 attempts)")
    print("3. Path Scanning (15 attempts)")
    print("4. User Agent Variations (10 attempts)")
    print("5. Full Simulation (All of the above)")
    print("6. Custom Continuous Attack")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    try:
        if choice == '1':
            simulate_ssh_attacks()
        elif choice == '2':
            simulate_http_attacks()
        elif choice == '3':
            simulate_path_scanning()
        elif choice == '4':
            simulate_user_agent_variations()
        elif choice == '5':
            print("\n[*] Starting FULL attack simulation...")
            simulate_ssh_attacks(count=20)
            time.sleep(2)
            simulate_http_attacks(count=20)
            time.sleep(2)
            simulate_path_scanning(count=15)
            time.sleep(2)
            simulate_user_agent_variations(count=10)
        elif choice == '6':
            duration = int(input("\nEnter duration in minutes: "))
            attacks_per_minute = int(input("Enter attacks per minute: "))
            
            print(f"\n[*] Running continuous attack for {duration} minutes...")
            print(f"[*] Rate: {attacks_per_minute} attacks/minute")
            print("[*] Press Ctrl+C to stop\n")
            
            start_time = time.time()
            end_time = start_time + (duration * 60)
            attack_count = 0
            
            try:
                while time.time() < end_time:
                    attack_type = random.choice(['ssh', 'http', 'scan'])
                    
                    if attack_type == 'ssh':
                        simulate_ssh_attacks(count=1)
                    elif attack_type == 'http':
                        simulate_http_attacks(count=1)
                    else:
                        simulate_path_scanning(count=1)
                    
                    attack_count += 1
                    time.sleep(60 / attacks_per_minute)
                    
            except KeyboardInterrupt:
                print("\n\n[!] Simulation stopped by user")
            
            print(f"\n[+] Total attacks performed: {attack_count}")
        else:
            print("\n[!] Invalid choice")
            return
        
        print("\n" + "="*70)
        print(" "*25 + "SIMULATION COMPLETE")
        print("="*70)
        print("\n[+] Check the Streamlit dashboard to see the logged attacks!")
        print("[+] Data has been written to: logs/honeypot.log\n")
        
    except KeyboardInterrupt:
        print("\n\n[!] Simulation interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    main()