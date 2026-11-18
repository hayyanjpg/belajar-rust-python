# Materi 11: Testing (Testing dengan unittest dan pytest)
# Testing penting untuk memastikan code berjalan sesuai harapan.
# Python punya built-in unittest dan pytest framework yang populer.

import unittest
import pytest

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
import pytest


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

# ============================================
# 3. pytest - Framework Testing Populer
# ============================================
print("\n=== 3. pytest ===")

# pytest lebih sederhana dan fleksibel.
# Install: pip install pytest
# Tulis fungsi dengan prefix test_ dan gunakan assert.

# Contoh fungsi yang diuji


def kali(a, b):
    return a * b


def bagi(a, b):
    if b == 0:
        raise ValueError("Tidak bisa membagi dengan nol")
    return a / b


# Test dengan pytest (fungsi test_ dan assert)
# Bisa dijalankan dengan: pytest python/11_testing.py


def test_kali():
    assert kali(2, 3) == 6
    assert kali(0, 5) == 0


def test_bagi():
    assert bagi(10, 2) == 5
    with pytest.raises(ValueError):
        bagi(10, 0)


# ============================================
# 4. Testing dengan Fixture
# ============================================
print("\n=== 4. Fixture ===")

# Fixture adalah setup dan teardown yang bisa dipakai berulang.


def test_with_fixture():
    data = [1, 2, 3, 4, 5]
    assert len(data) == 5
    assert sum(data) == 15


# ============================================
# 5. Mocking
# ============================================
print("\n=== 5. Mocking ===")

# Mocking menggantikan dependency dengan objek tiruan.


def test_mocking():
    from unittest.mock import MagicMock

    mock = MagicMock()
    mock.halo.return_value = "Halo Mock!"
    assert mock.halo() == "Halo Mock!"

# ============================================
# LATIHAN TAMBAHAN (Exercise)
# ============================================

print("\n=== LATIHAN TAMBAHAN ===")


# Latihan 1: Buat test untuk string


def test_string_manipulation():
    assert "hello".upper() == "HELLO"
    assert "HELLO".lower() == "hello"
    assert "hello world".split() == ["hello", "world"]


# Latihan 2: Test exception


def test_exception_handling():
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0


# Latihan 3: Test class


class Kalkulator:
    def __init__(self):
        self.hasil = 0

    def tambah(self, x):
        self.hasil += x
        return self.hasil

    def reset(self):
        self.hasil = 0


def test_kalkulator():
    calc = Kalkulator()
    calc.tambah(5)
    assert calc.hasil == 5
    calc.tambah(3)
    assert calc.hasil == 8
    calc.reset()
    assert calc.hasil == 0


# Latihan 4: Test dengan parameter


def test_parameter():
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (2, 3, 5),
        (0, 0, 0),
    ])
    def _test(a, b, expected):
        assert tambah(a, b) == expected


# Latihan 5: Test file handling


def test_file_handling(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello Testing")
    content = file_path.read_text()
    assert content == "Hello Testing"