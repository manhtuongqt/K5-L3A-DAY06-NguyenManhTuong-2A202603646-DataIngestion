"""Render actual measured outputs; leave unconfirmed human metrics unavailable."""
from __future__ import annotations
import csv
from .common import ROOT, read_json, read_jsonl, write_json, now
from .audit import metadata_correct


def fraction(v):
    return f"{v['n']}/{v['N']} ({100*v['n']/v['N']:.1f}%)" if v else "N/A"


def human_summary(rows, kind, strategy):
    required = [r for r in rows if r["kind"]==kind and r["strategy"]==strategy]
    complete = [r for r in required if r["human_label"] != "" and all(r[k] for k in ("human_reason","reviewer","reviewed_at"))]
    if len(complete) != len(required):
        return f"Chờ ({len(complete)}/{len(required)} đã xác nhận)"
    labels = [int(r["human_label"]) for r in complete]
    if kind == "metadata":
        return f"{sum(labels)}/{len(labels)}"
    distribution = "/".join(str(labels.count(i)) for i in (0,1,2))
    return f"{sum(labels)/len(labels):.2f}/2 (n={len(labels)}; mức 0/1/2: {distribution})"


def build():
    manifest = read_json("data/manifest.json")
    stats = read_json("results/chunk_stats.json")
    runtime = read_json("results/runtime.json")
    index = read_json("results/index.json")
    store_checks = read_json("results/store_checks.json")
    selection = read_json("results/selection.json")
    dev = read_json("results/metrics_dev.json")
    test = read_json("results/metrics_test.json")
    questions = read_json("benchmark/questions.json")
    pages = {p["page"]:p for p in read_jsonl("data/pages.jsonl")}
    with (ROOT/"results/audit/labels.csv").open(encoding="utf-8",newline="") as file:
        rows = list(csv.DictReader(file))
    audit_state = read_json("results/audit/status.json")
    confirmed = all(g["pending"] == 0 for g in audit_state["groups"].values())
    approval_text = "Tôi đã đối chiếu toàn bộ 110 nhãn cùng lý do và xác nhận chấp nhận ngày 13/11/2026. Bản chấm được Codex hỗ trợ chuẩn bị trước khi tôi kiểm tra; đây không phải hai lượt chấm độc lập hoặc chấm mù. Xác nhận được ghi tại [human_confirmation.json](../../results/audit/human_confirmation.json), gắn với từng dòng đã duyệt bằng hash." if confirmed else "Bản chấm hỗ trợ đã điền đủ; nhãn thủ công của người học đang chờ xác nhận."
    gold_approval = "Tôi đã đối chiếu và chấp nhận toàn bộ gold/evidence hiện có; hồ sơ xác nhận ở results/audit/human_confirmation.json." if confirmed else "Ngữ nghĩa gold và các cách chứng minh tương đương cần người học duyệt."
    review_limit = "Tác giả đã kiểm tra và chấp nhận nhãn hỗ trợ, nhưng vẫn có nguy cơ thiên lệch vì không chấm độc lập/mù." if confirmed else "Chưa có audit thủ công được người học xác nhận."
    replay_note = "Chưa chạy kiểm tra tái lập toàn bộ."
    if (ROOT/"results/reproduction.json").exists():
        replay=read_json("results/reproduction.json")
        replay_note = f"Đã chạy lại pipeline trong workspace mới: {replay['comparison_checks']} phép so sánh đều khớp={replay['passed']}; độ lệch score lớn nhất {replay['max_score_absolute_difference']}. Lựa chọn dev gốc {replay['original_selected_strategy']}, lần tái lập {replay['replay_selected_strategy']}. Đây là kiểm tra tái lập sau khi đã biết test, không phải holdout độc lập mới; không dùng để chỉnh hoặc chọn số liệu thay kết quả gốc. [Kết quả tái lập](../../results/reproduction.json), [console](../../results/reproduction_console.txt)."
    metrics_rows, audit_rows, resources, assistant_rows = [],[],[],[]
    assistant=read_json("results/audit/assistant_summary.json")["strategies"]
    traces = read_jsonl("results/traces_test.jsonl")
    for strategy in ("A","B","C"):
        for split,result in (("dev",dev),("test",test)):
            m = result["strategies"][strategy]
            metrics_rows.append(f"| {strategy} | {split} | {fraction(m['hit_at_1'])} | {fraction(m['evidence_hit_at_3'])} | {stats[strategy]['chunk_count']} | {m['mean_search_ms']:.3f} ms | 0 USD API |")
        metadata = [h for t in traces if t["strategy"]==strategy for h in t["hits"]]
        correct = sum(metadata_correct(h,pages) for h in metadata)
        audit_rows.append(f"| {strategy} | {human_summary(rows,'coherence',strategy)} | {human_summary(rows,'metadata',strategy)}; tự động {correct}/{len(metadata)} | {fraction(test['strategies'][strategy]['filter_compliance'])} | {human_summary(rows,'grounding',strategy)} |")
        a=assistant[strategy]
        distribution='/'.join(str(a['grounding']['counts'][str(k)]) for k in (0,1,2))
        assistant_rows.append(f"| {strategy} | {a['coherence']['mean']:.2f}/2 (n=10) | {a['metadata']['counts']['1']}/15 | {distribution}; {a['grounding']['mean']:.2f}/2 (n=5) |")
        if strategy != "C":
            r=index["strategies"][strategy]
            resources.append(f"| {strategy} | {stats[strategy]['chunk_count']} | {stats[strategy]['median_chars']:.1f} / {stats[strategy]['p95_chars']:.1f} / {stats[strategy]['max_chars']} | {r['total_model_tokens']:,} | {r['embedding_seconds']:.3f} s | {store_checks[strategy]['validated_store_ingest_seconds']:.3f} s |")
        else:
            resources.append(f"| C | {stats[strategy]['chunk_count']} (dùng chung B) | như B | 0 bổ sung | 0 bổ sung | 0 bổ sung |")
    content = f'''# Báo cáo cá nhân — Day06: Data Ingestion Engineering

**Nguyễn Mạnh Tường — 2A202603646 — L3A**

Ngày thí nghiệm: 13/11/2026. Repo: [bài nộp](https://github.com/manhtuongqt/K5-L3A-DAY06-NguyenManhTuong-2A202603646-DataIngestion).

## 1. Dữ liệu và pipeline

### 1.1. Bài toán và nguồn

Tôi sử dụng tài liệu Python 3.13 để thử việc tìm đúng bằng chứng trong tài liệu kỹ thuật. Bài này chỉ đo retrieval, không tạo câu trả lời bằng LLM và không xây chatbot. Corpus có {len(manifest['sources'])} tài liệu HTML: control flow, data structures, modules, input/output, errors, classes, json, csv và pathlib. Snapshot hiển thị Python 3.13.18. Mỗi URL, thời điểm tải, checksum và danh sách đơn vị được lưu trong [manifest](../../data/manifest.json).

Tài liệu có giấy phép PSF License Version 2; mã ví dụ còn có 0BSD. Tôi giữ snapshot HTML và [giấy phép đầy đủ](../../data/raw/python_license.html), ghi thay đổi trong [THIRD_PARTY_NOTICES](../../THIRD_PARTY_NOTICES.md). Không sử dụng tài liệu cá nhân hoặc dữ liệu cần key truy cập.

Đây không phải 69 trang PDF. Sau khi bỏ điều hướng, tôi chia text theo thứ tự, tại ranh giới đoạn, mục tiêu 3.500 ký tự; gộp phần đuôi ngắn để mỗi đơn vị có ít nhất 1.500 ký tự. Kết quả là **{manifest['total_content_units']} đơn vị nội dung**, ngắn nhất {min(len(p['text']) for p in pages.values()):,} ký tự. ID dạng `library_json:u001`; manifest ghi offsets và số ký tự. Không nhân bản để tăng số lượng.

### 1.2. Trích xuất, chuẩn hóa và metadata

Pipeline dùng BeautifulSoup đọc vùng `div.body`, giữ heading, đoạn, chữ ký API, code và một số list. Chuẩn hóa NFC, NBSP thành space, LF, bỏ khoảng trắng cuối dòng, tối đa một dòng trống, giữ thụt lề code. Text đã chuẩn hóa ở [data/normalized](../../data/normalized); các đơn vị ở [pages.jsonl](../../data/pages.jsonl). Bộ trích xuất chưa giữ đầy đủ bảng HTML dạng ô thuần, hình và mọi cấu trúc list lồng nhau. Do đó corpus là bản trích xuất có giới hạn, không phải bản sao toàn bộ hướng dẫn Python. Không OCR vì dùng HTML có text. [Log ingestion](../../results/ingestion_log.json) có 9 nguồn thành công, không có đơn vị rỗng; chưa chứng minh việc trích xuất giữ nguyên mọi nội dung có thể thấy trên trang.

Mỗi chunk có `document_id`, `source`, `page`, `start/end` trong đơn vị và `source_start/source_end` trong tài liệu. Các trường lọc `document_type`, `version`, `language` là string. `document_type` lấy từ vị trí `/tutorial/` hoặc `/library/` của URL chính thức, lần lượt là `tutorial` và `library_reference`. `version=3.13` lấy từ URL và tiêu đề, `language=en` theo nội dung. `title` giữ tên chương. Trường `document_type` có ích để giới hạn loại tài liệu theo yêu cầu câu hỏi; nó không phân biệt các hàm hoặc các phiên bản con trong cùng loại.

### 1.3. Model và lưu trữ

- Model thật: `{runtime['model']['model']}`, bản ONNX quantized `{runtime['model']['onnx_repository']}`, revision `{runtime['model']['revision']}`; **384 chiều**, FastEmbed {runtime['packages']['fastembed']}, ONNX Runtime {runtime['packages']['onnxruntime']}, CPU 4 threads. [Model lock](../../benchmark/model.json) có SHA-256 từng tệp.
- Document không thêm prefix; query thêm `Represent this sentence for searching relevant passages: `. CLS pooling, L2 normalization. Query/document cùng model và tokenizer. Giới hạn 512 token; token guard xác nhận A tối đa {index['strategies']['A']['max_model_tokens']}, B/C {index['strategies']['B']['max_model_tokens']} token, không truncate âm thầm.
- Qdrant client {runtime['packages']['qdrant-client']}, local persistent tại `.local/qdrant`, collection `day06_A`, `day06_B`. C dùng đúng collection B. Metric cosine, exact search, top-3, không reranker/hybrid.
- ID xác định từ strategy/page/offset/text. Nạp snapshot bằng upsert và xóa ID cũ qua API Qdrant; không tự quản SQLite. Đóng/mở lại trả cùng top-3; nạp lặp giữ A=585 và B=312 điểm. Test thay 2 điểm bằng 1 điểm đã xóa được điểm cũ. [Bằng chứng store](../../results/store_checks.json). Cập nhật chưa atomic; nếu lỗi giữa chừng phải nạp lại snapshot, không phù hợp phục vụ production đồng thời.
- Python {runtime['python']}; toàn bộ phiên bản ở [requirements-lock](../../requirements-lock.txt), [runtime](../../results/runtime.json). Không gọi API model, không có token tính phí: **0 USD phí API**. Chưa tính điện, khấu hao máy, mạng hay công tải model. Số token trong bảng là đầu vào embedding local, không phải token hóa đơn.

## 2. Cấu hình và benchmark

| Strategy | Chunking | Metadata/truy xuất |
|---|---|---|
| A | 500 ký tự, overlap 50; không cố giữ đoạn | Cùng metadata, không filter |
| B | Ghép các đoạn đến tối đa 1.000 ký tự; khối dài phải cắt ở khoảng trắng | Cùng metadata, không filter |
| C | Giống hệt B; không tạo thêm vector/index | Chỉ thêm filter `document_type` khi câu hỏi đã nêu phạm vi |

A–B đổi cách chunk. B–C chỉ đổi filter; query vector, tập chunk, model và cosine giữ nguyên. C chạy không filter cho câu không yêu cầu phạm vi. Không dùng gold document/page hay đáp án để lọc.

[20 câu hỏi](../../benchmark/questions.json) được viết trước khi truy xuất: D01–D15 là dev từ tutorial, T01–T05 là test từ json/csv/pathlib. Nguồn gold test không trùng tài liệu gold dev, nhưng tất cả cùng thuộc corpus Python; chưa phải kiểm định trên lĩnh vực mới. Có 6 câu filter: D02/D06/D12 và T01/T02/T05. Ngữ cảnh tutorial/library reference được viết ngay trong câu hỏi. Gold có đáp án, nguồn/page, quote, offsets và danh sách alternative chứa đúng quote. Code đã kiểm tra toàn bộ quote có trong snapshot. {gold_approval}

[Protocol](../../benchmark/protocol.json) khóa tiêu chí: ưu tiên dev Evidence Hit@3, rồi Hit@1, rồi latency tìm kiếm trung bình, cuối cùng thứ tự strategy. Mẫu coherence cố định: 10 page ID đầu sau sắp xếp, offset 200, chọn chunk chứa offset xuất hiện sớm nhất nếu có overlap. Metadata và grounding dùng đủ 5 câu test của từng strategy. [lock.json](../../benchmark/lock.json) giữ hash corpus/manifest/model/questions/protocol.

Trước mọi retrieval đã có hai lỗi triển khai: B/C ban đầu 1.200 ký tự vượt 512 token, và cách xóa/tạo lại collection local để sót dữ liệu trên Windows. Sửa B/C cùng về 1.000 ký tự và reconciliation bằng API Qdrant; lưu lock/protocol cũ, log lỗi và kiểm tra. Xem [nhật ký sửa](../../results/implementation_log.md). Không sửa tham số dựa trên test, không chọn lần chạy có điểm cao nhất.

Dev chạy xong lúc `{dev['completed_at']}`; lựa chọn **{selection['selected_strategy']}** được lưu lúc `{selection['selected_at']}` trước test hoàn thành lúc `{test['completed_at']}` (timestamps UTC). B/C cùng điểm dev, B thắng tie-break latency trong lần đo này. Tôi giữ nguyên cấu hình sau khi đọc dev và không coi vài ms khác biệt là bằng chứng tốc độ ổn định. [Phân tích dev trước test](../../results/dev_analysis.md).

## 3. Kết quả theo năm khía cạnh

### 3.1. Retrieval accuracy

Hit bắt buộc một chunk đúng gold source/page và chứa **toàn bộ quote đã khóa**. Không ghép nhiều chunk để nâng điểm. Đây là phép kiểm tra exact evidence tự động, có thể bảo thủ với diễn đạt/bằng chứng tương đương; không phải accuracy câu trả lời LLM.

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Search trung bình/câu | Phí API |
|---|---|---|---|---|---|---|
{chr(10).join(metrics_rows)}

Trace đầy đủ: [dev](../../results/traces_dev.jsonl), [test](../../results/traces_test.jsonl), gồm text, chunk ID, score, metadata, query/filter thực tế và gold. [Metrics dev](../../results/metrics_dev.json), [metrics test](../../results/metrics_test.json). Query embedding được dùng chung giữa A/B/C; không nằm trong cột search: dev {dev['shared_query_embedding_seconds']:.3f}s / 15 query, test {test['shared_query_embedding_seconds']:.3f}s / 5 query.

### 3.2–3.4. Coherence, metadata và grounding

{approval_text}

[Bảng audit chính](../../results/audit/labels.csv) ghi người kiểm tra ở `reviewer`, nhãn/lý do đã xác nhận ở `human_label`/`human_reason`. [Nhận xét nội dung ban đầu](../../results/audit/content_review.json) được giữ để truy vết hỗ trợ.

| Strategy | Coherence thủ công /2 | Metadata thủ công; kiểm tra tự động | Filter compliance trên 3 câu test có filter | Grounding thủ công /2 |
|---|---|---|---|---|
{chr(10).join(audit_rows)}

Phạm vi gồm 30 coherence, 45 metadata, 15 grounding và 20 gold. Gói [REVIEW](../../results/audit/REVIEW.md) ghép nguồn/chunk để đối chiếu; [trạng thái audit](../../results/audit/status.json) ghi số mẫu đã xác nhận. Khi nhãn/lý do của một dòng thay đổi, xác nhận cũ không được tự áp dụng cho nội dung mới.

Coherence dùng thang 0=bị cắt mất ý/chủ thể, 1=hiểu được phần nào nhưng thiếu ngữ cảnh, 2=tự hiểu được và đủ ý. Nội dung gồm 20 chunk A/B khác nhau; C dùng đúng 10 chunk B. A có nhiều phần bị cắt giữa câu/code; B giữ đoạn tốt hơn nhưng vẫn có heading hoặc chữ ký API thiếu phần giải thích, nên không mặc định cho B điểm 2. Mẫu 10 anchor đầu theo thứ tự ID tập trung vào csv/json, chưa đại diện mọi chương. Điểm trung bình được tính từ nhãn đã xác nhận trong bảng trên.

Metadata được code kiểm tra cả giá trị nguồn/type/version và text/offset so với trang chuẩn; người học đối chiếu và chấp nhận nhãn tại bảng audit. Mỗi strategy có 15/15 bản ghi top-3 test đúng theo phép đối chiếu đó. Filter compliance tính theo **câu hỏi**: top-3 của câu phải đều đúng phạm vi; A/B không bật filter nên có thể lệch phạm vi dù metadata bản ghi vẫn chính xác. C đạt 3/3; B đạt 2/3; A đạt 1/3. Với tập không có câu filter phải ghi N/A, không mặc định 100%.

Grounding xét đủ 5 test mỗi strategy và có lý do riêng. T01/T02/T03/T05 có evidence đúng nguồn trong top-3; T04 có đủ hai ý None thành chuỗi rỗng và không đảo ngược, dù thiếu đuôi quote. Không chấm theo top-1 riêng và không xem strict miss là grounding=0 tự động. [Nhận xét T04](../../results/audit/ai_review.json) ghi rõ ngoại lệ đã được đối chiếu; điểm strict hiện tại giữ nguyên, không nâng tự động theo nhãn grounding.

### 3.5. Tác động dữ liệu, tài nguyên và đánh đổi

| Strategy | Số chunk | Độ dài median / p95 / max (ký tự) | Token embedding local | Thời gian embedding | Ingest đo lại sau sửa store |
|---|---|---|---|---|---|
{chr(10).join(resources)}

B dùng ít hơn A {stats['A']['chunk_count']-stats['B']['chunk_count']} vector ({100*(1-stats['B']['chunk_count']/stats['A']['chunk_count']):.1f}%), nhưng chunk dài hơn nên thời gian embedding không giảm tương ứng. Đây là một lần đo trên máy local; batch/padding, độ dài và trạng thái máy ảnh hưởng kết quả. Model load {index['model_load_seconds']:.3f}s; thời gian tải model/cài môi trường và lần chạy lỗi trước đó không nằm trong bảng. Không suy ra tổng chi phí học bài chỉ từ thời gian thành công.

Trên dev, A→B tăng Hit@3 từ 10/15 lên 13/15 và Hit@1 từ 9/15 lên 12/15. Trên test, Hit@3 vẫn 4/5, Hit@1 tăng từ 2/5 lên 3/5. B giữ tốt điều kiện ở D03/D13 nhưng làm mất tính tập trung ở D01. Vì vậy không kết luận chunk lớn luôn tốt.

B→C không tăng strict retrieval trong bộ này; tác dụng quan sát là tuân thủ phạm vi: test 2/3→3/3. C thêm chi phí filter/search, không thêm embedding. Filter đúng loại tài liệu vẫn không giải quyết nhầm phương thức hoặc cắt thiếu câu. Nếu người dùng cung cấp sai scope, C có thể loại mất đáp án. Không suy ra C luôn vượt B chỉ vì filter compliance cao.

## 4. Ví dụ sai và giới hạn

1. **D03/A**, gold `tutorial_datastructures:u004`: điều kiện tuple làm dictionary key và ngoại lệ mutable bị chia qua các chunk. Top-1 đúng trang nhưng bắt đầu giữa chữ; một chunk khác có đầu câu nhưng thiếu cuối. Không đủ quote trong một chunk nên Hit@3=0, trong khi B/C hit. Đây là vấn đề ranh giới chunk.
2. **D01/B và C**, gold `tutorial_datastructures:u001`: hỏi lỗi của `list.remove` nhưng top-1 chứa mô tả `pop`/`index`, top-2 về `del`, top-3 về dictionary. Không lấy ValueError của `index` làm bằng chứng cho `remove`. A tìm được gold trong top-3. Đây là đánh đổi giữa ngữ cảnh và độ tập trung.
3. **D09/A/B/C**, gold `tutorial_modules:u002`: truy xuất nghiêng về module khi import, thiếu đoạn khi chạy script gán `__name__='__main__'`. Không phải thiếu dữ liệu nguồn; xếp hạng chưa phân biệt tốt tình huống.
4. **T04/A/B/C**, gold `library_csv:u001`: strict hit=0 vì thiếu phần cuối quote về `cursor.fetch*`; tuy nhiên A top-2, B/C top-3 đều nói None thành chuỗi rỗng và việc chuyển đổi không đảo ngược. Đây là hạn chế của gold quote/check exact, không đủ cơ sở gọi toàn bộ retrieval là không có bằng chứng. Nhãn grounding được đối chiếu riêng; không sửa quote sau khi xem test để làm đẹp điểm.

Giới hạn chính: 5 test rất nhỏ (một câu tương đương 20 điểm phần trăm), câu hỏi/gold do AI hỗ trợ soạn, chỉ tiếng Anh và một lĩnh vực, HTML trích xuất không giữ đủ bảng/hình, exact quote có thể phạt bằng chứng đủ nhưng khác ranh giới. {review_limit} Model nhỏ và chunking theo ký tự có thể chưa phù hợp tài liệu tiếng Việt hoặc bảng phức tạp. Không chạy LLM sinh câu trả lời, không đo answer accuracy hay độ ổn định qua nhiều seed/model. Chưa chứng minh kết quả tổng quát ngoài corpus này.

## 5. Lựa chọn, tái lập và vai trò AI

Lựa chọn giữ nguyên là **B theo dev**, không đổi sang cấu hình khác vì test. Với nhu cầu bắt buộc scope, C có ích để tuân thủ phạm vi, nhưng cần input scope đáng tin và không có bằng chứng nó tăng Hit@3 trong thí nghiệm hiện tại. Nếu mở rộng, tôi sẽ cải thiện gold bằng các đoạn hỗ trợ tối thiểu, xử lý chữ ký/heading và bảng tốt hơn, thêm câu khó và corpus tiếng Việt; mọi tinh chỉnh từ test hiện tại phải dùng holdout mới cho lần đánh giá sau.

Lệnh setup và tái lập ở [README](../../README.md). Code chạy thật nằm trong `src/` tại root, không phải các TODO của starter pgvector tùy chọn. [Nhật ký A/B/C](../../artifacts/experiment_log.csv), [gate checklist](../../docs/GATE_CHECKLIST.md), [unit/integration log](../../results/tests.txt) và [kiểm tra tự động](../../results/verification.json) là bằng chứng kỹ thuật.

{replay_note}

Codex hỗ trợ viết pipeline, soạn câu hỏi/gold, đọc log, tính chỉ số và chuẩn bị bản thảo phân tích/audit. Kiểm tra kỹ thuật bằng unit/integration tests, hash input, source/offset checks, token guard và Qdrant persistence/filter/reingest checks. {approval_text} Tôi tự trình bày và nộp bài. Chưa nộp LMS; việc nộp do tôi thực hiện.
'''
    destination = ROOT/"report/individual/2A202603646_NguyenManhTuong.md"
    destination.write_text(content,encoding="utf-8")
    write_json("results/metrics.json", {"dev":dev["strategies"],"test":test["strategies"],"selection":selection["selected_strategy"],
        "human_audit_status":read_json("results/audit/status.json"),"generated_at":now()})
    print(destination)
