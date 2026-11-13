# Gói kiểm tra của người học

Nguyễn Mạnh Tường đã đối chiếu và xác nhận toàn bộ 110 nhãn/lý do trong bản chính ngày 13/11/2026. Xác nhận được lưu tại human_confirmation.json. Bản chấm ban đầu được Codex hỗ trợ chuẩn bị, sau đó người học kiểm tra và chấp nhận.
Bảng chính đã ghi đủ `human_label`, `human_reason`, `reviewer`, `reviewed_at` theo xác nhận của người học; giữ hồ sơ xác nhận để truy vết.
Coherence/grounding dùng 0–2. Metadata/gold dùng 0=sai, 1=đúng. Khi sửa gold, ghi vào lý do và giữ nguyên benchmark đã chạy; không sửa âm thầm để thay điểm.
Mẫu coherence và tập test đã chốt trong `benchmark/protocol.json` trước khi chạy. Nguồn đầy đủ ở `data/normalized/` và `data/raw/`.

## COH-01-A: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u001, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases.  CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 .  The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications.  These
differences can make it annoying to process CSV files from multiple sources.
Still, while the delimiter
````

Chunk cần chấm:

````text
csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases.  CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 .  The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications.  These
differences can make it annoying to process CSV files
````

Nhãn bản chính: 1/2. Giới thiệu CSV đọc được nhưng câu về xử lý nhiều nguồn kết thúc ở 'CSV files', thiếu phần sau và kết luận của đoạn.

## COH-01-B: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u001, anchor 200; chunk [0, 780).
Ngữ cảnh quanh vị trí nguồn:

````text
csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases.  CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 .  The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications.  These
differences can make it annoying to process CSV files from multiple sources.
Still, while the delimiter
````

Chunk cần chấm:

````text
csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases.  CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 .  The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications.  These
differences can make it annoying to process CSV files from multiple sources.
Still, while the delimiters and quoting characters vary, the overall format is
similar enough that it is possible to write a single module which can
efficiently manipulate such data, hiding the details of reading and writing the
data from the programmer.


````

Nhãn bản chính: 2/2. Giữ trọn đoạn giới thiệu CSV, khác biệt định dạng giữa ứng dụng và khả năng dùng một module để xử lý; có tên csv và nguồn mã.

## COH-01-C: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u001, anchor 200; chunk [0, 780).
Ngữ cảnh quanh vị trí nguồn:

````text
csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases.  CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 .  The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications.  These
differences can make it annoying to process CSV files from multiple sources.
Still, while the delimiter
````

Chunk cần chấm:

````text
csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases.  CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 .  The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications.  These
differences can make it annoying to process CSV files from multiple sources.
Still, while the delimiters and quoting characters vary, the overall format is
similar enough that it is possible to write a single module which can
efficiently manipulate such data, hiding the details of reading and writing the
data from the programmer.


````

Nhãn bản chính: 2/2. Giữ trọn đoạn giới thiệu CSV, khác biệt định dạng giữa ứng dụng và khả năng dùng một module để xử lý; có tên csv và nguồn mã. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-02-A: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u002, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
A short usage example:

import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

which writes eggs.csv containing:

Spam Spam Spam Spam Spam |Baked Beans|
Spam |Lovely Spam| |Wonderful Spam|

csv. register_dialect ( name , / , dialect = 'excel' , ** fmtparams )

Associate dialect with name . name m
````

Chunk cần chấm:

````text
A short usage example:

import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

which writes eggs.csv containing:

Spam Spam Spam Spam Spam |Baked Beans|
Spam |Lovely Spam| |Wonderful Spam|

