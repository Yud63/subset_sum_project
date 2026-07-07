# Phân tích và Đánh giá Hiệu năng các Thuật toán giải bài toán Subset Sum

Đồ án môn **Phân tích Thiết kế Giải thuật (PTTKGT)** - so sánh 4 thuật toán giải bài toán **Tổng tập con (Subset Sum)**.

## 1. Bài toán

Cho một dãy số nguyên dương `nums` và một số nguyên `target`, hỏi có tồn tại một tập con của `nums` sao cho tổng các phần tử trong tập con đó bằng `target` hay không? Nếu có, chỉ ra tập con đó.

Đây là bài toán **NP-Complete** kinh điển, thường dùng để minh họa sự khác biệt giữa các chiến lược thiết kế thuật toán: vét cạn, quay lui, quy hoạch động, chia để trị.

## 2. Bốn thuật toán được cài đặt

| # | Thuật toán                        | File                              | Độ phức tạp thời gian                 |Độ phức tạp không gian|
|---|-----------------------------------|-----------------------------------|---------------------------------------|----------------------|
| 1 |Brute Force(Vét cạn)               |`algorithms/brute_force.py`        | O(2ⁿ · n)                             |O(n)                  |
| 2 |Backtracking(Quay lui)             |`algorithms/backtracking.py`       | O(2ⁿ)(thực tế nhanh hơn nhờ cắt nhánh)|O(n)                  |
| 3 |Dynamic Programming(Quy hoạch động)|`algorithms/dynamic_programming.py`| O(n · target) (giả đa thức)           |O(n·target)           |
| 4 |Meet in the Middle(Chia để trị)    |`algorithms/meet_in_middle.py`     | O(2^(n/2) · n)                        |O(2^(n/2))            |

Mỗi file thuật toán đều có docstring giải thích chi tiết ý tưởng, công thức, độ phức tạp, ưu/nhược điểm - có thể dùng trực tiếp làm nội dung cho phần "Cài đặt thuật toán" trong tiểu luận.

## 3. Cấu trúc thư mục

```
subset_sum_project/
│
├── algorithms/
│   ├── brute_force.py           # Thuật toán 1: Vét cạn
│   ├── backtracking.py          # Thuật toán 2: Quay lui
│   ├── dynamic_programming.py   # Thuật toán 3: Quy hoạch động
│   └── meet_in_middle.py        # Thuật toán 4: Chia để trị
│
├── utils/
│   ├── generator.py             # Sinh dữ liệu test ngẫu nhiên
│   └── timer.py                 # Đo thời gian chạy
│
├── benchmark.py                 # Chạy benchmark toàn bộ, xuất CSV + biểu đồ
├── main.py                      # Demo nhập tay, chạy thử 1 lần
└── results/
    ├── benchmark_results.csv    # Kết quả đo thời gian
    └── chart.png                # Biểu đồ so sánh (thang log)
```

## 4. Cách chạy

Yêu cầu: Python 3.8+, thư viện `matplotlib` (chỉ cần cho benchmark).

```bash
pip install matplotlib
```

**Lưu ý cho Windows (đặc biệt nếu máy có cài nhiều bản Python, ví dụ Python chính thức + MSYS64/Git Bash/Anaconda...):**
Lệnh `python` và `pip` trong PowerShell/CMD có thể vô tình trỏ tới **các bản Python khác nhau** (ví dụ `python` trỏ vào MSYS64 nhưng `pip` lại cài vào bản Python chính thức). Khi đó dù `pip install matplotlib` báo thành công, chạy `python benchmark.py` vẫn báo `ModuleNotFoundError: No module named 'matplotlib'` vì nó đang chạy nhầm bản Python không có thư viện đó.

**Cách kiểm tra:** chạy `where python` để xem có bao nhiêu bản Python trong PATH.

**Cách khắc phục nhanh nhất:** dùng **Python Launcher** thay vì gọi thẳng `python`/`pip`:
```bash
py -m pip install matplotlib
py main.py
py benchmark.py
```
`py` sẽ tự tìm đúng bản Python chính thức đã cài đặt đầy đủ thư viện, tránh xung đột với các bản Python khác trên máy (MSYS64, Git Bash, WSL, Anaconda...).

