import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_anomalous_data():
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    dates.reverse()
    
    # Normal pipeline metrics data
    df = pd.DataFrame({
        'date': dates,
        'active_users': np.random.randint(5000, 7000, size=30),
        'transaction_volume': np.random.uniform(20000, 50000, size=30),
        'null_user_id_rate': np.random.uniform(0.0, 0.02, size=30)
    })
    
    # Inject an anomaly on the last day (Data quality issue simulation)
    df.loc[df.index[-1], 'active_users'] = 1200  # Sudden drop
    df.loc[df.index[-1], 'null_user_id_rate'] = 0.35 # Spike in null rate
    
    df.to_csv('pipeline_metrics.csv', index=False)
    print("Synthetic anomalous data generated successfully!")

if __name__ == "__main__":
    generate_anomalous_data()