csv. register_dialect ( name , / , dialect = 'excel' , **
````

Nhãn bản chính: 1/2. Ví dụ csv.writer và output đầy đủ, nhưng chữ ký register_dialect bị cắt ngay sau ** nên chunk vẫn còn ý dang dở.

## COH-02-B: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u002, anchor 200; chunk [0, 887).
Ngữ cảnh quanh vị trí nguồn:

````text
A short usage example:

import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

which writes eggs.csv containing:

Spam Spam Spam Spam Spam |Baked Beans|
Spam |Lovely Spam| |Wonderful Spam|

csv. register_dialect ( name , / , dialect = 'excel' , ** fmtparams )

Associate dialect with name . name m
````

Chunk cần chấm:

````text
A short usage example:

import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

which writes eggs.csv containing:

Spam Spam Spam Spam Spam |Baked Beans|
Spam |Lovely Spam| |Wonderful Spam|

csv. register_dialect ( name , / , dialect = 'excel' , ** fmtparams )

Associate dialect with name . name must be a string. The
dialect can be specified either by passing a sub-class of Dialect , or
by fmtparams keyword arguments, or both, with keyword arguments overriding
parameters of the dialect. For full details about dialects and formatting
parameters, see section Dialects and Formatting Parameters .

csv. unregister_dialect ( name )


````

Nhãn bản chính: 1/2. Giữ ví dụ và mô tả register_dialect, nhưng kết thúc bằng chữ ký unregister_dialect chưa có giải thích; không chấm 2 chỉ vì dài hơn A.

## COH-02-C: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u002, anchor 200; chunk [0, 887).
Ngữ cảnh quanh vị trí nguồn:

````text
A short usage example:

import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

which writes eggs.csv containing:

Spam Spam Spam Spam Spam |Baked Beans|
Spam |Lovely Spam| |Wonderful Spam|

csv. register_dialect ( name , / , dialect = 'excel' , ** fmtparams )

Associate dialect with name . name m
````

Chunk cần chấm:

````text
A short usage example:

import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

which writes eggs.csv containing:

Spam Spam Spam Spam Spam |Baked Beans|
Spam |Lovely Spam| |Wonderful Spam|

csv. register_dialect ( name , / , dialect = 'excel' , ** fmtparams )

Associate dialect with name . name must be a string. The
dialect can be specified either by passing a sub-class of Dialect , or
by fmtparams keyword arguments, or both, with keyword arguments overriding
parameters of the dialect. For full details about dialects and formatting
parameters, see section Dialects and Formatting Parameters .

csv. unregister_dialect ( name )


````

Nhãn bản chính: 1/2. Giữ ví dụ và mô tả register_dialect, nhưng kết thúc bằng chữ ký unregister_dialect chưa có giải thích; không chấm 2 chỉ vì dài hơn A. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-03-A: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u003, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
Note that unlike the DictReader class, the fieldnames parameter
of the DictWriter class is not optional.

If the argument passed to fieldnames is an iterator, it will be coerced to a list .

A short usage example:

import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    wr
````

Chunk cần chấm:

````text
Note that unlike the DictReader class, the fieldnames parameter
of the DictWriter class is not optional.

If the argument passed to fieldnames is an iterator, it will be coerced to a list .

A short usage example:

import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'f
````

Nhãn bản chính: 1/2. Nêu được fieldnames bắt buộc nhưng đoạn ví dụ DictWriter bị cắt giữa khóa first_name, không còn là code hoàn chỉnh.

## COH-03-B: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u003, anchor 200; chunk [0, 732).
Ngữ cảnh quanh vị trí nguồn:

````text
Note that unlike the DictReader class, the fieldnames parameter
of the DictWriter class is not optional.

If the argument passed to fieldnames is an iterator, it will be coerced to a list .

A short usage example:

import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    wr
````

Chunk cần chấm:

````text
Note that unlike the DictReader class, the fieldnames parameter
of the DictWriter class is not optional.

If the argument passed to fieldnames is an iterator, it will be coerced to a list .

A short usage example:

import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

which writes names.csv containing:

first_name,last_name
Baked,Beans
Lovely,Spam
Wonderful,Spam

class csv. Dialect


````

Nhãn bản chính: 1/2. Ví dụ DictWriter và output trọn vẹn; cuối chunk lại có class csv.Dialect đứng riêng, phải xem tiếp để biết vai trò lớp này.

## COH-03-C: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u003, anchor 200; chunk [0, 732).
Ngữ cảnh quanh vị trí nguồn:

````text
Note that unlike the DictReader class, the fieldnames parameter
of the DictWriter class is not optional.

If the argument passed to fieldnames is an iterator, it will be coerced to a list .

A short usage example:

import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    wr
````

Chunk cần chấm:

````text
Note that unlike the DictReader class, the fieldnames parameter
of the DictWriter class is not optional.

If the argument passed to fieldnames is an iterator, it will be coerced to a list .

A short usage example:

import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

which writes names.csv containing:

first_name,last_name
Baked,Beans
Lovely,Spam
Wonderful,Spam

class csv. Dialect


````

Nhãn bản chính: 1/2. Ví dụ DictWriter và output trọn vẹn; cuối chunk lại có class csv.Dialect đứng riêng, phải xem tiếp để biết vai trò lớp này. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-04-A: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u004, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric fields.

Instructs reader objects to convert all non-qu
````

Chunk cần chấm:

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric field
````

Nhãn bản chính: 1/2. QUOTE_ALL và QUOTE_MINIMAL có ý nghĩa rõ, nhưng mô tả QUOTE_NONNUMERIC bị cắt giữa từ fields và thiếu chiều đọc thành float.

## COH-04-B: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u004, anchor 200; chunk [0, 796).
Ngữ cảnh quanh vị trí nguồn:

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric fields.

Instructs reader objects to convert all non-qu
````

Chunk cần chấm:

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric fields.

Instructs reader objects to convert all non-quoted fields to type float .

Note

Some numeric types, such as bool , Fraction ,
or IntEnum , have a string representation that cannot be
converted to float .
They cannot be read in the QUOTE_NONNUMERIC and QUOTE_STRINGS modes.

csv. QUOTE_NONE


````

Nhãn bản chính: 1/2. Giữ đủ hành vi QUOTE_NONNUMERIC và ngoại lệ kiểu số, nhưng kết thúc ở nhãn QUOTE_NONE chưa có định nghĩa.

## COH-04-C: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u004, anchor 200; chunk [0, 796).
Ngữ cảnh quanh vị trí nguồn:

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric fields.

Instructs reader objects to convert all non-qu
````

Chunk cần chấm:

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric fields.

Instructs reader objects to convert all non-quoted fields to type float .

Note

Some numeric types, such as bool , Fraction ,
or IntEnum , have a string representation that cannot be
converted to float .
They cannot be read in the QUOTE_NONNUMERIC and QUOTE_STRINGS modes.

csv. QUOTE_NONE


````

Nhãn bản chính: 1/2. Giữ đủ hành vi QUOTE_NONNUMERIC và ngoại lệ kiểu số, nhưng kết thúc ở nhãn QUOTE_NONE chưa có định nghĩa. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-05-A: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u005, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
the escapechar itself.

On reading, the escapechar removes any special meaning from
the following character. It defaults to None , which disables escaping.

Changed in version 3.10: Previously the escapechar itself was not escaped,
which lost it on reading.

Changed in version 3.11: An empty escapechar is not allowed.

Dialect. lineterminator

The string used to terminate lines produced by the writer . It defaults
to '\r\n' .

Note

The reader is hard-coded to recognise either '\r' or '\n' as
end-of-line, and ignores lineterminator . This behav
````

Chunk cần chấm:

````text
the escapechar itself.

On reading, the escapechar removes any special meaning from
the following character. It defaults to None , which disables escaping.

Changed in version 3.10: Previously the escapechar itself was not escaped,
which lost it on reading.

Changed in version 3.11: An empty escapechar is not allowed.

Dialect. lineterminator

The string used to terminate lines produced by the writer . It defaults
to '\r\n' .

Note

The reader is hard-coded to recognise either '\r' or '\n' as
en
````

Nhãn bản chính: 1/2. Có mô tả escapechar và lineterminator đọc được; mở đầu là mảnh của danh sách trước và ghi chú reader bị cắt ở giữa end-of-line.

## COH-05-B: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u005, anchor 200; chunk [0, 992).
Ngữ cảnh quanh vị trí nguồn:

````text
the escapechar itself.

On reading, the escapechar removes any special meaning from
the following character. It defaults to None , which disables escaping.

Changed in version 3.10: Previously the escapechar itself was not escaped,
which lost it on reading.

Changed in version 3.11: An empty escapechar is not allowed.

Dialect. lineterminator

The string used to terminate lines produced by the writer . It defaults
to '\r\n' .

Note

The reader is hard-coded to recognise either '\r' or '\n' as
end-of-line, and ignores lineterminator . This behav
````

Chunk cần chấm:

````text
the escapechar itself.

On reading, the escapechar removes any special meaning from
the following character. It defaults to None , which disables escaping.

Changed in version 3.10: Previously the escapechar itself was not escaped,
which lost it on reading.

Changed in version 3.11: An empty escapechar is not allowed.

Dialect. lineterminator

The string used to terminate lines produced by the writer . It defaults
to '\r\n' .

Note

The reader is hard-coded to recognise either '\r' or '\n' as
end-of-line, and ignores lineterminator . This behavior may change in the
future.

Dialect. quotechar

A one-character string used to quote fields containing special characters,
such as the delimiter or the quotechar , or which contain new-line
characters ( '\r' , '\n' or any of the characters in lineterminator ).
It defaults to '"' .
Can be set to None to prevent escaping '"' if quoting is set
to QUOTE_NONE .

Changed in version 3.11: An empty quotechar is not allowed.

Dialect. quoting


````

Nhãn bản chính: 1/2. Giữ trọn ghi chú reader và điều kiện quotechar, nhưng vẫn bắt đầu bằng mảnh 'the escapechar itself' và kết thúc tại tên thuộc tính quoting chưa giải thích.

## COH-05-C: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u005, anchor 200; chunk [0, 992).
Ngữ cảnh quanh vị trí nguồn:

````text
the escapechar itself.

On reading, the escapechar removes any special meaning from
the following character. It defaults to None , which disables escaping.

Changed in version 3.10: Previously the escapechar itself was not escaped,
which lost it on reading.

Changed in version 3.11: An empty escapechar is not allowed.

Dialect. lineterminator

The string used to terminate lines produced by the writer . It defaults
to '\r\n' .

Note

The reader is hard-coded to recognise either '\r' or '\n' as
end-of-line, and ignores lineterminator . This behav
````

Chunk cần chấm:

````text
the escapechar itself.

On reading, the escapechar removes any special meaning from
the following character. It defaults to None , which disables escaping.

Changed in version 3.10: Previously the escapechar itself was not escaped,
which lost it on reading.

Changed in version 3.11: An empty escapechar is not allowed.

Dialect. lineterminator

The string used to terminate lines produced by the writer . It defaults
to '\r\n' .

Note

The reader is hard-coded to recognise either '\r' or '\n' as
end-of-line, and ignores lineterminator . This behavior may change in the
future.

Dialect. quotechar

A one-character string used to quote fields containing special characters,
such as the delimiter or the quotechar , or which contain new-line
characters ( '\r' , '\n' or any of the characters in lineterminator ).
It defaults to '"' .
Can be set to None to prevent escaping '"' if quoting is set
to QUOTE_NONE .

Changed in version 3.11: An empty quotechar is not allowed.

Dialect. quoting


````

Nhãn bản chính: 1/2. Giữ trọn ghi chú reader và điều kiện quotechar, nhưng vẫn bắt đầu bằng mảnh 'the escapechar itself' và kết thúc tại tên thuộc tính quoting chưa giải thích. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-06-A: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u006, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV file:

import csv
with open('some.csv', newline='')
````

Chunk cần chấm:

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV f
````

Nhãn bản chính: 1/2. writeheader được giải thích đủ, nhưng tiêu đề chuyển sang ví dụ đọc CSV bị cắt giữa từ file; chunk chứa phần ngữ cảnh chưa xong.

## COH-06-B: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u006, anchor 200; chunk [0, 884).
Ngữ cảnh quanh vị trí nguồn:

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV file:

import csv
with open('some.csv', newline='')
````

Chunk cần chấm:

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV file:

import csv
with open('some.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

Reading a file with an alternate format:

import csv
with open('passwd', newline='') as f:
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)

The corresponding simplest possible writing example is:


````

Nhãn bản chính: 1/2. Có writeheader và hai ví dụ đọc hoàn chỉnh; cuối cùng giới thiệu ví dụ ghi đơn giản nhưng chưa có code của ví dụ đó.

## COH-06-C: coherence
Nguồn: https://docs.python.org/3.13/library/csv.html — library_csv:u006, anchor 200; chunk [0, 884).
Ngữ cảnh quanh vị trí nguồn:

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV file:

import csv
with open('some.csv', newline='')
````

Chunk cần chấm:

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV file:

import csv
with open('some.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

Reading a file with an alternate format:

import csv
with open('passwd', newline='') as f:
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)

The corresponding simplest possible writing example is:


````

Nhãn bản chính: 1/2. Có writeheader và hai ví dụ đọc hoàn chỉnh; cuối cùng giới thiệu ví dụ ghi đơn giản nhưng chưa có code của ví dụ đó. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-07-A: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u001, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be caut
````

Chunk cần chấm:

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces,
````

Nhãn bản chính: 1/2. Giới thiệu JSON rõ nhưng định nghĩa JSON object bị dừng sau curly braces, thiếu phần so sánh và ghi chú tiếp theo.

## COH-07-B: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u001, anchor 200; chunk [0, 895).
Ngữ cảnh quanh vị trí nguồn:

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be caut
````

Chunk cần chấm:

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.

This module exposes an API familiar to users of the standard library marshal and pickle modules.

Encoding basic Python object hierarchies:


````

Nhãn bản chính: 1/2. Giữ định nghĩa object và toàn bộ cảnh báo JSON không tin cậy; cuối chunk có nhãn Encoding basic Python object hierarchies nhưng chưa có ví dụ.

## COH-07-C: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u001, anchor 200; chunk [0, 895).
Ngữ cảnh quanh vị trí nguồn:

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be caut
````

Chunk cần chấm:

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.

This module exposes an API familiar to users of the standard library marshal and pickle modules.

Encoding basic Python object hierarchies:


````

Nhãn bản chính: 1/2. Giữ định nghĩa object và toàn bộ cảnh báo JSON không tin cậy; cuối chunk có nhãn Encoding basic Python object hierarchies nhưng chưa có ví dụ. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-08-A: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u002, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is n
````

Chunk cần chấm:

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion ta
````

Nhãn bản chính: 1/2. Có chữ ký json.dump nhưng câu mô tả bị cắt giữa từ table; cần đoạn kế tiếp để đọc hết ý.

## COH-08-B: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u002, anchor 200; chunk [0, 950).
Ngữ cảnh quanh vị trí nguồn:

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is n
````

Chunk cần chấm:

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.

Parameters :

obj ( object ) – The Python object to be serialized.

fp ( file-like object ) – The file-like object obj will be serialized to.
The json module always produces str objects,
not bytes objects,
therefore fp.write() must support str input.


````

Nhãn bản chính: 2/2. json.dump có chữ ký, mô tả, cảnh báo không framed protocol và hai tham số obj/fp với yêu cầu write str; các ý này đầy đủ trong chunk.

## COH-08-C: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u002, anchor 200; chunk [0, 950).
Ngữ cảnh quanh vị trí nguồn:

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is n
````

Chunk cần chấm:

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.

Parameters :

obj ( object ) – The Python object to be serialized.

fp ( file-like object ) – The file-like object obj will be serialized to.
The json module always produces str objects,
not bytes objects,
therefore fp.write() must support str input.


````

Nhãn bản chính: 2/2. json.dump có chữ ký, mô tả, cảnh báo không framed protocol và hai tham số obj/fp với yêu cầu write str; các ý này đầy đủ trong chunk. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-09-A: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u003, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
Changed in version 3.2: Allow strings for indent in addition to integers.

Changed in version 3.4: Use (',', ': ') as default if indent is not None .

Changed in version 3.6: All optional parameters are now keyword-only .

json. dumps ( obj , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj to a JSON formatted str using this conversion
table .  The arguments have the same meaning as in dump() .

jso
````

Chunk cần chấm:

````text
Changed in version 3.2: Allow strings for indent in addition to integers.

Changed in version 3.4: Use (',', ': ') as default if indent is not None .

Changed in version 3.6: All optional parameters are now keyword-only .

json. dumps ( obj , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj to a JSON formatted str using this conversion
table .  The a
````

Nhãn bản chính: 1/2. Có mô tả json.dumps nhưng câu dẫn sang ý nghĩa tham số bị cắt ngay 'The a'; đầu chunk là lịch sử thay đổi chưa nêu rõ API.

## COH-09-B: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u003, anchor 200; chunk [0, 919).
Ngữ cảnh quanh vị trí nguồn:

````text
Changed in version 3.2: Allow strings for indent in addition to integers.

Changed in version 3.4: Use (',', ': ') as default if indent is not None .

Changed in version 3.6: All optional parameters are now keyword-only .

json. dumps ( obj , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj to a JSON formatted str using this conversion
table .  The arguments have the same meaning as in dump() .

jso
````

Chunk cần chấm:

````text
Changed in version 3.2: Allow strings for indent in addition to integers.

Changed in version 3.4: Use (',', ': ') as default if indent is not None .

Changed in version 3.6: All optional parameters are now keyword-only .

json. dumps ( obj , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj to a JSON formatted str using this conversion
table .  The arguments have the same meaning as in dump() .

json. load ( fp , * , cls = None , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , object_pairs_hook = None , ** kw )

Deserialize fp to a Python object
using the JSON-to-Python conversion table .

Parameters :

fp ( file-like object ) – A .read() -supporting text file or binary file containing the JSON document to be deserialized.


````

Nhãn bản chính: 1/2. Mô tả dumps/load đọc được, nhưng nhiều tham số dumps chỉ dẫn 'same meaning as dump' không có định nghĩa trong chunk; các dòng Changed đầu cũng thiếu chủ thể API.

## COH-09-C: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u003, anchor 200; chunk [0, 919).
Ngữ cảnh quanh vị trí nguồn:

````text
Changed in version 3.2: Allow strings for indent in addition to integers.

Changed in version 3.4: Use (',', ': ') as default if indent is not None .

Changed in version 3.6: All optional parameters are now keyword-only .

json. dumps ( obj , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj to a JSON formatted str using this conversion
table .  The arguments have the same meaning as in dump() .

jso
````

Chunk cần chấm:

````text
Changed in version 3.2: Allow strings for indent in addition to integers.

Changed in version 3.4: Use (',', ': ') as default if indent is not None .

Changed in version 3.6: All optional parameters are now keyword-only .

json. dumps ( obj , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj to a JSON formatted str using this conversion
table .  The arguments have the same meaning as in dump() .

json. load ( fp , * , cls = None , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , object_pairs_hook = None , ** kw )

Deserialize fp to a Python object
using the JSON-to-Python conversion table .

Parameters :

fp ( file-like object ) – A .read() -supporting text file or binary file containing the JSON document to be deserialized.


````

Nhãn bản chính: 1/2. Mô tả dumps/load đọc được, nhưng nhiều tham số dumps chỉ dẫn 'same meaning as dump' không có định nghĩa trong chunk; các dòng Changed đầu cũng thiếu chủ thể API. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## COH-10-A: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u004, anchor 200; chunk [0, 500).
Ngữ cảnh quanh vị trí nguồn:

````text
Changed in version 3.6: s can now be of type bytes or bytearray . The
input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.9: The keyword argument encoding has been removed.

Encoders and Decoders

class json. JSONDecoder ( * , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , strict = True , object_pairs_hook = None )

Simple JSON decoder.

Performs the following translations in decoding by default:

JSON

Python

object

dict

array

list

string

str

number (int)

int

number (real)

flo
````

Chunk cần chấm:

````text
Changed in version 3.6: s can now be of type bytes or bytearray . The
input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.9: The keyword argument encoding has been removed.

Encoders and Decoders

class json. JSONDecoder ( * , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , strict = True , object_pairs_hook = None )

Simple JSON decoder.

Performs the following translations in decoding by default:

JSON

Python

object

dict

array

list


````

Nhãn bản chính: 1/2. Có JSONDecoder và đầu bảng quy đổi object/dict, array/list, nhưng bảng bị dừng giữa chừng; chưa đủ phần giới thiệu bộ giải mã.

## COH-10-B: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u004, anchor 200; chunk [0, 973).
Ngữ cảnh quanh vị trí nguồn:

````text
Changed in version 3.6: s can now be of type bytes or bytearray . The
input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.9: The keyword argument encoding has been removed.

Encoders and Decoders

class json. JSONDecoder ( * , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , strict = True , object_pairs_hook = None )

Simple JSON decoder.

Performs the following translations in decoding by default:

JSON

Python

object

dict

array

list

string

str

number (int)

int

number (real)

flo
````

Chunk cần chấm:

````text
Changed in version 3.6: s can now be of type bytes or bytearray . The
input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.9: The keyword argument encoding has been removed.

Encoders and Decoders

class json. JSONDecoder ( * , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , strict = True , object_pairs_hook = None )

Simple JSON decoder.

Performs the following translations in decoding by default:

JSON

Python

object

dict

array

list

string

str

number (int)

int

number (real)

float

true

True

false

False

null

None

It also understands NaN , Infinity , and -Infinity as their
corresponding float values, which is outside the JSON spec.

object_hook is an optional function that will be called with the result of
every JSON object decoded and its return value will be used in place of the
given dict .  This can be used to provide custom deserializations
(e.g. to support JSON-RPC class hinting).


````

Nhãn bản chính: 2/2. Giữ đầy đủ bảng quy đổi cơ bản, ghi chú NaN/Infinity ngoài đặc tả và vai trò object_hook. Dù bảng mất bố cục cột, các cặp JSON/Python vẫn đọc được theo thứ tự.

## COH-10-C: coherence
Nguồn: https://docs.python.org/3.13/library/json.html — library_json:u004, anchor 200; chunk [0, 973).
Ngữ cảnh quanh vị trí nguồn:

````text
Changed in version 3.6: s can now be of type bytes or bytearray . The
input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.9: The keyword argument encoding has been removed.

Encoders and Decoders

class json. JSONDecoder ( * , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , strict = True , object_pairs_hook = None )

Simple JSON decoder.

Performs the following translations in decoding by default:

JSON

Python

object

dict

array

list

string

str

number (int)

int

number (real)

flo
````

Chunk cần chấm:

````text
Changed in version 3.6: s can now be of type bytes or bytearray . The
input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.9: The keyword argument encoding has been removed.

Encoders and Decoders

class json. JSONDecoder ( * , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , strict = True , object_pairs_hook = None )

Simple JSON decoder.

Performs the following translations in decoding by default:

JSON

Python

object

dict

array

list

string

str

number (int)

int

number (real)

float

true

True

false

False

null

None

It also understands NaN , Infinity , and -Infinity as their
corresponding float values, which is outside the JSON spec.

object_hook is an optional function that will be called with the result of
every JSON object decoded and its return value will be used in place of the
given dict .  This can be used to provide custom deserializations
(e.g. to support JSON-RPC class hinting).


````

Nhãn bản chính: 2/2. Giữ đầy đủ bảng quy đổi cơ bản, ghi chú NaN/Infinity ngoài đặc tả và vai trò object_hook. Dù bảng mất bố cục cột, các cặp JSON/Python vẫn đọc được theo thứ tự. C dùng đúng chunk B tại cùng anchor, filter truy vấn không thay đổi coherence của chunk.

## GRD-T01-A: grounding và metadata top-3
Câu hỏi: In the library reference, what resource risk comes from parsing untrusted JSON, and what precaution is advised?
Đáp án dự kiến: A malicious JSON string may consume considerable CPU and memory; limit the size of input.
Gold: library_json / library_json:u001

````text
Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {}
### Top 1 / META-T01-A-1
Chunk 0a2794e289d543a85efeec82c618704f; source https://docs.python.org/3.13/tutorial/inputoutput.html; page tutorial_inputoutput:u005; type tutorial; version 3.13; offsets [3600,3887).

````text
jects.  As such, it is
specific to Python and cannot be used to communicate with applications
written in other languages.  It is also insecure by default:
deserializing pickle data coming from an untrusted source can execute
arbitrary code, if the data was crafted by a skilled attacker.
````

### Top 2 / META-T01-A-2
Chunk 60963d601df7a1689a44f226ec3445aa; source https://docs.python.org/3.13/library/json.html; page library_json:u003; type library_reference; version 3.13; offsets [3150,3596).

````text
a the interpreter’s integer string
conversion length limitation to help avoid denial
of service attacks.

json. loads ( s , * , cls = None , object_hook = None , parse_float = None , parse_int = None , parse_constant = None , object_pairs_hook = None , ** kw )

Identical to load() , but instead of a file-like object,
deserialize s (a str , bytes or bytearray instance containing a JSON document) to a Python object using this conversion table .
````

### Top 3 / META-T01-A-3
Chunk bd92ca4f68e2677041440b77de35c750; source https://docs.python.org/3.13/library/json.html; page library_json:u001; type library_reference; version 3.13; offsets [450,950).

````text
object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.

This module exposes an API familiar to users of the standard library marshal and pickle modules.

Encoding basic Python object hierarchies:

>>> import json
>>> json.dumps(['foo', {'bar': ('baz', 
````

Nhãn grounding bản chính: 2/2. Top-3 library_json:u001 có đủ rủi ro CPU/bộ nhớ và khuyến nghị giới hạn kích thước. Top-1 về pickle khác câu hỏi, nhưng không làm mất bằng chứng đầy đủ ở top-3.

## GRD-T01-B: grounding và metadata top-3
Câu hỏi: In the library reference, what resource risk comes from parsing untrusted JSON, and what precaution is advised?
Đáp án dự kiến: A malicious JSON string may consume considerable CPU and memory; limit the size of input.
Gold: library_json / library_json:u001

````text
Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {}
### Top 1 / META-T01-B-1
Chunk b5005503cf31f326cea566634baea461; source https://docs.python.org/3.13/library/json.html; page library_json:u001; type library_reference; version 3.13; offsets [0,895).

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.

This module exposes an API familiar to users of the standard library marshal and pickle modules.

Encoding basic Python object hierarchies:


````

### Top 2 / META-T01-B-2
Chunk 40e36e5259738af72f874b9b3c276b75; source https://docs.python.org/3.13/library/json.html; page library_json:u004; type library_reference; version 3.13; offsets [1868,2823).

````text
parse_constant is an optional function that will be called with one of the
following strings: '-Infinity' , 'Infinity' , 'NaN' .  This can be
used to raise an exception if invalid JSON numbers are encountered.

If strict is false ( True is the default), then control characters
will be allowed inside strings.  Control characters in this context are
those with character codes in the 0–31 range, including '\t' (tab), '\n' , '\r' and '\0' .

If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised.

Changed in version 3.6: All parameters are now keyword-only .

decode ( s )

Return the Python representation of s (a str instance
containing a JSON document).

JSONDecodeError will be raised if the given JSON document is not
valid.

raw_decode ( s )

Decode a JSON document from s (a str beginning with a
JSON document) and return a 2-tuple of the Python representation
and the index in s where the document ended.


````

### Top 3 / META-T01-B-3
Chunk be953708e8bde71b0fc5808f7c4493cd; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [876,1773).

````text
The RFC requires that JSON be represented using either UTF-8, UTF-16, or
UTF-32, with UTF-8 being the recommended default for maximum interoperability.

As permitted, though not required, by the RFC, this module’s serializer sets ensure_ascii=True by default, thus escaping the output so that the resulting
strings only contain printable ASCII characters.

Other than the ensure_ascii parameter, this module is defined strictly in
terms of conversion between Python objects and Unicode strings , and thus does not otherwise directly address
the issue of character encodings.

The RFC prohibits adding a byte order mark (BOM) to the start of a JSON text,
and this module’s serializer does not add a BOM to its output.
The RFC permits, but does not require, JSON deserializers to ignore an initial
BOM in their input.  This module’s deserializer raises a ValueError when an initial BOM is present.


````

Nhãn grounding bản chính: 2/2. Top-1 library_json:u001 chứa trọn cảnh báo dữ liệu JSON không tin cậy, đủ cả hai ý và có nguồn.

## GRD-T01-C: grounding và metadata top-3
Câu hỏi: In the library reference, what resource risk comes from parsing untrusted JSON, and what precaution is advised?
Đáp án dự kiến: A malicious JSON string may consume considerable CPU and memory; limit the size of input.
Gold: library_json / library_json:u001

````text
Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {'document_type': 'library_reference'}
### Top 1 / META-T01-C-1
Chunk b5005503cf31f326cea566634baea461; source https://docs.python.org/3.13/library/json.html; page library_json:u001; type library_reference; version 3.13; offsets [0,895).

````text
json — JSON encoder and decoder

Source code: Lib/json/__init__.py

JSON (JavaScript Object Notation) , specified by RFC 7159 (which obsoletes RFC 4627 ) and by ECMA-404 ,
is a lightweight data interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [ 1 ] ).

Note

The term “object” in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.

This module exposes an API familiar to users of the standard library marshal and pickle modules.

Encoding basic Python object hierarchies:


````

### Top 2 / META-T01-C-2
Chunk 40e36e5259738af72f874b9b3c276b75; source https://docs.python.org/3.13/library/json.html; page library_json:u004; type library_reference; version 3.13; offsets [1868,2823).

````text
parse_constant is an optional function that will be called with one of the
following strings: '-Infinity' , 'Infinity' , 'NaN' .  This can be
used to raise an exception if invalid JSON numbers are encountered.

If strict is false ( True is the default), then control characters
will be allowed inside strings.  Control characters in this context are
those with character codes in the 0–31 range, including '\t' (tab), '\n' , '\r' and '\0' .

If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised.

Changed in version 3.6: All parameters are now keyword-only .

decode ( s )

Return the Python representation of s (a str instance
containing a JSON document).

JSONDecodeError will be raised if the given JSON document is not
valid.

raw_decode ( s )

Decode a JSON document from s (a str beginning with a
JSON document) and return a 2-tuple of the Python representation
and the index in s where the document ended.


````

### Top 3 / META-T01-C-3
Chunk be953708e8bde71b0fc5808f7c4493cd; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [876,1773).

````text
The RFC requires that JSON be represented using either UTF-8, UTF-16, or
UTF-32, with UTF-8 being the recommended default for maximum interoperability.

As permitted, though not required, by the RFC, this module’s serializer sets ensure_ascii=True by default, thus escaping the output so that the resulting
strings only contain printable ASCII characters.

Other than the ensure_ascii parameter, this module is defined strictly in
terms of conversion between Python objects and Unicode strings , and thus does not otherwise directly address
the issue of character encodings.

The RFC prohibits adding a byte order mark (BOM) to the start of a JSON text,
and this module’s serializer does not add a BOM to its output.
The RFC permits, but does not require, JSON deserializers to ignore an initial
BOM in their input.  This module’s deserializer raises a ValueError when an initial BOM is present.


````

Nhãn grounding bản chính: 2/2. Top-1 như B, có cả rủi ro và cách giảm rủi ro; cả top-3 nằm trong library_reference đúng scope.

## GRD-T02-A: grounding và metadata top-3
Câu hỏi: In the library reference, why do repeated json.dump calls on the same file produce invalid JSON?
Đáp án dự kiến: JSON is not a framed protocol; repeated serialization of multiple objects to the same file is invalid.
Gold: library_json / library_json:u002

````text
Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {}
### Top 1 / META-T02-A-1
Chunk 8208acc55e5af214db1aa6b26255e675; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [2700,3200).

````text
deserializer, the parse_constant parameter can be used to
alter this behavior.

Repeated Names Within an Object

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:

>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}

The object_pairs_hook parameter c
````

### Top 2 / META-T02-A-2
Chunk 6e38f7be805a30a8164ed47a42c087da; source https://docs.python.org/3.13/library/json.html; page library_json:u002; type library_reference; version 3.13; offsets [450,950).

````text
e object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.

Parameters :

obj ( object ) – The Python object to be serialized.

fp ( file-like object ) – The file-like object obj will be serialized to.
The json module always produces str objects,
not bytes objects,
therefore fp.write() must support str input.


````

### Top 3 / META-T02-A-3
Chunk 6cb3714ab1771055867ce54717b84869; source https://docs.python.org/3.13/tutorial/inputoutput.html; page tutorial_inputoutput:u005; type tutorial; version 3.13; offsets [2700,3200).

````text

>>> import json
>>> x = [1, 'simple', 'list']
>>> json.dumps(x)
'[1, "simple", "list"]'

Another variant of the dumps() function, called dump() ,
simply serializes the object to a text file .  So if f is a text file object opened for writing, we can do this:

json.dump(x, f)

To decode the object again, if f is a binary file or text file object which has been opened for reading:

x = json.load(f)

Note

JSON files must be encoded in UTF-8. Use encoding="utf-8" when opening
JSON file as a text f
````

Nhãn grounding bản chính: 2/2. Top-2 library_json:u002 nói rõ JSON không framed và dump nhiều object vào cùng fp tạo file JSON không hợp lệ; đủ giải thích nguyên nhân.

## GRD-T02-B: grounding và metadata top-3
Câu hỏi: In the library reference, why do repeated json.dump calls on the same file produce invalid JSON?
Đáp án dự kiến: JSON is not a framed protocol; repeated serialization of multiple objects to the same file is invalid.
Gold: library_json / library_json:u002

````text
Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {}
### Top 1 / META-T02-B-1
Chunk 961e45cbf11cdc6767179f9e3390cd15; source https://docs.python.org/3.13/tutorial/inputoutput.html; page tutorial_inputoutput:u005; type tutorial; version 3.13; offsets [2790,3497).

````text
Another variant of the dumps() function, called dump() ,
simply serializes the object to a text file .  So if f is a text file object opened for writing, we can do this:

json.dump(x, f)

To decode the object again, if f is a binary file or text file object which has been opened for reading:

x = json.load(f)

Note

JSON files must be encoded in UTF-8. Use encoding="utf-8" when opening
JSON file as a text file for both of reading and writing.

This simple serialization technique can handle lists and dictionaries, but
serializing arbitrary class instances in JSON requires a bit of extra effort.
The reference for the json module contains an explanation of this.

See also

pickle - the pickle module


````

### Top 2 / META-T02-B-2
Chunk 22a33164b5b126c8bb870cf295a6ff14; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [2613,3276).

````text
In the serializer, the allow_nan parameter can be used to alter this
behavior.  In the deserializer, the parse_constant parameter can be used to
alter this behavior.

Repeated Names Within an Object

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:

>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}

The object_pairs_hook parameter can be used to alter this behavior.

Top-level Non-Object, Non-Array Values


````

### Top 3 / META-T02-B-3
Chunk 1518a830ffa51073f7b6bbb60fc3a999; source https://docs.python.org/3.13/library/json.html; page library_json:u002; type library_reference; version 3.13; offsets [0,950).

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.

Parameters :

obj ( object ) – The Python object to be serialized.

fp ( file-like object ) – The file-like object obj will be serialized to.
The json module always produces str objects,
not bytes objects,
therefore fp.write() must support str input.


````

Nhãn grounding bản chính: 2/2. Top-1 chỉ hướng dẫn dump/load thông thường, nhưng top-3 library_json:u002 giữ nguyên cảnh báo repeated dump; đánh giá cả top-3 nên đủ.

## GRD-T02-C: grounding và metadata top-3
Câu hỏi: In the library reference, why do repeated json.dump calls on the same file produce invalid JSON?
Đáp án dự kiến: JSON is not a framed protocol; repeated serialization of multiple objects to the same file is invalid.
Gold: library_json / library_json:u002

````text
Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {'document_type': 'library_reference'}
### Top 1 / META-T02-C-1
Chunk 22a33164b5b126c8bb870cf295a6ff14; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [2613,3276).

````text
In the serializer, the allow_nan parameter can be used to alter this
behavior.  In the deserializer, the parse_constant parameter can be used to
alter this behavior.

Repeated Names Within an Object

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:

>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}

The object_pairs_hook parameter can be used to alter this behavior.

Top-level Non-Object, Non-Array Values


````

### Top 2 / META-T02-C-2
Chunk 1518a830ffa51073f7b6bbb60fc3a999; source https://docs.python.org/3.13/library/json.html; page library_json:u002; type library_reference; version 3.13; offsets [0,950).

````text
Note

This module’s encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

Basic Usage

json. dump ( obj , fp , * , skipkeys = False , ensure_ascii = True , check_circular = True , allow_nan = True , cls = None , indent = None , separators = None , default = None , sort_keys = False , ** kw )

Serialize obj as a JSON formatted stream to fp (a .write() -supporting file-like object ) using this Python-to-JSON conversion table .

Note

Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.

Parameters :

obj ( object ) – The Python object to be serialized.

fp ( file-like object ) – The file-like object obj will be serialized to.
The json module always produces str objects,
not bytes objects,
therefore fp.write() must support str input.


````

### Top 3 / META-T02-C-3
Chunk 179f653d550e60385e5543d0814707f9; source https://docs.python.org/3.13/library/json.html; page library_json:u001; type library_reference; version 3.13; offsets [895,1633).

````text
>>> import json
>>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
'["foo", {"bar": ["baz", null, 1.0, 2]}]'
>>> print(json.dumps("\"foo\bar"))
"\"foo\bar"
>>> print(json.dumps('\u1234'))
"\u1234"
>>> print(json.dumps('\\'))
"\\"
>>> print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
{"a": 0, "b": 0, "c": 0}
>>> from io import StringIO
>>> io = StringIO()
>>> json.dump(['streaming API'], io)
>>> io.getvalue()
'["streaming API"]'

Compact encoding:

>>> import json
>>> json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
'[1,2,3,{"4":5,"6":7}]'

Pretty printing:

>>> import json
>>> print(json.dumps({'6': 7, '4': 5}, sort_keys=True, indent=4))
{
    "4": 5,
    "6": 7
}

Customizing JSON object encoding:


````

Nhãn grounding bản chính: 2/2. Sau filter, cảnh báo đầy đủ ở top-2 library_json:u002; không suy diễn từ repeated property names ở top-1.

## GRD-T03-A: grounding và metadata top-3
Câu hỏi: What does the standard JSON decoder do by default when an object repeats the same property name?
Đáp án dự kiến: It does not raise an exception and retains only the last name-value pair.
Gold: library_json / library_json:u006

````text
The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:
````

Filter người dùng: {}; filter thực tế: {}
### Top 1 / META-T03-A-1
Chunk 8208acc55e5af214db1aa6b26255e675; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [2700,3200).

````text
deserializer, the parse_constant parameter can be used to
alter this behavior.

Repeated Names Within an Object

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:

>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}

The object_pairs_hook parameter c
````

### Top 2 / META-T03-A-2
Chunk d22ad588f84c078e722b9b6e536b85ca; source https://docs.python.org/3.13/library/json.html; page library_json:u003; type library_reference; version 3.13; offsets [900,1400).

````text
 be deserialized.

cls (a JSONDecoder subclass) – If set, a custom JSON decoder.
Additional keyword arguments to load() will be passed to the constructor of cls .
If None (the default), JSONDecoder is used.

object_hook ( callable | None) – If set, a function that is called with the result of
any JSON object literal decoded (a dict ).
The return value of this function will be used
instead of the dict .
This feature can be used to implement custom decoders,
for example JSON-RPC class hinting.
Def
````

### Top 3 / META-T03-A-3
Chunk 31b207eab38964bdc9c03f21128da40f; source https://docs.python.org/3.13/library/json.html; page library_json:u002; type library_reference; version 3.13; offsets [1800,2300).

````text
 True (the default), their JavaScript equivalents
( NaN , Infinity , -Infinity ) are used.

cls (a JSONEncoder subclass) – If set, a custom JSON encoder with the default() method overridden,
for serializing into custom datatypes.
If None (the default), JSONEncoder is used.

indent ( int | str | None ) – If a positive integer or string, JSON array elements and
object members will be pretty-printed with that indent level.
A positive integer indents that many spaces per level;
a string (such as "\t
````

Nhãn grounding bản chính: 2/2. Top-1 library_json:u006 nói mặc định không raise, giữ cặp cuối, có ví dụ x=1,2,3 cho kết quả x=3.

## GRD-T03-B: grounding và metadata top-3
Câu hỏi: What does the standard JSON decoder do by default when an object repeats the same property name?
Đáp án dự kiến: It does not raise an exception and retains only the last name-value pair.
Gold: library_json / library_json:u006

````text
The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:
````

Filter người dùng: {}; filter thực tế: {}
### Top 1 / META-T03-B-1
Chunk 22a33164b5b126c8bb870cf295a6ff14; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [2613,3276).

````text
In the serializer, the allow_nan parameter can be used to alter this
behavior.  In the deserializer, the parse_constant parameter can be used to
alter this behavior.

Repeated Names Within an Object

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:

>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}

The object_pairs_hook parameter can be used to alter this behavior.

Top-level Non-Object, Non-Array Values


````

### Top 2 / META-T03-B-2
Chunk 0ef03621eb09e12a35369c6cd374505e; source https://docs.python.org/3.13/library/json.html; page library_json:u003; type library_reference; version 3.13; offsets [919,1770).

````text
cls (a JSONDecoder subclass) – If set, a custom JSON decoder.
Additional keyword arguments to load() will be passed to the constructor of cls .
If None (the default), JSONDecoder is used.

object_hook ( callable | None) – If set, a function that is called with the result of
any JSON object literal decoded (a dict ).
The return value of this function will be used
instead of the dict .
This feature can be used to implement custom decoders,
for example JSON-RPC class hinting.
Default None .

object_pairs_hook ( callable | None) – If set, a function that is called with the result of
any JSON object literal decoded with an ordered list of pairs.
The return value of this function will be used
instead of the dict .
This feature can be used to implement custom decoders.
If object_hook is also set, object_pairs_hook takes priority.
Default None .


````

### Top 3 / META-T03-B-3
Chunk 40e36e5259738af72f874b9b3c276b75; source https://docs.python.org/3.13/library/json.html; page library_json:u004; type library_reference; version 3.13; offsets [1868,2823).

````text
parse_constant is an optional function that will be called with one of the
following strings: '-Infinity' , 'Infinity' , 'NaN' .  This can be
used to raise an exception if invalid JSON numbers are encountered.

If strict is false ( True is the default), then control characters
will be allowed inside strings.  Control characters in this context are
those with character codes in the 0–31 range, including '\t' (tab), '\n' , '\r' and '\0' .

If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised.

Changed in version 3.6: All parameters are now keyword-only .

decode ( s )

Return the Python representation of s (a str instance
containing a JSON document).

JSONDecodeError will be raised if the given JSON document is not
valid.

raw_decode ( s )

Decode a JSON document from s (a str beginning with a
JSON document) and return a 2-tuple of the Python representation
and the index in s where the document ended.


````

Nhãn grounding bản chính: 2/2. Top-1 có cả điều kiện mặc định và hành vi giữ cặp tên-giá trị cuối; object_pairs_hook được nêu là cách thay đổi hành vi.

## GRD-T03-C: grounding và metadata top-3
Câu hỏi: What does the standard JSON decoder do by default when an object repeats the same property name?
Đáp án dự kiến: It does not raise an exception and retains only the last name-value pair.
Gold: library_json / library_json:u006

````text
The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:
````

Filter người dùng: {}; filter thực tế: {}
### Top 1 / META-T03-C-1
Chunk 22a33164b5b126c8bb870cf295a6ff14; source https://docs.python.org/3.13/library/json.html; page library_json:u006; type library_reference; version 3.13; offsets [2613,3276).

````text
In the serializer, the allow_nan parameter can be used to alter this
behavior.  In the deserializer, the parse_constant parameter can be used to
alter this behavior.

Repeated Names Within an Object

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:

>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}

The object_pairs_hook parameter can be used to alter this behavior.

Top-level Non-Object, Non-Array Values


````

### Top 2 / META-T03-C-2
Chunk 0ef03621eb09e12a35369c6cd374505e; source https://docs.python.org/3.13/library/json.html; page library_json:u003; type library_reference; version 3.13; offsets [919,1770).

````text
cls (a JSONDecoder subclass) – If set, a custom JSON decoder.
Additional keyword arguments to load() will be passed to the constructor of cls .
If None (the default), JSONDecoder is used.

object_hook ( callable | None) – If set, a function that is called with the result of
any JSON object literal decoded (a dict ).
The return value of this function will be used
instead of the dict .
This feature can be used to implement custom decoders,
for example JSON-RPC class hinting.
Default None .

object_pairs_hook ( callable | None) – If set, a function that is called with the result of
any JSON object literal decoded with an ordered list of pairs.
The return value of this function will be used
instead of the dict .
This feature can be used to implement custom decoders.
If object_hook is also set, object_pairs_hook takes priority.
Default None .


````

### Top 3 / META-T03-C-3
Chunk 40e36e5259738af72f874b9b3c276b75; source https://docs.python.org/3.13/library/json.html; page library_json:u004; type library_reference; version 3.13; offsets [1868,2823).

````text
parse_constant is an optional function that will be called with one of the
following strings: '-Infinity' , 'Infinity' , 'NaN' .  This can be
used to raise an exception if invalid JSON numbers are encountered.

If strict is false ( True is the default), then control characters
will be allowed inside strings.  Control characters in this context are
those with character codes in the 0–31 range, including '\t' (tab), '\n' , '\r' and '\0' .

If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised.

Changed in version 3.6: All parameters are now keyword-only .

decode ( s )

Return the Python representation of s (a str instance
containing a JSON document).

JSONDecodeError will be raised if the given JSON document is not
valid.

raw_decode ( s )

Decode a JSON document from s (a str beginning with a
JSON document) and return a 2-tuple of the Python representation
and the index in s where the document ended.


````

Nhãn grounding bản chính: 2/2. T03 không có filter, top-3 giống B; top-1 chứa đầy đủ hành vi mặc định cần trả lời.

## GRD-T04-A: grounding và metadata top-3
Câu hỏi: How is Python None written by csv.writer, and is that conversion reversible?
Đáp án dự kiến: As an empty string; this is not reversible.
Gold: library_csv / library_csv:u001

````text
To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string.  While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the data returned from a cursor.fetch* call.
````

Filter người dùng: {}; filter thực tế: {}
### Top 1 / META-T04-A-1
Chunk 938b5b04e54104f0764573d20ed46e74; source https://docs.python.org/3.13/library/csv.html; page library_csv:u005; type library_reference; version 3.13; offsets [2700,3200).

````text
ngs or numbers (by passing them through str() first) for DictWriter objects.  Note that complex numbers are written
out surrounded by parens. This may cause some problems for other programs which
read CSV files (assuming they support complex numbers at all).

csvwriter. writerow ( row , / )

Write the row parameter to the writer’s file object, formatted according
to the current Dialect . Return the return value of the call to the write method of the underlying file object.

Changed in version 3.
````

### Top 2 / META-T04-A-2
Chunk 88feb8ae650ec409caf10437f22e345c; source https://docs.python.org/3.13/library/csv.html; page library_csv:u001; type library_reference; version 3.13; offsets [3600,4100).

````text
mtparams keyword arguments
can be given to override individual formatting parameters in the current
dialect.  For full details about dialects and formatting parameters, see
the Dialects and Formatting Parameters section. To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string.  While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the data returned
````

### Top 3 / META-T04-A-3
Chunk b2b8f0568492e7e8298eda5943d125e7; source https://docs.python.org/3.13/library/csv.html; page library_csv:u006; type library_reference; version 3.13; offsets [0,500).

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV f
````

Nhãn grounding bản chính: 2/2. Top-2 library_csv:u001 ghi None thành chuỗi rỗng và chuyển đổi không đảo ngược. Thiếu đuôi quote về cursor.fetch* không làm thiếu hai ý của câu hỏi; strict hit vẫn giữ 0.

## GRD-T04-B: grounding và metadata top-3
Câu hỏi: How is Python None written by csv.writer, and is that conversion reversible?
Đáp án dự kiến: As an empty string; this is not reversible.
Gold: library_csv / library_csv:u001

````text
To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string.  While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the data returned from a cursor.fetch* call.
````

Filter người dùng: {}; filter thực tế: {}
### Top 1 / META-T04-B-1
Chunk 0872e85a8dd2148cd5725b262428a227; source https://docs.python.org/3.13/library/csv.html; page library_csv:u006; type library_reference; version 3.13; offsets [0,884).

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV file:

import csv
with open('some.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

Reading a file with an alternate format:

import csv
with open('passwd', newline='') as f:
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)

The corresponding simplest possible writing example is:


````

### Top 2 / META-T04-B-2
Chunk 2788ee6e34ada6b0c2c01ee5bf11f7b1; source https://docs.python.org/3.13/library/csv.html; page library_csv:u004; type library_reference; version 3.13; offsets [0,796).

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric fields.

Instructs reader objects to convert all non-quoted fields to type float .

Note

Some numeric types, such as bool , Fraction ,
or IntEnum , have a string representation that cannot be
converted to float .
They cannot be read in the QUOTE_NONNUMERIC and QUOTE_STRINGS modes.

csv. QUOTE_NONE


````

### Top 3 / META-T04-B-3
Chunk 8868ac10d3e8c519c490492c62dea798; source https://docs.python.org/3.13/library/csv.html; page library_csv:u001; type library_reference; version 3.13; offsets [3088,4087).

````text
Return a writer object responsible for converting the user’s data into delimited
strings on the given file-like object. csvfile can be any object with a write() method.  If csvfile is a file object, it should be opened with newline='' [ 1 ] .  An optional dialect parameter can be given which is used to define a set of parameters specific to a
particular CSV dialect.  It may be an instance of a subclass of the Dialect class or one of the strings returned by the list_dialects() function.  The other optional fmtparams keyword arguments
can be given to override individual formatting parameters in the current
dialect.  For full details about dialects and formatting parameters, see
the Dialects and Formatting Parameters section. To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string.  While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the 
````

Nhãn grounding bản chính: 2/2. Top-3 library_csv:u001 có đủ None -> empty string và not reversible. Gold quote bị cắt ở đoạn giải thích SQL cursor, nên strict miss không đồng nghĩa thiếu thông tin trả lời.

## GRD-T04-C: grounding và metadata top-3
Câu hỏi: How is Python None written by csv.writer, and is that conversion reversible?
Đáp án dự kiến: As an empty string; this is not reversible.
Gold: library_csv / library_csv:u001

````text
To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string.  While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the data returned from a cursor.fetch* call.
````

Filter người dùng: {}; filter thực tế: {}
### Top 1 / META-T04-C-1
Chunk 0872e85a8dd2148cd5725b262428a227; source https://docs.python.org/3.13/library/csv.html; page library_csv:u006; type library_reference; version 3.13; offsets [0,884).

````text
DictWriter objects have the following public method:

DictWriter. writeheader ( )

Write a row with the field names (as specified in the constructor) to
the writer’s file object, formatted according to the current dialect. Return
the return value of the csvwriter.writerow() call used internally.

Added in version 3.2.

Changed in version 3.8: writeheader() now also returns the value returned by
the csvwriter.writerow() method it uses internally.

Examples

The simplest example of reading a CSV file:

import csv
with open('some.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

Reading a file with an alternate format:

import csv
with open('passwd', newline='') as f:
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)

The corresponding simplest possible writing example is:


````

### Top 2 / META-T04-C-2
Chunk 2788ee6e34ada6b0c2c01ee5bf11f7b1; source https://docs.python.org/3.13/library/csv.html; page library_csv:u004; type library_reference; version 3.13; offsets [0,796).

````text
The csv module defines the following constants:

csv. QUOTE_ALL

Instructs writer objects to quote all fields.

csv. QUOTE_MINIMAL

Instructs writer objects to only quote those fields which contain
special characters such as delimiter , quotechar , '\r' , '\n' or any of the characters in lineterminator .
If doublequote is False and escapechar is set,
the quotechar is escaped instead of causing the field to be quoted.

csv. QUOTE_NONNUMERIC

Instructs writer objects to quote all non-numeric fields.

Instructs reader objects to convert all non-quoted fields to type float .

Note

Some numeric types, such as bool , Fraction ,
or IntEnum , have a string representation that cannot be
converted to float .
They cannot be read in the QUOTE_NONNUMERIC and QUOTE_STRINGS modes.

csv. QUOTE_NONE


````

### Top 3 / META-T04-C-3
Chunk 8868ac10d3e8c519c490492c62dea798; source https://docs.python.org/3.13/library/csv.html; page library_csv:u001; type library_reference; version 3.13; offsets [3088,4087).

````text
Return a writer object responsible for converting the user’s data into delimited
strings on the given file-like object. csvfile can be any object with a write() method.  If csvfile is a file object, it should be opened with newline='' [ 1 ] .  An optional dialect parameter can be given which is used to define a set of parameters specific to a
particular CSV dialect.  It may be an instance of a subclass of the Dialect class or one of the strings returned by the list_dialects() function.  The other optional fmtparams keyword arguments
can be given to override individual formatting parameters in the current
dialect.  For full details about dialects and formatting parameters, see
the Dialects and Formatting Parameters section. To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string.  While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the 
````

Nhãn grounding bản chính: 2/2. Không filter ở T04, kết quả giống B; đủ hai ý trong top-3. Đây là nhận xét ngữ nghĩa, không sửa strict metrics.

## GRD-T05-A: grounding và metadata top-3
Câu hỏi: In the library reference, does Path.mkdir(exist_ok=True) accept an existing path that is a regular file rather than a directory?
Đáp án dự kiến: No; FileExistsError is still raised if the path exists and is not a directory.
Gold: library_pathlib / library_pathlib:u011

````text
If exist_ok is true, FileExistsError will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX mkdir -p command).
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {}
### Top 1 / META-T05-A-1
Chunk 5ef5dddcfcc30f04ce398f9fccb4d39c; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u011; type library_reference; version 3.13; offsets [3150,3586).

````text
thout taking mode into account (mimicking the POSIX mkdir -p command).

If parents is false (the default), a missing parent raises FileNotFoundError .

If exist_ok is false (the default), FileExistsError is
raised if the target directory already exists.

If exist_ok is true, FileExistsError will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX mkdir -p command).
````

### Top 2 / META-T05-A-2
Chunk 489d947fdcc9a62e83df21397a354599; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u011; type library_reference; version 3.13; offsets [2700,3200).

````text
bytes() methods are often used to create files.

Path. mkdir ( mode = 0o777 , parents = False , exist_ok = False )

Create a new directory at this given path.  If mode is given, it is
combined with the process’s umask value to determine the file mode
and access flags.  If the path already exists, FileExistsError is raised.

If parents is true, any missing parents of this path are created
as needed; they are created with the default permissions without taking mode into account (mimicking the POSI
````

### Top 3 / META-T05-A-3
Chunk bbe5ee91cc177a12a1e7fd2d50dbc48f; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u011; type library_reference; version 3.13; offsets [2250,2750).

````text
n 3.12.

Creating files and directories

Path. touch ( mode = 0o666 , exist_ok = True )

Create a file at this given path.  If mode is given, it is combined
with the process’s umask value to determine the file mode and access
flags.  If the file already exists, the function succeeds when exist_ok is true (and its modification time is updated to the current time),
otherwise FileExistsError is raised.

See also

The open() , write_text() and write_bytes() methods are often used to create files.

P
````

Nhãn grounding bản chính: 2/2. Top-1 library_pathlib:u011 giữ đủ ngoại lệ: exist_ok=true vẫn raise khi đường dẫn tồn tại nhưng không phải directory; top-2 có chữ ký Path.mkdir để đối chiếu.

## GRD-T05-B: grounding và metadata top-3
Câu hỏi: In the library reference, does Path.mkdir(exist_ok=True) accept an existing path that is a regular file rather than a directory?
Đáp án dự kiến: No; FileExistsError is still raised if the path exists and is not a directory.
Gold: library_pathlib / library_pathlib:u011

````text
If exist_ok is true, FileExistsError will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX mkdir -p command).
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {}
### Top 1 / META-T05-B-1
Chunk a02e2af23332ec724e9076ce0acc2993; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u011; type library_reference; version 3.13; offsets [2664,3586).

````text
The open() , write_text() and write_bytes() methods are often used to create files.

Path. mkdir ( mode = 0o777 , parents = False , exist_ok = False )

Create a new directory at this given path.  If mode is given, it is
combined with the process’s umask value to determine the file mode
and access flags.  If the path already exists, FileExistsError is raised.

If parents is true, any missing parents of this path are created
as needed; they are created with the default permissions without taking mode into account (mimicking the POSIX mkdir -p command).

If parents is false (the default), a missing parent raises FileNotFoundError .

If exist_ok is false (the default), FileExistsError is
raised if the target directory already exists.

If exist_ok is true, FileExistsError will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX mkdir -p command).
````

### Top 2 / META-T05-B-2
Chunk bfae74873985957a25dcb5442022c65b; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u012; type library_reference; version 3.13; offsets [0,959).

````text
Changed in version 3.5: The exist_ok parameter was added.

Path. symlink_to ( target , target_is_directory = False )

Make this path a symbolic link pointing to target .

On Windows, a symlink represents either a file or a directory, and does not
morph to the target dynamically.  If the target is present, the type of the
symlink will be created to match. Otherwise, the symlink will be created
as a directory if target_is_directory is true or a file symlink (the
default) otherwise.  On non-Windows platforms, target_is_directory is ignored.

>>> p = Path('mylink')
>>> p.symlink_to('setup.py')
>>> p.resolve()
PosixPath('/home/antoine/pathlib/setup.py')
>>> p.stat().st_size
956
>>> p.lstat().st_size
8

Note

The order of arguments (link, target) is the reverse
of os.symlink() ’s.

Changed in version 3.13: Raises UnsupportedOperation if os.symlink() is not
available. In previous versions, NotImplementedError was raised.

Path. hardlink_to ( target )


````

### Top 3 / META-T05-B-3
Chunk fef467f56a4944f9eeb9c345015aba65; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u014; type library_reference; version 3.13; offsets [2758,3653).

````text
os.path.isdir()

Path.is_dir()

os.path.islink()

Path.is_symlink()

os.path.isjunction()

Path.is_junction()

os.path.ismount()

Path.is_mount()

os.path.samefile()

Path.samefile()

os.getcwd()

Path.cwd()

os.stat()

Path.stat()

os.lstat()

Path.lstat()

os.listdir()

Path.iterdir()

os.walk()

Path.walk() [ 4 ]

os.mkdir() , os.makedirs()

Path.mkdir()

os.link()

Path.hardlink_to()

os.symlink()

Path.symlink_to()

os.readlink()

Path.readlink()

os.rename()

Path.rename()

os.replace()

Path.replace()

os.remove() , os.unlink()

Path.unlink()

os.rmdir()

Path.rmdir()

os.chmod()

Path.chmod()

os.lchmod()

Path.lchmod()

Footnotes

os.path.relpath() calls abspath() to make paths
absolute and remove “ .. ” parts, whereas PurePath.relative_to() is a lexical operation that raises ValueError when its inputs’
anchors differ (e.g. if one path is absolute and the other relative.)


````

Nhãn grounding bản chính: 2/2. Top-1 có chữ ký mkdir, các mặc định và ngoại lệ path tồn tại không phải directory; không nhầm với touch ở cùng trang.

## GRD-T05-C: grounding và metadata top-3
Câu hỏi: In the library reference, does Path.mkdir(exist_ok=True) accept an existing path that is a regular file rather than a directory?
Đáp án dự kiến: No; FileExistsError is still raised if the path exists and is not a directory.
Gold: library_pathlib / library_pathlib:u011

````text
If exist_ok is true, FileExistsError will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX mkdir -p command).
````

Filter người dùng: {'document_type': 'library_reference'}; filter thực tế: {'document_type': 'library_reference'}
### Top 1 / META-T05-C-1
Chunk a02e2af23332ec724e9076ce0acc2993; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u011; type library_reference; version 3.13; offsets [2664,3586).

````text
The open() , write_text() and write_bytes() methods are often used to create files.

Path. mkdir ( mode = 0o777 , parents = False , exist_ok = False )

Create a new directory at this given path.  If mode is given, it is
combined with the process’s umask value to determine the file mode
and access flags.  If the path already exists, FileExistsError is raised.

If parents is true, any missing parents of this path are created
as needed; they are created with the default permissions without taking mode into account (mimicking the POSIX mkdir -p command).

If parents is false (the default), a missing parent raises FileNotFoundError .

If exist_ok is false (the default), FileExistsError is
raised if the target directory already exists.

If exist_ok is true, FileExistsError will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX mkdir -p command).
````

