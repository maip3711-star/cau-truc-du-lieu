import pandas as pd
import random

def create_datasets(n=20000, raw_path="kc_house_data.csv"):
    df = pd.read_csv(raw_path)
    price = df["price"].astype(int).tolist()
    random.seed(42)
    A = random.sample(price, n)
    B = sorted(A)
    C = B[::-1]
    D = A.copy()
    for _ in range(int(n * 0.05)):
        i, j = random.sample(range(n), 2)
        D[i], D[j] = D[j], D[i]
    E = A.copy()
    for _ in range(int(n * 0.3)):
        i, j = random.sample(range(n), 2)
        E[i], E[j] = E[j], E[i]
    return A, B, C, D, E
