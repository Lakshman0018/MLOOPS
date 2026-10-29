import json
import sys
MINIMUM_ACCURACY=0.70
with open('metrics.json') as f: m=json.load(f)
a=m['accuracy']; print('Model Accuracy:',round(a,4)); print('Required Accuracy:',MINIMUM_ACCURACY)
if a < MINIMUM_ACCURACY: print('QUALITY GATE FAILED'); sys.exit(1)
print('QUALITY GATE PASSED')
