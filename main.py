import pandas as pd
import random
import time
import heapq

# ================= ĐỌC FILE =================
df = pd.read_csv("kc_house_data.csv")
price = df["price"].astype(int).tolist()

# ================= TẠO DATA =================
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

# ================= SORT =================
def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key

def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[len(a)//2]
    left = [x for x in a if x < pivot]
    mid = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

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
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def heap_sort(a):
    heapq.heapify(a)
    return [heapq.heappop(a) for _ in range(len(a))]

# ================= ADAPTIVE =================
def adaptive_sort(a):
    n = len(a)
    disorder = sum(1 for i in range(1, n) if a[i] < a[i-1])

    if n < 50:
        insertion_sort(a)
        return a
    elif disorder < n * 0.1:
        insertion_sort(a)
        return a
    elif n > 10000:
        return heap_sort(a)
    else:
        return quick_sort(a)

# ================= CHECK =================
def is_sorted(a):
    return all(a[i] <= a[i+1] for i in range(len(a)-1))

def test(data, name):
    result = adaptive_sort(data.copy())
    if is_sorted(result):
        print(f"{name}: OK")
    else:
        print(f"{name}: FAIL")

# ================= TEST =================
test(A, "Random")
test(B, "Sorted")
test(C, "Reverse")
test(D, "Nearly Sorted")
test(E, "Duplicate")

# ================= BENCHMARK =================
def benchmark(data, name):
    start = time.time()
    adaptive_sort(data.copy())
    end = time.time()
    print(f"{name}: {end - start:.5f} s")

print("\nTime:")
benchmark(A, "Random")
benchmark(B, "Sorted")
benchmark(C, "Reverse")
benchmark(D, "Nearly Sorted")
benchmark(E, "Duplicate")
