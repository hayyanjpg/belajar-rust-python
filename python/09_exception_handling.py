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