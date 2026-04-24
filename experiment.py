import pandas as pd
import random
import time
import csv
import matplotlib.pyplot as plt

# ================= DATASET =================

def get_datasets(n=20000):
    df = pd.read_csv("kc_house_data.csv")
    price = df["price"].astype(int).tolist()[:n]

    A = price.copy()
    random.shuffle(A)

    B = sorted(price)

    C = B[::-1]

    D = B.copy()
    for _ in range(len(D) // 20):
        i = random.randint(0, len(D)-1)
        j = random.randint(0, len(D)-1)
        D[i], D[j] = D[j], D[i]

    E = [x % 1000 for x in price]

    return {
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "E": E
    }

# ================= SORT =================

def insertion_sort(a):
    arr = a.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a)//2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result += left[i:]
    result += right[j:]
    return result

def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[len(a)//2]
    left = [x for x in a if x < pivot]
    mid = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# ================= ADAPTIVE =================

def is_nearly_sorted(arr):
    disorder = sum(1 for i in range(len(arr)-1) if arr[i] > arr[i+1])
    return disorder < len(arr) * 0.1

def adaptive_sort(a):
    if is_nearly_sorted(a):
        return insertion_sort(a)
    else:
        return quick_sort(a)

# ================= MEASURE =================

def measure_time(func, data, repeats=10):
    total = 0
    for _ in range(repeats):
        arr = data.copy()
        start = time.perf_counter()
        func(arr)
        end = time.perf_counter()
        total += (end - start)
    return (total / repeats) * 1000  # ms

# ================= EXPERIMENT =================

def run_experiment():
    datasets = get_datasets()

    algorithms = {
        "Insertion": insertion_sort,
        "Merge": merge_sort,
        "Quick": quick_sort,
        "Adaptive": adaptive_sort
    }

    results = []

    for dname, data in datasets.items():
        for aname, func in algorithms.items():
            print(f"Running {aname} on dataset {dname}...")
            t = measure_time(func, data)
            results.append([dname, aname, t])

    return results

# ================= SAVE CSV =================

def save_csv(results):
    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Dataset", "Algorithm", "Time (ms)"])
        writer.writerows(results)

# ================= PLOT =================

def plot(results):
    datasets = sorted(set(r[0] for r in results))
    algorithms = sorted(set(r[1] for r in results))

    for algo in algorithms:
        y = [next(r[2] for r in results if r[0]==d and r[1]==algo) for d in datasets]
        plt.plot(datasets, y, marker='o', label=algo)

    plt.xlabel("Dataset (A-E)")
    plt.ylabel("Time (ms)")
    plt.title("Sorting Algorithm Comparison")
    plt.legend()
    plt.grid(True)

    plt.savefig("chart.png")
    plt.show()

# ================= MAIN =================

if __name__ == "__main__":
    results = run_experiment()
    save_csv(results)
    plot(results)