import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(filepath="data/input/suricata_logs.csv"):
    df = pd.read_csv(filepath)
    features = df.select_dtypes(include=['float64', 'int64'])
    clf = IsolationForest(contamination=0.01)
    df['anomaly'] = clf.fit_predict(features)
    df.to_csv("data/output/anomaly_results.csv", index=False)
    return df

if __name__ == "__main__":
    detect_anomalies()
