# -*- coding: utf-8 -*-
"""
analyzer.py

Phân tích đặc tính dữ liệu phục vụ thuật toán sắp xếp thích nghi:
- Đếm nghịch thế (O(n log n))
- Ước lượng độ lộn xộn (sampling O(k))
- Phát hiện xu hướng dữ liệu (tăng / giảm / ngẫu nhiên)
"""

import random

# ============================================================
# 1. ĐẾM NGHỊCH THẾ CHÍNH XÁC 
# ============================================================

def count_inversions(arr):
    """
    Đếm số nghịch thế bằng Merge Sort cải tiến — O(n log n)
    """
    if len(arr) <= 1:
        return 0
    _, inv = _merge_count(arr.copy())
    return inv


def _merge_count(arr):
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2

    left, inv_l = _merge_count(arr[:mid])
    right, inv_r = _merge_count(arr[mid:])

    merged = []
    i = j = 0
    inv = inv_l + inv_r

    while i < len(left) and j < len(right):

        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inv += len(left) - i
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged, inv


# ============================================================
# 2. ƯỚC LƯỢNG ĐỘ LỘN XỘN (FAST ANALYSIS)
# ============================================================

def inversion_ratio(arr, sample_size=1000):
    """
    Ước lượng % nghịch thế bằng sampling O(k)

    - ~0%   → gần sorted
    - ~100% → đảo ngược
    - ~50%  → random
    """

    n = len(arr)
    if n <= 1:
        return 0.0

    step = max(1, (n - 1) // min(sample_size, n - 1))

    indices = list(range(0, n - 1, step))
    total = len(indices)

    if total == 0:
        return 0.0

    inv_count = sum(
        1 for i in indices
        if arr[i] > arr[i + 1]
    )

    return (inv_count / total) * 100.0


# ============================================================
# 3. PHÁT HIỆN XU HƯỚNG DỮ LIỆU
# ============================================================

def detect_trend(arr, sample_size=1000):
    """
    Phân loại dữ liệu:

    - increasing  → gần tăng dần
    - decreasing  → gần giảm dần
    - random      → còn lại
    """

    n = len(arr)
    if n <= 1:
        return "random"

    step = max(1, (n - 1) // min(sample_size, n - 1))

    indices = list(range(0, n - 1, step))
    total = len(indices)

    if total == 0:
        return "random"

    inc_count = sum(
        1 for i in indices
        if arr[i] <= arr[i + 1]
    )

    inc_ratio = inc_count / total

    dec_ratio = 1 - inc_ratio

    # ========================================================
    # NGƯỠNG ĐIỀU CHỈNH (OPTIMIZED)
    # ========================================================

    if inc_ratio >= 0.90:
        return "increasing"

    elif dec_ratio >= 0.90:
        return "decreasing"

    else:
        return "random"


# ============================================================
# 4. HÀM HỖ TRỢ PHÂN TÍCH TỔNG HỢP
# ============================================================

def analyze_array(arr, sample_size=1000):
    """
    Trả về toàn bộ thông tin phân tích:

    - inversion ratio
    - trend
    - exact inversions
    """

    return {
        "inversion_ratio": inversion_ratio(arr, sample_size),
        "trend": detect_trend(arr, sample_size),
        "inversions": count_inversions(arr)
    }


# ============================================================
# 5. TEST NHANH
# ============================================================

if __name__ == "__main__":

    random.seed(42)

    n = 20000

    A = [random.randint(1, 1000000) for _ in range(n)]
    B = sorted(A)
    C = B[::-1]

    D = B.copy()
    idx = random.sample(range(n), int(n * 0.05))
    for i in range(0, len(idx) - 1, 2):
        D[idx[i]], D[idx[i + 1]] = D[idx[i + 1]], D[idx[i]]

    E = A.copy()
    idx = random.sample(range(n), int(n * 0.30))
    for i in range(0, len(idx) - 1, 2):
        E[idx[i]], E[idx[i + 1]] = E[idx[i + 1]], E[idx[i]]

    cases = {
        "A - Random": A,
        "B - Sorted": B,
        "C - Reverse": C,
        "D - Nearly Sorted": D,
        "E - Partially Shuffled": E,
    }

    print("=" * 70)
    print(f"{'Dataset':<25}{'Inv %':>10}{'Trend':>15}{'Inversions'}")
    print("=" * 70)

    for name, data in cases.items():

        result = analyze_array(data)

        print(
            f"{name:<25}"
            f"{result['inversion_ratio']:>9.1f}%"
            f"{result['trend']:>15}"
            f"{result['inversions']:>15}"
        )

    print("=" * 70)
    print("Analysis completed.")
