# Project 5 - Wine Quality Continuous Delivery

This project extends the Wine Quality ML pipeline into Continuous Delivery.

## Dataset
WineQT.csv

## Delivery flow
1. Train the Wine Quality model
2. Check the ML quality gate
3. Run ML pipeline tests
4. Run Flask prediction API tests
5. Prepare a release candidate
6. Upload the release candidate as a GitHub Actions artifact

Production deployment is intentionally not performed in this practical.

## Release package
- app.py
- wine_quality_model.pkl
- metrics.json
- requirements.txt
- DEPLOYMENT.txt

## Normal quality gate
Minimum accuracy: 0.70
