# Simulador Educacional do Ataque HTTP/2 Rapid Reset

Este projeto fornece um ambiente seguro e isolado para simular o comportamento do **Ataque HTTP/2 Rapid Reset** (CVE-2023-44487), utilizando um servidor NGINX configurado com HTTP/2 via Docker e scripts Python que simulam o ataque.

---

## 🎯 O que é o Ataque HTTP/2 Rapid Reset?

O HTTP/2 Rapid Reset (CVE-2023-44487) é uma vulnerabilidade que permite a um atacante:
1. Estabelecer conexões HTTP/2 com o servidor alvo
2. Enviar múltiplas requisições rapidamente
3. Imediatamente cancelar essas requisições com frames RST_STREAM
4. Forçar o servidor a desperdiçar recursos processando requisições que são canceladas

O resultado é um ataque de negação de serviço (DoS) eficiente que pode sobrecarregar servidores HTTP/2.

---

## 🏗️ Componentes

- **Servidor NGINX** com HTTP/2 e HTTPS configurado via Docker
- **Cliente Python** que simula múltiplas conexões e rapid resets
- **Scripts de monitoramento** para observar o impacto em tempo real
- **Análise automática** dos resultados do ataque
- **Geração automática de certificados** SSL auto-assinados

---

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.7+ instalado
- Bibliotecas Python: `h2`, `requests`

---

## 🚀 Como Usar

### 1. Subir o servidor NGINX vulnerável
```bash
cd server
docker compose up --build -d
```

### 2. Executar o ataque HTTP/2 Rapid Reset
```bash
cd ../client
pip install -r requirements.txt
python attack.py
```

### 3. Analisar os resultados do ataque

#### Usando Python:
```bash
python analyze_results.py
```

---

## 4. Monitoramento

### Monitoramento em Tempo Real
```bash
cd client
python monitor_server.py
```

### Verificação Manual
```bash
docker logs -f server-nginx-http2-1

docker stats server-nginx-http2-1

curl -k https://localhost:8443
```


## 🛡️ Mitigações Demonstradas

Este simulador também pode ser usado para testar mitigações:

---

## 📚 Estrutura de Arquivos

```
├── README.md
├── client/
│   ├── requirements.txt           # Dependências Python
│   └── attack.py                  # Script principal do ataque
└── server/
    ├── docker-compose.yml        # Configuração do Docker
    ├── Dockerfile                # Imagem do NGINX
    ├── nginx-safe.conf           # Configuração do NGINX seguro
    ├── nginx-vulneravel.conf     # Configuração do NGINX seguro
    └── create-certs.sh           # Geração de certificados SSL
```

