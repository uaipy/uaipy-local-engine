# 🛰️ FastAPI IoT Gateway — MQTT to Cloud Sync

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-%3E=0.95.0-teal.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/github/license/seuusuario/fastapi-iot-gateway)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

Este projeto é um gateway de integração para dispositivos IoT utilizando **FastAPI**. Ele consome mensagens publicadas em tópicos **MQTT**, armazena localmente em um banco **PostgreSQL**, e sincroniza os dados com um endpoint de nuvem protegido por autenticação **JWT**.

---

## 🧩 Funcionalidades

- 🔌 Escuta mensagens de dispositivos IoT via MQTT
- 📦 Persistência local das mensagens com PostgreSQL (jsonb)
- 🔐 Autenticação via JWT para envio seguro à nuvem
- ☁️ Envio em lote de mensagens não sincronizadas
- 🐳 Deploy com Docker + Docker Compose
- 🧠 Arquitetura modular com boas práticas Python
- 🛠️ CLI com [Typer](https://typer.tiangolo.com/) para facilitar o uso

---

## 🏗️ Arquitetura

```mermaid
graph TD
    A[Dispositivos IoT] -->|MQTT| B[MQTT Broker]
    B -->|Mensagens| C[FastAPI App]
    C -->|Armazena| D[(PostgreSQL)]
    C -->|Sincroniza em lote| E[API Nuvem (JWT)]
```

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/fastapi-iot-gateway.git
cd fastapi-iot-gateway
```

### 2. Configure o ambiente

```bash
cp .env.example .env
# Edite as variáveis conforme necessário
```

### 3. Suba os serviços

```bash
python cli/cli.py start
```

> O backend estará disponível em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Executar testes (em breve)

```bash
# Exemplo para testes futuros com pytest
pytest
```

---

## 📁 Estrutura do Projeto

```
.
├── app/
│   ├── main.py                  # Entrypoint do FastAPI
│   ├── core/                    # Configurações globais (config/env)
│   ├── db/                      # Conexão, models e session do SQLAlchemy
│   ├── crud/                    # Operações no banco
│   ├── services/                # MQTT + sync para nuvem
│   ├── api/                     # Rotas FastAPI
│   └── utils/                   # Logger e funções auxiliares
├── cli/
│   └── cli.py                   # CLI com Typer
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

---

## 🧠 Exemplo de Payload MQTT

```json
{
  "device_name": "sensor01",
  "data": {
    "temperature": 24.3,
    "humidity": 55
  }
}
```

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir _issues_, propor melhorias ou enviar _pull requests_.