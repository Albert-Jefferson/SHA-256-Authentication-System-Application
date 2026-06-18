# -*- coding: utf-8 -*-
"""Noi dung chi tiet bao cao - duoc generate_report.py su dung de tao DOCX."""

TABLE_OF_CONTENTS = [
    "DANH MỤC CÁC TỪ VIẾT TẮT",
    "LỜI MỞ ĐẦU",
    "CHƯƠNG 1. CƠ SỞ LÝ THUYẾT",
    "    1.1 Tổng quan về hàm băm mật mã",
    "        1.1.1 Khái niệm hàm băm và các tính chất bảo mật",
    "        1.1.2 Ứng dụng hàm băm trong bảo mật thông tin",
    "        1.1.3 Rủi ro khi lưu mật khẩu dạng plaintext",
    "    1.2 Thuật toán băm SHA-256",
    "        1.2.1 Lịch sử và vị trí trong họ SHA-2",
    "        1.2.2 Nguyên lý hoạt động và cấu trúc khối",
    "        1.2.3 Độ an toàn, hạn chế và so sánh với các thuật toán khác",
    "    1.3 Salt, pepper và phòng chống tấn công",
    "        1.3.1 Khái niệm salt và vai trò trong lưu trữ mật khẩu",
    "        1.3.2 Rainbow table và dictionary attack",
    "        1.3.3 Brute-force attack và timing attack",
    "        1.3.4 Pepper và các lớp bảo vệ bổ sung",
    "    1.4 PBKDF2-HMAC-SHA256 và lưu trữ mật khẩu an toàn",
    "        1.4.1 HMAC và vai trò của SHA-256 trong PBKDF2",
    "        1.4.2 Cơ chế PBKDF2",
    "        1.4.3 So sánh SHA-256 thuần và PBKDF2-HMAC-SHA256",
    "    1.5 Xác thực người dùng và mô hình đe dọa bảo mật",
    "        1.5.1 Khái niệm xác thực (authentication)",
    "        1.5.2 Luồng đăng ký và đăng nhập an toàn",
    "        1.5.3 Các mối đe dọa khi lưu trữ mật khẩu",
    "CHƯƠNG 2. THIẾT KẾ VÀ XÂY DỰNG HỆ THỐNG",
    "    2.1 Phân tích yêu cầu đề tài",
    "    2.2 Kiến trúc tổng thể và mô hình triển khai",
    "    2.3 Công nghệ, công cụ và cấu trúc mã nguồn",
    "    2.4 Thiết kế cơ sở dữ liệu SQLite",
    "    2.5 Module xử lý mật khẩu (password_hasher.py)",
    "    2.6 Module minh họa SHA-256 thuần (hash256_salt.py)",
    "    2.7 Tầng dữ liệu và nghiệp vụ (Database.py)",
    "    2.8 REST API và giao diện web (app.py, index.html)",
    "    2.9 Các biện pháp bảo mật bổ sung",
    "CHƯƠNG 3. KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ",
    "    3.1 Môi trường thử nghiệm và phương pháp kiểm thử",
    "    3.2 Thực nghiệm đăng ký và đăng nhập",
    "    3.3 Kiểm chứng không khôi phục được mật khẩu từ hash",
    "    3.4 So sánh hiệu quả khi có và không có salt",
    "    3.5 Kịch bản kiểm thử tấn công brute-force",
    "        3.5.1 Mục tiêu và phạm vi kiểm thử",
    "        3.5.2 Tấn công hệ thống không dùng salt",
    "        3.5.3 Tấn công hệ thống có dùng salt",
    "        3.5.4 So sánh kết quả và phân tích",
    "        3.5.5 Thực nghiệm bổ sung trên hệ thống PBKDF2",
    "    3.6 Kết quả unit test và API test",
    "    3.7 Đánh giá mức độ đáp ứng yêu cầu đề tài",
    "    3.8 Hạn chế và hướng phát triển",
    "    3.9 Hướng dẫn chạy thử nghiệm tái lập kết quả",
    "CHƯƠNG 4. KẾT LUẬN VÀ TÀI LIỆU THAM KHẢO",
]

ABBREVIATIONS = [
    ("API", "Application Programming Interface — giao diện lập trình ứng dụng"),
    ("CORS", "Cross-Origin Resource Sharing — chia sẻ tài nguyên đa nguồn"),
    ("DB", "Database — cơ sở dữ liệu"),
    ("GPU", "Graphics Processing Unit — đơn vị xử lý đồ họa, dùng crack hash"),
    ("HMAC", "Hash-based Message Authentication Code"),
    ("HTTP", "HyperText Transfer Protocol"),
    ("IV", "Initialization Vector — vectơ khởi tạo"),
    ("JSON", "JavaScript Object Notation"),
    ("NIST", "National Institute of Standards and Technology"),
    ("OWASP", "Open Web Application Security Project"),
    ("PBKDF2", "Password-Based Key Derivation Function 2"),
    ("PRF", "Pseudo-Random Function"),
    ("REST", "Representational State Transfer"),
    ("RFC", "Request for Comments — chuẩn kỹ thuật Internet"),
    ("SHA", "Secure Hash Algorithm"),
    ("SQL", "Structured Query Language"),
    ("UUID", "Universally Unique Identifier"),
]

INTRODUCTION = [
    (
        "Trong thời đại chuyển đổi số, hầu hết dịch vụ trực tuyến — từ ngân hàng, thương mại điện tử, mạng xã hội "
        "đến hệ thống quản lý nội bộ — đều yêu cầu người dùng xác thực danh tính thông qua tên đăng nhập và mật khẩu. "
        "Mật khẩu là lớp bảo vệ đầu tiên nhưng đồng thời là điểm yếu phổ biến nhất: người dùng thường chọn mật khẩu dễ "
        "đoán, tái sử dụng mật khẩu trên nhiều dịch vụ, hoặc hệ thống lưu trữ mật khẩu không đúng cách. Khi cơ sở dữ liệu "
        "bị rò rỉ, hàng triệu tài khoản có thể bị xâm phạm chỉ trong vài giờ nếu mật khẩu được lưu dưới dạng văn bản thuần "
        "(plaintext) hoặc băm yếu không kèm salt."
    ),
    (
        "Học phần Mật mã học cơ sở tại Học viện Công nghệ Bưu chính Viễn thông đặt ra đề tài số 6: Thiết kế hệ thống xác thực "
        "và bảo mật mật khẩu người dùng bằng thuật toán băm SHA-256. Đề tài yêu cầu sinh viên không chỉ lập trình được chức năng "
        "đăng ký, đăng nhập mà còn hiểu sâu lý thuyết về hàm băm, salt, rainbow table, brute-force; triển khai lưu trữ mật khẩu "
        "đã băm; xây dựng giao diện quản lý thử nghiệm; và đánh giá hiệu quả bảo mật qua thực nghiệm."
    ),
    (
        "Nhóm thực hiện đã xây dựng hệ thống hoàn chỉnh bằng Python 3, framework Flask, cơ sở dữ liệu SQLite. Hệ thống gồm: "
        "(1) module băm mật khẩu PBKDF2-HMAC-SHA256 với salt 256-bit, pepper, 100.000 vòng lặp; (2) REST API đầy đủ cho đăng ký, "
        "đăng nhập, đổi mật khẩu, quản lý phiên; (3) giao diện web demo hiện đại; (4) cơ chế rate limiting, khóa tài khoản, ghi log "
        "bảo mật; (5) script demo.py minh họa salt/no-salt và tấn công dictionary; (6) bộ unit test và API test tự động. "
        "File hash256_salt.py được giữ riêng để minh họa đúng công thức SHA-256(salt + password) theo yêu cầu học thuật."
    ),
    (
        "Phương pháp nghiên cứu kết hợp: (a) nghiên cứu tài liệu chuẩn NIST, RFC, OWASP về lưu trữ mật khẩu; (b) phân tích yêu cầu "
        "đề tài và thiết kế kiến trúc hệ thống; (c) lập trình và tích hợp các module; (d) kiểm thử chức năng, bảo mật và hiệu năng; "
        "(e) so sánh kịch bản có/không salt, mô phỏng tấn công brute-force bằng wordlist."
    ),
    (
        "Báo cáo được trình bày trong bốn chương. Chương 1 trình bày cơ sở lý thuyết về hàm băm, SHA-256, salt, pepper, PBKDF2 "
        "và các dạng tấn công liên quan. Chương 2 mô tả chi tiết thiết kế, kiến trúc, cơ sở dữ liệu, API và mã nguồn. Chương 3 "
        "trình bày kết quả thực nghiệm, kiểm thử và đánh giá mức độ đáp ứng yêu cầu. Chương 4 đưa ra kết luận, hướng phát triển "
        "và tài liệu tham khảo."
    ),
]

