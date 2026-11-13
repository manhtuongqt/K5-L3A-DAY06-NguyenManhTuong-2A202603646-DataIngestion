# Audit đã được người học xác nhận

Nguyễn Mạnh Tường đã thông báo đối chiếu và chấp nhận toàn bộ **110 dòng** của [labels.csv](labels.csv) ngày 13/11/2026. Hồ sơ được ghi thay mặt người học theo yêu cầu trực tiếp trong cuộc trao đổi, không tự suy luận từ việc ủy quyền. Xem [human_confirmation.json](human_confirmation.json), [status.json](status.json) và [human_summary.json](human_summary.json).

1. Bảng chính đã bỏ cột `annotator`; `reviewer` ghi Nguyễn Mạnh Tường. `human_label`, `human_reason`, `reviewed_at` ghi nhận việc đối chiếu và chấp nhận.
2. Hồ sơ xác nhận lưu commit/CSV đã xem và fingerprint nhãn, lý do, nguồn của từng dòng. Xác nhận chỉ áp dụng đúng nội dung đã được duyệt.
3. Coherence/grounding dùng 0–2; metadata/gold dùng 0=sai, 1=đúng. Nếu nội dung một dòng bị sửa, cần đối chiếu lại; không tự kế thừa xác nhận cũ.
4. Không sửa benchmark đã khóa, xóa kết quả cũ hoặc nâng strict metrics sau khi xem test.
5. Chạy `python -m src.pipeline audit`, `report`, `verify` và `python scripts/check_submission.py` để cập nhật bảng đo và gate; các lệnh này không gọi lại benchmark.

Phạm vi xác nhận: 30/30 coherence (10 anchor × A/B/C), 45/45 metadata (5 test × top-3 × A/B/C), 15/15 grounding (5 test × A/B/C), 20/20 gold. Gói [REVIEW.md](REVIEW.md) giữ nguyên nguồn và chunk để truy vết.

Codex hỗ trợ chuẩn bị bản chấm ban đầu từ nguồn/trace thật ở [content_review.json](content_review.json); người học đã đối chiếu và chấp nhận. Đây là human review của bản hỗ trợ, không phải hai lượt chấm độc lập hoặc chấm mù. [assistant_summary.json](assistant_summary.json) giữ nguồn gốc bản hỗ trợ; các bảng kết quả chính lấy nhãn người học đã xác nhận. Vẫn có nguy cơ thiên lệch theo gợi ý ban đầu.

T04 đã được chấp nhận grounding=2 vì top-3 có đủ None thành chuỗi rỗng và không đảo ngược; strict Hit@3 vẫn giữ 0 vì thiếu đuôi quote. [ai_review.json](ai_review.json) là ghi chú ban đầu được giữ lại, không phải một lần chạy hoặc lượt chấm độc lập mới.