### Top 2 / META-T05-C-2
Chunk bfae74873985957a25dcb5442022c65b; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u012; type library_reference; version 3.13; offsets [0,959).

````text
Changed in version 3.5: The exist_ok parameter was added.

Path. symlink_to ( target , target_is_directory = False )

Make this path a symbolic link pointing to target .

On Windows, a symlink represents either a file or a directory, and does not
morph to the target dynamically.  If the target is present, the type of the
symlink will be created to match. Otherwise, the symlink will be created
as a directory if target_is_directory is true or a file symlink (the
default) otherwise.  On non-Windows platforms, target_is_directory is ignored.

>>> p = Path('mylink')
>>> p.symlink_to('setup.py')
>>> p.resolve()
PosixPath('/home/antoine/pathlib/setup.py')
>>> p.stat().st_size
956
>>> p.lstat().st_size
8

Note

The order of arguments (link, target) is the reverse
of os.symlink() ’s.

Changed in version 3.13: Raises UnsupportedOperation if os.symlink() is not
available. In previous versions, NotImplementedError was raised.

Path. hardlink_to ( target )


````

### Top 3 / META-T05-C-3
Chunk fef467f56a4944f9eeb9c345015aba65; source https://docs.python.org/3.13/library/pathlib.html; page library_pathlib:u014; type library_reference; version 3.13; offsets [2758,3653).