CHAPTER_1 = [
    ("h1", "CHƯƠNG 1. CƠ SỞ LÝ THUYẾT"),
    ("h2", "1.1 Tổng quan về hàm băm mật mã"),
    ("h3", "1.1.1 Khái niệm hàm băm và các tính chất bảo mật"),
    (
        "p",
        "Hàm băm (hash function) H là ánh xạ từ không gian thông điệp đầu vào có độ dài tùy ý M sang không gian đầu ra "
        "cố định {0,1}^n. Kết quả H(M) gọi là digest, message digest hoặc giá trị băm. Trong mật mã học, hàm băm mật mã "
        "(cryptographic hash function) phải thỏa mãn các tính chất sau để đảm bảo an toàn trong ứng dụng thực tế:",
    ),
    (
        "bullets",
        [
            "Tính xác định (Deterministic): cùng đầu vào luôn cho cùng đầu ra.",
            "Hiệu năng cao: tính H(M) nhanh trên phần cứng thông thường.",
            "Tính một chiều / chống tiền ảnh (Pre-image resistance): với y cho trước, khó tìm x sao cho H(x) = y.",
            "Chống tiền ảnh thứ hai (Second pre-image resistance): với x cho trước, khó tìm x' ≠ x sao cho H(x') = H(x).",
            "Chống va chạm (Collision resistance): khó tìm cặp x ≠ x' sao cho H(x) = H(x').",
            "Hiệu ứng lan truyền (Avalanche effect): thay đổi nhỏ ở đầu vào làm thay đổi lớn, không dự đoán được ở đầu ra.",
        ],
    ),
    (
        "p",
        "Tính một chiều là nền tảng của việc lưu mật khẩu dưới dạng hash: kẻ tấn công có được digest từ database cũng không "
        "thể 'giải mã' ngược trực tiếp để lấy mật khẩu gốc. Cách duy nhất khả thi trong thực tế là đoán mật khẩu, băm lại và "
        "so sánh — đây chính là cơ sở của brute-force và dictionary attack được minh họa trong Chương 3.",
    ),
    ("h3", "1.1.2 Ứng dụng hàm băm trong bảo mật thông tin"),
    (
        "p",
        "Hàm băm mật mã có vai trò trung tâm trong nhiều lĩnh vực: xác thực và lưu trữ mật khẩu; kiểm tra toàn vẹn file "
        "(checksum, so sánh hash trước/sau truyền); chữ ký số (ký trên hash của thông điệp thay vì toàn bộ dữ liệu); "
        "blockchain và chứng minh công việc (Proof of Work); HMAC cho xác thực thông điệp.",
    ),
    (
        "p",
        "Trong phạm vi đề tài, ứng dụng chính là bảo vệ mật khẩu người dùng. Quy trình chuẩn được OWASP khuyến nghị:",
    ),
    (
        "code",
        "Đăng ký:  password → [validate] → [salt] → hash_function → stored_value → database\n"
        "Đăng nhập: password_nhập → [lấy salt từ DB] → hash_function → so_sánh(stored_hash, candidate_hash)",
    ),
    (
        "p",
        "Điểm mấu chốt: hệ thống KHÔNG BAO GIỜ so sánh mật khẩu gốc, KHÔNG BAO GIỜ lưu mật khẩu gốc, và KHÔNG BAO GIỜ "
        "gửi hash mật khẩu cho client trong API công khai.",
    ),
    ("h3", "1.1.3 Rủi ro khi lưu mật khẩu dạng plaintext"),
    (
        "p",
        "Lưu mật khẩu plaintext trong database là sai lầm nghiêm trọng: admin database, nhân viên nội bộ có quyền truy cập, "
        "hoặc attacker sau khi SQL injection đều đọc được mật khẩu trực tiếp. Các vụ rò rỉ lớn (LinkedIn 2012, Adobe 2013) "
        "cho thấy hậu quả khi hash yếu hoặc không salt: hàng triệu tài khoản bị crack trong thời gian ngắn.",
    ),
    (
        "table",
        ["Cách lưu trữ", "Mức rủi ro", "Ghi chú"],
        [
            ["Plaintext", "Rất cao", "Đọc trực tiếp được mật khẩu"],
            ["MD5/SHA-1 một vòng, không salt", "Cao", "Rainbow table, GPU crack nhanh"],
            ["SHA-256 một vòng, không salt", "Trung bình–cao", "Vẫn bị brute-force/GPU"],
            ["SHA-256 + salt một vòng", "Trung bình", "Chống rainbow table, vẫn nhanh trên GPU"],
            ["PBKDF2/bcrypt/Argon2 + salt", "Thấp hơn", "Chi phí mỗi lần thử cao, khuyến nghị production"],
        ],
    ),
    ("h2", "1.2 Thuật toán băm SHA-256"),
    ("h3", "1.2.1 Lịch sử và vị trí trong họ SHA-2"),
    (
        "p",
        "SHA (Secure Hash Algorithm) do NSA thiết kế, NIST chuẩn hóa. SHA-1 (160-bit) đã bị phá va chạm thực tế (SHAttered, 2017). "
        "SHA-2 gồm SHA-224, SHA-256, SHA-384, SHA-512; SHA-256 là lựa chọn phổ biến nhất với độ dài digest 256 bit. "
        "SHA-3 (Keccak) là chuẩn mới nhưng SHA-256 vẫn được dùng rộng rãi trong TLS, chứng chỉ số, Bitcoin và lưu trữ mật khẩu.",
    ),
    ("h3", "1.2.2 Nguyên lý hoạt động và cấu trúc khối"),
    (
        "p",
        "SHA-256 dựa trên cấu trúc Merkle-Damgård. Thông điệp đầu vào được bổ sung bit '1', padding zeros và độ dài 64-bit "
        "(big-endian), chia thành các block 512-bit. Mỗi block đi qua hàm nén gồm 64 vòng (rounds), cập nhật 8 biến trạng thái "
        "32-bit (a, b, c, d, e, f, g, h) ban đầu lấy từ hằng số IV. Mỗi vòng sử dụng: phép cộng modulo 2^32, AND, OR, XOR, "
        "rotate (ROTR, SHR), hàm Ch, Maj, Σ0, Σ1 và từ khóa K[i] từ 64 hằng số đầu tiên của căn bậc hai các số nguyên tố.",
    ),
    (
        "p",
        "Đầu ra cuối cùng là 256 bit, thường biểu diễn dạng 64 ký tự hexadecimal. Trong Python, có thể gọi trực tiếp:",
    ),
    (
        "code",
        "import hashlib\n"
        "digest = hashlib.sha256(b'Hello World').hexdigest()\n"
        "# Kết quả: 64 ký tự hex, ví dụ a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
    ),
    (
        "p",
        "Trong project, file hash256_salt.py triển khai công thức học thuật:",
    ),
    (
        "code",
        "salt_password = (salt + password).encode('utf-8')\n"
        "digest = hashlib.sha256(salt_password).hexdigest()\n"
        "stored = f'{salt}${digest}'",
    ),
    ("h3", "1.2.3 Độ an toàn, hạn chế và so sánh với các thuật toán khác"),
    (
        "p",
        "SHA-256 chưa có tấn công va chạm thực tế khả thi trên phần cứng hiện tại. Tuy nhiên, tốc độ băm rất cao: GPU hiện đại "
        "có thể tính hàng tỷ SHA-256/giây, khiến brute-force mật khẩu ngắn (6–8 ký tự, chỉ chữ thường) trở nên khả thi nếu chỉ "
        "băm một vòng. Do đó đề tài không dừng ở SHA-256 thuần mà dùng PBKDF2-HMAC-SHA256 với 100.000 iterations trong hệ thống chính.",
    ),
    (
        "table",
        ["Thuật toán", "Độ dài hash", "Tốc độ", "Khuyến nghị lưu mật khẩu"],
        [
            ["MD5", "128 bit", "Rất nhanh", "Không dùng"],
            ["SHA-1", "160 bit", "Rất nhanh", "Không dùng"],
            ["SHA-256 (1 vòng)", "256 bit", "Rất nhanh", "Chỉ minh họa học thuật"],
            ["PBKDF2-HMAC-SHA256", "256 bit", "Chậm (cấu hình được)", "Có, trong project"],
            ["bcrypt", "184 bit", "Chậm", "Có, production"],
            ["Argon2id", "Tùy chọn", "Chậm, chống GPU/ASIC", "Khuyến nghị cao nhất hiện nay"],
        ],
    ),
    ("h2", "1.3 Salt, pepper và phòng chống tấn công"),
    ("h3", "1.3.1 Khái niệm salt và vai trò trong lưu trữ mật khẩu"),
    (
        "p",
        "Salt là giá trị ngẫu nhiên (cryptographic nonce) sinh riêng cho mỗi tài khoản, kết hợp với mật khẩu trước khi băm. "
        "Salt được lưu cùng hash trong database — salt KHÔNG cần bí mật vì mục đích là làm unique digest cho mỗi user, "
        "không phải che giấu salt.",
    ),
    (
        "bullets",
        [
            "Hai user cùng mật khẩu 'Password123!' nhưng salt khác → hash hoàn toàn khác → attacker không nhận diện được password trùng.",
            "Rainbow table tổng quát (hash của 1 triệu password phổ biến) vô hiệu — phải tính lại cho từng salt.",
            "Salt phải đủ dài và ngẫu nhiên: project dùng 32 bytes (256 bit) từ os.urandom().",
            "Salt phải unique: test sinh 1000 salt không trùng nhau (test_password_hasher.py).",
        ],
    ),
    ("h3", "1.3.2 Rainbow table và dictionary attack"),
    (
        "p",
        "Rainbow table là cấu trúc dữ liệu lưu sẵn chuỗi password → hash (hoặc chuỗi hash trung gian) để tra cứu nhanh. "
        "Khi database bị lộ và hash không có salt, attacker tra bảng để tìm password tương ứng trong vài giây.",
    ),
    (
        "p",
        "Dictionary attack (tấn công từ điển) thử lần lượt các mật khẩu có trong danh sách từ điển (wordlist) — thường là "
        "các mật khẩu phổ biến, mật khẩu bị lộ từ vụ hack khác, hoặc biến thể của tên/brands. Brute-force thuần túy thử "
        "mọi tổ hợp ký tự theo không gian tìm kiếm; dictionary attack là tập con hiệu quả hơn khi người dùng chọn mật khẩu yếu. "
        "File wordlist-demo.txt trong project chứa khoảng 500 mật khẩu thường gặp (123456, password, qwerty, admin, ...).",
    ),
    (
        "p",
        "Khi không có salt, attacker có thể: (1) băm trước toàn bộ wordlist một lần; (2) tra cứu nhanh với mọi hash trong database; "
        "(3) nếu hai user cùng mật khẩu thì một lần crack được cả hai. Khi có salt, bước (1) phải lặp lại cho từng salt riêng biệt — "
        "đây là nội dung trọng tâm của kịch bản kiểm thử tại mục 3.5.",
    ),
    ("h3", "1.3.3 Brute-force attack và timing attack"),
    (
        "p",
        "Brute-force thử mọi tổ hợp ký tự có thể. Không gian tìm kiếm tăng theo cấp số nhân với độ dài và bảng ký tự. "
        "Mật khẩu 8 ký tự gồm chữ hoa, thường, số, ký tự đặc biệt có không gian rất lớn; kết hợp PBKDF2 100.000 vòng "
        "làm mỗi lần thử tốn ~0.1–0.3 giây trên CPU thông thường, khiến tấn công toàn diện không khả thi trong thời gian hợp lý.",
    ),
    (
        "p",
        "Timing attack khai thác thời gian so sánh chuỗi khác nhau: so sánh bằng '==' dừng sớm khi gặp byte khác, "
        "tạo ra thời gian phản hồi khác biệt. Project dùng hmac.compare_digest() — so sánh constant-time trên mọi byte. "
        "Unit test test_timing_attack_resistance kiểm tra tỷ lệ thời gian đúng/sai < 5 lần sau 500 vòng lặp.",
    ),
    ("h3", "1.3.4 Pepper và các lớp bảo vệ bổ sung"),
    (
        "p",
        "Pepper là secret key toàn cục, nối vào password trước khi hash: password_material = password + PEPPER. "
        "Pepper KHÔNG lưu trong database — chỉ có trong biến môi trường PASSWORD_PEPPER trên server. "
        "Nếu attacker chỉ dump database mà không có pepper, không thể verify được hash. "
        "Khác salt: pepper dùng chung cho toàn hệ thống, salt unique mỗi user.",
    ),
    ("h2", "1.4 PBKDF2-HMAC-SHA256 và lưu trữ mật khẩu an toàn"),
    ("h3", "1.4.1 HMAC và vai trò của SHA-256 trong PBKDF2"),
    (
        "p",
        "HMAC (Hash-based Message Authentication Code) kết hợp hàm băm (ở đây là SHA-256) với khóa bí mật để tạo mã xác thực "
        "thông điệp. Trong PBKDF2, HMAC-SHA256 đóng vai trò hàm PRF (Pseudo-Random Function): mỗi vòng lặp gọi HMAC với password, "
        "salt và chỉ số block, tạo chuỗi bit pseudo-ngẫu nhiên khó đoán. Như vậy SHA-256 không chỉ 'băm một lần' mà được dùng lặp "
        "đi lặp lại bên trong cấu trúc PBKDF2 — vẫn thỏa yêu cầu đề tài về thuật toán SHA-256 nhưng đạt mức an toàn cao hơn cho lưu mật khẩu.",
    ),
    (
        "code",
        "PRF = HMAC-SHA256\n"
        "PBKDF2_output = F(password, salt, iterations)  # F lặp HMAC iterations lần",
    ),
    ("h3", "1.4.2 Cơ chế PBKDF2"),
    (
        "p",
        "PBKDF2 (Password-Based Key Derivation Function 2) được định nghĩa trong PKCS#5/RFC 2898. Hàm nhận: password, salt, "
        "số vòng lặp iterations, hàm PRF (thường HMAC-SHA256). Mỗi vòng lặp tăng chi phí tính toán tuyến tính theo iterations. "
        "Project cấu hình: HASH_ALG='sha256', ITERATIONS=100_000, dklen=32 bytes.",
    ),
    (
        "code",
        "derived_key = hashlib.pbkdf2_hmac(\n"
        "    'sha256',\n"
        "    (password + pepper).encode('utf-8'),\n"
        "    salt_bytes,\n"
        "    100_000,\n"
        "    dklen=32\n"
        ")\n"
        "stored_value = f'sha256v2${salt}${iterations}${pepper_flag}${derived_key.hex()}'",
    ),
    (
        "p",
        "Định dạng stored_value hỗ trợ versioning: sha256v1 (legacy, 1 vòng, không pepper) và sha256v2 (hiện tại). "
        "Hàm needs_rehash() tự động nâng cấp hash cũ khi user đăng nhập thành công.",
    ),
    ("h3", "1.4.3 So sánh SHA-256 thuần và PBKDF2-HMAC-SHA256"),
    (
        "table",
        ["Tiêu chí", "SHA-256(salt+password)", "PBKDF2-HMAC-SHA256"],
        [
            ["Số vòng băm", "1", "100.000"],
            ["Tốc độ trên CPU", "Hàng triệu hash/giây", "Vài hash/giây"],
            ["Chống rainbow table", "Có (nhờ salt)", "Có (nhờ salt)"],
            ["Chống brute-force GPU", "Yếu", "Mạnh hơn đáng kể"],
            ["Dùng trong project", "hash256_salt.py (minh họa)", "password_hasher.py (hệ thống chính)"],
            ["Phù hợp production", "Không", "Chấp nhận được (có thể nâng Argon2id)"],
        ],
    ),
    (
        "p",
        "Kết luận lý thuyết: SHA-256 vẫn là thành phần lõi của hệ thống (qua HMAC/PBKDF2), đáp ứng yêu cầu đề tài về "
        "thuật toán SHA-256, đồng thời PBKDF2 bổ sung lớp bảo vệ thực tiễn trước brute-force — phù hợp tinh thần "
        "'bảo mật mật khẩu người dùng' của đề tài.",
    ),
    ("h2", "1.5 Xác thực người dùng và mô hình đe dọa bảo mật"),
    ("h3", "1.5.1 Khái niệm xác thực (authentication)"),
    (
        "p",
        "Xác thực (authentication) là quá trình chứng minh danh tính của thực thể (người dùng, thiết bị, dịch vụ). Trong hệ thống "
        "đăng nhập truyền thống, yếu tố xác thực phổ biến là: (1) thông tin biết (mật khẩu); (2) vật sở hữu (token, OTP); "
        "(3) đặc điểm sinh trắc học. Đề tài tập trung vào yếu tố (1) với mật khẩu được bảo vệ bằng hàm băm.",
    ),
    (
        "p",
        "Phân biệt quan trọng: xác thực (authentication — 'bạn là ai?') khác với phân quyền (authorization — 'bạn được làm gì?'). "
        "Hệ thống project xử lý authentication qua login; authorization đơn giản qua Bearer token cho các API /api/users, /api/auth/me.",
    ),
    ("h3", "1.5.2 Luồng đăng ký và đăng nhập an toàn"),
    (
        "p",
        "Theo đúng yêu cầu đề tài số 6, luồng chuẩn được triển khai như sau:",
    ),
    (
        "bullets",
        [
            "Đăng ký: nhập username, password → kiểm tra độ mạnh → sinh salt ngẫu nhiên → băm (SHA-256 qua PBKDF2-HMAC) → lưu stored_value, không lưu password gốc.",
            "Đăng nhập: nhập lại password → lấy salt/hash từ DB → băm lại password nhập → so sánh digest (hmac.compare_digest), không so sánh plaintext.",
            "Quản lý thử nghiệm: danh sách user qua API chỉ hiển thị metadata, ẩn hash/salt/password.",
        ],
    ),
    (
        "p",
        "Để minh họa học thuật đúng công thức đề bài SHA-256(salt + password), project tách riêng module hash256_salt.py; "
        "hệ thống chính dùng PBKDF2-HMAC-SHA256 — mở rộng bảo mật được OWASP khuyến nghị, không thay đổi vai trò cốt lõi của SHA-256.",
    ),
    ("h3", "1.5.3 Các mối đe dọa khi lưu trữ mật khẩu"),
    (
        "table",
        ["Mối đe dọa", "Mô tả", "Biện pháp trong project"],
        [
            ["Rò rỉ database", "Attacker lấy file users.db", "Chỉ có hash; pepper ngoài DB"],
            ["Rainbow table", "Tra cứu hash có sẵn", "Salt unique mỗi user"],
            ["Dictionary attack", "Thử wordlist", "PBKDF2 chậm + mật khẩu mạnh"],
            ["Brute-force", "Thử mọi tổ hợp", "PBKDF2 100k vòng + rate limit"],
            ["User enumeration", "Phân biệt user tồn tại/không", "Thông báo lỗi chung khi login"],
            ["Timing attack", "Đo thời gian so sánh", "hmac.compare_digest()"],
            ["Online guessing", "Thử login liên tục", "Khóa sau 5 lần sai, Flask-Limiter"],
        ],
    ),
]

