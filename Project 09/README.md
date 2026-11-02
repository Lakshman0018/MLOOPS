# Project 9 - Automated Docker Build, Test and GHCR Publish

Practical 9 adapts the manual GHCR process from Project 8 into GitHub Actions automation for the Wine Quality ML application.

## Workflow

1. Checkout repository.
2. Install Python dependencies.
3. Train the Wine Quality model.
4. Check the 0.70 accuracy quality gate.
5. Run ML and Flask application tests.
6. Build a fresh Docker image on the GitHub-hosted runner.
7. Start a temporary container on port 5000.
8. Verify GET /health.
9. Verify POST /predict.
10. Remove the test container even after failure.
11. Authenticate to GHCR using the automatically generated GITHUB_TOKEN.
12. Tag the tested image as latest and sha-<full-commit-sha>.
13. Push both tested tags to the existing GHCR package.

## GHCR

Registry: ghcr.io
Package: ghcr.io/lakshman0018/wine-quality-ml

The workflow does not use the personal access token from Project 8. It uses GITHUB_TOKEN with contents: read and packages: write.

## Practical 8 vs Project 9

Project 8 performed Docker login, tag, push, pull and validation manually.

Project 9 performs the build, container validation, GHCR authentication, tagging and publishing automatically after a push to main or a manual workflow dispatch.

## Release Gate

A failed Docker build, container startup, /health check, or prediction check stops the workflow before GHCR publication.

## Security

No personal access token is stored in the repository. Do not add tokens, kubeconfig files, passwords, or other credentials to the workflow or project files.

## CI/CD Repeatability Update

A second documented update was prepared to verify that a later push to main automatically rebuilds, tests, and republishes the Wine Quality image through GitHub Actions.
