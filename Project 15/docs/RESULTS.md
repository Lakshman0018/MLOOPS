# Project 15 - Final Execution Results

## Dataset
Wine Quality (WineQT.csv)

## Data Drift Detection
- Reference dataset: 1,143 rows
- Current simulated dataset: 200 rows
- Input features: 11
- Detection method: Kolmogorov-Smirnov two-sample test
- Significance threshold: 0.05
- Drift detected in the simulated batch.

## Model Retraining
- Algorithm: RandomForestClassifier
- Number of estimators: 100
- Historical records: 1,143
- Simulated recent labeled records: 200
- Training records: 1,074
- Testing records: 269

## Model Evaluation

| Model | Accuracy |
|---|---:|
| Original baseline | 71.62% |
| Retrained candidate | 65.80% |
| Required minimum | 70.00% |

Accuracy difference: -5.82 percentage points.

## Quality Gate
Result: FAIL

The candidate model did not meet the minimum accuracy requirement of 70%.
Therefore, it was rejected and no approved model was created.

The existing Project 12 model was not modified.

## Important Limitation
The recent labeled dataset was created for classroom demonstration.
Its labels were copied from original WineQT records while selected
input features were artificially shifted. These labels are not genuine
production ground truth.

## Conclusion
The data drift detection, conditional retraining, model evaluation,
and quality-gate rejection workflow executed successfully.
