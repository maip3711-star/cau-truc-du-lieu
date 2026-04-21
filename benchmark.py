import time
import random
import csv
import matplotlib.pyplot as plt
import copy

# ======================
# Các thuật toán mẫu
# ======================

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# ======================
# Tạo dữ liệu test
# ======================

def generate_datasets():
    sizes = [100, 500, 1000, 2000, 5000]
    datasets = []

    for size in sizes:
        data = [random.randint(0, 10000) for _ in range(size)]
        datasets.append((size, data))

    return datasets

# ======================
# Đo thời gian
# ======================

def measure_time(func, data, repeats=5):
    total_time = 0
    for _ in range(repeats):
        arr = data.copy()
        start = time.perf_counter()
        func(arr)
        end = time.perf_counter()
        total_time += (end - start)
    avg_time = (total_time / repeats) * 1000  # ms
    return avg_time

# ======================
# Chạy thực nghiệm
# ======================

def run_experiment():
    algorithms = {
        "Bubble": bubble_sort,
        "Insertion": insertion_sort,
        "Merge": merge_sort,
        "Quick": quick_sort
    }

    datasets = generate_datasets()

    results = []

    for size, data in datasets:
        for name, func in algorithms.items():
            print(f"Running {name} with n={size}...")
            avg_time = measure_time(func, data, repeats=5)
            results.append([name, size, avg_time])

    return results

# ======================
# Ghi CSV
# ======================

def save_to_csv(results, filename="results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Input Size", "Time (ms)"])
        writer.writerows(results)

# ======================
# Vẽ biểu đồ
# ======================

def plot_results(results):
    algorithms = list(set(r[0] for r in results))

    for algo in algorithms:
        x = [r[1] for r in results if r[0] == algo]
        y = [r[2] for r in results if r[0] == algo]
        plt.plot(x, y, marker='o', label=algo)

    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (ms)")
    plt.title("So sánh thời gian các thuật toán")
    plt.legend()
    plt.grid(True)
    plt.show()

# ======================
# Main
# ======================

if __name__ == "__main__":
    results = run_experiment()
    save_to_csv(results)
    plot_results(results)
    plt.savefig("chart.png")