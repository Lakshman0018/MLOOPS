# Project 13 - Wine Quality Kubernetes Deployment and Scaling

Project 13 deploys the already-tested Wine Quality Prediction Docker image from GHCR onto a local Minikube Kubernetes cluster.

## Current image

The initial deployment uses the immutable Project 12 CI image:

`ghcr.io/lakshman0018/wine-quality-ml:project12-54407660342573cd943e95918fe80189cb6fb010`

The Project 12 workflow publishes both `latest` and an immutable `project12-<commit-sha>` tag.

## Kubernetes objects

- Deployment: `wine-quality-prediction`
- Service: `wine-quality-prediction-service`
- Container port: 5000
- NodePort: 30080
- Readiness probe: `/health`
- Liveness probe: `/health`
- GHCR registry secret: `ghcr-secret`

## 1. Verify tools

```powershell
docker --version
minikube version
kubectl version --client
```

## 2. Start Minikube

```powershell
minikube start --driver=docker
kubectl cluster-info
kubectl get nodes
kubectl config current-context
```

## 3. Authenticate Minikube to the private GHCR package

The GHCR package is private, so create the secret locally. Do not commit the token or put it in screenshots.

```powershell
kubectl create secret docker-registry ghcr-secret `
  --docker-server=ghcr.io `
  --docker-username=Lakshman0018 `
  --docker-password="<YOUR_READ_PACKAGES_PAT>" `
  --docker-email="<YOUR_EMAIL>"
```

Verify only the secret name:

```powershell
kubectl get secret ghcr-secret
```

## 4. Apply the Deployment and Service

```powershell
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl rollout status deployment/wine-quality-prediction
kubectl get deployments
kubectl get pods
kubectl get services
```

## 5. Get the local service URL

```powershell
minikube service wine-quality-prediction-service --url
```

Keep the tunnel terminal open if Minikube asks you to.

The service exposes:

- `GET /health`
- `GET /docs`
- `GET /metrics`
- `POST /predict`

## 6. Verify the application

Example health test:

```powershell
curl.exe "<SERVICE_URL>/health"
```

Open Swagger in a browser:

`<SERVICE_URL>/docs`

Test the same Wine Quality prediction payload used in Project 12.

## 7. View Kubernetes logs

```powershell
kubectl get pods
kubectl logs <POD_NAME>
```

## 8. Scale to three replicas

```powershell
kubectl scale deployment wine-quality-prediction --replicas=3
kubectl get deployment wine-quality-prediction
kubectl get pods -o wide
kubectl get endpointslice -l kubernetes.io/service-name=wine-quality-prediction-service -o wide
```

## 9. Demonstrate self-healing

Record the current Pod names:

```powershell
kubectl get pods
```

Delete one running Pod:

```powershell
kubectl delete pod <POD_NAME>
kubectl get pods -w
```

A replacement Pod should be created automatically so the desired replica count returns to three.

## 10. Rolling update

For the classroom update demonstration, switch from the immutable commit tag to the existing tested `latest` tag:

```powershell
kubectl set image deployment/wine-quality-prediction wine-quality-api=ghcr.io/lakshman0018/wine-quality-ml:latest
kubectl rollout status deployment/wine-quality-prediction
kubectl rollout history deployment/wine-quality-prediction
```

Verify the running image:

```powershell
kubectl get deployment wine-quality-prediction -o jsonpath='{.spec.template.spec.containers[0].image}'
```

## 11. Rollback

```powershell
kubectl rollout undo deployment/wine-quality-prediction
kubectl rollout status deployment/wine-quality-prediction
kubectl rollout history deployment/wine-quality-prediction
```

Verify the active image:

```powershell
kubectl get deployment wine-quality-prediction -o jsonpath='{.spec.template.spec.containers[0].image}'
```

## 12. Scale back to one replica

```powershell
kubectl scale deployment wine-quality-prediction --replicas=1
kubectl get pods
```

## Evidence to capture

- Minikube node in Ready state
- Deployment and Service created
- Pod Running/Ready
- `/health`, `/docs`, `/predict`, and `/metrics) working
- Kubernetes logs
- Three replicas after scaling
- EndpointSlice with multiple ready backends
- Replacement Pod after manual deletion
- Rolling update status/history
- Successful rollback
- Final one-replica state

## Cleanup

```powershell
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
minikube stop
```

Do not delete `ghcr-secret` until you no longer need it for the lab.
