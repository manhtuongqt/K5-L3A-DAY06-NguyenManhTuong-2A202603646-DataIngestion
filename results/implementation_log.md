# Nhật ký sửa lỗi triển khai

## 1. Giới hạn ký tự không bảo đảm giới hạn token

- Bước: xây index, trước mọi truy xuất dev/test.
- Cấu hình ban đầu: B/C theo đoạn, tối đa 1.200 ký tự.
- Bằng chứng thật: token guard báo `Truncation would discard source evidence: B, max 564 tokens`. Model chỉ nhận 512 token. Index A đã tạo 585 vector trong 58,79 giây, nhưng chưa truy xuất benchmark.
- Nguyên nhân: chữ ký API và đoạn mã có tỷ lệ token/ký tự cao hơn văn xuôi.
- Sửa: B/C cùng giảm xuống 1.000 ký tự; giữ nguyên A, model, corpus, câu hỏi, evidence và filter. Kiểm tra lại token trước embedding; không cho phép âm thầm truncate.
- Lưu protocol/lock cũ ở `benchmark/history/pre_token_guard/`; khóa lại protocol mới trước dev/test. Đây là sửa giới hạn đầu vào bằng token của model, không phải tối ưu dựa trên điểm test.
- Lần tạo index bị ngắt không có thời gian ingest hoàn chỉnh; chạy lại index để lưu phép đo đầy đủ. Không báo lần lỗi như một benchmark hoàn thành.

## 2. Chunk cũ còn lại khi tạo lại collection local trên Windows

- Bằng chứng: integration test nạp 2 điểm, đóng/mở store, rồi thay snapshot bằng 1 điểm; nhận count=2 thay vì 1. Cleanup còn báo WinError 32 cho `storage.sqlite` đang mở.
- Nguyên nhân kiểm tra từ mã Qdrant local: `delete_collection` xóa thư mục bằng `shutil.rmtree(..., ignore_errors=True)`; tệp SQLite đang mở trên Windows có thể không bị xóa, khiến collection tạo lại nạp dữ liệu cũ.
- Sửa: giữ collection, upsert ID xác định, scroll ID hiện tại và xóa điểm không còn trong snapshot bằng API Qdrant. Không tự sửa SQLite hoặc tính similarity thay store.
- Không thay chunk/model/filter/benchmark. Kiểm tra lại đúng integration test về persistence, filter và obsolete deletion trước khi chạy dev/test.
