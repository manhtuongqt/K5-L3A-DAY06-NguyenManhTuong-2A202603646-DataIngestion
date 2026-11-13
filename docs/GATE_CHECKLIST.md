# Day06: kế hoạch và bảng gate

Nguyễn Mạnh Tường — 2A202603646 — L3A. Corpus dự kiến: tài liệu Python 3.13 chính thức, tiếng Anh. Đây là dữ liệu thử nghiệm truy xuất, không phải yêu cầu học Python của lab.

## Trình tự thực hiện

1. Chốt nguồn, giấy phép, cách tính đơn vị HTML và lưu snapshot có SHA-256.
2. Tạo ít nhất 20 câu hỏi, 15 dev / 5 test, gold và filter từ ngữ cảnh. Khóa benchmark, tiêu chí chọn và mẫu audit trước khi truy xuất.
3. Chuẩn hóa Unicode, giữ cấu trúc đoạn; tạo A chia cố định và B theo đoạn. C dùng đúng index B, chỉ thêm filter khi câu hỏi có yêu cầu.
4. Chạy embedding ONNX thật và Qdrant local bền vững; kiểm tra nạp lại, nạp lặp và xóa chunk cũ.
5. Chạy dev, chốt lựa chọn bằng dev, sau đó mới chạy test một lần. Lưu top-3 và chỉ số với mẫu số rõ ràng.
6. Chuẩn bị bản audit hỗ trợ; người học đối chiếu và xác nhận coherence, grounding và metadata/gold. Đã nhận xác nhận toàn bộ 110 dòng ngày 13/11/2026, lưu hồ sơ và fingerprint từng dòng.
7. Viết báo cáo theo năm khía cạnh, kiểm tra cấu trúc/rubric, commit và push. Người học tự nộp LMS.

## Bảng gate

| Gate | Căn cứ | Việc cần làm | Lệnh kiểm tra dự kiến | Minh chứng | Trạng thái | Giới hạn |
|---|---|---|---|---|---|---|
| A: corpus | GUIDE, RULES, SUBMISSION | ≥30 đơn vị hợp lệ, quyền sử dụng, nguồn/offset/độ dài | `python -m src.pipeline verify` | `data/manifest.json`, `data/pages.jsonl`, `results/ingestion_log.json` | đạt | 69 đơn vị, ít nhất 2.435 ký tự; HTML không phải trang PDF; bảng/hình chưa trích hết |
| B: benchmark | BENCHMARK | ≥20 câu; 15 dev/5 test; ≥3 filter, ≥1 test; gold trước truy xuất | `python -m src.pipeline verify` | `benchmark/questions.json`, `benchmark/protocol.json`, `benchmark/lock.json`, `results/audit/human_confirmation.json` | đạt | 20 câu, 6 filter (3 test); người học đã đối chiếu và xác nhận 20 gold/evidence. Giữ nguyên lock thí nghiệm |
| C: chunk | GUIDE | Unicode/whitespace; hai cách chia; metadata và phân bố | `python -m unittest discover -s tests -v` | `results/chunks_*.jsonl`, `results/chunk_stats.json` | đạt | A=585, B/C=312; khối dài vẫn phải cắt; không OCR vì HTML |
| D: embedding/store | RULES, SUBMISSION | Model thật; cosine/filter; persistence; replace/dedup | `python -m src.pipeline check-store`; unit tests | `benchmark/model.json`, `results/runtime.json`, `results/store_checks.json` | đạt | BGE ONNX 384d; cosine exact; mở lại/nạp lặp/xóa điểm cũ đã kiểm tra. Cập nhật chưa atomic |
| E: đối chứng | BENCHMARK | A/B/C; B–C chỉ khác filter; chọn bằng dev trước test | `python -m src.pipeline verify` | `benchmark/protocol.json`, `results/selection.json`, `results/dev_analysis.md`, `artifacts/experiment_log.csv` | đạt | Chọn B bằng dev; giữ một thí nghiệm, không tinh chỉnh bằng test |
| F1: retrieval | GUIDE | Hit@1/Evidence Hit@3, top-3 dev/test | `python -m src.pipeline verify` | `results/metrics.json`, `results/traces_*.jsonl` | đạt | 45 trace dev + 15 test; strict full-quote có thể bảo thủ (T04) |
| F2: audit | GUIDE | 10 anchors × 3; 5 test × top-3 metadata; 5 test × 3 grounding | Đọc `results/audit/REVIEW.md`, đối chiếu CSV, chạy `audit` | `results/audit/labels.csv`, `results/audit/human_confirmation.json`, `results/audit/status.json` | đạt | Nguyễn Mạnh Tường đã đối chiếu và chấp nhận 30 coherence + 45 metadata + 15 grounding; 0 dòng chờ xác nhận. Không chấm mù/độc lập |
| G: trung thực | RULES | Ghi nguồn hỗ trợ ban đầu và xác nhận human; công bố hỗ trợ AI | Đối chiếu cột nhãn/status và báo cáo | `results/audit/README.md`, `results/audit/human_confirmation.json`, báo cáo | đạt | Bản hỗ trợ đã được người học kiểm tra và chấp nhận; không tự nhận đã nộp LMS hoặc chấm độc lập |
| H: bài nộp | SUBMISSION, RUBRIC | Cấu trúc, chạy lại, báo cáo 5 khía cạnh, ≥2 lỗi, commit/push | `python scripts/check_submission.py`; `git status` | README, STUDENT, báo cáo, `results/submission_check.json`, `results/reproduction.json` | đạt phần chuẩn bị bài nộp | Audit đã được xác nhận; người học tự trình bày và nộp LMS. Không coi trạng thái sẵn sàng là đã nộp LMS |

