# -*- coding: utf-8 -*-

#Bộ điều phối thích nghi: dựa vào tỷ lệ nghịch thế và xu hướng để chọn thuật toán.

from sort_algorithms import insertion_sort, quick_sort, merge_sort
from data_analyzer import inversion_ratio, detect_trend

def adaptive_sort(arr):
    """
    Sắp xếp mảng theo chiến lược thích nghi.
    - Nếu tỷ lệ nghịch thế < 5% → dùng Insertion Sort (tận dụng O(n) khi gần đúng).
    - Ngược lại, nếu xu hướng là giảm dần → dùng Merge Sort (tránh worst-case của Quick Sort).
    - Còn lại → dùng Quick Sort (median-of-three pivot).
    """
    n = len(arr)
    if n <= 1:
        return arr

    inv_ratio = inversion_ratio(arr)
    trend = detect_trend(arr)

    if inv_ratio < 5.0:
        return insertion_sort(arr)
    elif trend == 'decreasing':
        return merge_sort(arr)
    else:
        return quick_sort(arr)

# ========== Kiểm thử nhanh (giả lập nếu chưa có sort_algorithms) ==========
if __name__ == "__main__":
    # Tạm định nghĩa các hàm giả để test logic (khi chưa có sort_algorithms)
    # Khi có file sort_algorithms thật, hãy xóa phần này và import thật.
    def insertion_sort(arr):
        return sorted(arr)
    def quick_sort(arr):
        return sorted(arr)
    def merge_sort(arr):
        return sorted(arr)

    test_data = [3, 1, 4, 1, 5, 9, 2, 6]
    print("Original:", test_data)
    result = adaptive_sort(test_data.copy())
    print("Adaptive sorted:", result)
