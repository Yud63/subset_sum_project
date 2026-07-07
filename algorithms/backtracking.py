"""
Thuat toan 2: Backtracking (Quay lui)
--------------------------------------
Y tuong:
    - Xay dung cay quyet dinh: tai moi phan tu, co 2 lua chon "chon" hoac "khong chon".
    - Khac voi Brute Force (duyet het roi moi kiem tra), Backtracking se
      CAT NHANH (pruning) ngay khi phat hien nhanh hien tai khong the dan
      den loi giai:
        + Neu tong hien tai > target => dung lai, khong di tiep nhanh do
          (vi nums chi chua so nguyen duong nen tong chi co tang).
        + Neu tong hien tai == target => tim thay loi giai, dung lai.
    - Nho cat nhanh som, Backtracking thuong nhanh hon Brute Force rat nhieu
      trong thuc te, du do phuc tap ly thuyet xau nhat van la O(2^n).

Do phuc tap:
    - Thoi gian: O(2^n) truong hop xau nhat, nhung thuc te nhanh hon nhieu
      nho cat nhanh.
    - Khong gian: O(n) cho do sau de quy + luu tap con hien tai.

Uu diem: nhanh hon Brute Force nho cat nhanh, van dam bao dung.
Nhuoc diem: van la ham mu trong truong hop xau nhat (vi du: tat ca phan tu
rat nho hoac target rat lon nen khong the cat nhanh duoc).
"""


def subset_sum_backtracking(nums, target):
    """
    Giai bai toan Subset Sum bang Backtracking (quay lui co cat nhanh).

    Tham so:
        nums (list[int]): danh sach cac so nguyen duong
        target (int): tong can tim

    Tra ve:
        (bool, list[int]): (co tim thay hay khong, tap con thoa man neu co)
    """
    n = len(nums)
    result_subset = []

    # Sap xep giam dan giup cat nhanh hieu qua hon trong nhieu truong hop
    # (khong bat buoc, nhung la 1 cai tien pho bien khi trinh bay trong tieu luan)
    nums_sorted = sorted(nums, reverse=True)

    def backtrack(index, current_sum, current_subset):
        # Truong hop dung: tim thay loi giai
        if current_sum == target:
            result_subset.extend(current_subset)
            return True

        # Cat nhanh: het phan tu hoac tong da vuot qua target
        if index == n or current_sum > target:
            return False

        # Nhanh 1: CHON phan tu tai index
        current_subset.append(nums_sorted[index])
        if backtrack(index + 1, current_sum + nums_sorted[index], current_subset):
            return True
        current_subset.pop()  # quay lui (undo lua chon)

        # Nhanh 2: KHONG CHON phan tu tai index
        if backtrack(index + 1, current_sum, current_subset):
            return True

        return False

    found = backtrack(0, 0, [])
    return found, result_subset
