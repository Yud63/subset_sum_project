"""
benchmark.py
-------------
Chay 4 thuat toan tren nhieu kich ban du lieu khac nhau, do thoi gian
chay, luu ket qua ra CSV va ve bieu do so sanh.

Benchmark gom 4 GIAI DOAN, moi giai doan nham lam ro MOT khia canh khac
nhau cua 4 thuat toan (khong giai doan nao la "du" de danh gia toan dien
mot minh):

    Giai doan 1: So sanh ca 4 thuat toan voi n nho, target NHO (bo test
                 "de", dam bao co loi giai).
                 -> Muc dich: thay ro do phuc tap ham mu O(2^n) cua
                    Brute Force so voi 3 thuat toan con lai.

    Giai doan 2: So sanh rieng Dynamic Programming va Meet in the Middle
                 voi n LON hon, target VAN NHO.
                 -> Muc dich: thay Meet in the Middle van la ham mu
                    (co so nho hon) trong khi DP gan nhu tuyen tinh.

    Giai doan 3: (MOI) So sanh Dynamic Programming va Meet in the Middle
                 khi target RAT LON (max_value len den 10^6), n vua phai
                 (18-24).
                 -> Muc dich QUAN TRONG: day moi la kich ban lam ro NHUOC
                    DIEM that su cua DP - do phuc tap O(n * target) khien
                    DP bi "no" thoi gian/bo nho khi target lon, trong khi
                    Meet in the Middle KHONG phu thuoc vao gia tri target,
                    chi phu thuoc vao n. Day la ly do Meet in the Middle
                    ton tai du DP "thang" o Giai doan 1 va 2.

    Giai doan 4: (MOI) So sanh Brute Force va Backtracking trong truong
                 hop KHONG CO LOI GIAI (target = tong tat ca phan tu + 1).
                 -> Muc dich QUAN TRONG: o cac giai doan truoc, test case
                    luon dam bao CO loi giai nen Backtracking thuong tim
                    thay dap an rat som (cat nhanh hieu qua, chay gan nhu
                    O(1)). Day khong phai worst-case that su. Khi KHONG CO
                    loi giai, Backtracking buoc phai duyet/quay lui QUA
                    HET khong gian tim kiem truoc khi ket luan "khong tim
                    thay" -> luc nay thoi gian chay moi tiem can Brute
                    Force, dung ban chat O(2^n) trong ly thuyet worst-case.

Ket qua duoc luu thanh nhieu file CSV/PNG rieng biet de de trich dan
tung phan vao tieu luan:
    results/benchmark_small_target.csv   + chart_small_target.png   (GD 1+2)
    results/benchmark_large_target.csv   + chart_large_target.png   (GD 3)
    results/benchmark_unsolvable.csv     + chart_unsolvable.png     (GD 4)

Cach chay:
    python benchmark.py
"""

import os
import csv

from algorithms.brute_force import subset_sum_brute_force
from algorithms.backtracking import subset_sum_backtracking
from algorithms.dynamic_programming import subset_sum_dp
from algorithms.meet_in_middle import subset_sum_meet_in_middle
from utils.generator import generate_test_case, generate_unsolvable_test_case
from utils.timer import measure_time

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
SEED_BASE = 42   # seed goc de tai lap ket qua
REPEAT = 3       # so lan lap lai moi cau hinh de lay trung binh, giam nhieu ngau nhien

ALL_ALGORITHMS = [
    ("Brute Force", subset_sum_brute_force),
    ("Backtracking", subset_sum_backtracking),
    ("Dynamic Programming", subset_sum_dp),
    ("Meet in the Middle", subset_sum_meet_in_middle),
]

DP_AND_MITM = [
    ("Dynamic Programming", subset_sum_dp),
    ("Meet in the Middle", subset_sum_meet_in_middle),
]

BF_AND_BACKTRACK = [
    ("Brute Force", subset_sum_brute_force),
    ("Backtracking", subset_sum_backtracking),
]

# ---- Cau hinh Giai doan 1 + 2: target NHO ----
SMALL_TARGET_MAX_VALUE = 50
SMALL_N_VALUES = [5, 10, 15, 18, 20, 22]    # test ca 4 thuat toan
LARGE_N_VALUES = [22, 24, 26, 28, 30, 32]   # test rieng DP vs MITM (n lon hon)

# ---- Cau hinh Giai doan 3: target RAT LON (de "vach tran" nhuoc diem DP) ----
LARGE_TARGET_MAX_VALUE = 200_000            # moi phan tu co the len den 200,000
LARGE_TARGET_N_VALUES = [14, 16, 18, 20]    # n vua phai, KHONG the qua lon vi
                                             # Meet in the Middle van la ham mu
LARGE_TARGET_REPEAT = 1                     # DP o day rat cham nen chi chay 1 lan/cau hinh

# ---- Cau hinh Giai doan 4: KHONG CO loi giai (worst-case that su) ----
UNSOLVABLE_MAX_VALUE = 50
UNSOLVABLE_N_VALUES = [10, 15, 18, 20, 22]  # n nho vi Brute Force van la O(2^n)


def run_single_benchmark(nums, target, algorithms):
    """Chay danh sach thuat toan tren 1 bo du lieu, tra ve {ten: thoi_gian}."""
    timings = {}
    for name, func in algorithms:
        _, elapsed = measure_time(func, nums, target)
        timings[name] = elapsed
    return timings


