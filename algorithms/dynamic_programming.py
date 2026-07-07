"""
Thuat toan 3: Dynamic Programming (Quy hoach dong)
-----------------------------------------------------
Y tuong:
    - Goi dp[i][s] = True neu co the chon mot so phan tu trong i phan tu
      dau tien (nums[0..i-1]) sao cho tong bang s.
    - Cong thuc truy hoi:
        dp[i][s] = dp[i-1][s]                       (khong chon phan tu thu i)
                   OR dp[i-1][s - nums[i-1]]         (co chon phan tu thu i,
                                                       neu s >= nums[i-1])
    - dp[0][0] = True (khong chon gi ca thi tong = 0), dp[0][s>0] = False
    - Dap so cuoi cung: dp[n][target]
    - Ta dung mang 1 chieu (toi uu khong gian) va duyet s tu target giam
      dan ve 0 de tranh dung lai 1 phan tu nhieu lan trong cung 1 lan cap nhat.
    - De truy vet (tim ra tap con cu the), ta luu lai bang dp day du 2 chieu
      (hoac luu "parent") roi truy nguoc.

Do phuc tap:
    - Thoi gian: O(n * target)   (giai "gia da thuc" - pseudo-polynomial)
    - Khong gian: O(n * target) neu luu bang day du de truy vet,
                  hoac O(target) neu chi can biet True/False.

Uu diem: nhanh hon han Brute Force / Backtracking khi target khong qua lon,
vi khong phu thuoc truc tiep vao 2^n.
Nhuoc diem: neu target rat lon (vi du hang trieu) thi bang dp se rat lon,
ton nhieu bo nho va thoi gian -> day la ly do goi la "gia da thuc".
"""


def subset_sum_dp(nums, target):
    """
    Giai bai toan Subset Sum bang Quy hoach dong (co truy vet lay tap con).

    Tham so:
        nums (list[int]): danh sach cac so nguyen duong
        target (int): tong can tim (target >= 0)

    Tra ve:
        (bool, list[int]): (co tim thay hay khong, tap con thoa man neu co)
    """
    n = len(nums)

    if target < 0:
        return False, []

    # dp[i][s]: True/False - co dat duoc tong s bang i phan tu dau khong
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True  # tong = 0 luon dat duoc bang cach khong chon gi

    for i in range(1, n + 1):
        num = nums[i - 1]
        for s in range(target + 1):
            dp[i][s] = dp[i - 1][s]  # khong chon phan tu i
            if not dp[i][s] and s >= num:
                dp[i][s] = dp[i - 1][s - num]  # co chon phan tu i

    if not dp[n][target]:
        return False, []

    # Truy vet de tim ra tap con cu the
    subset = []
    s = target
    for i in range(n, 0, -1):
        if s < 0:
            break
        # Neu dp[i][s] khac dp[i-1][s] tuc la phan tu i DA duoc chon
        if dp[i][s] and not dp[i - 1][s]:
            subset.append(nums[i - 1])
            s -= nums[i - 1]

    return True, subset
