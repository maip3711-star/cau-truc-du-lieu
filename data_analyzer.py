# -*- coding: utf-8 -*-
"""
data_analyzer.py
               - Đếm nghịch thế, tính tỷ lệ nghịch thế
               - Phát hiện xu hướng sắp xếp của mảng
"""

# ============================================================
# 1. ĐẾM NGHỊCH THẾ & TÍNH TỶ LỆ
# ============================================================

def count_inversions(arr):
    """
    Đếm số cặp nghịch thế (i < j nhưng arr[i] > arr[j])
    bằng Merge Sort cải tiến — O(n log n).

    Trả về: số cặp nghịch thế (int)
    """
    if len(arr) <= 1:
        return 0
    _, inv = _merge_count(arr.copy())
    return inv


def _merge_count(arr):
    """Hàm đệ quy: sắp xếp + đếm nghịch thế đồng thời."""
    if len(arr) <= 1:
        return arr, 0

    mid   = len(arr) // 2
    left,  inv_left  = _merge_count(arr[:mid])
    right, inv_right = _merge_count(arr[mid:])

    merged = []
    inv    = inv_left + inv_right
    i = j  = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            # left[i] > right[j] → tất cả phần tử còn lại bên trái
            # đều tạo nghịch thế với right[j]
            inv += len(left) - i
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv


def inversion_ratio(arr, sample_size=500):
    """
    Ước lượng tỷ lệ nghịch thế (%) bằng phương pháp sampling — O(sample_size).

    Thay vì duyệt toàn bộ O(n log n), chỉ kiểm tra ngẫu nhiên
    sample_size cặp liền kề → đủ chính xác để quyết định thuật toán,
    đồng thời không làm chậm adaptive_sort.

      - ~0%   → mảng đã sắp xếp tăng dần (Insertion Sort)
      - ~100% → mảng đảo ngược hoàn toàn (Merge Sort)
      - ~50%  → mảng ngẫu nhiên           (Quick Sort)

    Tham số:
      sample_size : số cặp liền kề kiểm tra (mặc định 500)

    Trả về: float trong khoảng [0.0, 100.0]
    """
    import random
    n = len(arr)
    if n <= 1:
        return 0.0

    # Lấy mẫu ngẫu nhiên các vị trí liền kề
    indices = random.sample(range(n - 1), min(sample_size, n - 1))
    inv     = sum(1 for i in indices if arr[i] > arr[i + 1])
    return (inv / len(indices)) * 100.0


# ============================================================
# 2. PHÁT HIỆN XU HƯỚNG
# ============================================================

def detect_trend(arr, sample_size=500):
    """
    Phát hiện xu hướng sắp xếp của mảng bằng sampling — O(sample_size).

    Kiểm tra ngẫu nhiên sample_size cặp liền kề:
      - Nếu > 95% cặp tăng  → 'increasing'
      - Nếu > 95% cặp giảm  → 'decreasing'
      - Còn lại              → 'random'

    Trả về: str — 'increasing' | 'decreasing' | 'random'
    """
    import random
    n = len(arr)
    if n <= 1:
        return 'random'

    indices   = random.sample(range(n - 1), min(sample_size, n - 1))
    inc_count = sum(1 for i in indices if arr[i] <= arr[i + 1])
    dec_count = len(indices) - inc_count

    inc_ratio = inc_count / len(indices)
    dec_ratio = dec_count / len(indices)

    if inc_ratio >= 0.95:
        return 'increasing'
    elif dec_ratio >= 0.95:
        return 'decreasing'
    else:
        return 'random'


# ============================================================
# KIỂM THỬ KHI CHẠY TRỰC TIẾP
# ============================================================

if __name__ == "__main__":
    test_cases = {
        "Tăng dần hoàn toàn" : [1, 2, 3, 4, 5, 6, 7, 8],
        "Giảm dần hoàn toàn" : [8, 7, 6, 5, 4, 3, 2, 1],
        "Ngẫu nhiên"         : [3, 1, 4, 1, 5, 9, 2, 6],
        "Gần đúng (1 lệch)"  : [1, 2, 4, 3, 5, 6, 7, 8],
    }

    print("=" * 60)
    print(f"{'Trường hợp':<25} {'inv_ratio':>12} {'detect_trend':>15}")
    print("=" * 60)
    for name, data in test_cases.items():
        ratio = inversion_ratio(data)
        trend = detect_trend(data)
        print(f"{name:<25} {ratio:>11.2f}%  {trend:>15}")
    print("=" * 60)
