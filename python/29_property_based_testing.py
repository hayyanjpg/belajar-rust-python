# Materi 29: Property-Based Testing dengan Hypothesis
"""Materi pengujian berbasis properti: menguji aturan, bukan contoh tunggal.

Jalankan dengan: python 29_property_based_testing.py
"""

from itertools import pairwise

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st


def balik_kata(teks: str) -> str:
    """Balik urutan karakter."""
    return teks[::-1]


def jumlah_genap(a: int, b: int) -> int:
    """Jumlahkan dua bilangan genap."""
    if a % 2 != 0 or b % 2 != 0:
        raise ValueError("kedua argumen harus genap")
    return a + b


def rata_rata(nilai: list[int]) -> float:
    """Hitung rata-rata sekumpulan bilangan."""
    if not nilai:
        raise ValueError("daftar tidak boleh kosong")
    return sum(nilai) / len(nilai)


@settings(
    max_examples=50,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
@given(teks=st.text())
def test_balik_kata_invansi(teks: str) -> None:
    """Membalik dua kali harus kembali ke teks semula."""
    assert balik_kata(balik_kata(teks)) == teks


genap: st.SearchStrategy[int] = st.integers().filter(lambda angka: angka % 2 == 0)


@given(a=genap, b=genap)
def test_jumlah_genap(a: int, b: int) -> None:
    """Hasil penjumlahan dua bilangan genap selalu genap."""
    assert jumlah_genap(a, b) % 2 == 0


@given(
    nilai=st.lists(
        st.integers(min_value=-1000, max_value=1000),
        min_size=1,
        max_size=20,
    )
)
def test_rata_rata_dalam_rentang(nilai: list[int]) -> None:
    """Rata-rata tidak boleh di luar nilai minimum dan maksimum."""
    hasil = rata_rata(nilai)
    assert min(nilai) <= hasil <= max(nilai)


def demo() -> None:
    print("=== DEMO PROPERTY-BASED TESTING ===")
    print("Menguji 3 properti dengan data yang dibangkitkan Hypothesis...")
    test_balik_kata_invansi()
    test_jumlah_genap()
    test_rata_rata_dalam_rentang()
    print("Semua properti lolos.")


def latihan() -> None:
    """Latihan: buktikan properti sorting dengan strategi Hypothesis."""

    @settings(max_examples=25, deadline=None)
    @given(nilai=st.lists(st.integers(), max_size=15))
    def urut_terurut(nilai: list[int]) -> None:
        tersusun = sorted(nilai)
        assert all(a <= b for a, b in pairwise(tersusun))
        assert len(tersusun) == len(nilai)

    urut_terurut()
    print("Latihan materi 29: properti sorting lolos.")


if __name__ == "__main__":
    demo()
    latihan()
