#!/usr/bin/env python3


import subprocess
import time
import threading
import signal
import sys

class ServerMonitor:
    def __init__(self):
        self.monitoring = True
        
    def monitor_docker_stats(self):
        print("=== MONITORAMENTO DO CONTAINER ===")
        try:
            while self.monitoring:
                result = subprocess.run([
                    'docker', 'stats', 'server-nginx-http2-1', 
                    '--no-stream', '--format', 
                    'table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}'
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] {result.stdout.strip()}")
                else:
                    print(f"Erro ao obter stats: {result.stderr}")
                
                time.sleep(2)
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
    
    def monitor_docker_logs(self):
        print("=== LOGS DO SERVIDOR ===")
        try:
            process = subprocess.Popen([
                'docker', 'logs', '-f', 'server-nginx-http2-1'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            text=True, bufsize=1, universal_newlines=True)
            
            while self.monitoring and process.poll() is None:
                line = process.stdout.readline()
                if line:
                    print(f"[LOG] {line.strip()}")
                    
        except Exception as e:
            print(f"Erro ao monitorar logs: {e}")
    
    def test_server_response(self):
        print("=== TESTE DE CONECTIVIDADE ===")
        while self.monitoring:
            try:
                result = subprocess.run([
                    'curl', '-k', '-4', '-s', '-o', '/dev/null', '-w', 
                    '%{http_code}', 'https://127.0.0.1:8443'
                ], capture_output=True, text=True, timeout=5)
                
                status_code = result.stdout.strip()
                print(f"[{time.strftime('%H:%M:%S')}] Status HTTP: {status_code}")
                
            except subprocess.TimeoutExpired:
                print(f"[{time.strftime('%H:%M:%S')}] Timeout - servidor pode estar sobrecarregado")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Erro ao testar: {e}")
            
            time.sleep(5)
    
    def stop_monitoring(self, signum=None, frame=None):
        print("\n=== PARANDO MONITORAMENTO ===")
        self.monitoring = False
        sys.exit(0)
    
    def start(self):
        print("Iniciando monitoramento do servidor...")
        print("Pressione Ctrl+C para parar")
        print("=" * 50)
        
        signal.signal(signal.SIGINT, self.stop_monitoring)
        
        threads = [
            threading.Thread(target=self.monitor_docker_stats, daemon=True),
            threading.Thread(target=self.monitor_docker_logs, daemon=True),
            threading.Thread(target=self.test_server_response, daemon=True)
        ]
        
        for t in threads:
            t.start()
        
        try:
            while self.monitoring:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()

if __name__ == "__main__":
    monitor = ServerMonitor()
    monitor.start()