def _run_scenario(n_values, algorithms, generator_func, generator_kwargs, label, repeat=REPEAT):
    """
    Ham dung chung: voi moi n trong n_values, sinh `repeat` bo du lieu,
    chay tat ca algorithms, lay thoi gian trung binh, in ra man hinh va
    tra ve list rows.
    """
    rows = []
    for n in n_values:
        sums = {name: 0.0 for name, _ in algorithms}
        for r in range(repeat):
            nums, target = generator_func(
                n, seed=SEED_BASE + n * 10 + r, **generator_kwargs
            )
            timings = run_single_benchmark(nums, target, algorithms)
            for name in sums:
                sums[name] += timings[name]

        for name in sums:
            avg_time = sums[name] / repeat
            rows.append({"n": n, "algorithm": name, "avg_time_seconds": avg_time})
            print(f"  n={n:<3} | {name:<20} | avg = {avg_time:.6f}s")

    return rows


def benchmark_small_target():
    """Giai doan 1 + 2: target nho, dam bao co loi giai."""
    print(">>> Giai doan 1: So sanh ca 4 thuat toan voi n nho, target nho...")
    rows = _run_scenario(
        SMALL_N_VALUES, ALL_ALGORITHMS, generate_test_case,
        {"max_value": SMALL_TARGET_MAX_VALUE, "ensure_solvable": True},
        "small_target_stage1",
    )

    print("\n>>> Giai doan 2: So sanh rieng DP va Meet in the Middle voi n lon hon, target van nho...")
    rows += _run_scenario(
        LARGE_N_VALUES, DP_AND_MITM, generate_test_case,
        {"max_value": SMALL_TARGET_MAX_VALUE, "ensure_solvable": True},
        "small_target_stage2",
    )
    return rows


def benchmark_large_target():
    """
    Giai doan 3: target RAT LON (max_value = 1,000,000), n vua phai.
    Day la kich ban lam ro nhuoc diem that su cua Dynamic Programming:
    bang dp co kich thuoc O(n * target), khi target len den hang trieu,
    DP se cham/ton bo nho ro ret, trong khi Meet in the Middle khong bi
    anh huong boi do lon cua target ma chi phu thuoc vao n.
    """
    print("\n>>> Giai doan 3: So sanh DP va Meet in the Middle khi TARGET RAT LON "
          f"(moi phan tu toi da {LARGE_TARGET_MAX_VALUE:,})...")
    rows = _run_scenario(
        LARGE_TARGET_N_VALUES, DP_AND_MITM, generate_test_case,
        {"max_value": LARGE_TARGET_MAX_VALUE, "ensure_solvable": True},
        "large_target_stage3",
        repeat=LARGE_TARGET_REPEAT,
    )
    return rows


def benchmark_unsolvable():
    """
    Giai doan 4: bo test KHONG CO loi giai (target = tong tat ca + 1).
    Day la worst-case THAT SU cho Brute Force va Backtracking, vi thuat
    toan buoc phai duyet/quay lui QUA HET khong gian tim kiem truoc khi
    ket luan khong co dap an -- khong con "an may" tim thay som nhu cac
    bo test dam bao co loi giai o Giai doan 1/2/3.
    """
    print("\n>>> Giai doan 4: So sanh Brute Force va Backtracking khi KHONG CO loi giai "
          "(worst-case that su)...")
    rows = _run_scenario(
        UNSOLVABLE_N_VALUES, BF_AND_BACKTRACK, generate_unsolvable_test_case,
        {"max_value": UNSOLVABLE_MAX_VALUE},
        "unsolvable_stage4",
    )
    return rows


def save_csv(rows, filename):
    """Luu 1 bo ket qua ra file CSV trong thu muc results/."""
    path = os.path.join(RESULTS_DIR, filename)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "algorithm", "avg_time_seconds"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Da luu CSV tai: {path}")


def save_chart(rows, filename, title, ylog=True):
    """Ve bieu do duong so sanh thoi gian chay theo n cho 1 bo ket qua."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data_by_algo = {}
    for row in rows:
        algo = row["algorithm"]
        data_by_algo.setdefault(algo, {"n": [], "time": []})
        data_by_algo[algo]["n"].append(row["n"])
        data_by_algo[algo]["time"].append(row["avg_time_seconds"])

    plt.figure(figsize=(9, 6))
    for algo, data in data_by_algo.items():
        paired = sorted(zip(data["n"], data["time"]))
        xs = [p[0] for p in paired]
        ys = [p[1] for p in paired]
        plt.plot(xs, ys, marker="o", label=algo)

    plt.xlabel("So luong phan tu (n)")
    ylabel = "Thoi gian chay trung binh (giay)"
    if ylog:
        ylabel += " - thang log"
        plt.yscale("log")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()

    path = os.path.join(RESULTS_DIR, filename)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(path, dpi=150)
    print(f"Da luu bieu do tai: {path}")


def main():
    # Giai doan 1 + 2 (target nho)
    small_rows = benchmark_small_target()
    save_csv(small_rows, "benchmark_small_target.csv")
    save_chart(
        small_rows, "chart_small_target.png",
        "GD 1+2: So sanh 4 thuat toan (target nho, luon co loi giai)"
    )

    # Giai doan 3 (target lon - lam ro nhuoc diem DP)
    large_rows = benchmark_large_target()
    save_csv(large_rows, "benchmark_large_target.csv")
    save_chart(
        large_rows, "chart_large_target.png",
        "GD 3: DP vs Meet in the Middle khi TARGET RAT LON"
    )

    # Giai doan 4 (worst-case khong co loi giai)
    unsolvable_rows = benchmark_unsolvable()
    save_csv(unsolvable_rows, "benchmark_unsolvable.csv")
    save_chart(
        unsolvable_rows, "chart_unsolvable.png",
        "GD 4: Brute Force vs Backtracking khi KHONG CO loi giai (worst-case)"
    )

    print("\n=== HOAN TAT TOAN BO BENCHMARK ===")
    print("Xem cac file CSV/PNG trong thu muc results/ de dua vao bao cao.")


if __name__ == "__main__":
    main()
