# Day06 — Bài cá nhân Nguyễn Mạnh Tường

**MSSV 2A202603646 — L3A**

Tôi xây pipeline truy xuất tài liệu Python để so sánh ba cách chuẩn bị dữ liệu. Bài dùng model embedding thật chạy local và Qdrant lưu trên đĩa, không cần API key hoặc Docker. Đây là thí nghiệm retrieval; không có chatbot hoặc LLM sinh câu trả lời.

## Kết quả và tình trạng bài

- Corpus: 9 tài liệu Python 3.13 chính thức, **69 đơn vị nội dung HTML** theo quy tắc GUIDE; không phải 69 trang PDF.
- Benchmark khóa trước truy xuất: **15 dev / 5 test**, 6 câu có filter. A fixed 500/50, B theo đoạn tối đa 1.000 ký tự, C dùng nguyên index B và thêm filter từ câu hỏi.
- Dev Hit@1 / Evidence Hit@3: A **9/15 / 10/15**, B **12/15 / 13/15**, C **12/15 / 13/15**.
- Test Hit@1 / Evidence Hit@3: A **2/5 / 4/5**, B **3/5 / 4/5**, C **3/5 / 4/5**. Chọn B bằng dev, không chọn lại theo test.
- **Bản audit chính đã điền đủ 110 nhãn và lý do**, dựa trên nguồn/trace thật. Người chấm hỗ trợ được ghi là Codex (AI); phần tôi đối chiếu thủ công sẽ được xác nhận riêng trước khi chốt gate nộp.

Đọc [báo cáo cá nhân](report/individual/2A202603646_NguyenManhTuong.md), [gate checklist](docs/GATE_CHECKLIST.md), [gói audit](results/audit/README.md), [trace dev](results/traces_dev.jsonl) và [trace test](results/traces_test.jsonl). Điểm exact quote có giới hạn: T04 chứa đủ thông tin chính nhưng thiếu phần cuối quote nên vẫn tính strict miss; không sửa gold sau test để tăng điểm.

## Cấu trúc bài làm

```text
src/                  pipeline Python thực thi của bài cá nhân
scripts/              kiểm tra bài nộp và chạy lại trong thư mục tách biệt
tests/                unit tests và integration test Qdrant với vector thật
data/raw/             snapshot HTML và giấy phép
data/normalized/      text chuẩn hóa, giữ nguồn và code indentation
data/manifest.json    nguồn, quyền, phiên bản, hash, page IDs/offsets
data/pages.jsonl      69 đơn vị nguồn hợp lệ
benchmark/            questions, model revision, protocol và lock
artifacts/            experiment_log.csv
results/              chunk, metrics, trace, audit, log và kiểm tra tái lập
report/individual/    báo cáo 2A202603646_NguyenManhTuong.md
.local/               model, vector cache và Qdrant trên máy; Git bỏ qua
```

`starter/` là khung pgvector tùy chọn của đề, giữ nguyên để tham khảo. Code tôi sử dụng nằm tại **`src/` ở gốc repo**. Không chạy `starter/src/run.py` để đánh giá bài này.

## Cài đặt

Đã kiểm tra với Python 3.11.9 trên Windows. Lần đầu cần mạng để cài dependencies và tải model ONNX khoảng 67 MB. Dữ liệu đã có snapshot trong repo; không phải tải lại website để xem hoặc tái lập kết quả.

PowerShell, từ thư mục gốc repository:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

macOS/Linux: dùng `python3 -m venv .venv`, sau đó thay `.\.venv\Scripts\python.exe` bằng `.venv/bin/python`. Môi trường khác nền tảng có thể cần cài `requirements.txt` thay lock Windows; khi đó ghi phiên bản thực tế và không coi thời gian đo là tương đương.

Không cần `.env`, key model, key tìm kiếm hay tài khoản vector DB. Model BGE được tải theo revision và hash trong [model.json](benchmark/model.json). Qdrant local dùng `.local/qdrant`, cosine exact search, không phải chỉ lưu RAM và không phải SQLite tự viết.

## Kiểm tra bài đã lưu

```powershell
.\.venv\Scripts\python.exe -m src.pipeline verify
.\.venv\Scripts\python.exe scripts/check_submission.py
```

Hai lệnh kiểm tra input/hash, cấu trúc, trace và bảng đo; không gọi lại embedding/benchmark. Gate audit chỉ đạt sau khi có nhãn human hợp lệ. Chỉ đọc báo cáo và trace thì không cần cài model.

## Tái lập đầy đủ, giữ nguyên bằng chứng đã nộp

```powershell
.\.venv\Scripts\python.exe scripts/reproduce.py
```

Script tạo workspace mới dưới `.local/reproduce/`, chép snapshot và benchmark đã khóa, dùng model cache nếu có rồi chạy **index → check-store → dev → test → audit → verify → unit tests**. Kết quả mới được so với chỉ số và top-3 đã lưu; không ghi đè trace gốc. Có thể tốn vài phút CPU. Latency và lựa chọn tie-break theo thời gian có thể dao động, nên script báo riêng lựa chọn, không giấu khác biệt.

Các stage dùng trong lần chạy gốc, theo đúng thứ tự:

```powershell
python -m src.pipeline ingest
python -m src.pipeline freeze
python -m src.pipeline index
python -m src.pipeline check-store
python -m unittest discover -s tests -v
python -m src.pipeline dev
python -m src.pipeline test
python -m src.pipeline audit
python -m src.pipeline verify
python -m src.pipeline report
```

