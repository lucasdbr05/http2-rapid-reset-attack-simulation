#!/usr/bin/env python3
"""
Script de análise e demonstração do ataque HTTP/2 Rapid Reset
"""

import subprocess
import time
import json
from datetime import datetime

def analyze_attack_results():
    
    print("=" * 80)
    print("ANÁLISE DO ATAQUE HTTP/2 RAPID RESET SIMULADO")
    print("=" * 80)
    
    
    stats_result = subprocess.run([
        'docker', 'stats', 'server-nginx-http2-1', 
        '--no-stream', '--format', 'json'
    ], capture_output=True, text=True)
    
    if stats_result.returncode == 0:
        stats = json.loads(stats_result.stdout)
        print(f"\n ====> ESTATÍSTICAS DO SERVIDOR:")
        print(f"   Container: {stats['Container']}")
        print(f"   CPU Usage: {stats['CPUPerc']}")
        print(f"   Memory Usage: {stats['MemUsage']}")
        print(f"   Network I/O: {stats['NetIO']}")
        print(f"   Block I/O: {stats['BlockIO']}")
    
    
    
    
    logs_result = subprocess.run([
        'docker', 'logs', 'server-nginx-http2-1'
    ], capture_output=True, text=True)
    
    if logs_result.returncode == 0:
        logs = logs_result.stdout
        
        http2_requests = logs.count('HTTP/2.0')
        total_lines = len(logs.split('\n'))
        error_lines = logs.count('error')
        warn_lines = logs.count('warn')
        
        print(f"\n ====== ANÁLISE DOS LOGS: =======")
        print(f"   Total de linhas de log: {total_lines}")
        print(f"   Requisições HTTP/2 processadas: {http2_requests}")
        print(f"   Linhas de erro: {error_lines}")
        print(f"   Linhas de aviso: {warn_lines}")
        
        recent_logs = '\n'.join(logs.split('\n')[-10:])
        print(f"\n =>  ÚLTIMAS ENTRADAS DO LOG:")
        print("   " + recent_logs.replace('\n', '\n   '))
        
    print("=" * 80)

def test_server_vulnerability():
    print("\n TESTANDO VULNERABILIDADE ATUAL:")
    
    result = subprocess.run([
        'curl', '-k', '-s', '-w', '%{http_code}\\n', 
        'https://localhost:8443/vulnerable?attack=rapid-reset&thread=7&req=28'
    ], capture_output=True, text=True, timeout=80)
    
    status_code = result.stdout.strip().split('\n')[-1]
    print(f"   Status da conectividade básica: {status_code}")
    
    if status_code == '200':
        print("   => Servidor ainda responde normalmente")
        print("   => Configuração atual é vulnerável ao ataque demonstrado")
    else:
        print(f"    Servidor retornou status {status_code}")
        

def analyze_response_codes():
    print(f"\n ======> ANÁLISE DETALHADA DOS CÓDIGOS DE RESPOSTA: <======")
    
    
    logs_result = subprocess.run([
        'docker', 'logs', 'server-nginx-http2-1'
    ], capture_output=True, text=True)
    
    if logs_result.returncode == 0:
        logs = logs_result.stdout
        
        code_200 = logs.count('" 200 ')
        code_499 = logs.count('" 499 ')  
        code_400 = logs.count('" 400 ')  
        code_500 = logs.count('" 500 ')  
        http2_requests = logs.count('HTTP/2.0')
        
        print(f"   📊 Distribuição de códigos de resposta:")
        print(f"      • 200 OK: {code_200}")
        print(f"      • 499 Client Disconnected: {code_499}")
        print(f"      • 400 Bad Request: {code_400}")
        print(f"      • 500 Server Error: {code_500}")
        print(f"      • Total HTTP/2 requests: {http2_requests}")
    
    
    
if __name__ == "__main__":
    analyze_attack_results()
    analyze_response_codes()
    test_server_vulnerability()
