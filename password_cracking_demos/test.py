from flask import Flask, request, render_template_string, redirect, url_for
import hashlib

app = Flask(__name__)

# ---------------------------
# 1. Database giả lập (không salt)
# ---------------------------
users = [
    {"id": 1, "email": "alice@example.com", "password_hash": hashlib.sha256(b"password123").hexdigest()},
    {"id": 2, "email": "bob@gmail.com",     "password_hash": hashlib.sha256(b"password123").hexdigest()},
    {"id": 3, "email": "carol@yahoo.com",   "password_hash": hashlib.sha256(b"password123").hexdigest()},
    {"id": 4, "email": "david@corp.vn",     "password_hash": hashlib.sha256(b"password").hexdigest()},
    {"id": 5, "email": "eve@hotmail.com",   "password_hash": hashlib.sha256(b"password").hexdigest()},
]

# Rainbow table giả lập (chỉ để demo)
rainbow_table = {
    hashlib.sha256(b"password123").hexdigest(): "password123",
    hashlib.sha256(b"password").hexdigest(): "password",
}

# ---------------------------
# 2. Giao diện HTML (inline)
# ---------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Demo lộ mật khẩu khi không có salt</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 80%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #f2f2f2; }
        .danger { color: red; }
        .info { background: #eef; padding: 10px; border-left: 5px solid blue; margin: 20px 0; }
        pre { background: #f4f4f4; padding: 10px; }
    </style>
</head>
<body>
    <h1>🔓 Demo: Database lộ mật khẩu khi KHÔNG có Salt</h1>
    <div class="info">
        <strong>⚠️ Vấn đề:</strong> Cùng một mật khẩu → giống hệt hash.<br>
        <strong>🎯 Kết quả:</strong> Nếu kẻ tấn công bẻ được <code>{{ same_hash_example }}</code> <br>
        → biết ngay mật khẩu của <strong>{{ count_same_password }}</strong> người dùng.
    </div>

    <h2>📋 Bảng người dùng (hash không salt)</h2>
    <table>
        <thead>
            <tr><th>ID</th><th>Email</th><th>Password Hash (SHA256)</th></tr>
        </thead>
        <tbody>
            {% for u in users %}
            <tr>
                <td>{{ u.id }}</td>
                <td>{{ u.email }}</td>
                <td><code>{{ u.password_hash }}</code>
                    <a href="/crack/{{ u.password_hash }}">🔨 Thử crack</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <h2>🔐 Đăng nhập thử (minh họa)</h2>
    <form method="POST" action="/login">
        Email: <input type="text" name="email" placeholder="alice@example.com" required>
        Mật khẩu: <input type="password" name="password" placeholder="mật khẩu thật" required>
        <button type="submit">Đăng nhập</button>
    </form>
    {% if login_msg %}
        <p><strong>{{ login_msg }}</strong></p>
    {% endif %}

    <hr>
    <h2>🧪 Giải thích code</h2>
    <pre>
- Tất cả password được băm bằng SHA256, **không salt**.
- Alice, Bob, Carol đều có cùng hash → dùng chung mật khẩu "password123".
- David & Eve cùng hash → dùng "password".
- Hàm /crack/&lt;hash&gt; sẽ tra trong rainbow table (có sẵn 2 mật khẩu).
- Nếu tìm thấy → hiện mật khẩu thật → lộ toàn bộ user có hash đó.
    </pre>
</body>
</html>
"""

# ---------------------------
# 3. Route hiển thị danh sách user
# ---------------------------
@app.route('/')
def index():
    # Tìm hash xuất hiện nhiều lần để cảnh báo
    from collections import Counter
    hash_counts = Counter(u["password_hash"] for u in users)
    most_common_hash, count = hash_counts.most_common(1)[0]
    return render_template_string(
        HTML_TEMPLATE,
        users=users,
        same_hash_example=most_common_hash,
        count_same_password=count,
        login_msg=None
    )

# ---------------------------
# 4. Đăng nhập (minh họa)
# ---------------------------
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    user = next((u for u in users if u["email"] == email), None)
    if user and user["password_hash"] == input_hash:
        login_msg = f"✅ Đăng nhập thành công với tư cách {email}"
    else:
        login_msg = "❌ Sai email hoặc mật khẩu"
    
    # Render lại trang với thông báo
    from collections import Counter
    hash_counts = Counter(u["password_hash"] for u in users)
    most_common_hash, count = hash_counts.most_common(1)[0]
    return render_template_string(
        HTML_TEMPLATE,
        users=users,
        same_hash_example=most_common_hash,
        count_same_password=count,
        login_msg=login_msg
    )

# ---------------------------
# 5. Route mô phỏng crack hash
# ---------------------------
@app.route('/crack/<hash_val>')
def crack(hash_val):
    if hash_val in rainbow_table:
        plain_password = rainbow_table[hash_val]
        # Tìm tất cả user dùng hash này
        affected_users = [u["email"] for u in users if u["password_hash"] == hash_val]
        message = f"""
        🔓 <strong>CRACKED!</strong><br>
        Hash <code>{hash_val}</code> → mật khẩu là <strong style="color:red">{plain_password}</strong><br>
        👥 Những người dùng bị lộ mật khẩu: {', '.join(affected_users)}<br>
        <em>=> Vì không có salt, chỉ cần crack 1 hash là biết mật khẩu của tất cả user dùng chung mật khẩu.</em>
        """
    else:
        message = f"❌ Không tìm thấy mật khẩu cho hash <code>{hash_val}</code> (rainbow table demo chỉ có 'password123' và 'password')"
    
    # Trả về trang kết quả đơn giản
    return f"<html><body><h2>Kết quả bẻ khóa</h2>{message}<br><a href='/'>Quay lại</a></body></html>"

# ---------------------------
# 6. Chạy app
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)