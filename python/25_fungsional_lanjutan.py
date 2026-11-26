# Materi 25: Pemrograman Fungsional Lanjutan
"""Materi functools, itertools, closure, dan fungsi sebagai nilai.

Jalankan dengan: python 25_fungsional_lanjutan.py
"""

from functools import lru_cache, partial, reduce, singledispatch
from itertools import accumulate, chain, groupby, islice, permutations


def kali(a: int, b: int) -> int:
    return a * b


def harga_diskon(persentase: int, harga: int) -> int:
    """Fungsi dua argumen yang akan dipartial menjadi satu argumen."""
    return harga - (harga * persentase // 100)


@lru_cache(maxsize=128)
def faktorial(n: int) -> int:
    """lru_cache menyimpan hasil agar perhitungan berulang jadi cepat."""
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    if n <= 1:
        return 1
    return n * faktorial(n - 1)


@singledispatch
def deskripsi(nilai: object) -> str:
    """Implementasi default singledispatch."""
    return f"objek: {nilai!r}"


@deskripsi.register
def deskripsi_int(nilai: int) -> str:
    return f"bilangan bulat: {nilai}"


@deskripsi.register
def deskripsi_list(nilai: list) -> str:
    return f"list dengan {len(nilai)} elemen"


def pembuat_pengali(faktor: int):
    """Closure: fungsi dalam mengingat variabel dari scope luar."""

    def pengali(nilai: int) -> int:
        return nilai * faktor

    return pengali


def grupkan_awal(kata: list[str]) -> dict[str, list[str]]:
    """groupby hanya mengelompokkan yang berurutan, jadi data diurutkan dulu."""
    terurut = sorted(kata, key=str.lower)
    return {
        huruf: list(kelompok)
        for huruf, kelompok in groupby(terurut, key=lambda item: item[0].lower())
    }


def demo() -> None:
    print("=== REDUCE ===")
    angka = [1, 2, 3, 4, 5]
    print("Data:", angka)
    print("Product dengan reduce:", reduce(kali, angka, 1))
    print("Jumlah dengan reduce:", reduce(lambda a, b: a + b, angka, 0))

    print("\n=== PARTIAL ===")
    diskon_20 = partial(harga_diskon, 20)
    for harga in [100_000, 250_000]:
        print(f"  {harga} -> {diskon_20(harga)}")

    print("\n=== LRU_CACHE ===")
    print("faktorial(10):", faktorial(10))
    print("faktorial(10) lagi (cache hit):", faktorial(10))
    print("Info cache:", faktorial.cache_info())

    print("\n=== SINGLE_DISPATCH ===")
    for nilai in [7, [1, 2, 3], {"a": 1}]:
        print(" ", deskripsi(nilai))

    print("\n=== CLOSURE ===")
    kali_tiga = pembuat_pengali(3)
    kali_lima = pembuat_pengali(5)
    print("kali_tiga(7):", kali_tiga(7), "kali_lima(7):", kali_lima(7))

    print("\n=== ITERTOOLS ===")
    print("chain:", list(chain([1, 2], ["a", "b"])))
    print("accumulate:", list(accumulate([1, 2, 3, 4])))
    print("permutations (3 ambil 2):", list(permutations([1, 2, 3], 2)))
    print("islice:", list(islice(range(100), 5, 10)))
    print("groupby:", grupkan_awal(["Apel", "anggur", "Buku", "apel"]))


def latihan() -> None:
    assert reduce(kali, [2, 3, 4], 1) == 24
    assert partial(harga_diskon, 50)(200) == 100

    assert faktorial(6) == 720
    assert faktorial(6) == 720
    assert faktorial.cache_info().hits >= 1

    assert deskripsi(5) == "bilangan bulat: 5"
    assert deskripsi([1, 2]) == "list dengan 2 elemen"

    assert pembuat_pengali(4)(3) == 12
    assert list(accumulate([1, 2, 3])) == [1, 3, 6]
    assert list(islice(range(10), 2, 5)) == [2, 3, 4]

    hasil = grupkan_awal(["Apel", "anggur", "Buku"])
    assert sorted(hasil) == ["a", "b"]
    assert len(hasil["a"]) == 2

    print("Latihan materi 25: semua assert lolos.")


if __name__ == "__main__":
    demo()
    latihan()
