# QLines: Scalable IoT Device Management Platform

**QLines** is a modern, open, and extensible platform for managing, monitoring, and automating IoT devices at scale. Designed for easy deployment, robust data handling, and seamless integration, QLines empowers businesses and developers to connect, control, and analyze their devices with minimal friction.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
- [Quick Start (Docker)](#quick-start-docker)
- [Production Deployment](#production-deployment)
- [Core Components](#core-components)
- [Device Data Flow](#device-data-flow)
- [Health Checks & Monitoring](#health-checks--monitoring)
- [Contributing & Roadmap](#contributing--roadmap)
- [References](#references)

---

## Features

- **Unified IoT Device Management:** Register, monitor, and control devices from a web dashboard.
- **Real-Time Data Processing:** Integrates with Kafka, Redis, and MQTT for scalable, low-latency data flows.
- **Multi-Database Support:** Uses MongoDB for device/user data and ClickHouse for high-performance analytics.
- **User Authentication:** Secure login, registration, and user management.
- **Extensible Architecture:** Easily add new device types, data sources, or integrations.
- **Modern Web UI:** Responsive dashboard for device overview, analytics, and settings.
- **Easy Deployment:** Docker-based setup for local development and production.
- **Blog & Documentation:** Integrated WordPress blog for updates and guides.

---

## Architecture Overview

QLines is composed of three main services, typically deployed as Docker containers:

- **qlines_app:** The main Flask-based backend and web dashboard.
- **qlines_blog:** A WordPress-based blog for documentation and news.
- **qlines_proxy:** An NGINX-based reverse proxy for SSL termination and routing.

**Typical deployment:**
```
[User] <---> [NGINX Proxy w/ SSL] <---> [Qlines App] <---> [MongoDB, ClickHouse, Redis, Kafka, Mosquitto]
                                    \--> [Qlines Blog (WordPress + MySQL)]
```

- All services communicate over a custom Docker network.
- Designed for high-availability: can be scaled across multiple VMs with redundant databases and proxies.

---

## Technology Stack

- **Backend:** Python (Flask, Flask-Login, MongoEngine, RQ, Redis, Kafka, ClickHouse)
- **Frontend:** Jinja2 templates, JavaScript, Bootstrap
- **Messaging:** MQTT (Mosquitto), Kafka
- **Databases:** MongoDB, ClickHouse, MySQL (for blog)
- **Web Server:** Gunicorn (with eventlet for WebSockets)
- **Proxy:** NGINX (with Certbot for SSL)
- **Containerization:** Docker, Docker Compose

---

## Quick Start (Docker)

### Prerequisites

- Docker Engine & Docker Compose installed
- (Optional) `docker network create custom_qlines_bridge_network` to create the shared network

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mehdiabolfathi/qlines_app.git
   cd qlines_app
   ```

2. **Build and start the stack:**
   ```bash
   docker compose up -d
   ```

3. **Access the dashboard:**
   - Visit [http://localhost:5000](http://localhost:5000) in your browser.

4. **Default services:**
   - QLines App: `localhost:5000`
   - MongoDB: `localhost:27017`
   - Redis: `localhost:6379`
   - Mosquitto MQTT: `localhost:1883`

---

## Production Deployment

- **Upgrade your VPS to the latest Debian for best compatibility.**
- **Clone and deploy each service (app, blog, proxy) on your production server.**
- **Configure NGINX and SSL certificates using Certbot.**
- **For multi-VM/high-availability, deploy redundant proxies and databases as described in the [Architecture Overview](#architecture-overview).**

**See the [detailed deployment guide](#) for step-by-step instructions.**

---

## Core Components

- **`qlines.py`:** Main Flask app, routes, and business logic.
- **`docker-compose.yml`:** Orchestrates all services (app, Redis, MongoDB, RQ worker, Mosquitto).
- **`Dockerfile_qlines`:** Build instructions for the main app container.
- **`templates/`:** Jinja2 HTML templates for the web UI.
- **`static/`:** JavaScript, CSS, and image assets.
- **`check_processes_and_ports.py`:** Health check script for all core services.

---

## Device Data Flow

1. **Device Registration:** Devices are registered via the dashboard and stored in MongoDB.
2. **Data Ingestion:** Devices send data via MQTT or HTTP; backend verifies and stores data.
3. **Analytics:** Data is processed and stored in ClickHouse for fast querying.
4. **User Dashboard:** Users view device status, analytics, and send commands via the web UI.
5. **Real-Time Updates:** WebSockets (via Flask-SocketIO) or polling for live data.

---

## Health Checks & Monitoring

- Run `./check_processes_and_ports.py` to verify all services are running and listening on the correct ports.
- Example healthy output:
  ```
  Process 'rqworker' is OK and running
  Process 'mongodb' is OK and running
  ...
  Port 5000 is open on 0.0.0.0.    Process: qlines
  ```

---

## Contributing & Roadmap

- **MVP complete:** Core device management, dashboard, and blog.
- **Planned:** Mobile apps, advanced analytics, more integrations, improved HA/DB sync, automated SSL renewal.
- **Contributions welcome!** Please open issues or pull requests.

---

## References

- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)
- [Kafka & Python Guide](https://towardsdatascience.com/how-to-build-a-simple-kafka-producer-and-consumer-with-python-a967769c4742)
- [System Design Guide](https://bit.ly/3SuUR0Y)

---

**For full documentation and advanced deployment, see the [Google Doc](https://docs.google.com/document/d/1RpFBwtAG9uG10FQ6VcyiW-3TbMRWepAfR2PxorEg0Eo/edit#).**

---

**SEO Keywords:** IoT device management, Flask IoT platform, Docker IoT stack, MQTT dashboard, scalable IoT backend, real-time device analytics, open source IoT, QLines

## Infrastructure & VM Specifications

Below are the VM specifications for the QLines deployment across multiple geographic sites. These specifications ensure that the platform can handle the expected load and provide redundancy.

| Site        | VM Function | CPU (vCPU) | Mem (GB) | Disk (GB) | Description                |
|-------------|-------------|------------|----------|-----------|----------------------------|
| Geo site 1  | LB+Proxy    | 2          | 2        | 100       | Load balancing and proxy   |
| Geo site 1  | App1        | 4          | 8        | 200       | Each could handle all load |
| Geo site 1  | App2        | 4          | 8        | 200       | Each could handle all load |
| Geo site 1  | App3        | 4          | 8        | 200       | Each could handle all load |
| Geo site 1  | DB1         | 8          | 16       | 500       | Database server            |

### Notes:
- **Load Balancing:** The LB+Proxy VM distributes traffic across the application servers.
- **Application Servers:** Each app server is capable of handling the full load, providing redundancy.
- **Database Server:** The DB1 VM is dedicated to database operations, ensuring data integrity and performance.
