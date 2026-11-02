from pathlib import Path
import joblib
import pandas as pd
from flask import Flask,jsonify,request
app=Flask(__name__)
MODEL_PATH=Path(__file__).resolve().parent/'wine_quality_model.pkl'
FEATURES=['fixed acidity','volatile acidity','citric acid','residual sugar','chlorides','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol']
def load_model(): return joblib.load(MODEL_PATH)
@app.get('/')
def root(): return jsonify({'status':'ok','service':'wine-quality-prediction'})
@app.get('/health')
def health(): return jsonify({'status':'healthy'})
@app.post('/predict')
def predict():
    data=request.get_json(silent=True)
    if not data: return jsonify({'error':'JSON request body is required'}),400
    missing=[f for f in FEATURES if f not in data]
    if missing: return jsonify({'error':'Missing required fields','missing_fields':missing}),400
    sample=pd.DataFrame([{f:data[f] for f in FEATURES}]); p=int(load_model().predict(sample)[0])
    return jsonify({'prediction':p,'prediction_code':p})
if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
