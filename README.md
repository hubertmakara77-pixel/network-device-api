# Network Device Management API

A professional REST API designed for managing and automatically monitoring network devices using the **SNMP** protocol. This project is fully containerized, implements a production-grade PostgreSQL database, and includes a comprehensive suite of automated integration tests.

This project serves as an excellent portfolio piece demonstrating core competencies for roles such as **Software Tester (QA)**, **Junior Python Developer**, or **Network Automation Engineer** within the telecommunications and networking industry.

---

## 🚀 Key Features

- **Device Management (CRUD):** Full control over the network device inventory (create, read, update, delete) via standard HTTP requests.
- **SNMP Automation (Network Automation):** Real-time extraction of diagnostic metrics (e.g., system services, uptime, performance indicators) directly from live or public network servers using **SNMPv2c**.
- **Time-Series Architecture (Metrics History):** Automated historical logging of network metrics with precise database-generated timestamps.
- **Docker Containerization:** Complete environment isolation for both the API service and the database, ensuring single-command replication across any operating system.
- **Automated Integration Testing:** Comprehensive coverage of critical API workflows using **Pytest**, leveraging an isolated in-memory SQLite database (`:memory:`) to guarantee test safety.

---

## 🛠️ Tech Stack

- **Programming Language:** Python 3.11
- **API Framework:** Flask
- **Databases:** PostgreSQL 15 (Production), SQLite (Testing/In-Memory)
- **Object-Relational Mapping (ORM):** Flask-SQLAlchemy (Psycopg2)
- **Network Protocol:** SNMP (via `pysnmp` & `pyasyncore` patch for modern Python compatibility)
- **Containerization & Orchestration:** Docker & Docker Compose
- **Automation Testing:** Pytest

---

## 📂 Project Structure

```text
network-device-api/
│
├── app/
│   ├── __init__.py          # App initialization, config, and DB setup
│   ├── database.py          # SQLAlchemy instance exposure
│   ├── models.py            # Relational database models (Device, Metric)
│   ├── routes.py            # REST API endpoint definitions (Routing)
│   └── snmp_connector.py    # Dedicated network communication module for SNMP
│
├── tests/
│   └── test_models.py       # Automated integration test suites
│
├── Dockerfile               # Docker build instructions for the Flask API
├── docker-compose.yml       # Multi-container orchestration (API + PostgreSQL)
├── main.py                  # Application entry point
└── requirements.txt         # Frozen, fully compatible dependency manifest

# 🚀 Getting Started & Installation

The project is fully containerized. You do not need Python or a local PostgreSQL engine installed on your host machine.  
The only prerequisite is Docker Desktop.

## 1. Clone the repository

```bash
git clone https://github.com/hubertmakara77-pixel/network-device-api.git
cd network-device-api
```

## 2. Start the infrastructure

```bash
docker-compose up --build -d
```

## 3. Access the API

The API will be available at:

```text
http://localhost:5000
```

---

# 🧪 Running Automated Tests

Following QA best practices, integration tests run completely isolated inside the test container using an independent in-memory SQLite database, guaranteeing zero side effects on production PostgreSQL data.

Run the test suite with:

```bash
docker exec -e DATABASE_URL="sqlite:///:memory:" network-device-api-api-1 python -m pytest
```

---

# 🔌 API Endpoints Documentation

## 1. Network Devices (`Device`)

### Get all monitored devices

```http
GET /api/devices
```

Retrieves a list of all monitored network devices.

---

### Register a new device

```http
POST /api/devices
```

#### Required Payload

```json
{
  "hostname": "router-core",
  "ip_address": "192.168.1.1",
  "snmp_community": "public"
}
```

---

### Get device details

```http
GET /api/devices/<id>
```

Retrieves technical details of a specific device.

---

### Update device configuration

```http
PUT /api/devices/<id>
```

Updates an existing device configuration.

---

### Delete a device

```http
DELETE /api/devices/<id>
```

Removes a device from active monitoring.

---

# 📊 SNMP Metrics (`Metric`)

## Trigger SNMP polling

```http
POST /api/devices/<id>/metrics
```

Commands the API to establish an SNMP connection to the device, query the provided OID, and store the numerical response in the database.

---

## Get metric history

```http
GET /api/devices/<id>/metrics
```

Retrieves the full chronological time-series metric history for a specific device.

---

# 📝 Sample Network Payload (Triggering SNMP Polling)

## Request

### `POST /api/devices/1/metrics`

```json
{
  "oid": "1.3.6.1.2.1.1.7.0",
  "metric_type": "system_services_score"
}
```

---

## Response (`201 Created`)

```json
{
  "message": "Measurement taken and saved!",
  "metric_type": "system_services_score",
  "value": 72.0
}
```
