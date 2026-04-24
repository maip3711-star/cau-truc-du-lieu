# generate_datasets.py
import pandas as pd
import random
import os

def load_or_create_datasets(n=20000):
    """
    Tải hoặc tạo 5 tập dữ liệu A, B, C, D, E.
    Trả về: (list các dataset, list tên tương ứng)
    """
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    # Nếu đã có file CSV thì đọc, nếu không thì tạo mới (cần dữ liệu gốc)
    if all(os.path.exists(os.path.join(processed_dir, f"{name}.csv")) for name in ["A","B","C","D","E"]):
        datasets = []
        for name in ["A","B","C","D","E"]:
            df = pd.read_csv(os.path.join(processed_dir, f"{name}.csv"))
            datasets.append(df["price"].tolist())
        return datasets, ["A","B","C","D","E"]
    else:
        # Nếu chưa có, cần sinh dữ liệu từ file gốc (giả sử có kc_house_data.csv)
        raw_path = "data/raw/kc_house_data.csv"
        if not os.path.exists(raw_path):
            raise FileNotFoundError("Không tìm thấy dữ liệu gốc. Hãy tải từ Kaggle và đặt vào data/raw/")
        df = pd.read_csv(raw_path)
        price = df["price"].astype(int).tolist()
        
        # Tạo tập A: chọn ngẫu nhiên n phần tử
        random.seed(42)
        A = random.sample(price, n)
        B = sorted(A)
        C = B[::-1]
        D = A.copy()
        n_swap = int(n * 0.05)
        for _ in range(n_swap):
            i, j = random.sample(range(n), 2)
            D[i], D[j] = D[j], D[i]
        E = A.copy()
        n_swap = int(n * 0.30)
        for _ in range(n_swap):
            i, j = random.sample(range(n), 2)
            E[i], E[j] = E[j], E[i]
        
        # Lưu lại
        for name, data in zip(["A","B","C","D","E"], [A,B,C,D,E]):
            pd.DataFrame(data, columns=["price"]).to_csv(os.path.join(processed_dir, f"{name}.csv"), index=False)
        return [A,B,C,D,E], ["A","B","C","D","E"]