````text
os.path.isdir()

Path.is_dir()

os.path.islink()

Path.is_symlink()

os.path.isjunction()

Path.is_junction()

os.path.ismount()

Path.is_mount()

os.path.samefile()

Path.samefile()

os.getcwd()

Path.cwd()

os.stat()

Path.stat()

os.lstat()

Path.lstat()

os.listdir()

Path.iterdir()

os.walk()

Path.walk() [ 4 ]

os.mkdir() , os.makedirs()

Path.mkdir()

os.link()

Path.hardlink_to()

os.symlink()

Path.symlink_to()

os.readlink()

Path.readlink()

os.rename()

Path.rename()

os.replace()

Path.replace()

os.remove() , os.unlink()

Path.unlink()

os.rmdir()

Path.rmdir()

os.chmod()

Path.chmod()

os.lchmod()

Path.lchmod()

Footnotes

os.path.relpath() calls abspath() to make paths
absolute and remove “ .. ” parts, whereas PurePath.relative_to() is a lexical operation that raises ValueError when its inputs’
anchors differ (e.g. if one path is absolute and the other relative.)


````

Nhãn grounding bản chính: 2/2. Top-1 như B, có đúng điều kiện exist_ok và loại đường dẫn. Metadata library_reference phù hợp yêu cầu người dùng.