CHAPTER_2 = [
    ("h1", "CHƯƠNG 2. THIẾT KẾ VÀ XÂY DỰNG HỆ THỐNG"),
    ("h2", "2.1 Phân tích yêu cầu đề tài"),
    (
        "p",
        "Dựa trên đề cương đề tài số 6 (Học phần Mật mã học cơ sở), nhóm phân tích yêu cầu thành các nhóm chức năng và phi chức năng:",
    ),
    (
        "table",
        ["Nhóm yêu cầu", "Chi tiết", "Module đáp ứng"],
        [
            ["Lý thuyết", "Hàm băm, SHA-256, salt, rainbow table", "Chương 1, hash256_salt.py, demo.py"],
            ["Đăng ký", "Username/password → salt → hash → lưu", "register_user(), /api/auth/register"],
            ["Đăng nhập", "Băm lại, so sánh hash, không so plaintext", "login_user(), verify_password()"],
            ["Lưu trữ", "SQLite/MySQL/JSON, không lưu password gốc", "Database.py, users.db"],
            ["Giao diện", "CLI/Tkinter/Web đăng ký, đăng nhập", "templates/index.html, Flask"],
            ["Quản lý thử nghiệm", "Danh sách user ẩn thông tin nhạy cảm", "GET /api/users"],
            ["Kiểm thử", "Không khôi phục password, salt/no-salt, brute-force", "demo.py, test_*.py"],
            ["Báo cáo", "Quyển báo cáo đề tài", "Báo cáo này"],
        ],
    ),
    ("h2", "2.2 Kiến trúc tổng thể và mô hình triển khai"),
    (
        "p",
        "Hệ thống triển khai theo mô hình ba tầng (Three-tier Architecture):",
    ),
    (
        "bullets",
        [
            "Tầng Presentation: Giao diện web (HTML/CSS/JavaScript) gọi REST API qua fetch(); người dùng tương tác qua trình duyệt tại http://localhost:5000.",
            "Tầng Business Logic: Flask app (app.py) xử lý routing, validation, rate limiting, quản lý token; password_hasher.py xử lý băm/xác thực; Database.py xử lý nghiệp vụ đăng ký/đăng nhập.",
            "Tầng Data Access: SQLite lưu bảng users và security_logs; file users.db tự tạo khi khởi động.",
        ],
    ),
    (
        "p",
        "Luồng đăng ký chi tiết (theo API_endpoint.txt và mã nguồn):",
    ),
    (
        "code",
        "POST /api/auth/register {username, password}\n"
        "  → validate_username() [3-50 ký tự, a-zA-Z0-9_]\n"
        "  → validate_password_request() [độ dài cơ bản]\n"
        "  → register_user()\n"
        "      → register_password() [validate độ mạnh đầy đủ]\n"
        "      → generate_salt() [os.urandom(32).hex()]\n"
        "      → hash_password() [PBKDF2-HMAC-SHA256, 100k iter]\n"
        "      → INSERT users (username, stored_value)\n"
        "      → log_security_event('REGISTER')\n"
        "  → HTTP 201 {success, user_id}",
    ),
    (
        "p",
        "Luồng đăng nhập chi tiết:",
    ),
    (
        "code",
        "POST /api/auth/login {username, password}\n"
        "  → Kiểm tra rate limiter / locked_until\n"
        "  → SELECT stored_value FROM users WHERE username=?\n"
        "  → Nếu không tồn tại: trả 'Sai thông tin đăng nhập' (chống enumeration)\n"
        "  → verify_password(password, stored_value)\n"
        "      → parse_stored_value() → salt, hash, iterations, pepper_flag\n"
        "      → _derive_hash() → candidate_hash\n"
        "      → hmac.compare_digest(candidate, original)\n"
        "  → Thành công: reset failed_attempts, tạo UUID token, expires 3600s\n"
        "  → Thất bại: tăng failed_attempts, khóa nếu >= 5 lần",
    ),
    ("h2", "2.3 Công nghệ, công cụ và cấu trúc mã nguồn"),
    (
        "table",
        ["Thành phần", "Công nghệ / Phiên bản", "Vai trò"],
        [
            ["Ngôn ngữ", "Python 3.10+", "Toàn bộ backend"],
            ["Web framework", "Flask >= 3.0", "HTTP server, routing, template"],
            ["Database", "SQLite3", "Lưu user và security log"],
            ["Hashing", "hashlib.pbkdf2_hmac, hashlib.sha256", "Băm mật khẩu"],
            ["So sánh an toàn", "hmac.compare_digest", "Chống timing attack"],
            ["Rate limit", "Flask-Limiter >= 3.0", "Giới hạn request theo IP"],
            ["CORS", "Flask-CORS", "Cho phép gọi API từ frontend"],
            ["Testing", "pytest, unittest", "Kiểm thử tự động"],
        ],
    ),
    (
        "p",
        "Cấu trúc thư mục project:",
    ),
    (
        "code",
        "SHA 256 Application/\n"
        "├── app.py                  # Flask app + REST API\n"
        "├── Database.py             # SQLite layer\n"
        "├── password_hasher.py      # PBKDF2-HMAC-SHA256 core\n"
        "├── hash256_salt.py         # SHA-256 thuần (minh họa)\n"
        "├── demo.py                 # Demo terminal\n"
        "├── test_api.py             # API tests\n"
        "├── test_password_hasher.py # Hash module tests\n"
        "├── wordlist-demo.txt       # ~500 passwords phổ biến\n"
        "├── templates/index.html    # Giao diện web\n"
        "├── requirements.txt\n"
        "└── users.db                # SQLite (tự tạo)",
    ),
    ("h2", "2.4 Thiết kế cơ sở dữ liệu SQLite"),
    (
        "p",
        "Database khởi tạo tự động qua init_database() khi import Database.py. Sử dụng context manager get_db_connection() "
        "đảm bảo commit/rollback đúng cách.",
    ),
    (
        "table",
        ["Cột (users)", "Kiểu", "Ràng buộc", "Mô tả"],
        [
            ["id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Định danh user"],
            ["username", "TEXT", "UNIQUE NOT NULL", "3-50 ký tự, regex ^[a-zA-Z0-9_]+$"],
            ["stored_value", "TEXT", "NOT NULL", "sha256v2$salt$iter$flag$hash"],
            ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Ngày tạo"],
            ["updated_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Cập nhật"],
            ["failed_attempts", "INTEGER", "DEFAULT 0", "Đếm đăng nhập sai"],
            ["locked_until", "TIMESTAMP", "NULL", "Hết hạn khóa tài khoản"],
            ["last_login", "TIMESTAMP", "NULL", "Lần đăng nhập cuối"],
            ["is_active", "BOOLEAN", "DEFAULT 1", "Kích hoạt/vô hiệu"],
        ],
    ),
    (
        "p",
        "Bảng security_logs ghi các event_type: REGISTER, REGISTER_FAILED_DUPLICATE, LOGIN_SUCCESS, LOGIN_FAILED_WRONG_PASSWORD, "
        "LOGIN_FAILED_USER_NOT_FOUND, LOGIN_BLOCKED_LOCKED, PASSWORD_CHANGED, PASSWORD_REHASHED, ... kèm ip_address, user_agent, "
        "details (JSON). Phục vụ audit và minh họa trong báo cáo.",
    ),
    ("h2", "2.5 Module xử lý mật khẩu (password_hasher.py)"),
    (
        "p",
        "Module password_hasher.py là lõi bảo mật, gồm các thành phần chính:",
    ),
    (
        "table",
        ["Hàm / Class", "Chức năng"],
        [
            ["generate_salt(num_bytes=32)", "Sinh salt hex 64 ký tự từ os.urandom()"],
            ["hash_password(password, salt, iterations, use_pepper)", "Trả về HashResult với stored_value"],
            ["verify_password(password, stored_value)", "Parse + derive + compare_digest"],
            ["validate_password(password)", "5 tiêu chí độ mạnh, trả ValidationResult"],
            ["register_password(password)", "Validate + hash, dùng khi đăng ký"],
            ["change_password(old, new, stored)", "Xác thực cũ, validate mới, hash mới"],
            ["needs_rehash(stored_value)", "Kiểm tra iterations/pepper/version"],
            ["format_stored_value / parse_stored_value", "Đóng gói/giải mã chuỗi lưu DB"],
            ["RateLimiter", "Khóa theo username sau MAX_FAILED_ATTEMPTS=5, LOCKOUT=900s"],
        ],
    ),
    (
        "p",
        "Chính sách mật khẩu (validate_password): tối thiểu 8, tối đa 128 ký tự; ít nhất 1 chữ hoa, 1 thường, 1 số, "
        "1 ký tự đặc biệt [!@#$%^&*(),.?\":{}|<>]. Điểm 0-5: Yếu (≤2), Trung bình (3-4), Mạnh (5).",
    ),
    ("h2", "2.6 Module minh họa SHA-256 thuần (hash256_salt.py)"),
    (
        "p",
        "File hash256_salt.py triển khai đúng yêu cầu học thuật đề tài: SHA-256(salt + password) một vòng, lưu dạng "
        "salt$digest. Cung cấp generate_salt(), hash_password(), verify_password() với hmac.compare_digest(), "
        "val_password() kiểm tra độ mạnh. File này KHÔNG dùng trong luồng production — chỉ để giảng dạy và so sánh "
        "với PBKDF2 trong demo.py mục 3.",
    ),
    ("h2", "2.7 Tầng dữ liệu và nghiệp vụ (Database.py)"),
    (
        "p",
        "Database.py bọc SQLite và tích hợp password_hasher. Các hàm public:",
    ),
    (
        "bullets",
        [
            "register_user(username, password, ip, ua): validate, hash, insert, log.",
            "login_user(username, password, ip, ua, rate_limiter): xác thực, khóa, rehash, cấp token UUID.",
            "change_user_password(username, old, new, ip): đổi mật khẩu an toàn.",
            "get_user_info(username) / list_users(limit): KHÔNG trả stored_value.",
            "get_security_logs(limit): log gần nhất cho demo.",
        ],
    ),
    (
        "p",
        "Cơ chế khóa tài khoản kép: (1) RateLimiter trong memory theo username; (2) failed_attempts + locked_until "
        "trong database — đồng bộ khi đăng nhập sai từ API. Sau 5 lần sai, locked_until = now + 900 giây.",
    ),
    ("h2", "2.8 REST API và giao diện web (app.py, index.html)"),
    (
        "table",
        ["Method", "Endpoint", "Auth", "Rate limit", "Mô tả"],
        [
            ["POST", "/api/auth/register", "Không", "10/phút", "Đăng ký, trả 201/400/409"],
            ["POST", "/api/auth/login", "Không", "20/phút", "Đăng nhập, trả token UUID"],
            ["GET", "/api/auth/me", "Bearer", "—", "Thông tin user hiện tại"],
            ["POST", "/api/auth/change-password", "Bearer", "5/phút", "Đổi mật khẩu"],
            ["POST", "/api/auth/logout", "Bearer", "—", "Xóa token khỏi RAM"],
            ["GET", "/api/users", "Bearer", "—", "Danh sách user (ẩn hash)"],
            ["GET", "/api/security-logs", "Bearer", "—", "50 log gần nhất"],
            ["GET", "/", "Không", "—", "Giao diện web demo"],
        ],
    ),
    (
        "p",
        "Giao diện templates/index.html: thiết kế dark theme hiện đại, responsive; gồm form đăng ký/đăng nhập, "
        "panel trạng thái phiên (token, username), nút xem danh sách user và security log, đổi mật khẩu, logout. "
        "JavaScript gọi API bằng fetch() với header Authorization: Bearer. Không hiển thị stored_value hay hash.",
    ),
    (
        "p",
        "Ví dụ response đăng ký thành công:",
    ),
    (
        "code",
        'HTTP/1.1 201 Created\n'
        '{"success": true, "message": "Đăng ký thành công", "user_id": 1}',
    ),
    (
        "p",
        "serialize_user() đảm bảo API chỉ trả: id, username, created_at, updated_at, last_login, failed_attempts, is_active.",
    ),
    ("h2", "2.9 Các biện pháp bảo mật bổ sung"),
    (
        "p",
        "Token phiên đăng nhập: sau khi login thành công, server tạo UUID4 làm token, lưu trong dictionary active_tokens "
        "kèm username và expiry (timestamp + 3600). Mọi endpoint bảo vệ gọi get_authenticated_username() để parse header "
        "Authorization: Bearer <token>, kiểm tra tồn tại và chưa hết hạn. Logout xóa token khỏi dictionary.",
    ),
    (
        "bullets",
        [
            "Không lưu password plaintext — chỉ stored_value.",
            "Pepper từ biến môi trường PASSWORD_PEPPER (không hardcode production).",
            "hmac.compare_digest() cho mọi so sánh hash.",
            "Thông báo lỗi đăng nhập thống nhất — chống user enumeration.",
            "Flask-Limiter: 200/day, 50/hour mặc định; endpoint-specific limits.",
            "Token demo lưu RAM (active_tokens), hết hạn 3600s — ghi chú nâng cấp JWT cho production.",
            "SECRET_KEY từ biến môi trường cho Flask.",
            "Tự động rehash khi đăng nhập nếu hash cũ (sha256v1 hoặc iterations thấp).",
            "Ghi security_logs đầy đủ sự kiện bảo mật.",
        ],
    ),
]

