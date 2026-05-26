import hashlib  
import time     
import os       

# ----------------------------------------------------------
# HÀM 1: Tính hash SHA256 của một chuỗi văn bản
# ----------------------------------------------------------
def tinh_sha256(van_ban):
    """
    Nhận vào một chuỗi văn bản (ví dụ: "password123")
    Trả về chuỗi hash SHA256 dạng hex (64 ký tự)

    Ví dụ:
        tinh_sha256("abc")
        → "ba7816bf8f01cfea414140de5dae2ec73b00361bbef0469f492c44e4b696cb3"
    """
    # Bước 1: Chuyển chuỗi sang dạng bytes (SHA256 cần bytes, không nhận string trực tiếp)
    van_ban_bytes = van_ban.encode("utf-8")

    # Bước 2: Tạo đối tượng SHA256 và tính hash
    hash_object = hashlib.sha256(van_ban_bytes)

    # Bước 3: Chuyển kết quả sang dạng chuỗi hex (dễ đọc, dễ so sánh)
    ket_qua = hash_object.hexdigest()

    return ket_qua


# ----------------------------------------------------------
# HÀM 2: Đọc file hash (mỗi dòng là một hash SHA256)
# ----------------------------------------------------------
def doc_file_hash(duong_dan_file):
    """
    Đọc file chứa danh sách hash SHA256 cần crack.
    Mỗi dòng trong file là một hash (64 ký tự hex).

    Trả về: danh sách (list) các hash đã được làm sạch
    """
    # Kiểm tra file có tồn tại không trước khi mở
    if not os.path.exists(duong_dan_file):
        print(f"[LỖI] Không tìm thấy file hash: '{duong_dan_file}'")
        return []

    danh_sach_hash = []

    # Mở file theo chế độ đọc ('r'), encoding utf-8 để hỗ trợ tiếng Việt
    with open(duong_dan_file, "r", encoding="utf-8") as file:
        for dong in file:
            # Xóa khoảng trắng và ký tự xuống dòng ở đầu/cuối
            hash_sach = dong.strip().lower()  # .lower() để đồng nhất chữ hoa/thường

            # Bỏ qua dòng trống hoặc dòng comment (bắt đầu bằng #)
            if hash_sach == "" or hash_sach.startswith("#"):
                continue

            # Kiểm tra hash SHA256 phải đúng 64 ký tự
            if len(hash_sach) != 64:
                print(f"[CẢNH BÁO] Dòng này không phải SHA256 hợp lệ, bỏ qua: '{hash_sach[:20]}...'")
                continue

            danh_sach_hash.append(hash_sach)

    print(f"[OK] Đã đọc {len(danh_sach_hash)} hash từ file '{duong_dan_file}'")
    return danh_sach_hash


# ----------------------------------------------------------
# HÀM 3: Đọc file wordlist (mỗi dòng là một mật khẩu để thử)
# ----------------------------------------------------------
def doc_file_wordlist(duong_dan_file):
    """
    Đọc file wordlist chứa các mật khẩu sẽ được thử.
    Ví dụ: rockyou.txt, passwords.txt, ...

    Trả về: danh sách (list) các từ cần thử
    """
    if not os.path.exists(duong_dan_file):
        print(f"[LỖI] Không tìm thấy file wordlist: '{duong_dan_file}'")
        return []

    danh_sach_tu = []

    with open(duong_dan_file, "r", encoding="utf-8", errors="ignore") as file:
        # errors="ignore" để bỏ qua các ký tự không đọc được (thường gặp trong wordlist lớn)
        for dong in file:
            tu = dong.strip()  # Xóa khoảng trắng và ký tự xuống dòng

            # Bỏ qua dòng trống
            if tu == "":
                continue

            danh_sach_tu.append(tu)

    print(f"[OK] Đã đọc {len(danh_sach_tu)} từ từ wordlist '{duong_dan_file}'")
    return danh_sach_tu


# ----------------------------------------------------------
# HÀM 4: Crack hash - so sánh từng từ trong wordlist với hash
# ----------------------------------------------------------
def crack_hash(danh_sach_hash, danh_sach_tu):
    """
    Thử từng từ trong wordlist:
      1. Tính SHA256 của từ đó
      2. So sánh với từng hash trong danh sách
      3. Nếu khớp → ghi nhận kết quả

    Trả về:
      - ket_qua: dict ánh xạ hash → mật khẩu tìm được
      - so_lan_thu: tổng số lần thử
    """
    # Dùng set cho hash để tìm kiếm nhanh hơn (O(1) thay vì O(n))
    tap_hash = set(danh_sach_hash)

    # Dict để lưu kết quả: {hash: mat_khau}
    ket_qua = {}

    # Biến đếm số lần thử
    so_lan_thu = 0

    print("\n" + "=" * 55)
    print("  BẮT ĐẦU QUÁ TRÌNH TÌM KIẾM...")
    print("=" * 55)

    # Lặp qua từng từ trong wordlist
    for tu in danh_sach_tu:
        so_lan_thu += 1

        # Tính SHA256 của từ hiện tại
        hash_cua_tu = tinh_sha256(tu)

        # In tiến trình mỗi 1000 lần thử để người dùng biết chương trình đang chạy
        if so_lan_thu % 1000 == 0:
            print(f"  ... Đã thử {so_lan_thu:,} từ | Tìm được: {len(ket_qua)} mật khẩu")

        # So sánh hash vừa tính với tập hash cần tìm
        if hash_cua_tu in tap_hash:
            # TRÙNG KHỚP! Lưu lại kết quả
            ket_qua[hash_cua_tu] = tu
            print(f"\n  ✓ TÌM THẤY! Hash: {hash_cua_tu[:16]}... → Mật khẩu: '{tu}'")

            # Xóa hash khỏi tập để không tìm lại nữa (tối ưu hóa)
            tap_hash.remove(hash_cua_tu)

            # Nếu đã tìm hết tất cả hash thì dừng sớm
            if len(tap_hash) == 0:
                print("\n  ✓ Đã tìm thấy tất cả mật khẩu! Dừng sớm.")
                break

    return ket_qua, so_lan_thu


