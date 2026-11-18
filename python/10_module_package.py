# Materi 10: Module dan Package
# Module adalah file Python yang berisi definisi fungsi, class, atau variabel.
# Package adalah kumpulan module yang disusun dalam satu direktori dengan __init__.py.

# ============================================
# 1. Membuat dan Mengimpor Module
# ============================================
print("=== 1. Module Dasar ===")

# Catatan: file ini bisa diimpor oleh file lain sebagai module.
# Fungsi dan variabel di bawah ini bisa diakses oleh module lain.


def halo(nama):
    return f"Halo, {nama}!"


PI = 3.14159


def hitung_luas_lingkar(jari_jari):
    return 2 * PI * jari_jari


print(halo("Dunia"))
print(f"Lingkaran r=5: {hitung_luas_lingkar(5):.2f}")

# ============================================
# 2. Import Statements
# ============================================
print("\n=== 2. Import ===")

# import math - mengakses fungsi standar
import math

print(f"Akar 25 = {math.sqrt(25)}")
print(f"Pi = {math.pi}")

# from ... import ... - mengimpor spesifik
from datetime import datetime

now = datetime.now()
print(f"Waktu sekarang: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# import with alias
import pandas as pd  # contoh library populer

# ============================================
# 3. Mengelola Package
# ============================================
print("\n=== 3. Package ===")

# Struktur package contoh:
# mypackage/
#   __init__.py        # dijalankan saat package diimpor
#   matematika.py      # module
#   util.py            # module

# Cara mengimpor:
# from mypackage.matematika import tambah, kurang

# ============================================
# 4. __init__.py dan __all__
# ============================================
print("\n=== 4. __init__.py ===")

# __init__.py bisa berisi inisialisasi package, mengimpor modul, atau mendefinisikan __all__
# __all__ mengontrol apa yang diekspor saat using "from package import *"

# Contoh:
# __all__ = ['tambah', 'kurang']

# ============================================
# 5. Menjalankan Module Sebagai Script
# ============================================
print("\n=== 5. if __name__ == '__main__' ===")

# Jika file dijalankan langsung: __name__ == '__main__'
# Jika file diimpor: __name__ == nama module


def main():
    print("Modul dijalankan sebagai script!")


if __name__ == "__main__":
    main()
else:
    print("Modul diimpor, tidak dijalankan otomatis.")

# ============================================
# LATIHAN TAMBAHAN (Exercise)
# ============================================

print("\n=== LATIHAN TAMBAHAN ===")


# Latihan 1: Buat module sederhana


def faktorial(n):
    if n <= 1:
        return 1
    return n * faktorial(n - 1)


print(f"\nLatihan 1 - Faktorial 5 = {faktorial(5)}")

# Latihan 2: Gunakan modul datetime


from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
print(f"Latihan 2 - Hari ini: {today}, Besok: {tomorrow}")

# Latihan 3: Buat package struktur


# Buat direktori dan file:
# utils/
#   __init__.py
#   string_utils.py


def reverse_string(s):
    return s[::-1]


print(f"Latihan 3 - Reverse 'python': {reverse_string('python')}")

# Latihan 4: Import dengan from


from math import ceil, floor, pow

print(f"Latihan 4 - ceil(3.2)={ceil(3.2)}, floor(3.8)={floor(3.8)}, pow(2,3)={pow(2,3)}")

# Latihan 5: Cek __name__


print(f"Latihan 5 - Nama modul: {__name__}")

# ============================================
# LATIHAN TAMBAHAN 2 (Exercise 6-10)
# ============================================

print("\n=== LATIHAN TAMBAHAN 2 ===")


# Latihan 6: Buat fungsi modular


def hitung_rata_rata(*args):
    if not args:
        return 0
    return sum(args) / len(args)


print(f"Latihan 6 - Rata-rata (80,90,75): {hitung_rata_rata(80, 90, 75):.1f}")

# Latihan 7: Gunakan modul os


import os

current_dir = os.getcwd()
files = os.listdir(current_dir)
print(f"Latihan 7 - File di current dir: {len(files)} file")

# Latihan 8: Buat konstanta


GRAVITASI_BUMI = 9.81  # m/s^2


def hitung_kecepatan(jarak, waktu):
    return jarak / waktu


kecepatan = hitung_kecepatan(100, 10)
print(f"Latihan 8 - Kecepatan: {kecepatan} m/s, G={GRAVITASI_BUMI}")

# Latihan 9: Import multiple modules


import sys
import json

data = {"nama": "Hayyan", "umur": 20}
json_str = json.dumps(data)
print(f"Latihan 9 - JSON: {json_str}")
print(f"Latihan 9 - Python version: {sys.version_info.major}.{sys.version_info.minor}")

# Latihan 10: Buat dan gunakan variabel global


GLOBAL_KONSTANS = "Modul 10"
print(f"Latihan 10 - {GLOBAL_KONSTANS} - Selesai!")