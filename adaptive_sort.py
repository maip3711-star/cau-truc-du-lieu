# -*- coding: utf-8 -*-
"""
adaptive_sort.py
 Xây dựng bộ điều phối thích nghi adaptive_sort()
             dựa vào tỷ lệ nghịch thế và xu hướng dữ liệu.
"""
import sys
import os
SCRIPT_DIR = r"C:\Users\TDG\Downloads"
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
from sort_algorithms import insertion_sort, quick_sort, merge_sort, heap_sort
from data_analyzer   import inversion_ratio, detect_trend


# ============================================================
# BỘ ĐIỀU PHỐI THÍCH NGHI
# ============================================================

def adaptive_sort(arr, verbose=False):
    """
    Sắp xếp mảng theo chiến lược thích nghi.

    Chiến lược lựa chọn:
      - trend == 'increasing' → Insertion Sort  (gần như đã sắp xếp, O(n))
      - trend == 'decreasing' → Merge Sort       (tránh worst-case Quick Sort)
      - trend == 'random'     → Quick Sort       (median-of-three, nhanh nhất tb)

    Trả về: list mới đã sắp xếp, KHÔNG sửa mảng gốc.
    """
    n = len(arr)
    if n <= 1:
        return arr.copy()

    # ── Phân tích đặc tính ───────────────────────────────────
    inv_ratio = inversion_ratio(arr)
    trend     = detect_trend(arr)

    # ── Chọn và gọi thuật toán ───────────────────────────────
    if trend == "increasing" and inv_ratio < 0.05:
        if verbose: print("→ Insertion Sort (near-sorted)")
        return insertion_sort(arr)
    elif trend == "decreasing":
        if verbose: print("→ Merge Sort (reverse)")
        return merge_sort(arr)
    else:  # Random/medium disorder → QuickSort WIN!
        if verbose: print("→ Quick Sort (random/medium)")
        return quick_sort(arr) 
    

# ============================================================
# KIỂM THỬ KHI CHẠY TRỰC TIẾP
# ============================================================

if __name__ == "__main__":
    import random
    import time
    from sort_algorithms import is_sorted

    random.seed(42)

    n = 20000

    A = [random.randint(100000, 2000000) for _ in range(n)]

    B = sorted(A)
    C = B[::-1]

    D = B.copy()
    idx = random.sample(range(n), 2000)

    for k in range(0, len(idx)-1, 2):
        D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]

    E = A.copy()
    idx = random.sample(range(n), 12000)

    for k in range(0, len(idx)-1, 2):
        E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]

    cases = {
        "A – Ngẫu nhiên": A,
        "B – Tăng dần": B,
        "C – Giảm dần": C,
        "D – 5% đảo": D,
        "E – 30% đảo": E,
    }

    print("=" * 65)
    print("KIỂM THỬ adaptive_sort")
    print("=" * 65)

    all_pass = True

    for name, data in cases.items():

        t0 = time.perf_counter()

        result = adaptive_sort(data, verbose=True)

        ms = (time.perf_counter() - t0) * 1000

        ok = is_sorted(result) and result == sorted(data)

        if not ok:
            all_pass = False

        print(f"{name}: {ms:.2f} ms → {'PASS' if ok else 'FAIL'}\n")

    print("Kết quả:", "Tất cả PASS" if all_pass else "Có lỗi!")
    print("=" * 65)
