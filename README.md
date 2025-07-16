# Educational Simulator for the HTTP/2 Rapid Reset Attack

This project provides a safe and isolated environment to simulate the behavior of the **HTTP/2 Rapid Reset Attack** (CVE-2023-44487), using an NGINX server configured with HTTP/2 via Docker and Python scripts that simulate the attack.

---

## 🎯 What is the HTTP/2 Rapid Reset Attack?

HTTP/2 Rapid Reset (CVE-2023-44487) is a vulnerability that allows an attacker to:
1. Establish HTTP/2 connections with the target server
2. Send multiple requests quickly
3. Immediately cancel these requests with RST_STREAM frames
4. Force the server to waste resources processing requests that are canceled

The result is an efficient denial-of-service (DoS) attack that can overload HTTP/2 servers.

---

## 🏗️ Components

- **NGINX Server** with HTTP/2 and HTTPS configured via Docker
- **Python Client** that simulates multiple connections and rapid resets
- **Monitoring scripts** to observe the impact in real time
- **Automatic analysis** of attack results
- **Automatic generation of self-signed SSL certificates**

---

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.7+ installed
- Python libraries: `h2`, `requests`

---

## 🚀 How to Use

### 1. Start the vulnerable NGINX server
```bash
cd server
docker compose up --build -d
```

### 2. Run the HTTP/2 Rapid Reset attack
```bash
cd ../client
pip install -r requirements.txt
python attack.py
```

### 3. Analyze the attack results

#### Using Python:
```bash
python analyze_results.py
```

---

## 4. Monitoring

### Real-Time Monitoring
```bash
cd client
python monitor_server.py
```

### Manual Verification
```bash
docker logs -f server-nginx-http2-1

docker stats server-nginx-http2-1

curl -k https://localhost:8443
```

---

## 📚 File Structure

```
├── README.md
├── client/
│   ├── requirements.txt           # Python dependencies
│   └── attack.py                 # Main attack script
└── server/
    ├── docker-compose.yml        # Docker configuration
    ├── Dockerfile                # NGINX image
    ├── nginx-safe.conf           # Safe NGINX configuration
    ├── nginx-vulneravel.conf     # Vulnerable NGINX configuration
    └── create-certs.sh           # SSL certificate generation
```

---

## 📈 Expected Results

### Successful Attack
- ✅ ~1000 HTTP/2 requests processed
- ✅ Rate of ~750+ resets per second
- ✅ Server processes requests but discards work
- ✅ Logs show multiple canceled requests

### Server Behavior
- Processing of valid HTTP/2 requests
- Resource waste due to resets
- Possible performance degradation
- In real scenarios: potential DoS

---

