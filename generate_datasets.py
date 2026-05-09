# -*- coding: utf-8 -*-
"""
generate_datasets.py 

Chức năng:
- Tạo 5 tập dữ liệu A–E từ kc_house_data.csv
- Đảm bảo tính tái lập (deterministic)
- Phục vụ benchmark thuật toán sắp xếp thích nghi
"""

import pandas as pd
import random
import os

# ============================================================
# CẤU HÌNH
# ============================================================

CSV_PATH = r"C:\Users\TDG\Downloads\kc_house_data.csv"

PROCESSED_DIR = r"C:\Users\TDG\Downloads\data\processed"

N = 20000

RANDOM_SEED = 42


# ============================================================
# HÀM CHÍNH TẠO DATASETS
# ============================================================

def generate_datasets(csv_path=CSV_PATH, n=N, force=False):

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    tap_names = ["A", "B", "C", "D", "E"]

    # ========================================================
    # LOAD CACHE (nếu có)
    # ========================================================

    if not force and all(
        os.path.exists(os.path.join(PROCESSED_DIR, f"tap_{t}.csv"))
        for t in tap_names
    ):
        print("✓ Đang đọc dữ liệu từ cache...")

        datasets = {}

        for t in tap_names:
            path = os.path.join(PROCESSED_DIR, f"tap_{t}.csv")
            datasets[t] = pd.read_csv(path)["price"].tolist()

        _print_summary(datasets)
        return datasets

    # ========================================================
    # LOAD CSV
    # ========================================================

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Không tìm thấy file: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    if "price" not in df.columns:
        raise ValueError("Thiếu cột 'price' trong dataset")

    price_all = df["price"].dropna().astype(int).tolist()

    if len(price_all) < n:
        raise ValueError("Không đủ dữ liệu để tạo tập n phần tử")

    print(f"✓ Tổng dữ liệu gốc: {len(price_all):,}")

    # ========================================================
    # TẠO TẬP A (NGẪU NHIÊN)
    # ========================================================

    random.seed(RANDOM_SEED)
    A = random.sample(price_all, n)

    # ========================================================
    # TẬP B (TĂNG DẦN)
    # ========================================================

    B = sorted(A)

    # ========================================================
    # TẬP C (GIẢM DẦN)
    # ========================================================

    C = B[::-1]

    # ========================================================
    # TẬP D (5% HOÁN ĐỔI - GẦN SORTED)
    # ========================================================

    random.seed(RANDOM_SEED + 1)

    D = B.copy()

    n_swap = int(n * 0.05)

    idx = random.sample(range(n), n_swap * 2)

    for i in range(0, len(idx) - 1, 2):
        D[idx[i]], D[idx[i + 1]] = D[idx[i + 1]], D[idx[i]]

    # ========================================================
    # TẬP E (30% HOÁN ĐỔI - HỖN LOẠN TRUNG BÌNH)
    # ========================================================

    random.seed(RANDOM_SEED + 2)

    E = A.copy()

    n_swap = int(n * 0.30)

    idx = random.sample(range(n), n_swap * 2)

    for i in range(0, len(idx) - 1, 2):
        E[idx[i]], E[idx[i + 1]] = E[idx[i + 1]], E[idx[i]]

    # ========================================================
    # GOM DATASETS
    # ========================================================

    datasets = {
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "E": E,
    }

    # ========================================================
    # SAVE CACHE
    # ========================================================

    for name, data in datasets.items():

        out_path = os.path.join(PROCESSED_DIR, f"tap_{name}.csv")

        pd.DataFrame({"price": data}).to_csv(out_path, index=False)

        print(f"  ✓ Saved {name} → {out_path}")

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    _print_summary(datasets)

    return datasets


# ============================================================
# THỐNG KÊ DATASET
# ============================================================

def _print_summary(datasets):

    labels = {
        "A": "Ngẫu nhiên",
        "B": "Tăng dần",
        "C": "Giảm dần",
        "D": "Gần sorted (5%)",
        "E": "Hỗn loạn (30%)",
    }

    print("\n" + "=" * 60)

    print(f"{'Tập':<5}{'Mô tả':<20}{'Size':>10}{'Min':>15}{'Max':>15}")

    print("=" * 60)

    for k, v in datasets.items():

        print(
            f"{k:<5}"
            f"{labels[k]:<20}"
            f"{len(v):>10,}"
            f"{min(v):>15,}"
            f"{max(v):>15,}"
        )

    print("=" * 60)


# ============================================================
# VERIFY DATASETS (KIỂM TRA NHANH)
# ============================================================

def _verify_datasets(datasets):

    A, B, C, D, E = [datasets[k] for k in "ABCDE"]

    n = len(A)

    print("\nKIỂM TRA TÍNH ĐÚNG ĐẮN:")

    checks = [
        ("B tăng dần", all(B[i] <= B[i + 1] for i in range(n - 1))),
        ("C giảm dần", all(C[i] >= C[i + 1] for i in range(n - 1))),
        ("B là đảo của C", B == C[::-1]),
        ("D gần sorted", sorted(D) == B),
        ("E giống phân phối A", sorted(E) == sorted(A)),
        ("Đúng kích thước", all(len(datasets[k]) == n for k in "ABCDE")),
    ]

    ok_all = True

    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")
        if not ok:
            ok_all = False

    print("\nKết quả:", "✓ OK" if ok_all else "✗ LỖI")


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":

    datasets = generate_datasets()

    _verify_datasets(datasets)

    print("\nImport dùng trong project:")

    print("from generate_datasets import generate_datasets")
    print("datasets = generate_datasets()")
