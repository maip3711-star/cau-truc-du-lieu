# -*- coding: utf-8 -*-
"""
adaptive_sort.py
 Xây dựng bộ điều phối thích nghi adaptive_sort()
             dựa vào tỷ lệ nghịch thế và xu hướng dữ liệu.
"""

from sort_algorithms import insertion_sort, quick_sort, merge_sort, heap_sort
from data_analyzer   import inversion_ratio, detect_trend


# ============================================================
# BỘ ĐIỀU PHỐI THÍCH NGHI
# ============================================================

def adaptive_sort(arr, verbose=False):
    """
    Sắp xếp mảng theo chiến lược thích nghi.

    Chiến lược lựa chọn:
      Bước 1 — Phân tích đặc tính:
        - Tính tỷ lệ nghịch thế (inv_ratio) bằng Merge Sort cải tiến O(n log n)
        - Phát hiện xu hướng (trend): increasing / decreasing / random

      Bước 2 — Chọn thuật toán:
        - inv_ratio < 5%          → Insertion Sort  (tận dụng O(n) khi gần sắp xếp)
        - trend == 'decreasing'   → Merge Sort       (tránh worst-case của Quick Sort)
        - còn lại                 → Quick Sort       (median-of-three, nhanh nhất tb)

    Tham số:
      arr     : list cần sắp xếp
      verbose : True → in ra thuật toán được chọn (dùng khi debug)

    Trả về: list mới đã sắp xếp, KHÔNG sửa mảng gốc.
    """
    n = len(arr)
    if n <= 1:
        return arr.copy()

    # ── Bước 1: Phân tích đặc tính ──────────────────────────
    inv_ratio = inversion_ratio(arr)
    trend     = detect_trend(arr)

    # ── Bước 2: Chọn và gọi thuật toán ──────────────────────
    if inv_ratio < 5.0:
        if verbose:
            print(f"  [adaptive_sort] → Insertion Sort "
                  f"(inv_ratio={inv_ratio:.2f}%, trend={trend})")
        return insertion_sort(arr)

    elif trend == 'decreasing':
        if verbose:
            print(f"  [adaptive_sort] → Merge Sort "
                  f"(inv_ratio={inv_ratio:.2f}%, trend={trend})")
        return merge_sort(arr)

    else:
        if verbose:
            print(f"  [adaptive_sort] → Quick Sort "
                  f"(inv_ratio={inv_ratio:.2f}%, trend={trend})")
        return quick_sort(arr)


# ============================================================
# KIỂM THỬ KHI CHẠY TRỰC TIẾP
# ============================================================

if __name__ == "__main__":
    from sort_algorithms import is_sorted

    test_cases = {
        "Ngẫu nhiên          ": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
        "Gần đúng (1 lệch)   ": [1, 2, 3, 5, 4, 6, 7, 8, 9, 10],
        "Tăng dần hoàn toàn  ": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Giảm dần hoàn toàn  ": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Phần tử bằng nhau   ": [5, 5, 5, 3, 3, 1, 1, 2, 2, 4],
        "1 phần tử           ": [42],
        "Mảng rỗng           ": [],
    }

    print("=" * 70)
    print("KIỂM THỬ adaptive_sort")
    print("=" * 70)
    print(f"{'Trường hợp':<25} {'Thuật toán chọn':<18} {'Kết quả':<10} {'Đúng?'}")
    print("-" * 70)

    all_pass = True
    for name, data in test_cases.items():
        original = data.copy()
        result   = adaptive_sort(data, verbose=False)

        # Xác định thuật toán được chọn
        if len(data) <= 1:
            chosen = "—"
        else:
            from data_analyzer import inversion_ratio as ir, detect_trend as dt
            ratio = ir(data)
            trend = dt(data)
            if ratio < 5.0:
                chosen = "Insertion Sort"
            elif trend == 'decreasing':
                chosen = "Merge Sort"
            else:
                chosen = "Quick Sort"

        ok = is_sorted(result) and (sorted(original) == result)
        if not ok:
            all_pass = False

        print(
            f"{name:<25} {chosen:<18} "
            f"{str(result[:4])+'...' if len(result)>4 else str(result):<22}"
            f"{'✓' if ok else '✗ LỖI'}"
        )

        # Kiểm tra mảng gốc không bị sửa
        assert data == original, f"Mảng gốc bị thay đổi ở: {name}"

    print("-" * 70)
    print("Mảng gốc được bảo vệ : ✓")
    print("Kết quả tổng          :", "✓ Tất cả PASS" if all_pass else "✗ Có lỗi!")
    print("=" * 70)
