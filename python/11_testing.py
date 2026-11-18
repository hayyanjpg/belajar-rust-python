# Materi 11: Testing (Testing dengan unittest dan pytest)
# Testing penting untuk memastikan code berjalan sesuai harapan.
# Python punya built-in unittest dan pytest framework yang populer.

# ============================================
# 1. Pengenalan Testing
# ============================================
print("=== 1. Pengenalan Testing ===")

# Testing dilakukan dengan:
# - unittest (built-in)
# - pytest (paling populer, perlu pip install pytest)

# File test biasanya di folder tests/ atau prefix test_*.py

# ============================================
# 2. unittest - Built-in Testing Framework
# ============================================
print("\n=== 2. unittest ===")

import unittest


# Fungsi yang akan diuji
def tambah(a, b):
    return a + b


def kurang(a, b):
    return a - b


def faktorial(n):
    if n <= 1:
        return 1
    return n * faktorial(n - 1)


# Class test
class TestMatematika(unittest.TestCase):
    def test_tambah(self):
        self.assertEqual(tambah(2, 3), 5)
        self.assertEqual(tambah(-1, 1), 0)

    def test_kurang(self):
        self.assertEqual(kurang(5, 3), 2)
        self.assertEqual(kurang(0, 5), -5)

    def test_faktorial(self):
        self.assertEqual(faktorial(0), 1)
        self.assertEqual(faktorial(1), 1)
        self.assertEqual(faktorial(5), 120)

    def test_tambah_type_error(self):
        with self.assertRaises(TypeError):
            tambah(2, "3")


# Menjalankan test (hanya jika file dijalankan langsung)
if __name__ == "__main__":
    unittest.main()