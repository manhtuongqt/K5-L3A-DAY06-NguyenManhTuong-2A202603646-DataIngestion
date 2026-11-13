# Cách xác nhận audit

Trạng thái hiện tại xem [status.json](status.json). **Bản chính đã có đủ 110 nhãn `label`, lý do `reason` và người chấm hỗ trợ `annotator`.** Codex đã đọc nội dung thực tế để điền; đây là bản dùng để người học đối chiếu và sửa tiếp, chưa thay thế việc xác nhận thủ công theo GUIDE.md.

1. Mở [REVIEW.md](REVIEW.md), đối chiếu chunk với nguồn `data/normalized/` và HTML gốc khi cần.
2. Mở [labels.csv](labels.csv). Giữ nguyên ID. Điền `human_label`, `human_reason`, `reviewer`, `reviewed_at` cho từng mẫu đã thực sự đọc.
3. Coherence và grounding: 0, 1 hoặc 2 theo GUIDE. Metadata và gold: 0 nếu sai, 1 nếu đúng. Ô trống nghĩa là chưa xác nhận, không phải điểm 0.
4. Nếu đề xuất sai thì ghi nhãn đúng và giải thích. Nếu thấy gold có nguồn tương đương khác hoặc thiếu điều kiện, ghi rõ câu/nguồn; không sửa lén benchmark đã khóa hoặc xóa kết quả cũ.
5. Chạy `python -m src.pipeline audit` để cập nhật số mẫu đã xác nhận. Lệnh giữ các cột human hiện có. Sau đó `python -m src.pipeline report` để cập nhật báo cáo.

Mẫu bắt buộc: 30 nhãn coherence (10 anchor × A/B/C), 45 nhãn metadata (5 test × top-3 × A/B/C), 15 nhãn grounding (5 test × A/B/C). Thêm 20 mục kiểm tra ngữ nghĩa gold. Tổng cộng 110 dòng; có thể dùng cùng kết luận cho B/C ở các chunk trùng, nhưng vẫn phải kiểm tra và ghi nhận đúng từng dòng.

Nhãn chính dùng [content_review.json](content_review.json): coherence được đọc nội dung chunk, grounding được đọc cả top-3 và các điều kiện cần trả lời, gold được đọc cùng ngữ cảnh nguồn. Metadata kết hợp đối chiếu source/page/type/version và text-offset bằng code với kiểm tra thông tin nguồn. C dùng cùng chunk B tại các anchor nên nhãn coherence tương ứng giống B. [assistant_summary.json](assistant_summary.json) tổng hợp riêng nhãn Codex; không lấy trung bình này làm điểm thủ công đã xác nhận của người học.

Ngoại lệ được ghi riêng: `ai_review.json` có nhận xét đọc nội dung của AI cho T04, đề xuất grounding=2 vì các ý cần trả lời đã có trong chunk dù quote bị cắt phần đuôi. Nhận xét này cũng chưa được người học xác nhận và không sửa điểm strict.
