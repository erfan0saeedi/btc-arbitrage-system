# Real-Time BTC Arbitrage Monitoring System

An asynchronous data pipeline for monitoring Bitcoin (BTC) price differences between international and local exchanges.

## Overview
The system collects live market data from KuCoin and Wallex, keeps the latest snapshots in Redis for fast access, and stores synchronized records in MySQL for historical analysis and dashboarding.

## Project Highlights
- Clear separation between ingestion, cache, and persistence layers.
- Async I/O design for continuous high-frequency data collection.
- Unit-tested parsing and extraction logic.

## Architecture
```text
KuCoin WebSocket ----->
                       \
                        > Redis (hot cache) --> Sync Worker --> MySQL (historical store) --> Power BI
                       /
Wallex REST API ------>
```

## Core Features
- **Asynchronous ingestion:** Concurrent non-blocking collectors for WebSocket and REST streams.
- **Low-latency cache layer:** Redis as a shared in-memory buffer between collectors and persistence worker.
- **Decoupled processing:** Data collection and SQL persistence are separated for cleaner scaling.
- **Containerized environment:** Docker Compose setup for reproducible local deployment.
- **Testable data processing units:** Key parsing and extraction logic is isolated and covered by tests.

## Tech Stack
- **Python 3.11** (`asyncio`, `httpx`, `sqlalchemy`, `redis`)
- **Databases:** Redis + MySQL
- **Data Sources:** KuCoin WebSocket + Wallex REST
- **Infrastructure:** Docker + Docker Compose
- **Analytics:** Power BI

## Repository Structure
```text
dashboards/
  screenshot.png               # Dashboard preview image
  btc_price_dashboard.pbix     # Power BI report file
  dashboard_preview.pdf        # Exported dashboard preview

src/
  collectors/
    kucoin.py                  # KuCoin ticker ingestion (WebSocket)
    wallex.py                  # Wallex orderbook polling (REST)
  processor/
    sync_worker.py             # Periodic persistence from Redis to MySQL
  config.py                    # Environment-driven runtime configuration
  database.py                  # Async Redis/MySQL client setup
  main.py                      # Application entrypoint

tests/
  test_wallex_collector.py
  test_sync_worker.py

Dockerfile
docker-compose.yml
requirements.txt
```

## Dashboard Preview
![Arbitrage Dashboard](./dashboards/screenshot.png)

### Dashboard Explanation
The dashboard compares BTC price movements between KuCoin and Wallex across a selected time range. It includes:
- A line chart showing KuCoin and Wallex BTC prices over time.
- A line chart for price difference (spread) between the two exchanges.
- A card showing the maximum difference amount in the selected time window.
- A card showing the exact timestamp where the maximum difference happened.

This makes it easier to observe which market fluctuations produced the strongest arbitrage opportunities.

## Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/btc-arbitrage-system.git
   cd btc-arbitrage-system
   ```

2. **Create a `.env` file**
   ```env
   MYSQL_URL=mysql+aiomysql://root:root@mysql:3306/trade
   REDIS_HOST=redis
   REDIS_PORT=6379
   SYNC_INTERVAL=1
   ```

3. **Start with Docker Compose**
   ```bash
   docker compose up --build
   ```

4. **Run locally (optional)**
   ```bash
   pip install -r requirements.txt
   python -m src.main
   ```

## Database Schema
```sql
CREATE DATABASE IF NOT EXISTS trade;

CREATE TABLE IF NOT EXISTS trade.btc_price (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    time DATETIME NOT NULL,
    price_kucoin DOUBLE NOT NULL,
    price_wallex DOUBLE NOT NULL
);
```

## Testing
```bash
python -m unittest discover -s tests -p 'test_*.py'
```
