# -*- coding: utf-8 -*-
"""
tung_test.py
Thành viên : Phạm Quang Tùng – 24070566
Nhiệm vụ   : Kiểm thử tính đúng đắn của adaptive_sort so với
             các thuật toán đơn lẻ trên 5 tập dữ liệu A–E.
Phụ trách  : Phần 3 báo cáo
Môi trường : Google Colab
"""

import sys
import random

from sort_algorithms   import insertion_sort, quick_sort, merge_sort, heap_sort, is_sorted
from adaptive_sort     import adaptive_sort
from generate_datasets import generate_datasets


# ============================================================
# KIỂM THỬ TÍNH ĐÚNG ĐẮN
# ============================================================

def test_correctness(datasets):
    """
    Kiểm thử adaptive_sort có cho kết quả đúng không bằng cách:
      1. Kiểm tra kết quả đã sắp xếp tăng dần (is_sorted)
      2. So sánh với sorted() của Python — ground truth tuyệt đối
      3. So sánh với từng thuật toán đơn lẻ (Insertion/Quick/Merge/Heap)
    """
    algorithms = {
        "Insertion Sort": insertion_sort,
        "Quick Sort"    : quick_sort,
        "Merge Sort"    : merge_sort,
        "Heap Sort"     : heap_sort,
    }

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
    print(f"{'Tập':<22} {'Đã sắp xếp?':<14} {'Khớp sorted()':<16} {'Khớp 4 thuật toán?'}")
    print("-" * 75)

    all_pass = True

    for tap, label in tap_labels.items():
        data = datasets[tap]

        result_adaptive = adaptive_sort(data)

        # Kiểm tra 1: đã sắp xếp tăng dần?
        ok_sorted = is_sorted(result_adaptive)

        # Kiểm tra 2: khớp sorted() Python?
        ok_match  = (result_adaptive == sorted(data))

        # Kiểm tra 3: khớp từng thuật toán đơn lẻ?
        ok_algos  = all(
            result_adaptive == func(data)
            for func in algorithms.values()
        )

        passed = ok_sorted and ok_match and ok_algos
        if not passed:
            all_pass = False

        print(
            f"{label:<22}"
            f"{'✓ Có'    if ok_sorted else '✗ Chưa':<14}"
            f"{'✓ Khớp'  if ok_match  else '✗ Lệch':<16}"
            f"{'✓ Tất cả khớp' if ok_algos else '✗ Có lệch'}"
        )

    print("-" * 75)
    print("Kết quả:", "✓ Tất cả PASS" if all_pass else "✗ Có lỗi – kiểm tra lại")
    print()
    return all_pass


# ============================================================
# DEBUG KHI CÓ LỖI
# ============================================================

def debug_mismatch(datasets):
    """In chi tiết 10 phần tử đầu của từng kết quả khi phát hiện lệch."""
    algorithms = {
        "adaptive_sort" : adaptive_sort,
        "insertion_sort": insertion_sort,
        "quick_sort"    : quick_sort,
        "merge_sort"    : merge_sort,
        "heap_sort"     : heap_sort,
        "sorted() Python": lambda x: sorted(x),
    }

    print("=" * 60)
    print("CHI TIẾT DEBUG (10 phần tử đầu mỗi kết quả)")
    print("=" * 60)
    for tap in "ABCDE":
        data = datasets[tap]
        print(f"\nTập {tap} (input[:5] = {data[:5]}):")
        for name, func in algorithms.items():
            print(f"  {name:<20}: {func(data)[:10]}")


# ============================================================
# MAIN — chạy trên Colab
# ============================================================

if __name__ == "__main__":
    # Đường dẫn file CSV trên Colab
    CSV_PATH = "/content/kc_house_data.csv"

    # Tải / tạo 5 tập dữ liệu
    try:
        datasets = generate_datasets(csv_path=CSV_PATH, n=20000)
    except FileNotFoundError as e:
        print(f"[Lỗi] {e}")
        print("\nDùng dữ liệu giả lập (1,000 phần tử) để demo...\n")
        random.seed(42)
        fake   = [random.randint(100_000, 2_000_000) for _ in range(1000)]
        B      = sorted(fake)
        D      = B.copy()
        idx    = random.sample(range(1000), 50 * 2)
        for k in range(0, len(idx)-1, 2):
            D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]
        E      = fake.copy()
        idx    = random.sample(range(1000), 300 * 2)
        for k in range(0, len(idx)-1, 2):
            E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]
        datasets = {"A": fake, "B": B, "C": sorted(fake, reverse=True), "D": D, "E": E}

    # Chạy kiểm thử
    passed = test_correctness(datasets)

    # Nếu có lỗi thì in chi tiết debug
    if not passed:
        debug_mismatch(datasets)
        sys.exit(1)
