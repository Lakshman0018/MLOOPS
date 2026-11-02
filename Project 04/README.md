# Project 4 - Preserve Wine Quality ML Artifacts

This project extends the Project 3 Wine Quality ML Quality Gate workflow so that validated ML outputs are preserved as a GitHub Actions artifact.

## Dataset
WineQT.csv

## Generated outputs
- wine_quality_model.pkl
- metrics.json
- student_results.csv

## Artifact
All three generated outputs are uploaded together as:
student-result-ml-artifacts

The upload happens only after model training, the quality gate, and automated ML tests succeed.
