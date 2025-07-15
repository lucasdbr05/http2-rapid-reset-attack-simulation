# Educational HTTP/2 Rapid Reset Attack Simulator

This project provides a safe and isolated environment to simulate the behavior of the **HTTP/2 Rapid Reset Attack** (CVE-2023-44487), using an NGINX server configured with HTTP/2 via Docker and a Python script that creates multiple connections and sends rapid resets to HTTP/2 streams.

---

## Components

- NGINX server with HTTP/2 and HTTPS configured via Docker
- Python script (`simulate_reset_attack.py`) that simulates multiple HTTP/2 stream resets with `hyper-h2`
- Shell script (`create_certs.sh`) that generates self-signed SSL certificates automatically during container build
- Docker Compose configuration to orchestrate the environment

---

## Prerequisites

- Docker and Docker Compose installed
- Python 3 installed (to run the simulation script)
- `pip install h2` for HTTP/2 library in Python

---

## How to use

### 1. Clone the repository

```bash
git clone <repository-url>
cd <folder-name>
```

### 2. Start the NGINX server

In the project root directory, run:

```bash
docker-compose up --build
```

This command will:

- Build the NGINX image
- Execute the `create_certs.sh` script to generate self-signed SSL certificates
- Start the container with the HTTP/2 server listening on port 8443

### 3. Run the simulation script


```bash
pip install -r requirements.txt
python3 simulate_reset_attack.py
```

The script will create multiple HTTP/2 connections and send rapid resets to streams, simulating the attack pattern.

---

## Monitoring

- To view NGINX logs in real time:

```bash
docker logs -f server-nginx-http2-1
```

- To monitor container resource usage:

```bash
docker stats server-nginx-http2-1
```

- You can use `htop`, `iftop` or other tools on the host to monitor CPU, memory and network.

---

## References

- [CVE-2023-44487 - HTTP/2 Rapid Reset Attack](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-44487)
- [Cloudflare Technical Breakdown](https://blog.cloudflare.com/technical-breakdown-http2-rapid-reset-ddos-attack/)
- [hyper-h2 Python Library](https://python-hyper.org/projects/h2/en/stable/)
- [NGINX HTTP/2 Documentation](https://nginx.org/en/docs/http/ngx_http_v2_module.html)

---
