# Project 15 - Wine Quality Data Drift Detection and Controlled Retraining

This project extends the **Wine Quality Prediction** MLOps pipeline already maintained in this repository. It adapts Practical 15's drift-detection and controlled-retraining workflow to the existing WineQT dataset and model schema. No Student Result Prediction data, labels, or model are used.

## Continuity with earlier MLOOPS projects

- Dataset: `WineQT.csv` (same Wine Quality dataset used by earlier projects).
- Inputs: all numeric wine-chemistry columns except `Id` and target `quality`.
- Target: `quality` (wine-quality class).
- Model family: `RandomForestClassifier(n_estimators=100, random_state=42)`, matching Project 12's training approach.
- Existing production/API and deployment work in Projects 12-14 remains separate and unchanged.
- The repository's established quality-gate threshold is **0.70 accuracy**, reused from Project 03. It is not changed to the 0.85 value in the Student Result practical because this repository's own gate is 0.70.

## Folder contents

- `WineQT.csv`: Wine Quality dataset copied from Project 01 for a self-contained Project 15 workflow.
- `drift/prepare_reference.py`: freezes the baseline input-feature distribution.
- `drift/simulate_current_data.py`: creates stable or deliberately shifted classroom batches.
- `drift/detect_drift.py`: runs a two-sample Kolmogorov-Smirnov test per feature and writes a JSON report.
- `drift/retrain_candidate.py`: retrains only after drift is detected and a labeled batch exists.
- `drift/approve_candidate.py`: applies the 0.70 quality gate and writes a separate approved Project 15 model.
- Generated CSV, JSON, and PKL artifacts are created when the steps are run; they are not fabricated or committed as completed experiment results.

## Setup (PowerShell)

Run from the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r "Project 15/requirements.txt"
Set-Location "Project 15"
```

If PowerShell blocks activation, use the Python executable directly or run:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

## Execute the practical

Run these commands from inside `Project 15`:

```powershell
python drift/prepare_reference.py

# Case 1: stable recent batch - should usually report no overall drift
python drift/simulate_current_data.py --mode stable
python drift/detect_drift.py

# Case 2: synthetic shifted batch - expected to flag drift
python drift/simulate_current_data.py --mode drift
python drift/detect_drift.py

# Classroom-only labeled sample for demonstrating supervised retraining
python drift/simulate_current_data.py --mode drift --make-labeled-batch
python drift/retrain_candidate.py
python drift/approve_candidate.py
```

The simulation script writes `current_labeled_data.csv` only when `--make-labeled-batch` is supplied. Its labels are copied from the sampled source rows for a **classroom demonstration only**; they are not genuine new production ground truth. In a real deployment, replace that file with verified labels collected from actual outcomes.

## Drift decision

- Per feature: drift is flagged when KS-test `p_value < 0.05`.
- Overall classroom alert: at least 2 input features are flagged.
- These are demonstration settings, not universal production thresholds. Consider batch size, multiple testing, domain impact, and false-alert history before production use.

## Model safety

The candidate is saved as `drift/wine_quality_model_candidate.pkl`. After its test accuracy is at least 0.70, the approval script copies it to `wine_quality_model_approved.pkl` **inside Project 15**. The existing Project 12 model and API are not overwritten. A drift alert alone never promotes or deploys a model.

After approval, rerun the existing Wine Quality tests and use the existing Projects 12-14 CI/CD and Kubernetes deployment process only after tests pass.

## Generated evidence

`drift/reference_data.csv`, `drift/current_data.csv`, optional `drift/current_labeled_data.csv`, `drift/drift_report.json`, `drift/retraining_metrics.json`, and the candidate model are runtime outputs. Commit them only after running the practical and reviewing the generated evidence. Avoid committing model binaries unless intentionally required.
