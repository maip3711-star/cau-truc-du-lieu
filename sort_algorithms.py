# -*- coding: utf-8 -*-
"""
sort_algorithms.py
Các thuật toán sắp xếp thuần túy (Insertion, Quick, Merge, Heap) và hàm kiểm tra.
"""

# =====================================
# 1. Insertion Sort
# =====================================
def insertion_sort(arr):
    """
    Sắp xếp chèn – trả về bản sao đã sắp xếp, KHÔNG sửa mảng gốc.
    Độ phức tạp:
      - Tốt nhất : O(n)   — dữ liệu đã gần sắp xếp
      - Trung bình: O(n²)
      - Xấu nhất : O(n²)  — dữ liệu đảo ngược
    """
    arr = arr.copy()  # bảo vệ mảng gốc
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# =====================================
# 2. Quick Sort (median-of-three)
# =====================================
def _median_of_three(arr, left, right):
    """Chọn pivot theo median-of-three, tránh worst-case O(n²)."""
    mid = (left + right) // 2
    if arr[left] > arr[mid]:
        arr[left], arr[mid] = arr[mid], arr[left]
    if arr[left] > arr[right]:
        arr[left], arr[right] = arr[right], arr[left]
    if arr[mid] > arr[right]:
        arr[mid], arr[right] = arr[right], arr[mid]
    # Đặt pivot vào right-1 để tránh xung đột với vòng lặp partition
    arr[mid], arr[right - 1] = arr[right - 1], arr[mid]
    return arr[right - 1]


def _quick_sort_recursive(arr, left, right):
    """Hàm đệ quy Quick Sort."""
    # Đoạn nhỏ (≤10 phần tử) dùng Insertion Sort tại chỗ để tối ưu
    if right - left < 1:
        return
    if right - left + 1 <= 10:
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return

    pivot = _median_of_three(arr, left, right)
    i = left
    j = right - 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            break
    arr[i], arr[right - 1] = arr[right - 1], arr[i]
    _quick_sort_recursive(arr, left, i - 1)
    _quick_sort_recursive(arr, i + 1, right)


def quick_sort(arr):
    """
    Quick Sort với pivot median-of-three – trả về bản sao đã sắp xếp.
    Độ phức tạp:
      - Tốt nhất / Trung bình: O(n log n)
      - Xấu nhất             : O(n²) — được giảm thiểu nhờ median-of-three
    """
    arr = arr.copy()  # bảo vệ mảng gốc
    if len(arr) <= 1:
        return arr
    _quick_sort_recursive(arr, 0, len(arr) - 1)
    return arr


# =====================================
# 3. Merge Sort
# =====================================
def _merge(arr, left, mid, right):
    """Gộp hai nửa đã sắp xếp vào mảng arr."""
    temp = []
    i, j = left, mid + 1
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp.append(arr[i]); i += 1
        else:
            temp.append(arr[j]); j += 1
    while i <= mid:
        temp.append(arr[i]); i += 1
    while j <= right:
        temp.append(arr[j]); j += 1
    for k in range(len(temp)):
        arr[left + k] = temp[k]


def _merge_sort_recursive(arr, left, right):
    """Hàm đệ quy Merge Sort."""
    if left >= right:
        return
    mid = (left + right) // 2
    _merge_sort_recursive(arr, left, mid)
    _merge_sort_recursive(arr, mid + 1, right)
    _merge(arr, left, mid, right)


def merge_sort(arr):
    """
    Merge Sort – trả về bản sao đã sắp xếp, KHÔNG sửa mảng gốc.
    Độ phức tạp: O(n log n) trong mọi trường hợp (ổn định).
    """
    arr = arr.copy()  # bảo vệ mảng gốc
    if len(arr) <= 1:
        return arr
    _merge_sort_recursive(arr, 0, len(arr) - 1)
    return arr


# =====================================
# 4. Heap Sort
# =====================================
def _heapify(arr, n, i):
    """Duy trì tính chất max-heap từ nút i."""
    largest = i
    left  = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


def heap_sort(arr):
    """
    Heap Sort – trả về bản sao đã sắp xếp, KHÔNG sửa mảng gốc.
    Độ phức tạp: O(n log n) — tốt nhất, trung bình, xấu nhất.
    """
    arr = arr.copy()  # bảo vệ mảng gốc
    n = len(arr)
    # Xây dựng max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    # Lần lượt đưa phần tử lớn nhất về cuối
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)
    return arr


# =====================================
# 5. Hàm kiểm tra đã sắp xếp
# =====================================
def is_sorted(arr, ascending=True):
    """
    Kiểm tra mảng có được sắp xếp đúng chiều không.
    Tham số:
      ascending = True  → kiểm tra tăng dần (mặc định)
      ascending = False → kiểm tra giảm dần
    Độ phức tạp: O(n)
    """
    for i in range(len(arr) - 1):
        if ascending:
            if arr[i] > arr[i + 1]:
                return False
        else:
            if arr[i] < arr[i + 1]:
                return False
    return True


# =====================================
# 6. Test thử
# =====================================
if __name__ == "__main__":
    import time

    test_arr = [8, 3, 5, 2, 9, 1, 4, 7, 6]
    print("=" * 50)
    print("KIỂM TRA CƠ BẢN")
    print("=" * 50)
    print("Mảng ban đầu:", test_arr)

    for name, func in [
        ("Insertion Sort", insertion_sort),
        ("Quick Sort    ", quick_sort),
        ("Merge Sort    ", merge_sort),
        ("Heap Sort     ", heap_sort),
    ]:
        result = func(test_arr)
        ok = is_sorted(result)
        print(f"{name}: {result} | Sorted: {ok}")

    # Kiểm tra mảng gốc không bị thay đổi
    print("\nMảng gốc sau khi gọi hàm:", test_arr)
    print("→ Mảng gốc được bảo vệ:", test_arr == [8, 3, 5, 2, 9, 1, 4, 7, 6])

    # Kiểm tra is_sorted() cả 2 chiều
    print("\n" + "=" * 50)
    print("KIỂM TRA is_sorted()")
    print("=" * 50)
    asc  = [1, 2, 3, 4, 5]
    desc = [5, 4, 3, 2, 1]
    rand = [3, 1, 4, 1, 5]
    print(f"[1,2,3,4,5] tăng dần : {is_sorted(asc,  ascending=True)}")   # True
    print(f"[5,4,3,2,1] giảm dần : {is_sorted(desc, ascending=False)}")  # True
    print(f"[5,4,3,2,1] tăng dần : {is_sorted(desc, ascending=True)}")   # False
    print(f"[3,1,4,1,5] tăng dần : {is_sorted(rand, ascending=True)}")   # False

    # Đo thời gian với dữ liệu lớn hơn
    import random
    print("\n" + "=" * 50)
    print("ĐO THỜI GIAN VỚI 5000 PHẦN TỬ")
    print("=" * 50)
    big = [random.randint(0, 1_000_000) for _ in range(5000)]
    for name, func in [
        ("Insertion Sort", insertion_sort),
        ("Quick Sort    ", quick_sort),
        ("Merge Sort    ", merge_sort),
        ("Heap Sort     ", heap_sort),
    ]:
        t0 = time.perf_counter()
        result = func(big)
        ms = (time.perf_counter() - t0) * 1000
        print(f"{name}: {ms:7.2f}ms | Sorted: {is_sorted(result)}")
