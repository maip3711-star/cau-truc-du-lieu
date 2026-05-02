# -*- coding: utf-8 -*-
"""
 Viết script đo thời gian chạy (ms) cho tất cả thuật toán
             trên 5 tập dữ liệu, lặp nhiều lần lấy trung bình,
             xuất kết quả ra CSV và vẽ biểu đồ matplotlib.
"""

import time
import csv
import random
import matplotlib.pyplot as plt

# Import từ file của các thành viên khác
from sort_algorithms   import insertion_sort, quick_sort, merge_sort, heap_sort
from adaptive_sort     import adaptive_sort
from generate_datasets import generate_datasets

# ============================================================
# CẤU HÌNH
# ============================================================
CSV_PATH    = "/content/kc_house_data.csv"
OUTPUT_CSV  = "/content/results.csv"
OUTPUT_PLOT = "/content/chart.png"

# Insertion Sort O(n²) rất chậm với dữ liệu lớn ngẫu nhiên
# → chỉ lặp 1 lần; các thuật toán khác lặp 5 lần bỏ max+min
REPEAT_FAST = 5
REPEAT_SLOW = 1

ALGORITHMS = {
    "Quick Sort"    : quick_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort"    : merge_sort,
    "Adaptive Sort" : adaptive_sort,
}

TAP_LABELS = {
    "A": "A-Ngẫu nhiên",
    "B": "B-Tăng dần",
    "C": "C-Giảm dần",
    "D": "D-5% đảo",
    "E": "E-30% đảo",
}


# ============================================================
# ĐO THỜI GIAN
# ============================================================

def measure_time(func, data, repeat):
    """
    Chạy func(data.copy()) nhiều lần, trả về thời gian trung bình (ms).
    Nếu repeat >= 5: bỏ max + min rồi lấy trung bình các lần còn lại.
    """
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        func(data.copy())
        times.append((time.perf_counter() - t0) * 1000)
    if repeat >= 5:
        times.remove(max(times))
        times.remove(min(times))
    return sum(times) / len(times)


# ============================================================
# CHẠY THỰC NGHIỆM
# ============================================================

def run_experiment(datasets):
    """
    Đo thời gian tất cả thuật toán trên 5 tập dữ liệu.
    Trả về: list of [tên_tập, tên_thuật_toán, thời_gian_ms]
    """
    results = []

    print("Đang đo thời gian chạy...")
    print("(Insertion Sort O(n²) sẽ mất vài phút – vui lòng chờ...)\n")

    for tap, label in TAP_LABELS.items():
        print(f"  [{tap}] {label}")
        for algo_name, algo_func in ALGORITHMS.items():
            repeat = REPEAT_SLOW if algo_name == "Insertion Sort" else REPEAT_FAST
            ms     = measure_time(algo_func, datasets[tap], repeat)
            note   = "" if repeat > 1 else " (1 lần)"
            print(f"    {algo_name:<16} {ms:>10.2f} ms{note}")
            results.append([label, algo_name, round(ms, 3)])
        print()

    return results


# ============================================================
# IN BẢNG KẾT QUẢ
# ============================================================

def print_table(results):
    col_w = 16
    print("=" * 90)
    print("BẢNG KẾT QUẢ THỰC NGHIỆM – THỜI GIAN CHẠY TRUNG BÌNH (ms)")
    print("=" * 90)

    header = f"{'Thuật toán':<20}"
    for label in TAP_LABELS.values():
        header += f"{label:>{col_w}}"
    print(header)
    print("-" * 90)

    for algo_name in ALGORITHMS:
        row = f"{algo_name:<20}"
        for label in TAP_LABELS.values():
            ms = next(r[2] for r in results if r[0] == label and r[1] == algo_name)
            row += f"{ms:>{col_w}.2f}ms"
        print(row)

    print("=" * 90)


# ============================================================
# XUẤT CSV
# ============================================================

