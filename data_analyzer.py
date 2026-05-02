# -*- coding: utf-8 -*-
"""
data_analyzer.py
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

def inversion_ratio(arr, sample_size=1000):
    """
    Ước lượng tỷ lệ nghịch thế (%) bằng systematic sampling — O(sample_size).

    Duyệt tuần tự sample_size cặp liền kề trải đều trên mảng.
      - ~0%   → mảng đã sắp xếp   (Insertion Sort)
      - ~100% → mảng đảo ngược    (Merge Sort)
      - ~50%  → mảng ngẫu nhiên   (Quick Sort)

    Trả về: float [0.0, 100.0]
    """
    n = len(arr)
    if n <= 1:
        return 0.0
    step      = max(1, (n - 1) // min(sample_size, n - 1))
    indices   = range(0, n - 1, step)
    total     = len(range(0, n - 1, step))
    inv_count = sum(1 for i in indices if arr[i] > arr[i + 1])
    return (inv_count / total) * 100.0


def detect_trend(arr, sample_size=1000):
    """
    Phát hiện xu hướng sắp xếp bằng systematic sampling — O(sample_size).

    Ngưỡng được hiệu chỉnh theo thực nghiệm:
      inc_ratio >= 95% → 'increasing'  Tập B (100%), tránh nhầm Tập D (90.5%)
      dec_ratio >= 95% → 'decreasing'  Tập C (100%)
      còn lại          → 'random'      Tập A, D, E

    Trả về: 'increasing' | 'decreasing' | 'random'
    """
    n = len(arr)
    if n <= 1:
        return 'random'

    step      = max(1, (n - 1) // min(sample_size, n - 1))
    indices   = range(0, n - 1, step)
    total     = len(range(0, n - 1, step))
    inc_count = sum(1 for i in indices if arr[i] <= arr[i + 1])
    dec_count = total - inc_count

    if inc_count / total >= 0.95:
        return 'increasing'   # Tập B: 100% tăng → Insertion Sort
    elif dec_count / total >= 0.95:
        return 'decreasing'   # Tập C: 100% giảm → Merge Sort
    else:
        return 'random'       # Tập A, D, E      → Quick Sort


# ============================================================
# KIỂM THỬ KHI CHẠY TRỰC TIẾP
# ============================================================

if __name__ == "__main__":
    import random
    random.seed(42)

    n   = 20000
    A   = [random.randint(75000, 7700000) for _ in range(n)]
    B   = sorted(A)
    C   = B[::-1]
    D   = B.copy()
    idx = random.sample(range(n), int(n * 0.05) * 2)
    for k in range(0, len(idx)-1, 2):
        D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]
    E   = A.copy()
    idx = random.sample(range(n), int(n * 0.30) * 2)
    for k in range(0, len(idx)-1, 2):
        E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]

    cases = {
        "A – Ngẫu nhiên  ": (A, "Quick Sort"),
        "B – Tăng dần    ": (B, "Insertion Sort"),
        "C – Giảm dần    ": (C, "Merge Sort"),
        "D – 5%  đảo     ": (D, "Quick Sort"),
        "E – 30% đảo     ": (E, "Quick Sort"),
    }

    print("=" * 68)
    print(f"{'Tập':<22} {'inv_ratio':>10}  {'trend':<14} {'Chọn đúng?'}")
    print("=" * 68)
    all_ok = True
    for name, (data, expected) in cases.items():
        ratio = inversion_ratio(data)
        trend = detect_trend(data)
        chosen = (
            "Insertion Sort" if trend == 'increasing' else
            "Merge Sort"     if trend == 'decreasing' else
            "Quick Sort"
        )
        ok = (chosen == expected)
        if not ok: all_ok = False
        print(f"{name:<22} {ratio:>9.1f}%  {trend:<14} "
              f"{'✓ ' + chosen if ok else '✗ ' + chosen + ' (cần ' + expected + ')'}")
    print("=" * 68)
    print("Kết quả:", "✓ Tất cả đúng" if all_ok else "✗ Có lỗi!")
