# -*- coding: utf-8 -*-
"""
data_analyzer.py

Phân tích đặc tính dữ liệu phục vụ thuật toán sắp xếp thích nghi:
- Đếm nghịch thế chính xác (O(n log n)) – dùng cho báo cáo
- Ước lượng tỷ lệ nghịch thế bằng sampling O(k) – dùng trong adaptive_sort
- Phát hiện xu hướng dữ liệu (tăng / giảm / ngẫu nhiên) với ngưỡng 95%
"""

import random

# ============================================================
# 1. ĐẾM NGHỊCH THẾ CHÍNH XÁC (cho báo cáo)
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
# 2. ƯỚC LƯỢNG ĐỘ LỘN XỘN BẰNG SAMPLING (dùng trong adaptive_sort)
# ============================================================

def inversion_ratio(arr, sample_size=1000):
    """
    Ước lượng tỷ lệ nghịch thế (%) bằng systematic sampling.
    Chỉ so sánh các cặp liền kề cách đều step.
    Độ phức tạp: O(sample_size) ≈ O(1000).
    """
    n = len(arr)
    if n <= 1:
        return 0.0
    step = max(1, (n - 1) // min(sample_size, n - 1))
    indices = range(0, n - 1, step)
    total = len(indices)
    if total == 0:
        return 0.0
    inv_count = sum(1 for i in indices if arr[i] > arr[i+1])
    return (inv_count / total) * 100.0


# ============================================================
# 3. PHÁT HIỆN XU HƯỚNG DỮ LIỆU (NGƯỠNG 95%)
# ============================================================

def detect_trend(arr, sample_size=1000):
    """
    Phân loại xu hướng dữ liệu dựa trên systematic sampling,
    bỏ qua các cặp bằng nhau để tránh nhiễu.

    Ngưỡng 95%:
      - inc_ratio >= 0.95 → 'increasing'
      - dec_ratio >= 0.95 → 'decreasing'
      - còn lại → 'random'
    """
    n = len(arr)
    if n <= 1:
        return "random"

    step = max(1, (n - 1) // min(sample_size, n - 1))
    indices = range(0, n - step, step)   # so sánh các cặp cách nhau step vị trí
    total = len(indices)
    if total == 0:
        return "random"

    inc = sum(1 for i in indices if arr[i] < arr[i + step])
    dec = sum(1 for i in indices if arr[i] > arr[i + step])

    inc_ratio = inc / total
    dec_ratio = dec / total

    if inc_ratio >= 0.95:
        return "increasing"
    elif dec_ratio >= 0.95:
        return "decreasing"
    else:
        return "random"


# ============================================================
# 4. HÀM TỔNG HỢP (cho tiện)
# ============================================================

def analyze_array(arr, sample_size=1000):
    """
    Trả về dict gồm:
      - inversion_ratio (ước lượng)
      - trend
      - exact_inversions (chính xác)
    """
    return {
        "inversion_ratio": inversion_ratio(arr, sample_size),
        "trend": detect_trend(arr, sample_size),
        "exact_inversions": count_inversions(arr)
    }


# ============================================================
# 5. KIỂM THỬ NHANH KHI CHẠY TRỰC TIẾP
# ============================================================
if __name__ == "__main__":
    random.seed(42)
    n = 20000

    A = [random.randint(100000, 2000000) for _ in range(n)]
    B = sorted(A)
    C = B[::-1]

    # D: đảo 5% từ B
    D = B.copy()
    idx = random.sample(range(n), int(n * 0.05))
    for i in range(0, len(idx)-1, 2):
        D[idx[i]], D[idx[i+1]] = D[idx[i+1]], D[idx[i]]

    # E: đảo 30% từ A
    E = A.copy()
    idx = random.sample(range(n), int(n * 0.30))
    for i in range(0, len(idx)-1, 2):
        E[idx[i]], E[idx[i+1]] = E[idx[i+1]], E[idx[i]]

    datasets = {
        "A - Random": A,
        "B - Sorted": B,
        "C - Reverse": C,
        "D - Nearly Sorted (5% swap)": D,
        "E - Partially Shuffled (30% swap)": E,
    }

    print("=" * 75)
    print(f"{'Dataset':<30} {'Inv Ratio %':>12} {'Trend':>12} {'Exact Inversions'}")
    print("=" * 75)

    for name, data in datasets.items():
        inv = inversion_ratio(data)
        trend = detect_trend(data)
        exact = count_inversions(data)
        print(f"{name:<30} {inv:>11.1f}% {trend:>12} {exact:>18,}")

    print("=" * 75)
    print(" Analysis completed. Ngưỡng xu hướng: 95%")
