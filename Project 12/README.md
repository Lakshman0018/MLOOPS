# Project 12 - Prometheus and Grafana Monitoring

Project 12 adds Prometheus metrics, local Prometheus scraping, Grafana visualization, and simple alert rules to the existing Wine Quality Prediction API from Project 11.

## Continuity

The same WineQT dataset, Random Forest model, Flask API, Docker pattern, GHCR package, and Render service are reused. The model algorithm and prediction schema are unchanged.

The uploaded practical guide describes a Student Result Prediction FastAPI service. This repository adapts that monitoring architecture to the existing Wine Quality Flask service.

## New metrics

- wine_quality_api_http_requests_total
- wine_quality_api_http_request_duration_seconds
- wine_quality_api_predictions_total
- wine_quality_api_model_loaded
- Prometheus built-in up metric

The /metrics endpoint is excluded from user-traffic counters so Prometheus scrapes do not distort application traffic metrics.

## API

- GET /
- GET /health
- GET /metrics
- POST /predict

## Local monitoring stack

Create a local monitoring folder or use these files directly:

- prometheus.yml
- wine_quality_alerts.yml

Create a Docker network:

```powershell
docker network create mlops-monitoring
```

Start Prometheus:

```powershell
docker run -d --name prometheus --network mlops-monitoring -p 9090:9090 -v "${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml:ro" -v "${PWD}/wine_quality_alerts.yml:/etc/prometheus/wine_quality_alerts.yml:ro" prom/prometheus
```

Open:

http://localhost:9090/targets

The target `wine-quality-api` should become **UP**.

Start Grafana:

```powershell
docker run -d --name grafana --network mlops-monitoring -p 3000:3000 grafana/grafana
```

Open:

http://localhost:3000

Configure Prometheus as a Grafana data source using:

http://prometheus:9090

## Suggested PromQL

```promql
wine_quality_api_model_loaded
```

```promql
sum(wine_quality_api_http_requests_total)
```

```promql
sum(rate(wine_quality_api_http_requests_total[1m]))
```

```promql
sum(wine_quality_api_predictions_total{result="success"})
```

```promql
sum(rate(wine_quality_api_http_requests_total{status=~"4..|5.."}[5m]))
```

```promql
histogram_quantile(0.95, sum by (le) (rate(wine_quality_api_http_request_duration_seconds_bucket[5m])))
```

```promql
up{job="wine-quality-api"}
```

## Suggested Grafana panels

1. Model Loaded - Stat
2. Total API Requests - Stat
3. Requests per Second - Time series
4. Successful Predictions - Stat
5. Client/Server Error Rate - Time series
6. P95 Request Latency - Time series

## Alert rules

`wine_quality_alerts.yml` contains:

- WineQualityAPIClientErrors: sustained 4xx traffic
- WineQualityAPIDown: Prometheus cannot scrape the deployed API

## Public metrics endpoint

https://wine-quality-ml-w8uk.onrender.com/metrics

Do not place tokens, credentials, private keys, or sensitive student/user data in metrics labels or screenshots.

## CI/CD

GitHub Actions trains the existing model pipeline, runs the ML and metrics tests, builds the monitoring-enabled Docker image, verifies /health, /metrics, /predict and logging behavior, then publishes the tested image to GHCR.

The existing Render service can then be redeployed with the latest image.
