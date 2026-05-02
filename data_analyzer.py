# -*- coding: utf-8 -*-
"""
data_analyzer.py
Phân tích đặc tính dữ liệu:
               - Tính tỷ lệ nghịch thế (sampling tuần tự O(sample_size))
               - Phát hiện xu hướng sắp xếp của mảng
"""

# ============================================================
# 1. ĐẾM NGHỊCH THẾ CHÍNH XÁC (dùng cho báo cáo)
# ============================================================

def count_inversions(arr):
    """
    Đếm số cặp nghịch thế (i < j nhưng arr[i] > arr[j])
    bằng Merge Sort cải tiến — O(n log n).
    Dùng để tính toán chính xác cho báo cáo, KHÔNG dùng trong adaptive_sort.
    """
    if len(arr) <= 1:
        return 0
    _, inv = _merge_count(arr.copy())
    return inv


def _merge_count(arr):
    if len(arr) <= 1:
        return arr, 0
    mid            = len(arr) // 2
    left,  inv_l   = _merge_count(arr[:mid])
    right, inv_r   = _merge_count(arr[mid:])
    merged, inv    = [], inv_l + inv_r
    i = j          = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            inv += len(left) - i
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv


# ============================================================
# 2. PHÂN TÍCH NHANH — dùng trong adaptive_sort
# ============================================================

def _analyze(arr, sample_size=1000):
    """
    Duyệt tuần tự sample_size cặp liền kề, trả về (inv_ratio, inc_ratio).
    Dùng chung 1 lần duyệt cho cả inversion_ratio và detect_trend
    → nhất quán, không bị lệch do random seed khác nhau.
    """
    n    = len(arr)
    if n <= 1:
        return 0.0, 1.0

    step      = max(1, (n - 1) // min(sample_size, n - 1))
    indices   = range(0, n - 1, step)
    total     = len(range(0, n - 1, step))
    inc_count = sum(1 for i in indices if arr[i] <= arr[i + 1])
    inv_count = total - inc_count

    return (inv_count / total) * 100.0, inc_count / total


def inversion_ratio(arr, sample_size=1000):
    """
    Ước lượng tỷ lệ nghịch thế (%) bằng systematic sampling — O(sample_size).

      - ~0%   → mảng đã sắp xếp (Insertion Sort)
      - ~100% → mảng đảo ngược  (Merge Sort)
      - ~50%  → mảng ngẫu nhiên (Quick Sort)

    Trả về: float [0.0, 100.0]
    """
    inv_ratio, _ = _analyze(arr, sample_size)
    return inv_ratio


def detect_trend(arr, sample_size=1000):
    """
    Phát hiện xu hướng sắp xếp bằng systematic sampling — O(sample_size).

    Ngưỡng:
      inc_ratio >= 90% → 'increasing'  (bắt cả tập B và D 5% đảo)
      dec_ratio >= 95% → 'decreasing'  (chỉ bắt tập C đảo ngược)
      còn lại          → 'random'

    Trả về: 'increasing' | 'decreasing' | 'random'
    """
    _, inc_ratio = _analyze(arr, sample_size)
    dec_ratio    = 1.0 - inc_ratio

    if inc_ratio >= 0.90:
        return 'increasing'
    elif dec_ratio >= 0.95:
        return 'decreasing'
    else:
        return 'random'


# ============================================================
# KIỂM THỬ KHI CHẠY TRỰC TIẾP
# ============================================================

if __name__ == "__main__":
    import random
    random.seed(42)

    n    = 20000
    A    = [random.randint(100000, 2000000) for _ in range(n)]
    B    = sorted(A)
    C    = B[::-1]
    D    = B.copy()
    idx  = random.sample(range(n), 2000)
    for k in range(0, len(idx)-1, 2):
        D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]
    E    = A.copy()
    idx  = random.sample(range(n), 12000)
    for k in range(0, len(idx)-1, 2):
        E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]

    cases = {
        "A – Ngẫu nhiên  ": A,
        "B – Tăng dần    ": B,
        "C – Giảm dần    ": C,
        "D – 5%  đảo     ": D,
        "E – 30% đảo     ": E,
    }

    print("=" * 65)
    print(f"{'Tập':<22} {'inv_ratio':>12}  {'detect_trend':>14}  {'Chọn'}")
    print("=" * 65)
    for name, data in cases.items():
        ratio = inversion_ratio(data)
        trend = detect_trend(data)
        if ratio < 20.0 or trend == 'increasing':
            chosen = "Insertion Sort"
        elif trend == 'decreasing':
            chosen = "Merge Sort"
        else:
            chosen = "Quick Sort"
        print(f"{name:<22} {ratio:>11.1f}%  {trend:>14}  {chosen}")
    print("=" * 65)
