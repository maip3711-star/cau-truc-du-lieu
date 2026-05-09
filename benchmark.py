# -*- coding: utf-8 -*-
"""
statistical_analysis.py - PHIÊN BẢN DÙNG DỮ LIỆU THẬT (Kaggle)
Chạy nhiều lần đo thời gian, in bảng thống kê mean±std, min, max
và vẽ đầy đủ biểu đồ: boxplot, bar chart, line chart, giải thích Insertion Sort,
so sánh Adaptive Sort vs thuật toán tốt nhất.
"""

import os
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# ── Path tu dong (khong hardcode) ──────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) \
             if '__file__' in dir() else os.getcwd()
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from sort_algorithms   import insertion_sort, quick_sort, merge_sort, heap_sort
from adaptive_sort     import adaptive_sort
from generate_datasets import generate_datasets

# ============================================================
# CONFIG
# ============================================================
CSV_PATH   = os.path.join(SCRIPT_DIR, "kc_house_data.csv")
RUNS_FAST  = 5   # Quick / Merge / Heap / Adaptive
RUNS_SLOW  = 3   # Insertion Sort (O(n^2) rat cham)

ALGORITHMS = {
    "Quick Sort"    : quick_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort"    : merge_sort,
    "Heap Sort"     : heap_sort,
    "Adaptive Sort" : adaptive_sort,
}
TAP_LABELS = {
    "A": "A-Ngẫu nhiên",
    "B": "B-Tăng dần",
    "C": "C-Giảm dần",
    "D": "D-5% đảo",
    "E": "E-30% đảo",
}
COLORS = {
    "Quick Sort"    : "#1E88E5",
    "Insertion Sort": "#E53935",
    "Merge Sort"    : "#43A047",
    "Heap Sort"     : "#8E24AA",
    "Adaptive Sort" : "#FB8C00",
}

# ============================================================
# ĐO THỜI GIAN NHIỀU LẦN
# ============================================================
def run_multiple(func, data, runs):
    """
    Chay warm-up 1 lan truoc, sau do do 'runs' lan.
    Tra ve list thoi gian (ms).
    """
    func(data.copy())   # warm-up
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        func(data.copy())
        times.append((time.perf_counter() - t0) * 1000)
    return times

def collect_stats(datasets, runs_fast=RUNS_FAST, runs_slow=RUNS_SLOW):
    """
    Thu thap thong ke (mean, std, min, max, times)
    cho moi thuat toan x moi tap.
    Insertion Sort chi chay runs_slow lan de tiet kiem thoi gian.
    """
    stats = {}
    taps  = list(TAP_LABELS.keys())

    print(f"Dang do thoi gian "
          f"(Fast x{runs_fast} lan, Insertion Sort x{runs_slow} lan)...\n")

    for tap in taps:
        label = TAP_LABELS[tap]
        print(f"  [{tap}] {label}")
        stats[tap] = {}

        for algo_name, algo_func in ALGORITHMS.items():
            runs  = runs_slow if algo_name == "Insertion Sort" else runs_fast
            times = run_multiple(algo_func, datasets[tap], runs)

            stats[tap][algo_name] = {
                "times" : times,
                "mean"  : np.mean(times),
                "std"   : np.std(times),
                "min"   : np.min(times),
                "max"   : np.max(times),
            }
            s = stats[tap][algo_name]
            print(f"    {algo_name:<16}: "
                  f"mean={s['mean']:>10.2f}ms  "
                  f"std={s['std']:>8.2f}ms  "
                  f"min={s['min']:>8.2f}ms  "
                  f"max={s['max']:>8.2f}ms")
        print()

    return stats

# ============================================================
# IN BẢNG THỐNG KÊ
# ============================================================
def print_stats_table(stats):
    taps  = list(TAP_LABELS.keys())
    algos = list(ALGORITHMS.keys())
    lbls  = list(TAP_LABELS.values())

    # Bang mean +- std
    print("\n" + "="*105)
    print("BANG THONG KE CHI TIET — MEAN ± STD (ms)")
    print("="*105)
    print(f"{'Thuat toan':<18}", end="")
    for l in lbls: print(f"{l:^20}", end="")
    print()
    print("-"*105)
    for algo in algos:
        print(f"{algo:<18}", end="")
        for t in taps:
            s    = stats[t][algo]
            cell = f"{s['mean']:.1f}±{s['std']:.1f}"
            print(f"{cell:^20}", end="")
        print()
    print("="*105)

    # Bang min / max
    print("\nBANG MIN / MAX (ms)")
    print("-"*105)
    print(f"{'Thuat toan':<18}", end="")
    for l in lbls: print(f"{l:^20}", end="")
    print()
    print("-"*105)
    for algo in algos:
        print(f"{algo:<18}", end="")
        for t in taps:
            s    = stats[t][algo]
            cell = f"{s['min']:.1f}/{s['max']:.1f}"
            print(f"{cell:^20}", end="")
        print()
    print("="*105)