Không sửa RULES/RUBRIC/SUBMISSION để giảm điều kiện đạt. Gate chỉ chuyển sang đạt khi có minh chứng thực tế. Việc cần người học sẽ ghi “cần người dùng”.

## Đối chiếu từng checkpoint của đề

| Mốc trong CHECKPOINTS.md | Kết quả hiện tại | Cần làm tiếp |
|---|---|---|
| 0:25 — dữ liệu/setup | Đạt phần kỹ thuật: 9 snapshot được phép dùng, 69 đơn vị; extractor và Qdrant chạy thật | Người học hiểu quy tắc đếm HTML |
| 1:00 — benchmark | Đạt: 20 câu/15 dev/5 test, gold tồn tại, lock trước truy xuất; người học đã đối chiếu gold | Không sửa test để tăng điểm |
| 1:50 — normalize/chunk | Đạt: NFC/offset/log; hai cấu hình; thống kê và metadata | Nhãn coherence đã xác nhận ở checkpoint audit |
| 2:40 — ba chiến lược | Đạt: model thật, index bền vững, exact cosine, filter, reingest, reopen | Không có key hoặc Docker cần bổ sung |
| 3:30 — benchmark/audit | Đạt: retrieval/trace và toàn bộ 110 nhãn đã được người học kiểm tra/chấp nhận | Không còn nhãn chờ xác nhận |
| 4:00 — báo cáo/nộp | Đã chuẩn bị báo cáo 5 khía cạnh, ví dụ lỗi, lệnh, kết quả tái lập và audit đã duyệt | Người học tự trình bày/nộp LMS |

## Kiểm tra tái lập

`scripts/reproduce.py` đã xây index mới, chạy dev/test và unit/integration tests trong `.local/reproduce/`. Có 78 phép so sánh điểm đếm/filter/top-3 khớp; độ lệch score tối đa 0.0. B được chọn ở cả lượt gốc và lượt kiểm tra. Đây là tái lập cấu hình đã chốt, không phải thêm holdout độc lập. Console và tổng kết đã lưu ở `results/reproduction_console.txt`, `results/reproduction.json`.

## Đối chiếu RUBRIC.md (không tự cấp điểm)

| Nhóm tiêu chí | Bằng chứng có | Thành phần còn chờ |
|---|---|---|
| Corpus/xử lý — 20 | Manifest/license/raw/normalized, 69 đơn vị, source offsets, log extractor và unit tests | Không có lỗi kỹ thuật mở; công khai phần HTML chưa giữ được |
| Chiến lược/store — 20 | A/B/C, B/C chung index, 384d model revision/hash, cosine, filter, persistence/reingest | Không có lỗi kỹ thuật mở; cập nhật không atomic |
| Benchmark/retrieval — 20 | 20 câu, 6 filter, lock trước truy xuất, 60 traces, metrics, lựa chọn trước test và gold đã được người học đối chiếu | Test nhỏ và chỉ một corpus; không tuyên bố tốt nhất tổng quát |
| Năm khía cạnh — 25 | Retrieval, phân tích A–B/B–C, metadata, tài nguyên, ví dụ lỗi; toàn bộ nhãn và lý do đã được người học xác nhận | Audit không độc lập/mù; không tự cấp điểm thay giảng viên |
| Tái lập/báo cáo — 15 | README/code/pins/model/chi phí, báo cáo, tests, 78 checks tái lập và hồ sơ xác nhận human | LMS ngoài phạm vi coding agent |

Không xây UI, chatbot hoặc hybrid. Không dùng benchmark cao để thay thế bằng chứng audit.
