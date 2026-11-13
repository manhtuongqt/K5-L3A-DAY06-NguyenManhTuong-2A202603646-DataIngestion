# Phân tích dev trước test

Đọc sau `metrics_dev.json` và `selection.json`, trước khi gọi stage `test`.

- A: Hit@1 = 9/15, Evidence Hit@3 = 10/15.
- B: 12/15 và 13/15.
- C: 12/15 và 13/15.
- B được chọn bằng quy tắc đã khóa: Hit@3, Hit@1, rồi latency trung bình. B/C hòa cả hai điểm; B có latency quan sát thấp hơn trong lần đo này. Không coi khác biệt vài ms là chứng cứ hiệu năng ổn định.

## Các lỗi đọc từ trace

1. D03/A: gold `tutorial_datastructures:u004`. Top-1 đúng trang nhưng bắt đầu ở giữa câu (`nly strings...`), top-3 có đầu câu ở chunk khác và bị cắt ở cuối. Không chunk nào chứa đủ điều kiện và ngoại lệ; strict Hit@3=0 dù ghép các chunk có thể có thông tin. B/C giữ đầy đủ quote và hit.
2. D01/B: câu hỏi `list.remove(value)` không tìm thấy giá trị. Top-1 có `pop()`/`index()` nhưng không có đoạn gold về `remove`; top-2 là `del`, top-3 là dictionary. Đoạn B lớn hơn làm loãng tín hiệu. A tìm được evidence trong top-3. Không được suy ra ValueError của `list.index` là evidence tương đương cho `list.remove`.
3. D09: A/B/C đều không hit. Top-3 nghiêng về tên module khi import thay vì trạng thái `__name__` khi thực thi script. Đây là lỗi xếp hạng với câu có điều kiện; không tự sửa câu hỏi cho dễ hơn.

Không thực hiện tìm tham số theo điểm dev trong lượt này. Giữ một so sánh A/B/C và lưu các thất bại. Không có yêu cầu phải tăng điểm để gate đạt; ưu tiên đối chứng rõ và giữ holdout. Lần sửa giới hạn token và reconciliation store đều xảy ra trước dev, được ghi trong `implementation_log.md`.