## GOLD-D01: gold
What happens if list.remove(value) cannot find that value?
Đáp án: It raises ValueError.
Nguồn: tutorial_datastructures / tutorial_datastructures:u001

````text
Remove the first item from the list whose value is equal to value .  It raises a ValueError if there is no such item.
````


## GOLD-D02: gold
In the tutorial, which container supports a queue with fast appends and pops at either end?
Đáp án: collections.deque.
Nguồn: tutorial_datastructures / tutorial_datastructures:u002

````text
To implement a queue, use collections.deque which was designed to
have fast appends and pops from both ends.  For example:
````


## GOLD-D03: gold
Under what condition can a tuple be used as a dictionary key, and what disqualifies it?
Đáp án: Its contents must be immutable; a mutable object directly or indirectly inside it disqualifies it.
Nguồn: tutorial_datastructures / tutorial_datastructures:u004

````text
Tuples can be used
as keys if they contain only strings, numbers, or tuples; if a tuple contains
any mutable object either directly or indirectly, it cannot be used as a key.
````


## GOLD-D04: gold
How can I test whether a single key is present in a dictionary?
Đáp án: Use the in keyword.
Nguồn: tutorial_datastructures / tutorial_datastructures:u005

````text
To check whether a single key is in the
dictionary, use the in keyword.
````


