# Báo cáo cá nhân — Day06: Data Ingestion Engineering

**Nguyễn Mạnh Tường — 2A202603646 — L3A**

Ngày thí nghiệm: 13/11/2026. Repo: [bài nộp](https://github.com/manhtuongqt/K5-L3A-DAY06-NguyenManhTuong-2A202603646-DataIngestion).

## 1. Dữ liệu và pipeline

### 1.1. Bài toán và nguồn

Tôi sử dụng tài liệu Python 3.13 để thử việc tìm đúng bằng chứng trong tài liệu kỹ thuật. Bài này chỉ đo retrieval, không tạo câu trả lời bằng LLM và không xây chatbot. Corpus có 9 tài liệu HTML: control flow, data structures, modules, input/output, errors, classes, json, csv và pathlib. Snapshot hiển thị Python 3.13.18. Mỗi URL, thời điểm tải, checksum và danh sách đơn vị được lưu trong [manifest](../../data/manifest.json).

Tài liệu có giấy phép PSF License Version 2; mã ví dụ còn có 0BSD. Tôi giữ snapshot HTML và [giấy phép đầy đủ](../../data/raw/python_license.html), ghi thay đổi trong [THIRD_PARTY_NOTICES](../../THIRD_PARTY_NOTICES.md). Không sử dụng tài liệu cá nhân hoặc dữ liệu cần key truy cập.

Đây không phải 69 trang PDF. Sau khi bỏ điều hướng, tôi chia text theo thứ tự, tại ranh giới đoạn, mục tiêu 3.500 ký tự; gộp phần đuôi ngắn để mỗi đơn vị có ít nhất 1.500 ký tự. Kết quả là **69 đơn vị nội dung**, ngắn nhất 2,435 ký tự. ID dạng `library_json:u001`; manifest ghi offsets và số ký tự. Không nhân bản để tăng số lượng.

### 1.2. Trích xuất, chuẩn hóa và metadata

Pipeline dùng BeautifulSoup đọc vùng `div.body`, giữ heading, đoạn, chữ ký API, code và một số list. Chuẩn hóa NFC, NBSP thành space, LF, bỏ khoảng trắng cuối dòng, tối đa một dòng trống, giữ thụt lề code. Text đã chuẩn hóa ở [data/normalized](../../data/normalized); các đơn vị ở [pages.jsonl](../../data/pages.jsonl). Bộ trích xuất chưa giữ đầy đủ bảng HTML dạng ô thuần, hình và mọi cấu trúc list lồng nhau. Do đó corpus là bản trích xuất có giới hạn, không phải bản sao toàn bộ hướng dẫn Python. Không OCR vì dùng HTML có text. [Log ingestion](../../results/ingestion_log.json) có 9 nguồn thành công, không có đơn vị rỗng; chưa chứng minh việc trích xuất giữ nguyên mọi nội dung có thể thấy trên trang.

Mỗi chunk có `document_id`, `source`, `page`, `start/end` trong đơn vị và `source_start/source_end` trong tài liệu. Các trường lọc `document_type`, `version`, `language` là string. `document_type` lấy từ vị trí `/tutorial/` hoặc `/library/` của URL chính thức, lần lượt là `tutorial` và `library_reference`. `version=3.13` lấy từ URL và tiêu đề, `language=en` theo nội dung. `title` giữ tên chương. Trường `document_type` có ích để giới hạn loại tài liệu theo yêu cầu câu hỏi; nó không phân biệt các hàm hoặc các phiên bản con trong cùng loại.

### 1.3. Model và lưu trữ

- Model thật: `BAAI/bge-small-en-v1.5`, bản ONNX quantized `qdrant/bge-small-en-v1.5-onnx-q`, revision `aa8f8b060edb00e03bfdd08813a2949946c8ba55`; **384 chiều**, FastEmbed 0.7.3, ONNX Runtime 1.31.1, CPU 4 threads. [Model lock](../../benchmark/model.json) có SHA-256 từng tệp.
- Document không thêm prefix; query thêm `Represent this sentence for searching relevant passages: `. CLS pooling, L2 normalization. Query/document cùng model và tokenizer. Giới hạn 512 token; token guard xác nhận A tối đa 275, B/C 479 token, không truncate âm thầm.
- Qdrant client 1.16.0, local persistent tại `.local/qdrant`, collection `day06_A`, `day06_B`. C dùng đúng collection B. Metric cosine, exact search, top-3, không reranker/hybrid.
- ID xác định từ strategy/page/offset/text. Nạp snapshot bằng upsert và xóa ID cũ qua API Qdrant; không tự quản SQLite. Đóng/mở lại trả cùng top-3; nạp lặp giữ A=585 và B=312 điểm. Test thay 2 điểm bằng 1 điểm đã xóa được điểm cũ. [Bằng chứng store](../../results/store_checks.json). Cập nhật chưa atomic; nếu lỗi giữa chừng phải nạp lại snapshot, không phù hợp phục vụ production đồng thời.
- Python 3.11.9; toàn bộ phiên bản ở [requirements-lock](../../requirements-lock.txt), [runtime](../../results/runtime.json). Không gọi API model, không có token tính phí: **0 USD phí API**. Chưa tính điện, khấu hao máy, mạng hay công tải model. Số token trong bảng là đầu vào embedding local, không phải token hóa đơn.

## 2. Cấu hình và benchmark

| Strategy | Chunking | Metadata/truy xuất |
|---|---|---|
| A | 500 ký tự, overlap 50; không cố giữ đoạn | Cùng metadata, không filter |
| B | Ghép các đoạn đến tối đa 1.000 ký tự; khối dài phải cắt ở khoảng trắng | Cùng metadata, không filter |
| C | Giống hệt B; không tạo thêm vector/index | Chỉ thêm filter `document_type` khi câu hỏi đã nêu phạm vi |

A–B đổi cách chunk. B–C chỉ đổi filter; query vector, tập chunk, model và cosine giữ nguyên. C chạy không filter cho câu không yêu cầu phạm vi. Không dùng gold document/page hay đáp án để lọc.

[20 câu hỏi](../../benchmark/questions.json) được viết trước khi truy xuất: D01–D15 là dev từ tutorial, T01–T05 là test từ json/csv/pathlib. Nguồn gold test không trùng tài liệu gold dev, nhưng tất cả cùng thuộc corpus Python; chưa phải kiểm định trên lĩnh vực mới. Có 6 câu filter: D02/D06/D12 và T01/T02/T05. Ngữ cảnh tutorial/library reference được viết ngay trong câu hỏi. Gold có đáp án, nguồn/page, quote, offsets và danh sách alternative chứa đúng quote. Code đã kiểm tra toàn bộ quote có trong snapshot, nhưng **ngữ nghĩa và các cách chứng minh tương đương vẫn cần người học duyệt**.

[Protocol](../../benchmark/protocol.json) khóa tiêu chí: ưu tiên dev Evidence Hit@3, rồi Hit@1, rồi latency tìm kiếm trung bình, cuối cùng thứ tự strategy. Mẫu coherence cố định: 10 page ID đầu sau sắp xếp, offset 200, chọn chunk chứa offset xuất hiện sớm nhất nếu có overlap. Metadata và grounding dùng đủ 5 câu test của từng strategy. [lock.json](../../benchmark/lock.json) giữ hash corpus/manifest/model/questions/protocol.

Trước mọi retrieval đã có hai lỗi triển khai: B/C ban đầu 1.200 ký tự vượt 512 token, và cách xóa/tạo lại collection local để sót dữ liệu trên Windows. Sửa B/C cùng về 1.000 ký tự và reconciliation bằng API Qdrant; lưu lock/protocol cũ, log lỗi và kiểm tra. Xem [nhật ký sửa](../../results/implementation_log.md). Không sửa tham số dựa trên test, không chọn lần chạy có điểm cao nhất.

Dev chạy xong lúc `2026-11-13T10:35:00.292241+00:00`; lựa chọn **B** được lưu lúc `2026-11-13T10:35:00.334123+00:00` trước test hoàn thành lúc `2026-11-13T10:35:46.432977+00:00` (timestamps UTC). B/C cùng điểm dev, B thắng tie-break latency trong lần đo này. Tôi giữ nguyên cấu hình sau khi đọc dev và không coi vài ms khác biệt là bằng chứng tốc độ ổn định. [Phân tích dev trước test](../../results/dev_analysis.md).

## 3. Kết quả theo năm khía cạnh

### 3.1. Retrieval accuracy

Hit bắt buộc một chunk đúng gold source/page và chứa **toàn bộ quote đã khóa**. Không ghép nhiều chunk để nâng điểm. Đây là phép kiểm tra exact evidence tự động, có thể bảo thủ với diễn đạt/bằng chứng tương đương; không phải accuracy câu trả lời LLM.

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Search trung bình/câu | Phí API |
|---|---|---|---|---|---|---|
| A | dev | 9/15 (60.0%) | 10/15 (66.7%) | 585 | 2.278 ms | 0 USD API |
| A | test | 2/5 (40.0%) | 4/5 (80.0%) | 585 | 1.783 ms | 0 USD API |
| B | dev | 12/15 (80.0%) | 13/15 (86.7%) | 312 | 1.827 ms | 0 USD API |
| B | test | 3/5 (60.0%) | 4/5 (80.0%) | 312 | 1.245 ms | 0 USD API |
| C | dev | 12/15 (80.0%) | 13/15 (86.7%) | 312 | 2.942 ms | 0 USD API |
| C | test | 3/5 (60.0%) | 4/5 (80.0%) | 312 | 3.605 ms | 0 USD API |

Trace đầy đủ: [dev](../../results/traces_dev.jsonl), [test](../../results/traces_test.jsonl), gồm text, chunk ID, score, metadata, query/filter thực tế và gold. [Metrics dev](../../results/metrics_dev.json), [metrics test](../../results/metrics_test.json). Query embedding được dùng chung giữa A/B/C; không nằm trong cột search: dev 0.154s / 15 query, test 0.053s / 5 query.

### 3.2–3.4. Coherence, metadata và grounding

Bản audit chính đã có đủ **110 nhãn và lý do theo từng mẫu**, do Codex đọc source/trace và hỗ trợ điền để tôi đối chiếu sau. Nhãn này có người chấm ghi rõ `Codex (AI)`, không giả thành nhãn thủ công của tôi. [Bảng chính](../../results/audit/labels.csv), [nhận xét nội dung](../../results/audit/content_review.json) và [tổng hợp nhãn hỗ trợ](../../results/audit/assistant_summary.json).

| Strategy | Coherence do Codex chấm /2 | Metadata đủ/đúng do Codex đối chiếu | Grounding do Codex chấm: số mức 0/1/2; trung bình |
|---|---|---|---|
| A | 1.00/2 (n=10) | 15/15 | 0/0/5; 2.00/2 (n=5) |
| B | 1.30/2 (n=10) | 15/15 | 0/0/5; 2.00/2 (n=5) |
| C | 1.30/2 (n=10) | 15/15 | 0/0/5; 2.00/2 (n=5) |

Trạng thái xác nhận của người học được giữ riêng:

| Strategy | Coherence thủ công /2 | Metadata thủ công; kiểm tra tự động | Filter compliance trên 3 câu test có filter | Grounding thủ công /2 |
|---|---|---|---|---|
| A | Chờ (0/10 đã xác nhận) | Chờ (0/15 đã xác nhận); tự động 15/15 | 1/3 (33.3%) | Chờ (0/5 đã xác nhận) |
| B | Chờ (0/10 đã xác nhận) | Chờ (0/15 đã xác nhận); tự động 15/15 | 2/3 (66.7%) | Chờ (0/5 đã xác nhận) |
| C | Chờ (0/10 đã xác nhận) | Chờ (0/15 đã xác nhận); tự động 15/15 | 3/3 (100.0%) | Chờ (0/5 đã xác nhận) |

Đây là **trạng thái chờ xác nhận**, không phải điểm 0. Bản chính đã điền 30 coherence, 45 metadata, 15 grounding và 20 gold. Gói [REVIEW](../../results/audit/REVIEW.md) ghép nguồn/chunk để đối chiếu; [hướng dẫn](../../results/audit/README.md) nêu cách sửa và xác nhận. Không ghi người học đã chấm khi chưa có cột xác nhận.

Coherence dùng thang 0=bị cắt mất ý/chủ thể, 1=hiểu được phần nào nhưng thiếu ngữ cảnh, 2=tự hiểu được và đủ ý. Nhãn Codex đã xét nội dung đầy đủ của 20 chunk A/B khác nhau; C dùng đúng 10 chunk B. A có nhiều phần bị cắt giữa câu/code; B giữ đoạn tốt hơn nhưng vẫn có heading hoặc chữ ký API thiếu phần giải thích, nên không mặc định cho B điểm 2. Mẫu 10 anchor đầu theo thứ tự ID tập trung vào csv/json, chưa đại diện mọi chương. Trung bình hỗ trợ A=1,00; B/C=1,30, chưa phải điểm thủ công đã được người học xác nhận.

Metadata được code kiểm tra cả giá trị nguồn/type/version và text/offset so với trang chuẩn. Mỗi strategy có 15/15 bản ghi top-3 test đúng theo phép đối chiếu đó; vẫn cần kiểm tra tay với HTML gốc. Filter compliance tính theo **câu hỏi**: top-3 của câu phải đều đúng phạm vi; A/B không bật filter nên có thể lệch phạm vi dù metadata bản ghi vẫn chính xác. C đạt 3/3; B đạt 2/3; A đạt 1/3. Với tập không có câu filter phải ghi N/A, không mặc định 100%.

Grounding đã được Codex đọc đủ 5 test mỗi strategy và ghi lý do riêng. Cả 5 câu của mỗi cấu hình được đề xuất mức 2, trung bình 2,00/2: T01/T02/T03/T05 có evidence đúng nguồn trong top-3; T04 có đủ hai ý None thành chuỗi rỗng và không đảo ngược, dù thiếu đuôi quote. Không chấm theo top-1 riêng và không xem strict miss là grounding=0 tự động. [Nhận xét T04](../../results/audit/ai_review.json) ghi rõ ngoại lệ này. Người học chưa xác nhận nhãn, nên các số trên chỉ là đánh giá hỗ trợ, không thay nhãn thủ công bắt buộc. Điểm strict hiện tại giữ nguyên.

### 3.5. Tác động dữ liệu, tài nguyên và đánh đổi

| Strategy | Số chunk | Độ dài median / p95 / max (ký tự) | Token embedding local | Thời gian embedding | Ingest đo lại sau sửa store |
|---|---|---|---|---|---|
| A | 585 | 500.0 / 500.0 / 500 | 77,315 | 57.416 s | 3.765 s |
| B | 312 | 875.5 / 992.0 / 1000 | 69,268 | 59.968 s | 1.998 s |
| C | 312 (dùng chung B) | như B | 0 bổ sung | 0 bổ sung | 0 bổ sung |

B dùng ít hơn A 273 vector (46.7%), nhưng chunk dài hơn nên thời gian embedding không giảm tương ứng. Đây là một lần đo trên máy local; batch/padding, độ dài và trạng thái máy ảnh hưởng kết quả. Model load 0.675s; thời gian tải model/cài môi trường và lần chạy lỗi trước đó không nằm trong bảng. Không suy ra tổng chi phí học bài chỉ từ thời gian thành công.

Trên dev, A→B tăng Hit@3 từ 10/15 lên 13/15 và Hit@1 từ 9/15 lên 12/15. Trên test, Hit@3 vẫn 4/5, Hit@1 tăng từ 2/5 lên 3/5. B giữ tốt điều kiện ở D03/D13 nhưng làm mất tính tập trung ở D01. Vì vậy không kết luận chunk lớn luôn tốt.

B→C không tăng strict retrieval trong bộ này; tác dụng quan sát là tuân thủ phạm vi: test 2/3→3/3. C thêm chi phí filter/search, không thêm embedding. Filter đúng loại tài liệu vẫn không giải quyết nhầm phương thức hoặc cắt thiếu câu. Nếu người dùng cung cấp sai scope, C có thể loại mất đáp án. Không suy ra C luôn vượt B chỉ vì filter compliance cao.

## 4. Ví dụ sai và giới hạn

1. **D03/A**, gold `tutorial_datastructures:u004`: điều kiện tuple làm dictionary key và ngoại lệ mutable bị chia qua các chunk. Top-1 đúng trang nhưng bắt đầu giữa chữ; một chunk khác có đầu câu nhưng thiếu cuối. Không đủ quote trong một chunk nên Hit@3=0, trong khi B/C hit. Đây là vấn đề ranh giới chunk.
2. **D01/B và C**, gold `tutorial_datastructures:u001`: hỏi lỗi của `list.remove` nhưng top-1 chứa mô tả `pop`/`index`, top-2 về `del`, top-3 về dictionary. Không lấy ValueError của `index` làm bằng chứng cho `remove`. A tìm được gold trong top-3. Đây là đánh đổi giữa ngữ cảnh và độ tập trung.
3. **D09/A/B/C**, gold `tutorial_modules:u002`: truy xuất nghiêng về module khi import, thiếu đoạn khi chạy script gán `__name__='__main__'`. Không phải thiếu dữ liệu nguồn; xếp hạng chưa phân biệt tốt tình huống.
4. **T04/A/B/C**, gold `library_csv:u001`: strict hit=0 vì thiếu phần cuối quote về `cursor.fetch*`; tuy nhiên A top-2, B/C top-3 đều nói None thành chuỗi rỗng và việc chuyển đổi không đảo ngược. Đây là hạn chế của gold quote/check exact, không đủ cơ sở gọi toàn bộ retrieval là không có bằng chứng. Chờ xác nhận ngữ nghĩa; không sửa quote sau khi xem test để làm đẹp điểm.

Giới hạn chính: 5 test rất nhỏ (một câu tương đương 20 điểm phần trăm), câu hỏi/gold do AI hỗ trợ soạn, chưa có audit thủ công, chỉ tiếng Anh và một lĩnh vực, HTML trích xuất không giữ đủ bảng/hình, exact quote có thể phạt bằng chứng đủ nhưng khác ranh giới. Model nhỏ và chunking theo ký tự có thể chưa phù hợp tài liệu tiếng Việt hoặc bảng phức tạp. Không chạy LLM sinh câu trả lời, không đo answer accuracy hay độ ổn định qua nhiều seed/model. Chưa chứng minh kết quả tổng quát ngoài corpus này.

## 5. Lựa chọn, tái lập và vai trò AI

Lựa chọn giữ nguyên là **B theo dev**, không đổi sang cấu hình khác vì test. Với nhu cầu bắt buộc scope, C có ích để tuân thủ phạm vi, nhưng cần input scope đáng tin và không có bằng chứng nó tăng Hit@3 trong thí nghiệm hiện tại. Nếu mở rộng, tôi sẽ cải thiện gold bằng các đoạn hỗ trợ tối thiểu, xử lý chữ ký/heading và bảng tốt hơn, thêm câu khó và corpus tiếng Việt; mọi tinh chỉnh từ test hiện tại phải dùng holdout mới cho lần đánh giá sau.

Lệnh setup và tái lập ở [README](../../README.md). Code chạy thật nằm trong `src/` tại root, không phải các TODO của starter pgvector tùy chọn. [Nhật ký A/B/C](../../artifacts/experiment_log.csv), [gate checklist](../../docs/GATE_CHECKLIST.md), [unit/integration log](../../results/tests.txt) và [kiểm tra tự động](../../results/verification.json) là bằng chứng kỹ thuật.

Đã chạy lại pipeline trong workspace mới: 78 phép so sánh đều khớp=True; độ lệch score lớn nhất 0.0. Lựa chọn dev gốc B, lần tái lập B. Đây là kiểm tra tái lập sau khi đã biết test, không phải holdout độc lập mới; không dùng để chỉnh hoặc chọn số liệu thay kết quả gốc. [Kết quả tái lập](../../results/reproduction.json), [console](../../results/reproduction_console.txt).

Codex hỗ trợ viết pipeline, soạn câu hỏi/gold, đọc log, tính chỉ số và chuẩn bị bản thảo phân tích. Kiểm tra bằng unit/integration tests, hash input, source/offset checks, token guard và Qdrant persistence/filter/reingest checks. Các đề xuất AI có nhãn riêng; phần người học cần xác nhận chưa được giả làm kết quả đã làm thủ công. Tôi cần đọc nguồn, xác nhận nhãn và tự giải thích bài trước khi nộp. Chưa nộp LMS; việc nộp do tôi thực hiện.
