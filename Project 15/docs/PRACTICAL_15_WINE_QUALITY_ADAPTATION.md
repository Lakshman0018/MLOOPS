# Practical 15 - Wine Quality: Detect Data Drift and Trigger Model Retraining

## Aim
Extend the existing Wine Quality Prediction MLOps workflow by comparing recent wine input-feature distributions with a fixed baseline, detecting significant data drift, and retraining a candidate model only when drift is detected and labeled examples are available.

## Dataset and model continuity
This repository uses only the WineQT dataset already present in MLOOPS. The target is `quality`; `Id` is an identifier and is excluded from model features. All other numeric WineQT columns are input features. Project 12 trains a RandomForestClassifier with 100 trees and random_state 42; Project 15 follows that model family.

## Procedure
1. Install packages from `requirements.txt`.
2. Run `python drift/prepare_reference.py` to create the fixed baseline from WineQT input features.
3. Run `python drift/simulate_current_data.py --mode stable`, then `python drift/detect_drift.py` to test the no-drift case.
4. Run `python drift/simulate_current_data.py --mode drift`, then `python drift/detect_drift.py` to test a deliberately shifted batch.
5. Review `drift/drift_report.json`. Each feature is tested with the two-sample KS test; p < 0.05 flags a feature, and at least two flagged features trigger the classroom overall-drift decision.
6. For the supervised retraining demonstration, run `python drift/simulate_current_data.py --mode drift --make-labeled-batch`. This uses source-row quality labels for a synthetic classroom example only.
7. Run `python drift/retrain_candidate.py`. It exits without training when no overall drift exists and requires the labeled recent batch otherwise.
8. Run `python drift/approve_candidate.py`. Candidate accuracy must be at least 0.70, matching the repository's Project 03 quality gate. The candidate is copied to a separate Project 15 approved-model path only when the gate passes.
9. Rerun the existing model/API tests before continuing through the Projects 12-14 container and deployment workflow.

## Important interpretation
Data drift is a change in input-feature distributions. It does not by itself prove that model accuracy has fallen or that the relationship between features and quality has changed. Supervised retraining and performance evaluation require trustworthy labels. Synthetic labels in this classroom simulation are not production ground truth.

## Evidence to preserve after execution
- Fixed baseline: `drift/reference_data.csv`
- Recent feature batch: `drift/current_data.csv`
- Classroom labeled batch (optional): `drift/current_labeled_data.csv`
- Statistical result: `drift/drift_report.json`
- Candidate evaluation: `drift/retraining_metrics.json`
- Candidate model: `drift/wine_quality_model_candidate.pkl`
- Approved Project 15 model after passing the gate: `wine_quality_model_approved.pkl`

Record actual KS statistics, p-values, row counts, and accuracy from your own run. Do not copy sample metrics as if they were measured results.
