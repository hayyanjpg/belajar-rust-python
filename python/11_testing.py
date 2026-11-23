# Materi 11: Testing (Testing dengan unittest dan pytest)
# Testing penting untuk memastikan code berjalan sesuai harapan.
# Python punya built-in unittest dan pytest framework yang populer.

import unittest
from unittest.mock import MagicMock

import pytest


# ============================================
# 1. Fungsi yang akan diuji
# ============================================
def tambah(a, b):
    return a + b


def kurang(a, b):
    return a - b


def faktorial(n):
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    if n <= 1:
        return 1
    return n * faktorial(n - 1)


def kali(a, b):
    return a * b


def bagi(a, b):
    if b == 0:
        raise ValueError("Tidak bisa membagi dengan nol")
    return a / b


# ============================================
# 2. unittest - Built-in Testing Framework
# ============================================
# Jalankan dengan: python -m unittest python/11_testing.py -v


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

    def test_faktorial_negatif(self):
        with self.assertRaises(ValueError):
            faktorial(-1)

    def test_tambah_type_error(self):
        with self.assertRaises(TypeError):
            tambah(2, "3")


# ============================================
# 3. pytest - Framework Testing Populer
# ============================================
# pytest lebih sederhana dan fleksibel.
# Install: pip install pytest
# Tulis fungsi dengan prefix test_ dan gunakan assert.
# Jalankan dengan: pytest python/11_testing.py -v


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
# Fixture adalah setup/teardown yang bisa dipakai berulang.


@pytest.fixture
def data_siswa():
    """Setup data yang dipakai oleh beberapa test."""
    return {"nama": "Hayyan", "nilai": [80, 90, 100]}


def test_fixture_isi_data(data_siswa):
    assert data_siswa["nama"] == "Hayyan"
    assert len(data_siswa["nilai"]) == 3


def test_fixture_rata_rata(data_siswa):
    nilai = data_siswa["nilai"]
    assert sum(nilai) / len(nilai) == 90


# ============================================
# 5. Mocking
# ============================================
# Mocking menggantikan dependency dengan objek tiruan.


def test_mocking():
    mock = MagicMock()
    mock.halo.return_value = "Halo Mock!"
    assert mock.halo() == "Halo Mock!"
    mock.halo.assert_called_once()


# ============================================
# LATIHAN TAMBAHAN (Exercise)
# ============================================

# Latihan 1: Test untuk string


def test_string_manipulation():
    assert "hello".upper() == "HELLO"
    assert "HELLO".lower() == "hello"
    assert ["hello", "world"] == ["hello", "world"]


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
# Decorator parametrize HARUS menempel pada fungsi test level modul,
# bukan pada fungsi di dalam fungsi (kalau di dalam, test tidak pernah jalan).


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_tambah_parameter(a, b, expected):
    assert tambah(a, b) == expected


# Latihan 5: Test file handling (fixture bawaan pytest: tmp_path)


def test_file_handling(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello Testing")
    content = file_path.read_text()
    assert content == "Hello Testing"


# ============================================
# Menjalankan test (hanya jika file dijalankan langsung)
# ============================================
if __name__ == "__main__":
    # exit=False supaya proses tidak langsung berhenti setelah unittest selesai
    unittest.main(exit=False, verbosity=2)
    print("\nSemua test pytest bisa dijalankan dengan: pytest python/11_testing.py -v")
