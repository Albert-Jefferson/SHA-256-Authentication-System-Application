import hashlib
import time

# ---------------------------
# 1. Xây dựng rainbow table từ file wordlist
# ---------------------------
def build_rainbow_table(wordlist_file, max_passwords=None):
    """
    Đọc file wordlist, mỗi dòng là một mật khẩu.
    Trả về dictionary: {hash: password}
    """
    rainbow = {}
    count = 0
    try:
        with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                pw = line.strip()
                if pw:  # bỏ dòng trống
                    h = hashlib.sha256(pw.encode()).hexdigest()
                    rainbow[h] = pw
                    count += 1
                    if max_passwords and count >= max_passwords:
                        break
        print(f"Đã xây dựng rainbow table với {count} mật khẩu từ {wordlist_file}")
    except FileNotFoundError:
        print(f"Không tìm thấy file {wordlist_file}")
    return rainbow

# ---------------------------
# 2. Hàm tra cứu hash
# ---------------------------
def lookup_hash(rainbow_table, target_hash):
    return rainbow_table.get(target_hash, None)

# ---------------------------
# 3. Demo với nhiều mật khẩu
# ---------------------------
if __name__ == "__main__":
    wordlist_file = "1000-common-password.txt" 
    rainbow = build_rainbow_table(wordlist_file)

    test_hashes = [
        hashlib.sha256(b"password123").hexdigest(),
        hashlib.sha256(b"password").hexdigest(),
        hashlib.sha256(b"123456").hexdigest(),
        "abc123hashkhongcothuc",  # hash không có trong bảng
    ]

    print("\n--- TRA CỨU RAINBOW TABLE ---")
    for h in test_hashes:
        result = lookup_hash(rainbow, h)
        if result:
            print(f"✅ Hash {h[:16]}... -> mật khẩu: {result}")
        else:
            print(f"❌ Hash {h[:16]}... -> không tìm thấy")