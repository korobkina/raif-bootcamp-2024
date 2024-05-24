# Status 
[![Deployment Status](https://github.com/korobkina/raif-bootcamp-2024/actions/workflows/main.yml/badge.svg)](https://github.com/korobkina/raif-bootcamp-2024/actions/workflows/main.yml) [![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![MongoDB](https://img.shields.io/badge/database-MongoDB-green) ![Prometheus](https://img.shields.io/badge/monitoring-Prometheus-orange) ![Grafana](https://img.shields.io/badge/monitoring-Grafana-blue)


# Raiffeisen bootcamp 2024 - Data Scientist assistant telegram bot

**Bot**: - link \
**Service dashboard**: http://159.65.124.137:3000/d/edmo0ry0ykphca/ds-bootcamp-telegram-bot-team-3?orgId=1 


# How to test locally
1. Install dependencies
```
poetry install --only main,test,format
```
2. Check TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, GPT_VERSION in `wolf_assistant/settings.py`
3. Set environment 
```
export ENV=DEV
```
4. Set database
```
docker-compose -f docker-compose.mongodb.yml up -d
```
5. Run script
```
poetry run python wolf_assistant/app.py
```


# Docker
You can build and run Docker locally 
```
docker build -t ds_wolves/telegram-bot:latest .
docker run -d -e TELEGRAM_BOT_TOKEN=<your token> -e OPENAI_API_KEY=<your api key> \
   -e MONGO_INITDB_ROOT_USERNAME=<your mongo user> -e MONGO_INITDB_ROOT_PASSWORD=<your mongo pass> \
   -e ENV=PROD --name telegram-bot ds_wolves/telegram-bot:latest
```
(you also can specify these variables in settings.py and backend/db_con.py) \
\
Or get latest version from DockerHub (https://hub.docker.com/repository/docker/dswolves/telegram-bot/general)
```
docker pull ds_wolves/telegram-bot:latest
docker run -d -e TELEGRAM_BOT_TOKEN=<your token> -e OPENAI_API_KEY=<your api key> \
   -e MONGO_INITDB_ROOT_USERNAME=<your mongo user> -e MONGO_INITDB_ROOT_PASSWORD=<your mongo pass> \
   -e ENV=PROD --name telegram-bot ds_wolves/telegram-bot:latest
```

Using docker compose (for `bot`, `mongodb`, `prometheus` and `grafana`)
```
export ENV=DEV_DOCKER
docker-compose -f docker-compose.yml up -d
```
# Prometheus and Grafana

Configure Grafana:
- Open Grafana at http://localhost:3000.
- Log in (default credentials: admin/admin).
- Add Prometheus as a data source:
  - Go to Configuration > Data Sources.
  - Click on "Add data source".
  - Select "Prometheus".
  - Set the URL to http://prometheus:9090. \

Create a dashboard:
- Go to Create > Dashboard.
- Add a new panel and configure it to use the metrics from Prometheus.


# Deploy

Force deployment manually:
1. go to https://github.com/korobkina/raif-bootcamp-2024/actions/workflows/main.yml
2. Press "Run workflow" button and actually run it

or tag a commit with some version in format `v*.*.*` (for ex. `v1.0.1`) and let CI/CD do its work:
1. `git tag v1.0.1`
2. `git push --tags`