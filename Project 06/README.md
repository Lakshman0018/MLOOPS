# Project 6 - Dockerize Wine Quality ML Prediction Application

This practical containerizes the validated Wine Quality prediction application from Project 5.

## Dataset
WineQT.csv

## Manual Docker workflow
1. Generate the validated model and metrics from WineQT.csv.
2. Build the Docker image.
3. Verify the image.
4. Run the container with host port 5000 mapped to container port 5000.
5. Test the health and prediction API endpoints.
6. Inspect container logs.
7. Stop and remove the container.

## Image
wine-quality-ml:1.0

## Container
wine-quality-ml-container

The model and metrics files are generated locally by train_model.py before the Docker build.
