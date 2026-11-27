# Materi 30: Benchmark Mikro dengan timeit
"""Materi benchmarking memakai modul stdlib ``timeit``.

Jalankan dengan: python 30_benchmark_timeit.py
"""

from collections.abc import Callable
from timeit import repeat, timeit


def gabung_dengan_tambah(jumlah: int) -> str:
    """Gabung string dengan operator + di dalam loop."""
    hasil = ""
    for angka in range(jumlah):
        hasil += str(angka)
    return hasil


def gabung_dengan_join(jumlah: int) -> str:
    """Gabung string dengan str.join (lebih efisien)."""
    return "".join(str(angka) for angka in range(jumlah))


def cari_linear(nilai: list[int], target: int) -> bool:
    """Cari target dengan memindai satu per satu."""
    return target in nilai


def cari_dengan_set(nilai: set[int], target: int) -> bool:
    """Cari target dengan lookup hash set."""
    return target in nilai


def ukur(judul: str, fungsi: Callable[[], object], number: int = 2000) -> float:
    """Ukur waktu tercepat dari beberapa kali pengulangan."""
    hasil = repeat(fungsi, number=number, repeat=3)
    tercepat = min(hasil)
    print(f"{judul:28} {tercepat:.6f} detik / {number} kali")
    return tercepat


def demo() -> None:
    print("=== DEMO BENCHMARK timeit ===")
    print("timeit.pyttime():", round(timeit("sum(range(100))", number=1000), 6))
    ukur("gabung dengan +", lambda: gabung_dengan_tambah(200))
    ukur("gabung dengan join", lambda: gabung_dengan_join(200))

    daftar = list(range(1000))
    kumpulan = set(daftar)
    ukur("cari di list", lambda: cari_linear(daftar, 999))
    ukur("cari di set", lambda: cari_dengan_set(kumpulan, 999))


def latihan() -> None:
    """Pastikan kedua versi menghasilkan output yang sama."""
    assert gabung_dengan_tambah(20) == gabung_dengan_join(20)

    daftar = [1, 2, 3, 4, 5]
    kumpulan = set(daftar)
    for target in (1, 3, 5):
        assert cari_linear(daftar, target) == cari_dengan_set(kumpulan, target)
    assert not cari_linear(daftar, 99)
    assert not cari_dengan_set(kumpulan, 99)

    print("Latihan materi 30: semua assert lolos.")


if __name__ == "__main__":
    demo()
    latihan()