## GOLD-D05: gold
How can I iterate over a sequence's distinct elements in sorted order?
Đáp án: Combine sorted() with set().
Nguồn: tutorial_datastructures / tutorial_datastructures:u006

````text
Using set() on a sequence eliminates duplicate elements. The use of sorted() in combination with set() over a sequence is an idiomatic
way to loop over unique elements of the sequence in sorted order.
````


## GOLD-D06: gold
According to the tutorial, why can a list used as a default argument keep values between function calls?
Đáp án: The default is evaluated only once, so the mutable default can accumulate arguments across calls.
Nguồn: tutorial_controlflow / tutorial_controlflow:u006

````text
Important warning: The default value is evaluated only once. This makes a
difference when the default is a mutable object such as a list, dictionary, or
instances of most classes.  For example, the following function accumulates the
arguments passed to it on subsequent calls:
````


## GOLD-D07: gold
Does range include its specified end point?
Đáp án: No; the given end point is excluded.
Nguồn: tutorial_controlflow / tutorial_controlflow:u001

````text
The given end point is never part of the generated sequence;
````


## GOLD-D08: gold
When does the else clause of a for or while loop execute in relation to break?
Đáp án: When the loop finishes without executing break.
Nguồn: tutorial_controlflow / tutorial_controlflow:u002

