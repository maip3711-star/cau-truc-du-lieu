import pandas as pd
import random
import os

def create_datasets(n=20000, raw_path="kc_house_data.csv", save_csv=True, data_dir="data/processed"):
    """
    Tạo 5 tập dữ liệu A, B, C, D, E.
    Nếu save_csv=True và thư mục data_dir tồn tại, sẽ lưu các tập thành file CSV.
    Trả về: (list các dataset, list tên)
    """
    # Đọc dữ liệu gốc
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
    
    datasets = [A, B, C, D, E]
    names = ["A", "B", "C", "D", "E"]
    
    if save_csv:
        os.makedirs(data_dir, exist_ok=True)
        for name, data in zip(names, datasets):
            df_out = pd.DataFrame(data, columns=["price"])
            df_out.to_csv(os.path.join(data_dir, f"{name}.csv"), index=False)
        print(f"Đã lưu 5 tập dữ liệu vào thư mục {data_dir}")
    
    return datasets, names

def load_or_create_datasets(n=20000, raw_path="kc_house_data.csv", data_dir="data/processed"):
    """
    Nếu đã có file CSV trong data_dir thì đọc, nếu không thì tạo mới.
    Trả về: (list các dataset, list tên)
    """
    if all(os.path.exists(os.path.join(data_dir, f"{name}.csv")) for name in ["A","B","C","D","E"]):
        datasets = []
        for name in ["A","B","C","D","E"]:
            df = pd.read_csv(os.path.join(data_dir, f"{name}.csv"))
            datasets.append(df["price"].tolist())
        print("Đã đọc dữ liệu từ file CSV.")
        return datasets, ["A","B","C","D","E"]
    else:
        print("Chưa có file CSV, tiến hành tạo dữ liệu mới...")
        return create_datasets(n, raw_path, save_csv=True, data_dir=data_dir)

if __name__ == "__main__":
    # Chạy thử: tạo và lưu dữ liệu
    datasets, names = create_datasets()
    for name, data in zip(names, datasets):
        print(f"{name}: {len(data)} phần tử, ví dụ: {data[:5]}")