Nếu dùng VS Code, có thể chọn interpreter cố định qua `Ctrl+Shift+P` → **Python: Select Interpreter** → chọn đúng bản Python313 (hoặc bản đã cài matplotlib), để mỗi terminal mới mở đều dùng đúng bản đó mà không cần gõ `py`.

### Demo nhập tay (chạy thử 1 lần, so sánh kết quả + thời gian):
```bash
python main.py
```
Chương trình sẽ hỏi nhập danh sách số và target, sau đó in bảng so sánh 4 thuật toán.

### Benchmark hiệu năng đầy đủ:
```bash
python benchmark.py
```
Script sẽ:
- Sinh dữ liệu ngẫu nhiên với `n` tăng dần (có seed cố định để tái lập được kết quả)
- Chạy giai đoạn 1: so sánh cả 4 thuật toán với `n` nhỏ (5–22), vì Brute Force/Backtracking là hàm mũ nên không thể test với `n` lớn
- Chạy giai đoạn 2: so sánh riêng Dynamic Programming và Meet in the Middle với `n` lớn hơn (22–32)
- Xuất kết quả ra `results/benchmark_results.csv`
- Vẽ biểu đồ so sánh (trục tung dùng thang log) ra `results/chart.png`

## 5. Bốn kịch bản benchmark và ý nghĩa của từng kịch bản

Một điểm rất quan trọng cần hiểu trước khi đọc số liệu: **benchmark với 1 kịch bản duy nhất không đủ để đánh giá đúng cả 4 thuật toán**, vì mỗi thuật toán chỉ lộ rõ điểm mạnh/yếu trong một điều kiện dữ liệu nhất định. Vì vậy `benchmark.py` chạy **4 giai đoạn**, mỗi giai đoạn nhắm vào 1 khía cạnh riêng:

### Giai đoạn 1 + 2 - `target` nhỏ, luôn có lời giải
File: `benchmark_small_target.csv`, `chart_small_target.png`

Mục đích: minh chứng độ phức tạp hàm mũ O(2ⁿ) của Brute Force, và cho thấy Backtracking/DP/Meet-in-Middle đều nhanh hơn nhiều trong điều kiện dễ.

Kết quả mẫu: Brute Force tăng từ 0.007s (n=15) lên 5.6s (n=22) - đúng tỉ lệ ~2ⁿ. DP và Meet in the Middle đều rất nhanh (dưới vài mili giây).

**Lưu ý quan trọng**: ở giai đoạn này `target` chỉ là tổng của một tập con ngẫu nhiên trong khoảng giá trị nhỏ (1-50), nên `target` luôn nhỏ dù `n` tăng. Điều này khiến DP "thắng" gần như tuyệt đối - nhưng đây **không phải là toàn bộ sự thật**, xem giai đoạn 3.

### Giai đoạn 3 - `target` RẤT LỚN (điểm mấu chốt để hiểu vì sao cần Meet in the Middle)
File: `benchmark_large_target.csv`, `chart_large_target.png`

Dynamic Programming có độ phức tạp **O(n × target)**. Ở giai đoạn 1+2, `target` luôn nhỏ nên chi phí này gần như không đáng kể. Giai đoạn 3 cố tình cho mỗi phần tử có giá trị lên tới **200,000**, khiến `target` lớn theo - lúc này bảng quy hoạch động phải có kích thước hàng trăm nghìn cột, và DP bắt đầu chậm hẳn.

Kết quả mẫu (n chỉ từ 14-20, nhỏ hơn nhiều so với giai đoạn 1-2!):
| n  | Dynamic Programming | Meet in the Middle |
|----|---------------------|--------------------|
| 14 | 1.96s               | 0.0003s            |
| 18 | 3.02s               | 0.0015s            |
| 20 | 2.42s               | 0.0045s            |

