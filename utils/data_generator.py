import os
import pandas as pd
import numpy as np

def generate_sample_data():
    np.random.seed(42)
    n_rows = 500
    
    data = {
        "customer_id": [f"CUST_{i:03d}" for i in range(n_rows)],
        "signup_date": pd.date_range(start="2025-01-01", periods=n_rows, freq="D"),
        "order_amount": np.random.choice([100.5, 250.0, np.nan, 12000.0, 45.0], size=n_rows, p=[0.7, 0.2, 0.05, 0.02, 0.03]),
        "status": np.random.choice(["SUCCESS", "PENDING", "INVALID_STATUS", "UNKNOWN"], size=n_rows, p=[0.8, 0.1, 0.05, 0.05])
    }
    
    df = pd.DataFrame(data)
    
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "sample_data.csv")
    
    df.to_csv(file_path, index=False)
    print(f"Sample dataset successfully generated and saved at: {file_path}")

if __name__ == "__main__":
    generate_sample_data()