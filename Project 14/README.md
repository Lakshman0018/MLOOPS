# Project 14 - Automated Kubernetes Deployment with GitHub Actions

Project 14 extends the Wine Quality MLOps pipeline from Project 13 by automating the Kubernetes deployment stage with GitHub Actions.

## Continuity

- Project 12: Prometheus/Grafana monitoring and GHCR publishing.
- Project 13: Manual Minikube Kubernetes deployment, Service exposure, scaling, and API verification.
- Project 14: Automated CI/CD from GitHub Actions to the existing Minikube Deployment.

Existing Kubernetes resources reused:
- Deployment: `wine-quality-prediction`
- Service: `wine-quality-prediction-service`
- Container: `wine-quality-api`
- Service port: `80 -> 5000`

## Self-hosted runner

The Minikube cluster runs on the student's Windows machine, so the deployment job uses a self-hosted GitHub Actions runner installed on the same machine.

Verify the runner account can run:

```powershell
minikube status
kubectl config current-context
kubectl get nodes
kubectl get deployment wine-quality-prediction
```

## Workflow

1. Build and test the existing Wine Quality application from Project 12.
2. Publish immutable `sha-<commit>` and `latest` tags to GHCR.
3. Run the deployment job on the self-hosted Windows runner.
4. Pull the tested image with Docker.
5. Load the exact image into Minikube.
6. Update the existing Kubernetes Deployment to the immutable image.
7. Wait for rollout.
8. Verify the API through the Kubernetes Service.
9. Roll back automatically when the deployment job fails.

The image is loaded into Minikube before deployment because the Docker-driver Minikube environment used in Project 13 could not resolve `ghcr.io` directly.

## Workflow file

`.github/workflows/project14-kubernetes-cicd.yml`

The workflow supports `workflow_dispatch` so the self-hosted runner can be configured before the first CD run.

## Security

Do not commit PATs, runner registration tokens, kubeconfig contents, or Kubernetes Secret values.