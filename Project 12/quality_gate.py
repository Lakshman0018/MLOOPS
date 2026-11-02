import json
import sys

MINIMUM_ACCURACY = 0.70

with open("metrics.json") as f:
    metrics = json.load(f)

accuracy = metrics["accuracy"]
print("Model Accuracy:", round(accuracy, 4))

if accuracy < MINIMUM_ACCURACY:
    print("QUALITY GATE FAILED")
    sys.exit(1)

print("QUALITY GATE PASSED")
