import pandas as pd

def load_csv(file):
    df = pd.read_csv(file)
    return df.to_string(index=False)
