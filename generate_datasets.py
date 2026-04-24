import pandas as pd
import random

def load_or_create_datasets(n=20000, raw_path="kc_house_data.csv"):
    """
    Tạo 5 tập dữ liệu A, B, C, D, E theo đúng yêu cầu:
    - A: ngẫu nhiên từ dữ liệu gốc
    - B: tăng dần từ A
    - C: giảm dần từ A
    - D: gần sắp xếp (đảo 5% các phần tử của B)
    - E: hỗn loạn trung bình (đảo 30% các phần tử của A)
    """
    df = pd.read_csv(raw_path)
    price = df["price"].astype(int).tolist()
    random.seed(42)  # cố định kết quả

    # Lấy mẫu ngẫu nhiên n phần tử cho tập A
    A = random.sample(price, n)

    B = sorted(A)
    C = B[::-1]

    # Tập D: từ B (đã sắp xếp) đảo 5% phần tử
    D = B.copy()
    n_swap_D = int(n * 0.05)
    for _ in range(n_swap_D):
        i, j = random.sample(range(n), 2)
        D[i], D[j] = D[j], D[i]

    # Tập E: từ A (ngẫu nhiên) đảo 30% phần tử
    E = A.copy()
    n_swap_E = int(n * 0.3)
    for _ in range(n_swap_E):
        i, j = random.sample(range(n), 2)
        E[i], E[j] = E[j], E[i]

    datasets = [A, B, C, D, E]
    names = ["A", "B", "C", "D", "E"]
    return datasets, names