````text
In a for or while loop the break statement
may be paired with an else clause.  If the loop finishes without
executing the break , the else clause executes.
````


## GOLD-D09: gold
When a module file is executed as a script, what value is assigned to __name__?
Đáp án: __main__.
Nguồn: tutorial_modules / tutorial_modules:u002

````text
the code in the module will be executed, just as if you imported it, but with
the __name__ set to "__main__" .  That means that by adding this code at
the end of your module:
````


## GOLD-D10: gold
What names does from module import * exclude, and why is this generally discouraged?
Đáp án: It excludes names starting with underscore and may introduce unknown names that hide existing names.
Nguồn: tutorial_modules / tutorial_modules:u002

````text
This imports all names except those beginning with an underscore ( _ ).
In most cases Python programmers do not use this facility since it introduces
an unknown set of names into the interpreter, possibly hiding some things
you have already defined.
````


## GOLD-D11: gold
Where does Python cache a module's compiled code to speed loading?
Đáp án: In the __pycache__ directory.
Nguồn: tutorial_modules / tutorial_modules:u003

````text
To speed up loading modules, Python caches the compiled version of each module
in the __pycache__ directory
````


## GOLD-D12: gold
In the tutorial's file handling guidance, what encoding is recommended for text files unless another is needed?
Đáp án: Explicit encoding='utf-8'.
Nguồn: tutorial_inputoutput / tutorial_inputoutput:u003

