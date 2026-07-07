"""
Thuat toan 1: Brute Force (Vet can)
------------------------------------
Y tuong:
    - Voi n phan tu, co tat ca 2^n tap con co the.
    - Ta duyet qua tat ca cac tap con (dung bitmask tu 0 -> 2^n - 1),
      tinh tong tung tap con va so sanh voi target.
    - Neu tim thay tap con co tong = target => tra ve True va tap con do.

Do phuc tap:
    - Thoi gian: O(2^n * n)  (2^n tap con, moi tap con mat O(n) de tinh tong)
    - Khong gian: O(n) (luu tap con hien tai)

Uu diem: don gian, de cai dat, chac chan tim ra dap an (neu co).
Nhuoc diem: cuc ky cham voi n lon (n > ~25 la khong kha thi).
"""


def subset_sum_brute_force(nums, target):
    """
    Giai bai toan Subset Sum bang phuong phap vet can (duyet toan bo bitmask).

    Tham so:
        nums (list[int]): danh sach cac so nguyen duong
        target (int): tong can tim

    Tra ve:
        (bool, list[int]): (co tim thay hay khong, tap con thoa man neu co)
    """
    n = len(nums)

    # Duyet tat ca 2^n bitmask, moi bit tuong ung voi 1 phan tu co duoc chon hay khong
    for mask in range(1 << n):
        subset = []
        current_sum = 0
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
                current_sum += nums[i]
        if current_sum == target:
            return True, subset

    return False, []
