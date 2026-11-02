import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
BASE_DIR=Path(__file__).resolve().parent
DATASET_PATH=BASE_DIR/'WineQT.csv'
MODEL_PATH=BASE_DIR/'wine_quality_model.pkl'
METRICS_PATH=BASE_DIR/'metrics.json'
def main():
    data=pd.read_csv(DATASET_PATH)
    X=data.drop(columns=['quality','Id']); y=data['quality']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)
    print('Number of records:',len(data)); print('Training records:',len(X_train)); print('Testing records:',len(X_test))
    model=RandomForestClassifier(n_estimators=100,random_state=42); model.fit(X_train,y_train)
    accuracy=accuracy_score(y_test,model.predict(X_test)); print('Accuracy:',round(accuracy,4))
    joblib.dump(model,MODEL_PATH)
    with open(METRICS_PATH,'w') as f: json.dump({'accuracy':float(accuracy),'training_records':len(X_train),'testing_records':len(X_test),'classes':[int(v) for v in model.classes_]},f,indent=4)
if __name__=='__main__': main()
