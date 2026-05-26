import hashlib
import time
import sys

def hash_sha256(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def benchmark(wordlist_path: str, limit: int = None):
    print(f"\n--- Đang đọc: {wordlist_path} ---")
    passwords = []
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                pw = line.strip()
                if pw:
                    passwords.append(pw)
    except FileNotFoundError:
        print(f"Không tìm thấy file {wordlist_path}")
        return

    if not passwords:
        print("Wordlist rỗng.")
        return

    print(f"Số lượng mật khẩu: {len(passwords)}")
    start = time.perf_counter()
    hashes = [hash_sha256(pw) for pw in passwords]
    end = time.perf_counter()
    elapsed = end - start
    speed = len(passwords) / elapsed
    print(f"Thời gian băm: {elapsed:.4f} giây")
    print(f"Tốc độ: {speed:,.0f} hash/giây")

if __name__ == "__main__":

    files = [
        "1000-common-password.txt",
        "10000-common-password.txt",
        "100000-common-password.txt",
        "1000000-common-password.txt"
    ]
    for f in files:
        benchmark(f)
        print("-" * 50)