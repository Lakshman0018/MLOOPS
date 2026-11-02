# Project 10 - Deploy Wine Quality ML to Render

Practical 10 deploys the tested Wine Quality Docker image from GitHub Container Registry (GHCR) as a Render Web Service.

## Deployment chain

Project 9 tested and published:
ghcr.io/lakshman0018/wine-quality-ml:latest

Project 10 deployed the same image to Render in the MLOOPS workspace.

## Render configuration

- Workspace: MLOOPS
- Service: wine-quality-ml
- Service type: Web Service
- Source: Existing Image
- Image: ghcr.io/lakshman0018/wine-quality-ml:latest
- Registry credential: GitHub GHCR Read
- Plan: Free
- Region: Oregon (US West)
- Port: 5000
- Health check path: /health
- Docker command override: none
- Pre-deploy command: none
- Environment variables: none

## Public service

https://wine-quality-ml-w8uk.onrender.com

## Verification

GET / returned:
{"service":"wine-quality-prediction","status":"ok"}

POST /predict with the practical sample returned:
prediction = 8
prediction_code = 8

The deployment was successfully shown as Live in Render.
