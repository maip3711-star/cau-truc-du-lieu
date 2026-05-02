# -*- coding: utf-8 -*-
"""
generate_datasets.py
 Tải dữ liệu gốc từ Kaggle, trích cột price,
             tạo 5 tập dữ liệu A–E theo đúng yêu cầu đề tài.
"""

import pandas as pd
import random
import os

# ============================================================
# CẤU HÌNH – chỉ cần chỉnh ở đây nếu đổi đường dẫn
# ============================================================
CSV_PATH      = "/content/kc_house_data.csv"   # file đã upload lên Colab
PROCESSED_DIR = "/content/data/processed"       # thư mục lưu 5 tập
N             = 20000                           # số bản ghi mỗi tập
RANDOM_SEED   = 42


# ============================================================
# HÀM CHÍNH
# ============================================================

def generate_datasets(csv_path=CSV_PATH, n=N, force=False):
    """
    Đọc file CSV Kaggle, trích cột price và tạo 5 tập A–E.

    Tập A : n phần tử chọn ngẫu nhiên từ dữ liệu gốc
    Tập B : Tập A sắp xếp tăng dần  (đã sắp xếp hoàn toàn)
    Tập C : Tập A sắp xếp giảm dần  (đảo ngược hoàn toàn)
    Tập D : Tập B hoán đổi ngẫu nhiên đúng 5%  phần tử (gần như đã sắp xếp)
    Tập E : Tập A hoán đổi ngẫu nhiên đúng 30% phần tử (độ hỗn loạn trung bình)

    Tham số:
      csv_path : đường dẫn file kc_house_data.csv
      n        : số bản ghi mỗi tập (mặc định 20,000)
      force    : True → tạo lại dù đã có file cache

    Trả về: dict {"A": [...], "B": [...], "C": [...], "D": [...], "E": [...]}
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    tap_names = ["A", "B", "C", "D", "E"]

    # ── Nếu đã có file cache thì đọc luôn ──────────────────
    if not force and all(
        os.path.exists(os.path.join(PROCESSED_DIR, f"tap_{name}.csv"))
        for name in tap_names
    ):
        print("✓ Đọc 5 tập từ file cache...")
        datasets = {}
        for name in tap_names:
            path = os.path.join(PROCESSED_DIR, f"tap_{name}.csv")
            datasets[name] = pd.read_csv(path)["price"].tolist()
        _print_summary(datasets)
        return datasets

    # ── Bước 1: Đọc file CSV ────────────────────────────────
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Không tìm thấy file '{csv_path}'.\n"
            f"Hãy upload file kc_house_data.csv lên Colab:\n"
            f"  Cách 1: Kéo thả file vào panel bên trái\n"
            f"  Cách 2: Dùng lệnh: from google.colab import files; files.upload()"
        )

    print(f"Đọc dữ liệu từ: {csv_path}")
    df = pd.read_csv(csv_path)

    if "price" not in df.columns:
        raise ValueError(
            f"Không tìm thấy cột 'price'.\n"
            f"Các cột hiện có: {list(df.columns)}"
        )

    price_all = df["price"].dropna().astype(int).tolist()
    print(f"  Tổng bản ghi gốc : {len(price_all):,}")

    if len(price_all) < n:
        raise ValueError(f"File chỉ có {len(price_all):,} bản ghi, cần ít nhất {n:,}.")

    # ── Bước 2: Tạo Tập A ──────────────────────────────────
    random.seed(RANDOM_SEED)
    A = random.sample(price_all, n)

    # ── Bước 3: Tạo Tập B và C ─────────────────────────────
    B = sorted(A)
    C = B[::-1]

    # ── Bước 4: Tập D — Tập B hoán đổi đúng 5% ────────────
    D      = B.copy()
    n_swap = int(n * 0.05)
    idx    = random.sample(range(n), n_swap * 2)
    for k in range(0, len(idx) - 1, 2):
        D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]

    # ── Bước 5: Tập E — Tập A hoán đổi đúng 30% ───────────
    E      = A.copy()
    n_swap = int(n * 0.30)
    idx    = random.sample(range(n), n_swap * 2)
    for k in range(0, len(idx) - 1, 2):
        E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]

    datasets = {"A": A, "B": B, "C": C, "D": D, "E": E}

    # ── Bước 6: Lưu cache ──────────────────────────────────
    for name, data in datasets.items():
        out = os.path.join(PROCESSED_DIR, f"tap_{name}.csv")
        pd.DataFrame({"price": data}).to_csv(out, index=False)
        print(f"  Đã lưu Tập {name} → {out}")

    _print_summary(datasets)
    return datasets


# ============================================================
# IN THỐNG KÊ
# ============================================================

def _print_summary(datasets):
    labels = {
        "A": "Ngẫu nhiên        ",
        "B": "Tăng dần          ",
        "C": "Giảm dần          ",
        "D": "Gần sắp xếp (5%)  ",
        "E": "Hỗn loạn TB (30%) ",
    }
    print()
    print("=" * 62)
    print(f"{'Tập':<4} {'Mô tả':<22} {'Bản ghi':>8}  {'Min':>10}  {'Max':>12}")
    print("=" * 62)
    for name, data in datasets.items():
        print(
            f"  {name}  {labels[name]}"
            f"{len(data):>8,}  "
            f"{min(data):>10,}  "
            f"{max(data):>12,}"
        )
    print("=" * 62)


# ============================================================
# KIỂM TRA TÍNH ĐÚNG ĐẮN
# ============================================================

def _verify_datasets(datasets):
    A, B, C, D, E = [datasets[k] for k in "ABCDE"]
    n = len(A)

    print("\nKIỂM TRA TÍNH ĐÚNG ĐẮN:")
    print("-" * 45)
    checks = [
        ("Tập B tăng dần",        all(B[i] <= B[i+1] for i in range(n-1))),
        ("Tập C giảm dần",        all(C[i] >= C[i+1] for i in range(n-1))),
        ("B và C là đảo nhau",    B == C[::-1]),
        ("D xuất phát từ B",      sorted(D) == B),
        ("E xuất phát từ A",      sorted(E) == sorted(A)),
        ("Mỗi tập đủ N phần tử", all(len(datasets[k]) == n for k in "ABCDE")),
    ]
    all_ok = True
    for desc, ok in checks:
        print(f"  {'✓' if ok else '✗ LỖI'}  {desc}")
        if not ok: all_ok = False
    print("-" * 45)
    print("  Kết quả:", "✓ Tất cả hợp lệ" if all_ok else "✗ Có lỗi!")
    print()


# ============================================================
# CHẠY TRỰC TIẾP TRÊN COLAB
# ============================================================

if __name__ == "__main__":
    datasets = generate_datasets()
    _verify_datasets(datasets)
    print("Dùng trong notebook:")
    print("  from generate_datasets import generate_datasets")
    print("  datasets = generate_datasets()")
    print("  price_A  = datasets['A']   # hoặc B, C, D, E")
