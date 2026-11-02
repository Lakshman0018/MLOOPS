# Project 3 - Wine Quality ML Quality Gate

This project extends the Wine Quality ML CI workflow with an automated model-quality gate.

## Dataset
WineQT.csv

## Pipeline
1. Install ML dependencies
2. Train the Wine Quality model
3. Generate metrics.json
4. Check the minimum accuracy quality gate
5. Run automated ML tests when the gate passes

## Quality Gate
Normal minimum accuracy: 0.70

The threshold is adapted for the WineQT model used in Projects 1 and 2. The model achieved 0.7162 accuracy in the verified CI run, so 0.70 allows the normal workflow to pass.

For the controlled failure demonstration, set the threshold to 0.99.