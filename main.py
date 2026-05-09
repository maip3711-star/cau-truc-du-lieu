# -*- coding: utf-8 -*-
"""
main.py
Kiểm thử tính đúng đắn của adaptive_sort trên 5 tập dữ liệu A–E.
Mục tiêu:
- Kiểm tra output có đúng không (so với sorted())
- Kiểm tra tính ổn định của hệ thống
"""

import sys
import random
sys.path.append(r"C:\Users\TDG\Downloads")

from sort_algorithms import (
    insertion_sort,
    quick_sort,
    merge_sort,
    heap_sort,
    is_sorted
)

from adaptive_sort import adaptive_sort
from generate_datasets import generate_datasets


# ============================================================
# KIỂM THỬ TÍNH ĐÚNG ĐẮN
# ============================================================

def test_correctness(datasets):
    """
    Kiểm thử adaptive_sort:
      - Có sắp xếp đúng không (is_sorted)
      - Có khớp với sorted() Python không
    """

    tap_labels = {
        "A": "A – Ngẫu nhiên  ",
        "B": "B – Tăng dần    ",
        "C": "C – Giảm dần    ",
        "D": "D – 5%  đảo     ",
        "E": "E – 30% đảo     ",
    }

    print("=" * 75)
    print("KIỂM THỬ TÍNH ĐÚNG ĐẮN CỦA adaptive_sort")
    print("=" * 75)
    print(f"{'Tập':<22} {'Sorted?':<12} {'Khớp sorted()':<18}")
    print("-" * 75)

    all_pass = True

    for tap, label in tap_labels.items():

        data = datasets[tap]

        # QUAN TRỌNG: copy để tránh side-effect
        result = adaptive_sort(data.copy())

        # Kiểm tra đúng
        ok_sorted = is_sorted(result)
        ok_match  = (result == sorted(data))

        passed = ok_sorted and ok_match
        if not passed:
            all_pass = False

        print(
            f"{label:<22}"
            f"{'✓' if ok_sorted else '✗':<12}"
            f"{'✓' if ok_match else '✗'}"
        )

    print("-" * 75)
    print("Kết quả:", "✓ TẤT CẢ PASS" if all_pass else "✗ CÓ LỖI")
    print()

    return all_pass


# ============================================================
# DEBUG KHI LỖI
# ============================================================

def debug_mismatch(datasets):
    """
    In 10 phần tử đầu để kiểm tra lỗi nếu có sai lệch.
    """

    print("=" * 60)
    print("DEBUG CHI TIẾT (10 PHẦN TỬ ĐẦU)")
    print("=" * 60)

    for tap in "ABCDE":
        data = datasets[tap]

        print(f"\nTập {tap}: {data[:5]}")

        result = adaptive_sort(data.copy())

        print(f"Adaptive Sort : {result[:10]}")
        print(f"Sorted()      : {sorted(data)[:10]}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    CSV_PATH = r"C:\Users\TDG\Downloads\kc_house_data.csv"

    # ========================================================
    # LOAD DATASETS
    # ========================================================

    try:
        datasets = generate_datasets(csv_path=CSV_PATH, n=20000)

    except FileNotFoundError as e:

        print(f"[Lỗi] {e}")
        print("Dùng dữ liệu giả lập...")

        random.seed(42)

        fake = [
            random.randint(100_000, 2_000_000)
            for _ in range(1000)
        ]

        B = sorted(fake)

        C = B[::-1]

        D = B.copy()
        idx = random.sample(range(1000), 100)
        for i in range(0, len(idx) - 1, 2):
            D[idx[i]], D[idx[i+1]] = D[idx[i+1]], D[idx[i]]

        E = fake.copy()
        idx = random.sample(range(1000), 300)
        for i in range(0, len(idx) - 1, 2):
            E[idx[i]], E[idx[i+1]] = E[idx[i+1]], E[idx[i]]

        datasets = {
            "A": fake,
            "B": B,
            "C": C,
            "D": D,
            "E": E
        }

    # ========================================================
    # RUN TEST
    # ========================================================

    passed = test_correctness(datasets)

    # ========================================================
    # DEBUG IF FAIL
    # ========================================================

    if not passed:
        debug_mismatch(datasets)
        sys.exit(1)

    print("Hoàn thành kiểm thử thành công.")