# ----------------------------------------------------------
# HÀM 5: In báo cáo kết quả cuối cùng
# ----------------------------------------------------------
def in_bao_cao(danh_sach_hash, ket_qua, so_lan_thu, thoi_gian_giay):
    """
    In ra bảng tổng hợp kết quả sau khi chạy xong.
    """
    print("\n" + "=" * 55)
    print("  KẾT QUẢ THỐNG KÊ")
    print("=" * 55)

    # Thống kê tổng quát
    print(f"  Tổng số hash cần crack : {len(danh_sach_hash)}")
    print(f"  Số hash tìm được       : {len(ket_qua)}")
    print(f"  Số hash chưa tìm được  : {len(danh_sach_hash) - len(ket_qua)}")
    print(f"  Tổng số lần thử        : {so_lan_thu:,}")
    print(f"  Thời gian thực hiện    : {thoi_gian_giay:.3f} giây")

    # Tính tốc độ thử (số từ mỗi giây)
    if thoi_gian_giay > 0:
        toc_do = so_lan_thu / thoi_gian_giay
        print(f"  Tốc độ trung bình      : {toc_do:,.0f} từ/giây")

    # Bảng chi tiết các mật khẩu tìm được
    print("\n" + "-" * 55)
    print("  CHI TIẾT MẬT KHẨU TÌM ĐƯỢC:")
    print("-" * 55)

    if len(ket_qua) == 0:
        print("  (Không tìm thấy mật khẩu nào trong wordlist)")
    else:
        for hash_val, mat_khau in ket_qua.items():
            # Chỉ hiện 16 ký tự đầu của hash cho gọn
            print(f"  {hash_val[:16]}...  →  '{mat_khau}'")

    # Liệt kê các hash CHƯA tìm được
    hash_chua_tim = [h for h in danh_sach_hash if h not in ket_qua]
    if hash_chua_tim:
        print("\n" + "-" * 55)
        print("  HASH CHƯA TÌM ĐƯỢC (thử wordlist lớn hơn):")
        print("-" * 55)
        for hash_val in hash_chua_tim:
            print(f"  {hash_val[:16]}...")

    print("=" * 55 + "\n")


# ----------------------------------------------------------
# HÀM CHÍNH: Điều phối toàn bộ chương trình
# ----------------------------------------------------------
def main():
    print("=" * 55)
    print("   SHA256 HASH CRACKER - PHIÊN BẢN HỌC TẬP")
    print("=" * 55)

    # --- BƯỚC 1: Nhận tên file từ người dùng ---
    print("\nNhập đường dẫn đến file hash SHA256")
    print("(Ví dụ: hashes.txt)")
    file_hash = input("  > File hash: ").strip()

    print("\nNhập đường dẫn đến file wordlist")
    print("(Ví dụ: wordlist.txt, rockyou.txt)")
    file_wordlist = input("  > File wordlist: ").strip()

    # --- BƯỚC 2: Đọc dữ liệu từ file ---
    print()
    danh_sach_hash = doc_file_hash(file_hash)
    danh_sach_tu   = doc_file_wordlist(file_wordlist)

    # Kiểm tra nếu file rỗng hoặc không đọc được
    if not danh_sach_hash:
        print("[LỖI] Không có hash nào để crack. Thoát chương trình.")
        return
    if not danh_sach_tu:
        print("[LỖI] Wordlist rỗng. Thoát chương trình.")
        return

    # --- BƯỚC 3: Bắt đầu đếm thời gian và crack ---
    thoi_diem_bat_dau = time.time()  # Ghi lại thời điểm bắt đầu (giây Unix)

    ket_qua, so_lan_thu = crack_hash(danh_sach_hash, danh_sach_tu)

    thoi_diem_ket_thuc = time.time()  # Ghi lại thời điểm kết thúc

    # Tính tổng thời gian chạy
    thoi_gian_giay = thoi_diem_ket_thuc - thoi_diem_bat_dau

    # --- BƯỚC 4: In báo cáo kết quả ---
    in_bao_cao(danh_sach_hash, ket_qua, so_lan_thu, thoi_gian_giay)


# ----------------------------------------------------------
# ĐIỂM KHỞI CHẠY CHƯƠNG TRÌNH
# ----------------------------------------------------------
# Khối if này đảm bảo main() chỉ chạy khi ta chạy trực tiếp
# file này, không chạy khi file được import từ nơi khác.
if __name__ == "__main__":
    main()