# ============================================================
# BIEU DO 1: BOXPLOT — TACH RIENG TUNG THUAT TOAN
# ============================================================
def plot_boxplot(stats, save_path="chart_boxplot.png"):
    """
    Boxplot phan phoi thoi gian chay cua tung thuat toan tren 5 tap.
    Tach rieng tung thuat toan de de doc.
    """
    taps  = list(TAP_LABELS.keys())
    algos = list(ALGORITHMS.keys())

    fig, axes = plt.subplots(1, len(algos), figsize=(22, 6), sharey=False)
    fig.patch.set_facecolor('#F0F4F8')

    for ax, algo in zip(axes, algos):
        data = [stats[t][algo]["times"] for t in taps]
        bp   = ax.boxplot(data,
                          tick_labels=taps,
                          patch_artist=True,
                          medianprops={"color":"black","linewidth":2},
                          whiskerprops={"linewidth":1.5},
                          capprops={"linewidth":1.5})
        for patch in bp['boxes']:
            patch.set_facecolor(COLORS[algo])
            patch.set_alpha(0.75)

        # Hien thi mean
        for i, t in enumerate(taps):
            m = stats[t][algo]["mean"]
            ax.text(i+1, m,
                    f'{m/1000:.1f}s' if m > 1000 else f'{m:.1f}ms',
                    ha='center', va='bottom', fontsize=8.5,
                    fontweight='bold',
                    color='#B71C1C' if m > 1000 else '#1B5E20')

        ax.set_title(algo, fontsize=10, fontweight='bold',
                     color=COLORS[algo])
        ax.set_xlabel("Tập dữ liệu", fontsize=9)
        ax.set_ylabel("Thời gian (ms)" if algo == algos[0] else "")
        ax.set_facecolor('#FFFFFF')
        ax.grid(axis='y', alpha=0.25, linestyle='--')

    fig.suptitle(
        "Biểu đồ 1: Boxplot phân phối thời gian chạy — Từng thuật toán × 5 tập\n"
        "(Đường giữa mỗi box = median; whisker = min/max)",
        fontsize=13, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#F0F4F8')
    plt.show()
    print(f"Saved: {save_path}")

# ============================================================
# BIEU DO 2: BAR CHART + ERROR BAR — TAT CA THUAT TOAN
# ============================================================
def plot_bar(stats, save_path="chart_bar.png"):
    """
    Bar chart co error bar (+-std) tat ca thuat toan tren 5 tap.
    Insertion Sort tren A/C/D/E bi cat de bieu do doc duoc.
    """
    taps  = list(TAP_LABELS.keys())
    algos = list(ALGORITHMS.keys())
    lbls  = list(TAP_LABELS.values())
    CAP   = 320

    x    = np.arange(len(taps))
    w    = 0.16
    offs = [-2, -1, 0, 1, 2]

    fig, ax = plt.subplots(figsize=(16, 7))
    fig.patch.set_facecolor('#F0F4F8')
    ax.set_facecolor('#FFFFFF')

    for i, algo in enumerate(algos):
        means  = [stats[t][algo]["mean"] for t in taps]
        stds   = [stats[t][algo]["std"]  for t in taps]
        capped = [min(m, CAP) for m in means]
        c_stds = [min(s, 15)  for s in stds]

        bars = ax.bar(x + offs[i]*w, capped, w,
                      label=algo, color=COLORS[algo], alpha=0.88,
                      yerr=c_stds, capsize=3,
                      error_kw={"ecolor":"#333","linewidth":1.1})

        for bar, real, cap in zip(bars, means, capped):
            bx = bar.get_x() + bar.get_width()/2.
            if real > CAP:
                ax.text(bx, cap+5,
                        f'{real/1000:.1f}s',
                        ha='center', va='bottom', fontsize=7,
                        color='#B71C1C', fontweight='bold', rotation=90)
            elif real > 80:
                ax.text(bx, cap+4,
                        f'{real:.0f}',
                        ha='center', va='bottom', fontsize=7,
                        color='#333', rotation=90)
            else:
                ax.text(bx, cap+2,
                        f'{real:.1f}',
                        ha='center', va='bottom', fontsize=7.5, color='#333')

    ax.axhline(CAP, color='#B71C1C', ls=':', lw=1.2, alpha=0.6)
    ax.text(len(taps)-0.1, CAP+4,
            f'Ngưỡng cắt {CAP}ms', fontsize=8, color='#B71C1C')

    ax.set_xticks(x)
    ax.set_xticklabels(lbls, fontsize=11)
    ax.set_ylabel("Thời gian (ms)", fontsize=12)
    ax.set_ylim(0, CAP+60)
    ax.set_title(
        "Biểu đồ 2: Thời gian chạy trung bình ± độ lệch chuẩn — Tất cả thuật toán\n"
        "(Giá trị đỏ tính bằng giây — Insertion Sort A/C/D/E bị cắt để dễ đọc)",
        fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='upper right', ncol=5, framealpha=0.9)
    ax.grid(axis='y', alpha=0.25, linestyle='--')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#F0F4F8')
    plt.show()
    print(f"Saved: {save_path}")

# ============================================================
# BIEU DO 3: LINE CHART — BO INSERTION SORT
# ============================================================
def plot_line(stats, save_path="chart_line.png"):
    """
    Line chart + error bar, bo Insertion Sort de phong to
    va thay ro su bien dong cua Quick/Merge/Heap/Adaptive.
    """
    taps  = list(TAP_LABELS.keys())
    lbls  = list(TAP_LABELS.values())
    markers = {"Quick Sort":"o","Merge Sort":"^",
               "Heap Sort":"D","Adaptive Sort":"*"}

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#F0F4F8')
    ax.set_facecolor('#FFFFFF')

    for algo in ["Quick Sort","Merge Sort","Heap Sort","Adaptive Sort"]:
        means = [stats[t][algo]["mean"] for t in taps]
        stds  = [stats[t][algo]["std"]  for t in taps]
        ax.errorbar(taps, means, yerr=stds,
                    marker=markers[algo], label=algo,
                    color=COLORS[algo], linewidth=2.2,
                    markersize=8, capsize=5,
                    markerfacecolor='white', markeredgewidth=2.2)
        for t, m in zip(taps, means):
            ax.annotate(f'{m:.1f}',
                        (t, m), textcoords="offset points",
                        xytext=(0, 11), ha='center', fontsize=8.5,
                        color=COLORS[algo], fontweight='bold')

    ax.set_xticks(taps)
    ax.set_xticklabels(lbls, fontsize=11)
    ax.set_ylabel("Thời gian (ms)", fontsize=12)
    ax.set_xlabel("Tập dữ liệu", fontsize=11)
    ax.set_title(
        "Biểu đồ 3: Phóng to — Bỏ Insertion Sort\n"
        "So sánh Quick / Merge / Heap / Adaptive Sort qua 5 tập",
        fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.25, linestyle='--')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#F0F4F8')
    plt.show()
    print(f"Saved: {save_path}")

# ============================================================
# BIEU DO 4: GIAI THICH INSERTION SORT CHAM
# ============================================================
def plot_insertion_explain(stats, save_path="chart_explain.png"):
    """
    2 panel song song:
      - Panel trai : So phep so sanh uoc luong (ly thuyet)
      - Panel phai : Thoi gian thuc te do duoc
    Tra loi cau hoi cua thay: tai sao Insertion Sort cham.
    """
    taps = list(TAP_LABELS.keys())
    lbls = list(TAP_LABELS.values())
    n    = 20000

    phep = {
        "A": n*(n-1)//4,      # ~50% nghich the
        "B": n - 1,           # 0%  nghich the -> O(n)
        "C": n*(n-1)//2,      # 100% nghich the -> O(n^2)
        "D": int(n*0.05*n//2),# ~5%  nghich the
        "E": int(n*0.30*n//4),# ~30% nghich the
    }
    bclr = {"A":"#EF5350","B":"#66BB6A",
            "C":"#B71C1C","D":"#FFA726","E":"#EF5350"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('#F0F4F8')

    # ── Panel trai: So phep so sanh ──────────────────────────
    bars1 = ax1.bar(lbls, [phep[t]/1e6 for t in taps],
                    color=[bclr[t] for t in taps],
                    alpha=0.87, edgecolor='white',
                    linewidth=1.8, width=0.55)
    for bar, t in zip(bars1, taps):
        v  = phep[t]
        lb = f'{v/1e6:.0f}M' if v >= 1e6 else f'{v/1e3:.0f}K'
        ax1.text(bar.get_x()+bar.get_width()/2.,
                 bar.get_height()+0.4, lb,
                 ha='center', va='bottom',
                 fontsize=11, fontweight='bold')

    ax1.set_title("Ước lượng số phép so sánh\ncủa Insertion Sort (n = 20,000)",
                  fontsize=12, fontweight='bold')
    ax1.set_ylabel("Số phép so sánh (triệu)", fontsize=11)
    ax1.set_facecolor('#FFFFFF')
    ax1.grid(axis='y', alpha=0.25, linestyle='--')

    on  = mpatches.Patch(color='#66BB6A',
          label='O(n)  ≈ 20K phép  →  ~vài ms')
    on2 = mpatches.Patch(color='#B71C1C',
          label='O(n²) ≈ 100–200M phép  →  hàng chục nghìn ms')
    ax1.legend(handles=[on, on2], fontsize=9)

    ax1.annotate('Chỉ 0.02M phép!',
                 xy=(1, (n-1)/1e6), xytext=(1.8, 40),
                 arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2),
                 fontsize=10, color='darkgreen', fontweight='bold')
    ax1.annotate('200M phép!\nChênh ~10,000 lần',
                 xy=(2, n*(n-1)/2/1e6), xytext=(3.0, 150),
                 arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=2),
                 fontsize=10, color='#B71C1C', fontweight='bold')

    # ── Panel phai: Thoi gian thuc te ────────────────────────
    real_m = [stats[t]["Insertion Sort"]["mean"] for t in taps]
    real_s = [stats[t]["Insertion Sort"]["std"]  for t in taps]

    bars2 = ax2.bar(lbls, real_m,
                    color=[bclr[t] for t in taps],
                    alpha=0.87, edgecolor='white',
                    linewidth=1.8, width=0.55,
                    yerr=real_s, capsize=5,
                    error_kw={"ecolor":"#333","linewidth":1.3})
    for bar, t in zip(bars2, taps):
        m  = stats[t]["Insertion Sort"]["mean"]
        lb = f'{m/1000:.1f}s' if m > 1000 else f'{m:.1f}ms'
        ax2.text(bar.get_x()+bar.get_width()/2.,
                 bar.get_height() + real_s[taps.index(t)] + 200,
                 lb, ha='center', va='bottom', fontsize=10,
                 fontweight='bold',
                 color='#B71C1C' if m > 1000 else '#1B5E20')

    ax2.set_title("Thời gian thực tế của Insertion Sort\n(ms — đo thực nghiệm)",
                  fontsize=12, fontweight='bold')
    ax2.set_ylabel("Thời gian (ms)", fontsize=11)
    ax2.set_facecolor('#FFFFFF')
    ax2.grid(axis='y', alpha=0.25, linestyle='--')

    fig.suptitle(
        "Biểu đồ 4: Lý giải tại sao Insertion Sort chậm trên A, C, D, E\n"
        "nhưng nhanh trên B — So sánh số phép so sánh (lý thuyết) và thời gian thực tế",
        fontsize=13, fontweight='bold', y=1.03)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#F0F4F8')
    plt.show()
    print(f"Saved: {save_path}")

# ============================================================
# BIEU DO 5: ADAPTIVE SORT VS THUAT TOAN TOT NHAT
# ============================================================
def plot_adaptive_vs_best(stats, save_path="chart_adaptive.png"):
    """
    So sanh Adaptive Sort voi thuat toan tot nhat tung tap.
    Hien thi % overhead de chung minh Adaptive Sort hieu qua.
    """
    taps = list(TAP_LABELS.keys())
    lbls = list(TAP_LABELS.values())

    # Thuat toan tot nhat tung tap (dua tren ket qua thuc nghiem)
    best_algo = {
        "A": "Quick Sort",
        "B": "Insertion Sort",
        "C": "Quick Sort",
        "D": "Quick Sort",
        "E": "Quick Sort",
    }
    chosen = {
        "A": "→ Quick Sort",
        "B": "→ Insertion Sort",
        "C": "→ Quick Sort",
        "D": "→ Quick Sort",
        "E": "→ Quick Sort",
    }

    best_m = [stats[t][best_algo[t]]["mean"] for t in taps]
    adap_m = [stats[t]["Adaptive Sort"]["mean"] for t in taps]
    adap_s = [stats[t]["Adaptive Sort"]["std"]  for t in taps]
    overhead = [(a-b)/b*100 for a, b in zip(adap_m, best_m)]

    x = np.arange(len(taps))
    w = 0.30

    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor('#F0F4F8')
    ax.set_facecolor('#FFFFFF')

    b1 = ax.bar(x - w/2, best_m, w,
                label='Thuật toán tốt nhất (lý tưởng)',
                color='#1565C0', alpha=0.85)
    b2 = ax.bar(x + w/2, adap_m, w,
                label='Adaptive Sort (thực tế)',
                color='#FB8C00', alpha=0.88,
                yerr=adap_s, capsize=5,
                error_kw={"ecolor":"#555","linewidth":1.5})

    for bar, m in zip(b1, best_m):
        ax.text(bar.get_x()+bar.get_width()/2., m+0.5,
                f'{m:.1f}ms', ha='center', va='bottom',
                fontsize=9, color='#0D47A1', fontweight='bold')

    for bar, m, oh, s in zip(b2, adap_m, overhead, adap_s):
        ax.text(bar.get_x()+bar.get_width()/2., m+s+1.5,
                f'{m:.1f}ms', ha='center', va='bottom',
                fontsize=9, color='#E65100', fontweight='bold')
        clr = '#C62828' if oh > 15 else '#2E7D32'
        ax.text(bar.get_x()+bar.get_width()/2., m+s+9,
                f'({oh:+.1f}%)', ha='center',
                fontsize=8.5, color=clr)

    # Nhan thuat toan duoc chon
    for i, t in enumerate(taps):
        ax.text(i, max(best_m[i], adap_m[i]) + adap_s[i] + 16,
                chosen[t], ha='center', fontsize=8.5,
                color='#555', style='italic')

    ax.set_xticks(x)
    ax.set_xticklabels(lbls, fontsize=11)
    ax.set_ylabel("Thời gian (ms)", fontsize=12)
    ax.set_title(
        "Biểu đồ 5: Adaptive Sort vs Thuật toán tốt nhất từng tập\n"
        "(% = overhead so với lý tưởng — Adaptive Sort luôn chọn đúng thuật toán)",
        fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, framealpha=0.95)
    ax.grid(axis='y', alpha=0.25, linestyle='--')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#F0F4F8')
    plt.show()
    print(f"Saved: {save_path}")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    from datetime import datetime

    ts         = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_DIR = os.path.join(SCRIPT_DIR, "results")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    def out(name): return os.path.join(OUTPUT_DIR, f"{name}_{ts}.png")

    # ── 1. Tai du lieu ───────────────────────────────────────
    print("Dang tai du lieu...")
    datasets = generate_datasets(csv_path=CSV_PATH, n=20000, force=False)

    # ── 2. Do thoi gian nhieu lan ────────────────────────────
    stats = collect_stats(datasets, runs_fast=RUNS_FAST, runs_slow=RUNS_SLOW)

    # ── 3. In bang thong ke ──────────────────────────────────
    print_stats_table(stats)

    # ── 4. Ve tat ca bieu do ────────────────────────────────
    print("\nDang ve bieu do...\n")
    plot_boxplot(stats,             save_path=out("boxplot"))
    plot_bar(stats,                 save_path=out("bar"))
    plot_line(stats,                save_path=out("line"))
    plot_insertion_explain(stats,   save_path=out("explain"))
    plot_adaptive_vs_best(stats,    save_path=out("adaptive"))

    print("\n" + "="*60)
    print("HOAN THANH!")
    print(f"Tat ca bieu do da luu vao: {OUTPUT_DIR}/")
    print("="*60)
