# -*- coding: utf-8 -*-
"""
adaptive_sort.py
Xây dựng bộ điều phối thích nghi adaptive_sort()
             dựa vào tỷ lệ nghịch thế và xu hướng dữ liệu.
"""

from sort_algorithms import insertion_sort, quick_sort, merge_sort, heap_sort
from data_analyzer   import _analyze


# ============================================================
# BỘ ĐIỀU PHỐI THÍCH NGHI
# ============================================================

def adaptive_sort(arr, verbose=False):
    """
    Sắp xếp mảng theo chiến lược thích nghi.

    Chiến lược lựa chọn (1 lần duyệt sampling duy nhất):
      - trend == 'increasing' → Insertion Sort  (gần như đã sắp xếp, O(n))
      - trend == 'decreasing' → Merge Sort       (tránh worst-case Quick Sort)
      - trend == 'random'     → Quick Sort       (median-of-three, nhanh nhất tb)

    Ngưỡng phát hiện trend:
      inc_ratio >= 90% → increasing  (bắt cả Tập B lẫn Tập D 5% đảo)
      dec_ratio >= 95% → decreasing  (chỉ bắt Tập C đảo ngược hoàn toàn)
      còn lại          → random

    Trả về: list mới đã sắp xếp, KHÔNG sửa mảng gốc.
    """
    n = len(arr)
    if n <= 1:
        return arr.copy()

    # ── Phân tích đặc tính (1 lần duyệt duy nhất) ───────────
    inv_ratio, inc_ratio = _analyze(arr)
    dec_ratio            = 1.0 - inc_ratio / 100 if inc_ratio > 1 else 1.0 - inc_ratio

    # Xác định trend từ inc_ratio (0.0–1.0)
    if inc_ratio >= 0.90:
        trend = 'increasing'
    elif (1.0 - inc_ratio) >= 0.95:
        trend = 'decreasing'
    else:
        trend = 'random'

    # ── Chọn và gọi thuật toán ───────────────────────────────
    if trend == 'increasing':
        if verbose:
            print(f"  [adaptive_sort] → Insertion Sort "
                  f"(inv={inv_ratio:.2f}%, trend={trend})")
        return insertion_sort(arr)

    elif trend == 'decreasing':
        if verbose:
            print(f"  [adaptive_sort] → Merge Sort "
                  f"(inv={inv_ratio:.2f}%, trend={trend})")
        return merge_sort(arr)

    else:
        if verbose:
            print(f"  [adaptive_sort] → Quick Sort "
                  f"(inv={inv_ratio:.2f}%, trend={trend})")
        return quick_sort(arr)


# ============================================================
# KIỂM THỬ KHI CHẠY TRỰC TIẾP
# ============================================================

if __name__ == "__main__":
    import random
    from sort_algorithms import is_sorted

    random.seed(42)
    n   = 20000
    A   = [random.randint(100000, 2000000) for _ in range(n)]
    B   = sorted(A); C = B[::-1]
    D   = B.copy()
    idx = random.sample(range(n), 2000)
    for k in range(0, len(idx)-1, 2):
        D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]
    E   = A.copy()
    idx = random.sample(range(n), 12000)
    for k in range(0, len(idx)-1, 2):
        E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]

    cases = {
        "A – Ngẫu nhiên": A,
        "B – Tăng dần  ": B,
        "C – Giảm dần  ": C,
        "D – 5%  đảo   ": D,
        "E – 30% đảo   ": E,
    }

    print("=" * 70)
    print("KIỂM THỬ adaptive_sort")
    print("=" * 70)
    all_pass = True
    for name, data in cases.items():
        result = adaptive_sort(data, verbose=True)
        ok     = is_sorted(result) and result == sorted(data)
        if not ok: all_pass = False
        assert data == data, "Mảng gốc bị thay đổi!"
        print(f"  {name}: {'✓ PASS' if ok else '✗ FAIL'}\n")

    print("=" * 70)
    print("Kết quả:", "✓ Tất cả PASS" if all_pass else "✗ Có lỗi!")
    print("=" * 70)
