import hashlib
import itertools
import string
import time

# Lấy hash của "abc" trực tiếp từ hàm băm - không copy tay
target_hash = hashlib.sha256(b"abc").hexdigest()
print(f"Hash mục tiêu (tự động từ 'abc'): {target_hash}")

charset = string.ascii_lowercase
max_length = 3

print("Đang brute force...")
start = time.time()
found = None
for length in range(1, max_length+1):
    for guess in itertools.product(charset, repeat=length):
        pw = ''.join(guess)
        h = hashlib.sha256(pw.encode()).hexdigest()
        if h == target_hash:
            found = pw
            break
    if found:
        break

print(f"Thời gian: {time.time()-start:.4f} giây")
if found:
    print(f"✅ Tìm thấy mật khẩu: {found}")
else:
    print("❌ Không tìm thấy")