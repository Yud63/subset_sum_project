"""
Module sinh du lieu test ngau nhien cho bai toan Subset Sum.
"""

import random


def generate_test_case(n, max_value=100, ensure_solvable=True, seed=None):
    """
    Sinh ngau nhien 1 bo test cho bai toan Subset Sum.

    Tham so:
        n (int): so luong phan tu can sinh
        max_value (int): gia tri lon nhat cua moi phan tu (1..max_value)
        ensure_solvable (bool):
            - True: dam bao bo test CO loi giai (bang cach chon ngau nhien
              1 tap con lam target truoc)
            - False: target duoc sinh hoan toan ngau nhien (co the co hoac
              khong co loi giai)
        seed (int|None): gia tri seed de tai lap ket qua ngau nhien (danh
            cho muc dich kiem thu/bao cao)

    Tra ve:
        (list[int], int): (danh sach so nguyen duong, target)
    """
    if seed is not None:
        random.seed(seed)

    nums = [random.randint(1, max_value) for _ in range(n)]

    if ensure_solvable:
        # Chon ngau nhien 1 tap con lam "loi giai co san", roi lay tong lam target
        subset_size = random.randint(1, n)
        chosen_subset = random.sample(nums, subset_size)
        target = sum(chosen_subset)
    else:
        target = random.randint(1, max_value * n)

    return nums, target


def generate_unsolvable_test_case(n, max_value=100, seed=None):
    """
    Sinh 1 bo test CHAC CHAN KHONG CO loi giai (dung de do worst-case
    thuc su cua Brute Force / Backtracking).

    Ky thuat: target = tong TAT CA phan tu + 1. Vi tat ca phan tu deu
    duong, khong co tap con nao (ke ca lay het) co the dat duoc tong nay,
    nen thuat toan BAT BUOC phai duyet/quay lui QUA HET khong gian tim
    kiem truoc khi ket luan "khong tim thay" -> day moi la truong hop
    O(2^n) day du, khong bi "an may" tim thay som.

    Tham so:
        n (int): so luong phan tu
        max_value (int): gia tri lon nhat cua moi phan tu
        seed (int|None): seed de tai lap ket qua

    Tra ve:
        (list[int], int): (danh sach so nguyen duong, target khong co loi giai)
    """
    if seed is not None:
        random.seed(seed)

    nums = [random.randint(1, max_value) for _ in range(n)]
    target = sum(nums) + 1  # vuot qua tong lon nhat co the -> chac chan vo nghiem

    return nums, target
