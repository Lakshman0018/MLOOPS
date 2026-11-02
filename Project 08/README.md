# Project 8 - Wine Quality GHCR Publishing

## Objective

Publish the already-tested Wine Quality Docker image from Project 7 to GitHub Container Registry (GHCR), verify the published package, pull the versioned image, run it as a new container, and confirm that the application still performs predictions correctly.

## Continuity

Project 8 reuses the tested Docker image from Project 6/7. The image is not rebuilt or retrained for the registry step.

## Docker Image

- Local image: `wine-quality-ml:1.0`
- GHCR image: `ghcr.io/lakshman0018/wine-quality-ml`
- Version tag: `v1`
- Current tag: `latest`
- Image ID used: `d33b43dbe8ba`

## GHCR Publication

The image was authenticated to GHCR, tagged, and pushed successfully.

Published references:

```text
ghcr.io/lakshman0018/wine-quality-ml:v1
ghcr.io/lakshman0018/wine-quality-ml:latest
```

Published digest:

```text
sha256:d33b43dbe8bae9ef2c57ea054c783d97730e9a12e2910d7da265025d85ad6696
```

The GitHub Container Registry package is named `wine-quality-ml`.

## Verification

The versioned image was pulled back from GHCR and started as:

```text
wine-quality-from-ghcr
```

Port mapping:

```text
5000:5000
```

Application verification:

- Root endpoint: `GET /` returned `{"service":"wine-quality-prediction","status":"ok"}`
- Prediction endpoint: `POST /predict` returned prediction `8` and `prediction_code: 8`
- The container was stopped and removed after verification.
- Docker was logged out from GHCR after the practical.

## Note on Health Verification

The published image used for this practical exposes the application root endpoint and prediction endpoint. The root endpoint was therefore used as the runtime availability check for the pulled GHCR image.

## Result

The tested Wine Quality Docker image was successfully distributed through GHCR, pulled again from the registry, executed as a fresh container, and validated with the same prediction application behavior established in the previous practical.
