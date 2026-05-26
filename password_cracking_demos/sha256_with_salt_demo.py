import hashlib

# Ba salt khác nhau (đủ dài, ngẫu nhiên)
salt_alice = "X7A91kP2mN3qR5tY"
salt_bob   = "K2L8PmN5vB6wE9xQ"
salt_carol = "Qw3ErTy7uI8oP9aS"

# Mật khẩu chung
password = "password123"

# Tạo hash = SHA256(salt + password)
hash_alice = hashlib.sha256((salt_alice + password).encode()).hexdigest()
hash_bob   = hashlib.sha256((salt_bob   + password).encode()).hexdigest()
hash_carol = hashlib.sha256((salt_carol + password).encode()).hexdigest()

# In kết quả
print("Alice (salt = {}) -> hash: {}".format(salt_alice, hash_alice))
print("Bob   (salt = {}) -> hash: {}".format(salt_bob,   hash_bob))
print("Carol (salt = {}) -> hash: {}".format(salt_carol, hash_carol))

# Kiểm tra xem các hash có khác nhau không
if len({hash_alice, hash_bob, hash_carol}) == 3:
    print("\n✅ Ba hash hoàn toàn khác nhau – không thể biết ba người dùng chung mật khẩu!")
else:
    print("\n❌ Có hash trùng – sai nguyên lý salt.")