Danh sách trên giải thích pipeline, **không chạy lại nguyên xi trên kết quả gốc đã có**: `ingest` thay manifest/thời điểm tải làm đổi hash; index/dev/test chủ động từ chối ghi đè bằng chứng. Dùng `scripts/reproduce.py` để chạy lại từ snapshot đã khóa. Nếu thu thập corpus mới, tạo thí nghiệm mới và lock mới trước dev/test; không sửa âm thầm benchmark hiện tại.

Để chỉ kiểm tra DB sau khi đã build: `python -m src.pipeline check-store`. Để chạy unit/integration tests: `python -m unittest discover -s tests -v`; integration test cần vector thật do stage index tạo, không fallback mock khi thiếu.

## Hoàn thành audit trước khi nộp

Mở [REVIEW.md](results/audit/REVIEW.md), đối chiếu nguồn rồi điền các cột `human_label`, `human_reason`, `reviewer`, `reviewed_at` trong [labels.csv](results/audit/labels.csv). Có 30 mẫu coherence, 45 metadata, 15 grounding và 20 gold. Sau khi đọc và điền thật, chạy lại `audit`, `report`, `verify` và kiểm tra bài nộp. Các cột xác nhận hiện tại được giữ lại khi tạo lại gói audit.

Tôi cần tự hiểu và giải thích bài; Codex hỗ trợ viết code, chuẩn bị benchmark và phân tích. Chưa có tuyên bố tôi đã chấm tay, trình bày với coach hoặc nộp LMS. Thông tin nguồn/giấy phép xem [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

## Nội dung đề bài gốc

# Day 06 · Data Ingestion Engineering

**Lab cá nhân** · **4 giờ** · **Dữ liệu tự chọn**

Biến tài liệu thành kho tri thức có thể truy xuất cho AI agent, rồi đo xem cách chuẩn bị dữ liệu nào hiệu quả nhất.

| 📄 Dữ liệu | 🧩 Chiến lược | 🎯 Benchmark |
|---|---|---|
| Tối thiểu **30 trang nội dung** | Tối thiểu **3 cấu hình** | Tối thiểu **20 câu hỏi** |

## Bắt đầu nhanh

Dùng [starter PostgreSQL + pgvector](starter/README.md) để dựng database và hoàn thiện các hàm TODO, hoặc tự chọn vector store tương đương. Starter chỉ là khung: **bạn tự hiện thực pipeline và benchmark**.

## 1. Xây pipeline

![Đọc tài liệu, chuẩn hóa, chia chunk, tạo vector, lưu và kiểm tra](assets/ingestion-pipeline.svg)

Chọn tài liệu được phép sử dụng; giữ **ID tài liệu, nguồn, trang/vị trí** và metadata phù hợp. Dùng embedding model thật qua API hoặc chạy local; lưu và truy xuất bằng pgvector, Qdrant, Chroma hoặc một store tương đương.

## 2. So sánh và đánh giá

![Ba chiến lược được đánh giá trên cùng corpus và benchmark dev/test](assets/benchmark-workflow.svg)

Dùng cùng dữ liệu, model và câu hỏi cho cả ba cấu hình. Tách **15 câu dev / 5 câu test** trước khi chạy; chọn cấu hình trên dev, rồi đánh giá test sau khi cố định. Mỗi câu hỏi cần có đoạn bằng chứng và trang nguồn; thiết kế bộ câu hỏi và đánh giá theo [BENCHMARK.md](BENCHMARK.md).

Đánh giá theo năm khía cạnh: **độ chính xác truy xuất**, **tính mạch lạc của chunk**, **tính hữu dụng của metadata**, **chất lượng grounding** và **tác động của chiến lược dữ liệu**. Giải thích lựa chọn bằng kết quả, ví dụ lỗi và các đánh đổi.

## 3. Chuẩn bị bài nộp

1. Chạy pipeline và lưu cấu hình, kết quả top-3, trace cùng nhãn đánh giá thủ công.
2. Điền [thông tin học viên](STUDENT.md), [nhật ký thí nghiệm](artifacts/experiment_log.csv) và bản sao [mẫu báo cáo cá nhân](report/individual/MSSV_HoTen.md).
3. Kiểm tra mã nguồn, cách chạy, manifest dữ liệu và checklist trong [SUBMISSION.md](SUBMISSION.md).

## Tài liệu hướng dẫn

| Bạn cần tìm | Tài liệu |
|---|---|
| Setup baseline PostgreSQL + pgvector | [starter/README.md](starter/README.md) |
| Các bước làm và cách tính chỉ số | [GUIDE.md](GUIDE.md) |
| Tiến độ trong 4 giờ | [CHECKPOINTS.md](CHECKPOINTS.md) |
| Năm tiêu chí benchmark và bộ câu hỏi | [BENCHMARK.md](BENCHMARK.md) |
| Tiêu chí chấm điểm | [RUBRIC.md](RUBRIC.md) |
| Quy tắc sử dụng dữ liệu, AI và API | [RULES.md](RULES.md) |
| Cách nộp bài | [SUBMISSION.md](SUBMISSION.md) |

[data/format-example.json](data/format-example.json) chỉ minh họa định dạng, không phải corpus đủ điều kiện. Phần xử lý và benchmark do bạn tự hiện thực; không bắt buộc xây chatbot.