def save_csv(results, path=OUTPUT_CSV):
    """Lưu kết quả ra file CSV để dùng trong báo cáo."""
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Tập dữ liệu", "Thuật toán", "Thời gian (ms)"])
        writer.writerows(results)
    print(f"\n  Đã lưu kết quả CSV → {path}")


# ============================================================
# VẼ BIỂU ĐỒ
# ============================================================

def plot(results, path=OUTPUT_PLOT):
    """
    Vẽ biểu đồ đường so sánh thời gian chạy của các thuật toán
    trên 5 tập dữ liệu A–E.
    """
    tap_list  = list(TAP_LABELS.values())
    algo_list = list(ALGORITHMS.keys())

    # Màu và marker riêng cho từng thuật toán
    styles = {
        "Quick Sort"    : {"color": "#2196F3", "marker": "o", "ls": "-"},
        "Insertion Sort": {"color": "#F44336", "marker": "s", "ls": "--"},
        "Merge Sort"    : {"color": "#4CAF50", "marker": "^", "ls": "-."},
        "Adaptive Sort" : {"color": "#FF9800", "marker": "D", "ls": "-",
                           "lw": 2.5},
    }

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # ── Biểu đồ 1: Tất cả thuật toán ───────────────────────
    ax1 = axes[0]
    for algo in algo_list:
        y  = [next(r[2] for r in results if r[0] == t and r[1] == algo)
              for t in tap_list]
        st = styles[algo]
        ax1.plot(
            tap_list, y,
            marker=st["marker"],
            color=st["color"],
            linestyle=st.get("ls", "-"),
            linewidth=st.get("lw", 1.8),
            label=algo
        )
    ax1.set_title("So sánh tất cả thuật toán", fontsize=13, fontweight="bold")
    ax1.set_xlabel("Tập dữ liệu")
    ax1.set_ylabel("Thời gian (ms)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # ── Biểu đồ 2: Không có Insertion Sort (phóng to) ───────
    ax2 = axes[1]
    for algo in algo_list:
        if algo == "Insertion Sort":
            continue
        y  = [next(r[2] for r in results if r[0] == t and r[1] == algo)
              for t in tap_list]
        st = styles[algo]
        ax2.plot(
            tap_list, y,
            marker=st["marker"],
            color=st["color"],
            linestyle=st.get("ls", "-"),
            linewidth=st.get("lw", 1.8),
            label=algo
        )
    ax2.set_title("So sánh (bỏ Insertion Sort để phóng to)", fontsize=13, fontweight="bold")
    ax2.set_xlabel("Tập dữ liệu")
    ax2.set_ylabel("Thời gian (ms)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle("Kết quả thực nghiệm – Đề tài 16\nThuật toán sắp xếp thích nghi",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  Đã lưu biểu đồ → {path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # Tải / tạo 5 tập dữ liệu
    try:
        datasets = generate_datasets(csv_path=CSV_PATH, n=20000)
    except FileNotFoundError:
        print("Không có file CSV → dùng dữ liệu giả lập (20,000 phần tử)...\n")
        random.seed(42)
        fake = [random.randint(100_000, 2_000_000) for _ in range(20000)]
        B    = sorted(fake)
        D    = B.copy()
        idx  = random.sample(range(20000), 2000)
        for k in range(0, len(idx)-1, 2):
            D[idx[k]], D[idx[k+1]] = D[idx[k+1]], D[idx[k]]
        E    = fake.copy()
        idx  = random.sample(range(20000), 12000)
        for k in range(0, len(idx)-1, 2):
            E[idx[k]], E[idx[k+1]] = E[idx[k+1]], E[idx[k]]
        datasets = {
            "A": fake,
            "B": B,
            "C": sorted(fake, reverse=True),
            "D": D,
            "E": E,
        }

    # Chạy thực nghiệm
    results = run_experiment(datasets)

    # In bảng, lưu CSV và vẽ biểu đồ
    print_table(results)
    save_csv(results)
    plot(results)
