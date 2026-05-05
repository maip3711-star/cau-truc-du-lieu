# -*- coding: utf-8 -*-
"""
data_analyzer.py
               - Tinh ty le nghich the (sampling tuan tu O(sample_size))
               - Phat hien xu huong sap xep cua mang
"""

# ============================================================
# 1. DEM NGHICH THE CHINH XAC (dung cho bao cao)
# ============================================================

def count_inversions(arr):
    """
    Dem so cap nghich the bang Merge Sort cai tien - O(n log n).
    Dung de tinh toan chinh xac cho bao cao, KHONG dung trong adaptive_sort.
    """
    if len(arr) <= 1:
        return 0
    _, inv = _merge_count(arr.copy())
    return inv


def _merge_count(arr):
    if len(arr) <= 1:
        return arr, 0
    mid           = len(arr) // 2
    left,  inv_l  = _merge_count(arr[:mid])
    right, inv_r  = _merge_count(arr[mid:])
    merged, inv   = [], inv_l + inv_r
    i = j         = 0
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
# 2. PHAN TICH NHANH - dung trong adaptive_sort
# ============================================================

def inversion_ratio(arr, sample_size=1000):
    """
    Uoc luong ty le nghich the (%) bang systematic sampling - O(sample_size).
    Duyet tuan tu sample_size cap lien ke trai deu tren toan mang.
    Tra ve: float [0.0, 100.0]
    """
    n = len(arr)
    if n <= 1:
        return 0.0
    step      = max(1, (n - 1) // min(sample_size, n - 1))
    indices   = range(0, n - 1, step)
    total     = len(range(0, n - 1, step))
    inv_count = sum(1 for i in indices if arr[i] > arr[i + 1])
    return (inv_count / total) * 100.0


def detect_trend(arr, sample_size=500):
    """
    Phat hien xu huong sap xep bang step-based sampling - O(sample_size).

    So sanh phan tu cach nhau 'step' vi tri thay vi cap lien ke,
    tranh bi anh huong boi cac gia tri trung nhau lien tiep trong du lieu thuc te
    (vi du: du lieu gia nha co nhieu gia bang nhau).

    Nguong 95%:
      inc >= 95% -> 'increasing'   Tap B (100%), tranh nham Tap D (90%)
      dec >= 95% -> 'decreasing'   Tap C (100%)
      con lai    -> 'random'       Tap A, D, E

    Tra ve: 'increasing' | 'decreasing' | 'random'
    """
    n = len(arr)
    if n <= 1:
        return 'random'

    # So sanh phan tu cach nhau step vi tri
    step  = max(10, n // sample_size)
    total = n // step
    if total == 0:
        return 'random'

    inc = sum(1 for i in range(0, n - step, step) if arr[i] < arr[i + step])
    dec = sum(1 for i in range(0, n - step, step) if arr[i] > arr[i + step])

    if inc / total >= 0.95:
        return 'increasing'
    elif dec / total >= 0.95:
        return 'decreasing'
    else:
        return 'random'


# ============================================================
# KIEM THU KHI CHAY TRUC TIEP
# ============================================================

if __name__ == "__main__":
    import random
    random.seed(42)

    prices = list(range(75000, 7700000, 375)) * 3
    A = random.sample(prices, 20000)
    B = sorted(A); C = B[::-1]
    D = B.copy()
    idx = random.sample(range(20000), 2000)
    for k in range(0, len(idx)-1, 2):
        D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]
    E = A.copy()
    idx = random.sample(range(20000), 12000)
    for k in range(0, len(idx)-1, 2):
        E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]

    expected = {'A':'random','B':'increasing','C':'decreasing','D':'random','E':'random'}

    print("=" * 62)
    print(f"{'Tap':<6} {'inv_ratio':>10}  {'trend':<14} {'Dung?'}")
    print("=" * 62)
    all_ok = True
    for name, data in [('A',A),('B',B),('C',C),('D',D),('E',E)]:
        ratio = inversion_ratio(data)
        trend = detect_trend(data)
        ok    = trend == expected[name]
        if not ok: all_ok = False
        print(f"  {name}    {ratio:>9.1f}%   {trend:<14} {'OK' if ok else 'LOI - can ' + expected[name]}")
    print("=" * 62)
    print("Ket qua:", "Tat ca dung" if all_ok else "Co loi!")