````text
Because UTF-8 is the modern de-facto standard, encoding="utf-8" is
recommended unless you know that you need to use a different encoding.
````


## GOLD-D13: gold
Why should I use with when working with a file, even if the block may raise an exception?
Đáp án: The file is properly closed when the suite finishes, even if an exception occurs.
Nguồn: tutorial_inputoutput / tutorial_inputoutput:u004

````text
It is good practice to use the with keyword when dealing
with file objects.  The advantage is that the file is properly closed
after its suite finishes, even if an exception is raised at some
point.
````


## GOLD-D14: gold
What is the name for converting a Python data hierarchy into a JSON string, and the reverse operation?
Đáp án: Serializing and deserializing, respectively.
Nguồn: tutorial_inputoutput / tutorial_inputoutput:u005

````text
The standard module called json can take Python
data hierarchies, and convert them to string representations; this process is
called serializing .  Reconstructing the data from the string representation
is called deserializing .
````


## GOLD-D15: gold
Why put success-only code in try/except's else clause rather than inside try?
Đáp án: It avoids accidentally catching exceptions from code outside the intended protected operation.
Nguồn: tutorial_errors / tutorial_errors:u003

````text
The use of the else clause is better than adding additional code to
the try clause because it avoids accidentally catching an exception
that wasn’t raised by the code being protected by the try … except statement.
````


## GOLD-T01: gold
In the library reference, what resource risk comes from parsing untrusted JSON, and what precaution is advised?
Đáp án: A malicious JSON string may consume considerable CPU and memory; limit the size of input.
Nguồn: library_json / library_json:u001

````text
Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.
````


## GOLD-T02: gold
In the library reference, why do repeated json.dump calls on the same file produce invalid JSON?
Đáp án: JSON is not a framed protocol; repeated serialization of multiple objects to the same file is invalid.
Nguồn: library_json / library_json:u002

````text
Unlike pickle and marshal , JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to dump() using the same fp will result in an invalid JSON file.
````


## GOLD-T03: gold
What does the standard JSON decoder do by default when an object repeats the same property name?
Đáp án: It does not raise an exception and retains only the last name-value pair.
Nguồn: library_json / library_json:u006

````text
The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:
````


## GOLD-T04: gold
How is Python None written by csv.writer, and is that conversion reversible?
Đáp án: As an empty string; this is not reversible.
Nguồn: library_csv / library_csv:u001

````text
To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string.  While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the data returned from a cursor.fetch* call.
````


## GOLD-T05: gold
In the library reference, does Path.mkdir(exist_ok=True) accept an existing path that is a regular file rather than a directory?
Đáp án: No; FileExistsError is still raised if the path exists and is not a directory.
Nguồn: library_pathlib / library_pathlib:u011

````text
If exist_ok is true, FileExistsError will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX mkdir -p command).
````

