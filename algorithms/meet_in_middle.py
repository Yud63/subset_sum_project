"""
Thuat toan 4: Meet in the Middle (Chia de tri)
--------------------------------------------------
Y tuong:
    - Chia danh sach nums thanh 2 nua: left (n/2 phan tu dau) va
      right (n/2 phan tu con lai).
    - Tinh tat ca tong tap con co the co cua left (co 2^(n/2) tap con)
      va tat ca tong tap con co the co cua right (co 2^(n/2) tap con).
    - Sap xep danh sach tong cua right.
    - Voi moi tong s_left cua left, ta chi can tim trong right mot tong
      s_right = target - s_left bang tim kiem nhi phan (binary search).
    - Neu tim thay -> ket hop 2 tap con lai la ra dap so.

    Vi sao nhanh hon Brute Force?
    - Brute Force: O(2^n)
    - Meet in the Middle: O(2^(n/2) * log(2^(n/2))) = O(2^(n/2) * n)
      Vi du n = 40: 2^40 ~ 10^12 (Brute Force khong kha thi)
                    2^20 ~ 10^6  (Meet in the Middle kha thi!)
    => Day la ky thuat "chia de tri" kinh dien de tang gap doi kich thuoc
       bai toan co the giai duoc so voi vet can thuan tuy.

Do phuc tap:
    - Thoi gian: O(2^(n/2) * n)
    - Khong gian: O(2^(n/2))  (luu danh sach tong cua 1 nua)

Uu diem: xu ly duoc n lon hon nhieu so voi Brute Force/Backtracking thuan tuy
(vi du n = 30-40) ma van dam bao ket qua dung chinh xac.
Nhuoc diem: cai dat phuc tap hon, van la ham mu (chi la co so mu nho hon),
khong hieu qua bang DP neu target nho.
"""

from bisect import bisect_left


def _all_subset_sums(arr):
    """
    Sinh ra tat ca (tong, danh_sach_chi_so_da_chon) cho moi tap con cua arr.
    Tra ve list cac tuple (sum, subset_elements).
    """
    n = len(arr)
    result = []
    for mask in range(1 << n):
        s = 0
        subset = []
        for i in range(n):
            if mask & (1 << i):
                s += arr[i]
                subset.append(arr[i])
        result.append((s, subset))
    return result


def subset_sum_meet_in_middle(nums, target):
    """
    Giai bai toan Subset Sum bang ky thuat Meet in the Middle (chia de tri).

    Tham so:
        nums (list[int]): danh sach cac so nguyen duong
        target (int): tong can tim

    Tra ve:
        (bool, list[int]): (co tim thay hay khong, tap con thoa man neu co)
    """
    n = len(nums)
    if n == 0:
        return (target == 0), []

    mid = n // 2
    left = nums[:mid]
    right = nums[mid:]

    left_sums = _all_subset_sums(left)   # danh sach (tong, tap con) cua nua trai
    right_sums = _all_subset_sums(right)  # danh sach (tong, tap con) cua nua phai

    # Sap xep right theo tong de tim kiem nhi phan
    right_sums.sort(key=lambda x: x[0])
    right_values = [x[0] for x in right_sums]

    for s_left, subset_left in left_sums:
        need = target - s_left
        # Tim kiem nhi phan gia tri "need" trong right_values
        pos = bisect_left(right_values, need)
        if pos < len(right_values) and right_values[pos] == need:
            subset_right = right_sums[pos][1]
            return True, subset_left + subset_right

    return False, []