CHAPTER_3 = [
    ("h1", "CHƯƠNG 3. KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ"),
    ("h2", "3.1 Môi trường thử nghiệm và phương pháp kiểm thử"),
    (
        "p",
        "Môi trường: Windows 10/11 hoặc Linux, Python 3.12, Flask development server tại http://localhost:5000. "
        "Cài đặt: python -m venv .venv, pip install -r requirements.txt. Biến môi trường khuyến nghị: "
        "SECRET_KEY, PASSWORD_PEPPER.",
    ),
    (
        "p",
        "Phương pháp kiểm thử gồm bốn lớp: (1) Kiểm thử thủ công qua giao diện web; (2) Kiểm thử API bằng curl/Postman; "
        "(3) Script demo.py trên terminal; (4) Unit test tự động pytest/unittest.",
    ),
    ("h2", "3.2 Thực nghiệm đăng ký và đăng nhập"),
    (
        "p",
        "Kịch bản 1 — Đăng ký thành công: username='nguyenhonga', password='Pass@1234' → HTTP 201, user_id tăng dần. "
        "Database chỉ lưu username và stored_value dạng sha256v2$... — không có cột password.",
    ),
    (
        "table",
        ["Kịch bản", "Input", "HTTP", "Message"],
        [
            ["Đăng ký OK", "user hợp lệ + pass mạnh", "201", "Đăng ký thành công"],
            ["Username trùng", "duplicate_user", "409", "Tên đăng nhập đã tồn tại"],
            ["Password yếu", "password='weak'", "400", "phải có ít nhất 8 ký tự"],
            ["Thiếu username", "chỉ có password", "400", "username là bắt buộc"],
            ["Username sai format", "test@user hoặc 'ab'", "400", "3-50 ký tự, a-z0-9_"],
            ["Đăng nhập OK", "đúng user/pass", "200", "token + expires_in=3600"],
            ["Sai mật khẩu", "pass sai", "401", "Sai thông tin đăng nhập"],
            ["User không tồn tại", "nonexistent", "401", "Sai thông tin đăng nhập (không lộ user)"],
            ["Token hết hạn", "sau 3600s", "401", "Token đã hết hạn"],
        ],
    ),
    (
        "p",
        "Kịch bản 2 — Đổi mật khẩu: đăng nhập lấy token → POST /api/auth/change-password với old_password, new_password. "
        "Thành công → đăng nhập lại bằng mật khẩu mới. Mật khẩu cũ sai → 401. Mật khẩu mới yếu → 400.",
    ),
    (
        "p",
        "Kịch bản 3 — Khóa tài khoản: đăng nhập sai 5 lần liên tiếp → failed_attempts=5, locked_until=now+900s. "
        "Lần đăng nhập tiếp theo (kể cả đúng mật khẩu) trả thông báo tài khoản bị khóa.",
    ),
    ("h2", "3.3 Kiểm chứng không khôi phục được mật khẩu từ hash"),
    (
        "p",
        "Demo mục 6 trong demo.py: password gốc 'SuperSecret@1' → register_password() → in stored_value. "
        "Kiểm tra: password gốc NOT IN stored_value. Kết luận: digest là one-way; hệ thống và attacker đều "
        "phải dùng phương pháp thử đoán (brute-force/dictionary) thay vì 'giải mã' hash.",
    ),
    (
        "p",
        "Nếu admin xem trực tiếp users.db, chỉ thấy chuỗi dạng:",
    ),
    (
        "code",
        "sha256v2$a3f2...salt_hex...$100000$1$9b7c...hash_hex...",
    ),
    (
        "p",
        "Không có cách nào trong phạm vi đề tài để suy ra 'SuperSecret@1' từ chuỗi trên mà không thử lại password.",
    ),
    ("h2", "3.4 So sánh hiệu quả khi có và không có salt"),
    (
        "p",
        "Demo mục 3 (demo.py) so sánh trực tiếp:",
    ),
    (
        "table",
        ["Trường hợp", "Password", "Salt", "Kết quả hash"],
        [
            ["Không salt — User A", "Password123!", "—", "H1 = SHA256('Password123!')"],
            ["Không salt — User B", "Password123!", "—", "H2 = H1 (GIỐNG NHAU)"],
            ["Có salt — User A", "Password123!", "salt_A (random)", "H3 (unique)"],
            ["Có salt — User B", "Password123!", "salt_B (random)", "H4 ≠ H3"],
        ],
    ),
    (
        "p",
        "Khi H1 = H2: attacker thấy hai tài khoản cùng hash → biết cùng password → dùng một rainbow table. "
        "Khi H3 ≠ H4: mỗi tài khoản cần brute-force riêng. Salt 256-bit có 2^256 khả năng — không thể xây rainbow table cho mỗi salt.",
    ),
    (
        "p",
        "Thêm PBKDF2 100.000 vòng: mỗi lần verify_password() trong vòng lặp wordlist tốn ~0.1–0.3s thay vì "
        "vài microsecond của SHA-256 thuần — làm dictionary attack với 500 từ trong wordlist-demo.txt vẫn khả thi "
        "cho mật khẩu yếu có trong list, nhưng không khả thi cho mật khẩu mạnh 'Secure@Pass99'.",
    ),
    ("h2", "3.5 Kịch bản kiểm thử tấn công brute-force"),
    (
        "p",
        "Phần này trình bày kịch bản kiểm thử tấn công brute-force/dictionary theo tài liệu "
        "'KỊCH BẢN KIỂM THỬ TẤN CÔNG BRUTE-FORCE', đối chứng giữa việc sử dụng salt và không sử dụng salt "
        "trên nền SHA-256, kết hợp minh họa thực tế qua demo.py, hash256_salt.py và wordlist-demo.txt.",
    ),
    ("h3", "3.5.1 Mục tiêu và phạm vi kiểm thử"),
    (
        "p",
        "Mục tiêu kiểm thử:",
    ),
    (
        "bullets",
        [
            "Đo lường thời gian và số lần thử cần thiết để khôi phục mật khẩu từ mã băm bằng tấn công từ điển (Dictionary Attack / Wordlist).",
            "So sánh hiệu năng và rủi ro bảo mật giữa lưu trữ băm SHA-256 thuần và băm SHA-256 kết hợp salt ngẫu nhiên.",
            "Chứng minh: hệ thống dùng salt buộc kẻ tấn công phải tính toán lại từ điển cho từng người dùng riêng biệt, "
            "làm chậm tấn công brute-force trên diện rộng và vô hiệu hóa rainbow table tổng quát.",
        ],
    ),
    (
        "p",
        "Phạm vi kiểm thử: phương pháp tấn công brute-force dạng wordlist; môi trường localhost, script Python đọc SQLite "
        "(users.db) hoặc mô phỏng trong demo.py; dữ liệu mẫu gồm 5 tài khoản có mật khẩu yếu, phổ biến, nằm sẵn trong wordlist-demo.txt.",
    ),
    (
        "table",
        ["STT", "Username", "Mật khẩu gốc", "Có trong wordlist?"],
        [
            ["1", "user_password", "password", "Có (dòng 2)"],
            ["2", "user_123456", "123456", "Có (dòng 1)"],
            ["3", "user_admin123", "admin123", "Có (dòng 5)"],
            ["4", "user_qwerty", "qwerty", "Có (dòng 8)"],
            ["5", "user_dragon", "dragon", "Có (dòng 7)"],
        ],
    ),
    (
        "p",
        "Năm tài khoản trên được đăng ký qua API hoặc mô phỏng bằng hash256_salt.py / register_password() trước khi chạy script tấn công. "
        "Mật khẩu đều thuộc nhóm yếu, dễ nằm trong top password phổ biến — phù hợp mục đích minh họa rủi ro, không dùng trong production.",
    ),
    ("h3", "3.5.2 Tấn công hệ thống không dùng salt"),
    (
        "p",
        "Kịch bản mô phỏng cách lưu trữ sai: chỉ lưu SHA-256(password) không salt. Trình tự thực hiện:",
    ),
    (
        "bullets",
        [
            "Bước 1: Lấy danh sách các giá trị băm mật khẩu của người dùng từ cơ sở dữ liệu (hoặc mảng hash mô phỏng).",
            "Bước 2: Script đọc lần lượt từng mật khẩu trong file wordlist-demo.txt.",
            "Bước 3: Với mỗi mật khẩu thử, tính băm SHA-256(password) và so sánh với tất cả các băm đã lấy.",
            "Bước 4: Nếu khớp, ghi lại mật khẩu tìm được cùng thời gian và số lần thử.",
            "Bước 5: Lưu toàn bộ kết quả ra file (hoặc in console).",
        ],
    ),
    (
        "code",
        "import hashlib\n"
        "for candidate in wordlist:\n"
        "    h = hashlib.sha256(candidate.encode()).hexdigest()\n"
        "    for user, stored_hash in users_no_salt.items():\n"
        "        if h == stored_hash:\n"
        "            print(f'Cracked {user}: {candidate}')",
    ),
    (
        "p",
        "Đặc điểm tấn công không salt: mỗi mật khẩu trong wordlist chỉ cần băm MỘT lần, sau đó so khớp với MỌI user cùng lúc. "
        "Nếu user_password và một user khác cùng dùng 'password', một lần tìm ra sẽ crack cả hai. Tốc độ rất cao (hàng triệu hash/giây "
        "trên GPU), rainbow table có thể tra cứu tức thì mà không cần chạy lại script.",
    ),
    ("h3", "3.5.3 Tấn công hệ thống có dùng salt"),
    (
        "p",
        "Kịch bản đúng hướng dẫn đề tài: SHA-256(salt + password) với salt riêng mỗi user (module hash256_salt.py). Trình tự:",
    ),
    (
        "bullets",
        [
            "Bước 1: Lấy danh sách các cặp (băm mật khẩu, salt) của từng người dùng từ cơ sở dữ liệu.",
            "Bước 2: Với MỖI người dùng, script đọc từng mật khẩu trong wordlist.",
            "Bước 3: Với mỗi mật khẩu thử, nối salt vào phía trước password, tính SHA-256, so sánh với băm của user đó.",
            "Bước 4: Ghi lại mật khẩu tìm được (nếu có), thời gian và số lần thử cho từng người dùng.",
            "Bước 5: Lưu kết quả ra file riêng.",
        ],
    ),
    (
        "code",
        "from hash256_salt import hash_password, verify_password\n"
        "for username, stored in users_with_salt.items():\n"
        "    for candidate in wordlist:\n"
        "        if verify_password(candidate, stored):\n"
        "            print(f'Cracked {username}: {candidate}')",
    ),
    (
        "p",
        "Đặc điểm tấn công có salt: không thể dùng chung một lần băm wordlist cho tất cả user. Với N user và W từ trong wordlist, "
        "số lần băm tối đa là N × W (thay vì W khi không salt). Rainbow table tổng quát vô hiệu vì mỗi user có salt 256-bit khác nhau.",
    ),
    ("h3", "3.5.4 So sánh kết quả và phân tích"),
    (
        "p",
        "Đối chiếu hai kịch bản (ước lượng trên CPU, wordlist ~500 từ, 5 user):",
    ),
    (
        "table",
        ["Tiêu chí", "Không salt", "Có salt"],
        [
            ["Số lần băm tối đa (5 user, 500 từ)", "~500 (một lần cho cả DB)", "~2.500 (500 × 5 user)"],
            ["Crack đồng thời user trùng mật khẩu", "Có — một hash khớp → nhiều user", "Không — phải thử riêng từng salt"],
            ["Dùng rainbow table", "Hiệu quả", "Không hiệu quả"],
            ["Thời gian (SHA-256 thuần, CPU)", "Rất nhanh (< 1 giây)", "Nhanh hơn ~5 lần so với no-salt"],
            ["Mật khẩu yếu trong wordlist", "Bị crack", "Vẫn bị crack nếu nằm trong wordlist"],
            ["Mật khẩu mạnh ngoài wordlist", "An toàn trong phạm vi test", "An toàn trong phạm vi test"],
        ],
    ),
    (
        "p",
        "Nhận xét: salt KHÔNG ngăn crack mật khẩu yếu nếu password vẫn nằm trong wordlist — salt chống rainbow table và buộc attacker "
        "tính riêng từng tài khoản. Để chống dictionary attack hiệu quả cần thêm: mật khẩu mạnh, PBKDF2/bcrypt làm chậm mỗi lần thử, "
        "rate limiting khi đăng nhập online.",
    ),
    (
        "p",
        "Demo.py mục 3 minh họa trực quan: cùng password 'Password123!' — không salt cho hash giống nhau; có salt cho hash khác nhau. "
        "Mục 7 chạy dictionary attack với target Secure@Pass99: không tìm thấy trong 500 từ → chứng minh mật khẩu mạnh + salt + PBKDF2.",
    ),
    ("h3", "3.5.5 Thực nghiệm bổ sung trên hệ thống PBKDF2"),
    (
        "p",
        "Hệ thống production (password_hasher.py) dùng PBKDF2-HMAC-SHA256, 100.000 iterations. Khi chạy dictionary attack qua "
        "verify_password() như demo.py mục 7, mỗi lần thử tốn ~0,1–0,3 giây trên CPU thông thường. Với 500 từ, tổng thời gian "
        "có thể từ vài chục giây đến vài phút — chậm hơn hàng nghìn lần so với SHA-256 một vòng, làm tấn công quy mô lớn tốn kém hơn đáng kể.",
    ),
    (
        "bullets",
        [
            "Mật khẩu yếu có trong wordlist (password, 123456, dragon...): vẫn bị crack khi attacker có dump DB và đủ thời gian offline.",
            "Mật khẩu Secure@Pass99: không có trong wordlist → thất bại sau 500 lần thử trong demo.",
            "Kết hợp pepper (PASSWORD_PEPPER): attacker chỉ có DB không thể verify nếu thiếu pepper trên server.",
            "Rate limit + khóa tài khoản: chống thử mật khẩu qua API online, bổ sung cho kiểm thử offline.",
        ],
    ),
    (
        "p",
        "Kết luận kịch bản: thí nghiệm xác nhận đúng lý thuyết Chương 1 — salt là cần thiết nhưng không thay thế mật khẩu mạnh; "
        "SHA-256 thuần không đủ cho production; PBKDF2-HMAC-SHA256 + salt + pepper + chính sách mật khẩu tạo nên hệ thống đáp ứng đề tài.",
    ),
    ("h2", "3.6 Kết quả unit test và API test"),
    (
        "p",
        "test_password_hasher.py — các nhóm test:",
    ),
    (
        "table",
        ["Nhóm test", "Số case", "Nội dung kiểm tra"],
        [
            ["TestGenerateSalt", "2", "Độ dài 64 hex, 1000 salt unique"],
            ["TestHashPassword", "3", "Hash 64 hex, salt khác → hash khác, empty raise"],
            ["TestVerifyPassword", "3", "Đúng/sai password, timing attack ratio < 5"],
            ["TestValidatePassword", "2", "Mật khẩu mạnh/yếu"],
            ["TestChangePassword", "4", "Đổi OK, sai cũ, trùng cũ, mới yếu"],
            ["TestNeedsRehash", "3", "v1 cần rehash, iter thấp, v2 OK"],
            ["TestRateLimiter", "5", "Đếm fail, khóa, hết hạn, reset"],
            ["TestPepper", "3", "Pepper đổi hash, verify đúng"],
            ["TestPBKDF2Iterations", "3", "Iter khác → hash khác, performance < 0.5s/10k"],
        ],
    ),
    (
        "p",
        "test_api.py — các test API (pytest): register success/duplicate/weak/missing/invalid username; "
        "login success/wrong/nonexistent/missing/rate limit; change password success/wrong/weak; "
        "get current user; logout; unauthorized; api rate limiting. Chạy: python -m pytest -v.",
    ),
    ("h2", "3.7 Đánh giá mức độ đáp ứng yêu cầu đề tài"),
    (
        "table",
        ["STT", "Yêu cầu đề tài", "Cách thực hiện", "Đánh giá"],
        [
            ["1", "Nghiên cứu hàm băm, SHA-256, salt", "Chương 1 + hash256_salt.py", "Đạt"],
            ["2", "Giao diện đăng ký/đăng nhập", "index.html + Flask", "Đạt"],
            ["3", "Đăng ký: salt → hash → lưu", "register_user + PBKDF2", "Đạt"],
            ["4", "Đăng nhập: băm lại, so sánh hash", "verify_password + compare_digest", "Đạt"],
            ["5", "Lưu SQLite, không password gốc", "users.stored_value", "Đạt"],
            ["6", "Danh sách user ẩn nhạy cảm", "GET /api/users", "Đạt"],
            ["7", "So sánh có/không salt", "demo.py mục 3", "Đạt"],
            ["8", "Brute-force demo", "Mục 3.5 + demo.py + wordlist", "Đạt"],
            ["9", "Kiểm thử tự động", "test_*.py", "Đạt"],
            ["10", "Báo cáo đề tài", "BaoCao_SHA256_MMHCS.docx", "Đạt"],
        ],
    ),
    ("h2", "3.8 Hạn chế và hướng phát triển"),
    (
        "p",
        "Hạn chế hiện tại (phục vụ học tập/demo):",
    ),
    (
        "bullets",
        [
            "Token lưu trong RAM — mất khi restart server; chưa dùng JWT/session DB.",
            "Chưa triển khai HTTPS — cần reverse proxy (nginx) cho production.",
            "Pepper/SECRET_KEY mặc định development nếu không set env.",
            "Chưa có reset password qua email, xác minh 2 yếu tố (2FA).",
            "SQLite phù hợp demo — production nên PostgreSQL/MySQL.",
        ],
    ),
    (
        "p",
        "Hướng phát triển: chuyển sang Argon2id; JWT + refresh token; Docker; CI/CD GitHub Actions; "
        "trang admin; migration database; E2E test; tích hợp CAPTCHA sau nhiều lần đăng nhập sai.",
    ),
    ("h2", "3.9 Hướng dẫn chạy thử nghiệm tái lập kết quả"),
    (
        "p",
        "Để tái lập kết quả trong báo cáo, thực hiện các bước sau trên máy có Python 3.10+:",
    ),
    (
        "code",
        "# Buoc 1: Cai dat\n"
        "python -m venv .venv\n"
        ".venv\\Scripts\\activate          # Windows\n"
        "pip install -r requirements.txt\n\n"
        "# Buoc 2: Cau hinh (khuyen nghi)\n"
        "set SECRET_KEY=your-secret-key\n"
        "set PASSWORD_PEPPER=your-pepper\n\n"
        "# Buoc 3: Chay server\n"
        "python app.py\n"
        "# Mo trinh duyet: http://localhost:5000\n\n"
        "# Buoc 4: Demo terminal\n"
        "python demo.py\n\n"
        "# Buoc 5: Unit test\n"
        "python -m pytest -v",
    ),
    (
        "p",
        "Ví dụ kiểm thử API bằng curl (Linux/macOS/Git Bash):",
    ),
    (
        "code",
        "# Dang ky\n"
        'curl -X POST http://localhost:5000/api/auth/register \\\n'
        '  -H "Content-Type: application/json" \\\n'
        '  -d \'{"username":"alice","password":"Alice@1234"}\'\n\n'
        "# Dang nhap\n"
        'curl -X POST http://localhost:5000/api/auth/login \\\n'
        '  -H "Content-Type: application/json" \\\n'
        '  -d \'{"username":"alice","password":"Alice@1234"}\'\n\n'
        "# Lay thong tin user (thay <token>)\n"
        'curl http://localhost:5000/api/auth/me \\\n'
        '  -H "Authorization: Bearer <token>"',
    ),
    (
        "p",
        "Trên giao diện web: tab Đăng ký nhập username/password hợp lệ → Đăng ký → chuyển tab Đăng nhập → "
        "sau khi đăng nhập thành công, panel bên phải hiển thị token và username; có thể bấm 'Xem danh sách người dùng' "
        "để kiểm tra endpoint ẩn hash/salt; bấm 'Xem security log' để thấy các sự kiện REGISTER, LOGIN_SUCCESS được ghi lại.",
    ),
]

