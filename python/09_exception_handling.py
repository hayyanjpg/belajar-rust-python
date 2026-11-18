# Materi 09: Exception Handling (Penanganan Error)
# Python menggunakan exception handling untuk menangani kesalahan yang terjadi saat runtime.
# Struktur dasar: try, except, finally, raise, else.

# ============================================
# 1. try / except dasar
# ============================================
print("=== 1. Try/Except Dasar ===")

try:
    # Kode yang mungkin mengalami error
    angka = int("abc")  # ValueError: invalid literal for int() with base 10
except ValueError as e:
    print(f"Terjadi kesalahan: {e}")
except Exception as e:
    print(f"Kesalahan umum: {e}")
else:
    # else dijalankan jika try tidak mengalami exception
    print("Kode berjalan tanpa error!")
finally:
    # finally selalu dijalankan, meskipun ada return/exception
    print("Finally: blok ini selalu dijalankan.\n")

# ============================================
# 2. Beberapa contoh exception yang umum
# ============================================
print("=== 2. Jenis Exception ===")

contoh_exceptions = [
    ("ZeroDivisionError", lambda: 10 / 0),
    ("TypeError", lambda: 10 + "20"),
    ("IndexError", lambda: [1, 2, 3][5]),
    ("KeyError", lambda: {"nama": "Hayyan"}["umur"]),
    ("FileNotFoundError", lambda: open("file_tidak_ada.txt")),
]

for nama, fungsi in contoh_exceptions:
    try:
        fungsi()
    except Exception as e:
        print(f"  {nama}: {type(e).__name__} - {e}")

print()

# ============================================
# 3. raise - Membuat exception sendiri
# ============================================
print("=== 3. Membuat Exception dengan raise ===")


def cek_umur(umur):
    if umur < 0:
        raise ValueError("Umur tidak boleh negatif!")
    if umur > 150:
        raise ValueError("Umur tidak masuk akal!")
    return True


try:
    cek_umur(-5)
except ValueError as e:
    print(f"Error: {e}")

# ============================================
# 4. Custom Exception Class
# ============================================
print("=== 4. Custom Exception ===")


class CustomError(Exception):
    """Exception khusus untuk contoh."""

    def __init__(self, pesan, code):
        super().__init__(pesan)
        self.code = code


try:
    raise CustomError("Ini adalah custom error", 999)
except CustomError as e:
    print(f"Custom Error: {e} (code: {e.code})")

# ============================================
# 5. Multiple except with tuple
# ============================================
print("=== 5. Multiple Except ===")


def hitung_bagi(a, b):
    try:
        result = a / b
        print(f"Hasil: {result}")
    except (ZeroDivisionError, TypeError) as e:
        print(f"Error: {type(e).__name__} - {e}")


hitung_bagi(10, 2)
hitung_bagi(10, 0)
hitung_bagi(10, "2")

# ============================================
# LATIHAN TAMBAHAN (Exercise)
# ============================================

print("\n=== LATIHAN TAMBAHAN ===")


# Latihan 1: Buat fungsi yang mengenerate custom exception


class InvalidEmailError(Exception):
    """Exception untuk email yang tidak valid."""

    def __init__(self, email):
        self.email = email
        super().__init__(f"Email tidak valid: {email}")


def validasi_email(email):
    if "@" not in email or "." not in email:
        raise InvalidEmailError(email)
    return True


try:
    validasi_email("tidakvalid")
except InvalidEmailError as e:
    print(f"Latihan 1 - {e}")

# Latihan 2: Hitung rata-rata dengan penanganan error


def hitung_rata_rata(nilai_list):
    if not nilai_list:
        raise ValueError("Daftar nilai tidak boleh kosong")
    return sum(nilai_list) / len(nilai_list)


try:
    result = hitung_rata_rata([80, 90, 75, 85])
    print(f"Latihan 2 - Rata-rata: {result:.1f}")
except ValueError as e:
    print(f"Latihan 2 - Error: {e}")

# Latihan 3: with statement untuk file (context manager exception)


print("\nLatihan 3 - Menulis file dengan with statement:")
try:
    with open("contoh_tulis.txt", "w") as f:
        f.write("Ini adalah contoh penulisan file.\n")
    print("  File tertulis.")
except IOError as e:
    print(f"  Gagal menulis file: {e}")

# Latihan 4: Baca file dengan exception handling


print("\nLatihan 4 - Membaca file:")
try:
    with open("contoh_tulis.txt", "r") as f:
        konten = f.read()
    print(f"  Konten: {konten.strip()}")
except FileNotFoundError:
    print("  File tidak ditemukan.")
except PermissionError:
    print("  Tidak ada izin membaca.")

# Latihan 5: Exception chaining


print("\nLatihan 5 - Exception chaining:")
try:
    try:
        angka = int("not_a_number")
    except ValueError as original:
        raise RuntimeError("Gagal mengonversi angka") from original
except RuntimeError as e:
    print(f"  Error: {e}")
    print(f"  Dari: {e.__cause__}")