"""
main.py
--------
Chuong trinh demo: cho phep nguoi dung nhap tay danh sach so va target,
sau do chay ca 4 thuat toan de so sanh ket qua va thoi gian chay.

Cach chay:
    python main.py
"""

from algorithms.brute_force import subset_sum_brute_force
from algorithms.backtracking import subset_sum_backtracking
from algorithms.dynamic_programming import subset_sum_dp
from algorithms.meet_in_middle import subset_sum_meet_in_middle
from utils.timer import measure_time


def get_user_input():
    """Doc danh sach so va target tu ban phim."""
    print("=" * 60)
    print("DEMO: BAI TOAN SUBSET SUM (TONG TAP CON)")
    print("=" * 60)

    raw = input("Nhap danh sach so nguyen duong, cach nhau boi dau cach\n"
                "(vi du: 3 34 4 12 5 2): ").strip()
    nums = [int(x) for x in raw.split()]

    target = int(input("Nhap tong can tim (target): ").strip())
    return nums, target


def run_all_algorithms(nums, target):
    """Chay lan luot ca 4 thuat toan tren cung 1 bo du lieu va in ket qua."""
    algorithms = [
        ("Brute Force        ", subset_sum_brute_force),
        ("Backtracking       ", subset_sum_backtracking),
        ("Dynamic Programming", subset_sum_dp),
        ("Meet in the Middle ", subset_sum_meet_in_middle),
    ]

    print("\nDu lieu dau vao:")
    print(f"  nums   = {nums}")
    print(f"  target = {target}\n")

    print(f"{'Thuat toan':<22} | {'Ket qua':<10} | {'Tap con tim duoc':<30} | {'Thoi gian (s)'}")
    print("-" * 95)

    for name, func in algorithms:
        (found, subset), elapsed = measure_time(func, nums, target)
        result_str = "Co" if found else "Khong"
        subset_str = str(subset) if found else "-"
        print(f"{name:<22} | {result_str:<10} | {subset_str:<30} | {elapsed:.8f}")


def main():
    # Neu muon test nhanh khong can nhap tay, co the bo comment 2 dong duoi:
    # nums, target = [3, 34, 4, 12, 5, 2], 9
    nums, target = get_user_input()

    run_all_algorithms(nums, target)


if __name__ == "__main__":
    main()