CHAPTER_4 = [
    ("h1", "CHƯƠNG 4. KẾT LUẬN VÀ TÀI LIỆU THAM KHẢO"),
    ("h2", "4.1 Kết luận"),
    (
        "p",
        "Đề tài đã hoàn thành hệ thống xác thực và bảo mật mật khẩu bằng SHA-256 kết hợp salt, đáp ứng đầy đủ yêu cầu "
        "đề cương Mật mã học cơ sở. Về mặt lý thuyết, nhóm đã trình bày hàm băm mật mã, thuật toán SHA-256, vai trò salt/pepper, "
        "các dạng tấn công rainbow table, dictionary, brute-force và timing attack. Về mặt thực tiễn, hệ thống triển khai "
        "PBKDF2-HMAC-SHA256 với 100.000 vòng lặp, giao diện web, REST API, SQLite, rate limiting và khóa tài khoản.",
    ),
    (
        "p",
        "Thực nghiệm chứng minh: (1) mật khẩu gốc không thể khôi phục trực tiếp từ hash; (2) salt làm hash unique "
        "cho mỗi user, vô hiệu hóa rainbow table tổng quát; (3) kịch bản brute-force mục 3.5 cho thấy tấn công không salt "
        "nhanh hơn và crack được nhiều user cùng lúc, trong khi có salt buộc tính toán riêng từng tài khoản; "
        "(4) mật khẩu yếu trong wordlist vẫn bị crack dù có salt; mật khẩu mạnh không bị crack trong phạm vi demo; "
        "(5) PBKDF2 làm chậm đáng kể mỗi lần thử so với SHA-256 thuần.",
    ),
    (
        "p",
        "Bài học rút ra: bảo mật mật khẩu không chỉ là 'băm SHA-256' mà cần kết hợp salt, hàm dẫn xuất chậm (PBKDF2/bcrypt/Argon2), "
        "chính sách mật khẩu mạnh, rate limiting và logging. SHA-256 đóng vai trò hàm băm lõi đáng tin cậy, nhưng phải "
        "được dùng đúng ngữ cảnh — lặp nhiều vòng qua PBKDF2-HMAC — mới phù hợp lưu trữ mật khẩu.",
    ),
    ("h2", "4.2 Tài liệu tham khảo"),
]