Meet in the Middle **không hề bị ảnh hưởng bởi độ lớn của target** - vì độ phức tạp của nó là O(2^(n/2) × n), chỉ phụ thuộc vào số lượng phần tử chứ không phụ thuộc giá trị của chúng. Đây chính là **lý do Meet in the Middle tồn tại**: khi `target` (hoặc tổng các phần tử) lớn tới mức DP không còn khả thi về bộ nhớ/thời gian, Meet in the Middle vẫn hoạt động tốt.

### Giai đoạn 4 - Trường hợp KHÔNG CÓ lời giải (worst-case thật sự của Backtracking)
File: `benchmark_unsolvable.csv`, `chart_unsolvable.png`

Ở giai đoạn 1-2, dữ liệu luôn được tạo để **chắc chắn có lời giải**, nên Backtracking thường tìm ra đáp án rất sớm nhờ cắt nhánh - đây không phải trường hợp xấu nhất. Giai đoạn 4 tạo dữ liệu **chắc chắn vô nghiệm** (target = tổng tất cả phần tử + 1), buộc Backtracking phải duyệt/quay lui qua **toàn bộ** không gian tìm kiếm trước khi kết luận "không tìm thấy".

Kết quả mẫu (n=22): Brute Force 8.94s, Backtracking 1.04s - tỉ lệ chênh lệch chỉ còn ~8.6 lần (so với hàng trăm nghìn lần ở giai đoạn 1-2 khi có lời giải). Điều này đúng bản chất lý thuyết: **cả hai đều là O(2ⁿ) trong trường hợp xấu nhất**, Backtracking chỉ nhanh hơn nhờ hệ số hằng số nhỏ hơn (cắt được một phần nhánh), chứ không đổi được bậc phức tạp.

## 6. Nhận xét tổng hợp

- **Brute Force**: luôn là O(2ⁿ) trong mọi trường hợp, cả tốt nhất lẫn xấu nhất. Chỉ dùng được với `n` rất nhỏ (≤ ~25).
- **Backtracking**: vẫn là O(2ⁿ) worst-case (giai đoạn 4 chứng minh điều này), nhưng thực tế nhanh hơn Brute Force nhiều lần nhờ cắt nhánh - đặc biệt hiệu quả khi dữ liệu "dễ" (có lời giải, tìm thấy sớm).
- **Dynamic Programming**: rất nhanh khi `target` nhỏ (O(n × target) gần như tuyến tính), nhưng **chính là nhược điểm** khi `target` lớn - đây là thuật toán "giả đa thức" (pseudo-polynomial), không phải đa thức thật sự.
- **Meet in the Middle**: không phụ thuộc vào độ lớn `target`, chỉ phụ thuộc vào `n` (O(2^(n/2) × n)) - là lựa chọn thay thế tốt cho DP khi `target` quá lớn để làm bảng quy hoạch động, dù vẫn tăng theo hàm mũ (cơ số nhỏ hơn) nên không xử lý được `n` quá lớn (ví dụ n > 40-45).

**Kết luận chung**: không có thuật toán nào tốt nhất tuyệt đối. Lựa chọn phụ thuộc vào đặc điểm cụ thể của bài toán:
- `n` nhỏ, không quan tâm `target` → Backtracking đơn giản, đủ nhanh.
- `target` nhỏ/vừa → Dynamic Programming là lựa chọn tối ưu.
- `target` rất lớn nhưng `n` vừa phải (≤ 40) → Meet in the Middle.
- `n` rất lớn và `target` rất lớn → bài toán trở nên khó xử lý chính xác, cần thuật toán xấp xỉ hoặc heuristic (ngoài phạm vi đồ án này).

## 7. Ghi chú khi viết tiểu luận

- Có thể trích các đoạn docstring trong từng file thuật toán để giải thích ý tưởng/độ phức tạp trong tiểu luận.
- File `benchmark_results.csv` là số liệu thô để vẽ bảng/biểu đồ trong Chương "Thực nghiệm và đánh giá".
- Có thể chỉnh các tham số trong `benchmark.py` (`SMALL_N_VALUES`, `LARGE_N_VALUES`, `MAX_VALUE`, `REPEAT`) để phù hợp với cấu hình máy và thời gian cho phép khi chạy benchmark.