REFERENCES = [
    "[1] NIST FIPS 180-4 — Secure Hash Standard (SHS), August 2015.",
    "[2] NIST SP 800-132 — Recommendation for Password-Based Key Derivation, December 2010.",
    "[3] RFC 2898 — PKCS #5: Password-Based Cryptography Specification Version 2.0, September 2000.",
    "[4] RFC 6234 — US Secure Hash Algorithms (SHA and SHA-based HMAC and HKDF), May 2011.",
    "[5] OWASP Cheat Sheet Series — Password Storage Cheat Sheet, https://cheatsheetseries.owasp.org/",
    "[6] OWASP Cheat Sheet Series — Authentication Cheat Sheet.",
    "[7] Đề cương Đề tài số 6 — Mật mã học cơ sở, Học viện Công nghệ Bưu chính Viễn thông.",
    "[8] Python 3 Documentation — hashlib module, https://docs.python.org/3/library/hashlib.html",
    "[9] Python 3 Documentation — hmac module, https://docs.python.org/3/library/hmac.html",
    "[10] Flask Documentation — https://flask.palletsprojects.com/",
    "[11] SQLite Documentation — https://www.sqlite.org/docs.html",
    "[12] Colin Percival — Stronger Key Derivation via Sequential Memory-Hard Functions (scrypt), 2009.",
    "[13] Alex Biryukov, Daniel Dinu, Dmitry Khovratovich — Argon2: the memory-hard function for password hashing, 2015.",
    "[14] KỊCH BẢN KIỂM THỬ TẤN CÔNG BRUTE-FORCE — Tài liệu tham khảo nhóm, Học phần Mật mã học cơ sở.",
]
