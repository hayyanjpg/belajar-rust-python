# Materi 23: Tuple, Set, dan Unpacking Lanjutan
"""Catatan belajar Python: tuple (immutable), set (unik), dan unpacking lanjutan.

Semua contoh memakai standard library agar bisa dijalankan tanpa paket tambahan.
Jalankan dengan: python 23_tuple_set_unpacking.py
"""

from collections import namedtuple
from typing import NamedTuple

# namedtuple gaya lama: cocok untuk data ringan yang tidak ingin class penuh.
Menu = namedtuple("Menu", ["nama", "harga"])


# typing.NamedTuple gaya baru: lebih ramah type checker dan bisa ada docstring.
class Mahasiswa(NamedTuple):
    """Data mahasiswa sederhana."""

    nama: str
    nilai: int


def total_belanja(items: tuple[tuple[str, int], ...]) -> int:
    """Jumlahkan harga dari kumpulan pasangan (nama, harga)."""
    return sum(harga for _, harga in items)


def kata_unik(teks: str) -> set[str]:
    """Ambil kata unik (case-insensitive) setelah membersihkan tanda baca."""
    hasil: set[str] = set()
    for kata in teks.split():
        bersih = kata.strip(".,!?;:()").lower()
        if bersih:
            hasil.add(bersih)
    return hasil


def pasangkan(nama: list[str], nilai: list[int]) -> dict[str, int]:
    """zip(strict=True) akan error jika panjang kedua iterable berbeda."""
    return dict(zip(nama, nilai, strict=True))


def ringkasan_nilai(data: tuple[str, tuple[int, int]]) -> str:
    """Contoh unpacking bersarang: (nama, (uts, uas))."""
    nama, (uts, uas) = data
    return f"{nama}: UTS={uts}, UAS={uas}, rata-rata={(uts + uas) / 2}"


def pola_pengiriman(*angka: int, awal: int = 0) -> tuple[int, list[int]]:
    """*args menampung positional, keyword-only `awal` menjadi nilai awal."""
    diterima = [awal + nilai for nilai in angka]
    return sum(diterima), diterima


def demo() -> None:
    print("=== TUPLE ===")
    koordinat: tuple[int, int] = (3, 4)
    print("Tuple:", koordinat, "index 0:", koordinat[0])
    print("Tuple satu elemen butuh koma:", (42,))
    print("Tuple bisa di-slice:", koordinat[0:1])

    menu = Menu("kopi", 18000)
    print("namedtuple:", menu.nama, menu.harga, "->", tuple(menu))

    mhs = Mahasiswa("Hayyan", 90)
    print("NamedTuple:", mhs.nama, mhs.nilai, "->", mhs._asdict())

    print("\n=== SET ===")
    daftar_hobi = ["baca", "koding", "baca", "musik"]
    hobi = set(daftar_hobi)
    print("Set otomatis unik:", hobi)
    hobi.add("olahraga")
    hobi.discard("musik")
    print("Setelah add/discard:", hobi)
    lain = {"koding", "masak"}
    print("Union:", hobi | lain)
    print("Intersection:", hobi & lain)
    print("Difference:", hobi - lain)
    print("Symmetric difference:", hobi ^ lain)
    print("Subset:", {"koding"} <= hobi, "Superset:", hobi >= {"baca"})
    print("frozenset (immutable):", frozenset([1, 2, 2, 3]))

    print("\n=== UNPACKING ===")
    a, b = (10, 20)
    print("Unpacking dasar:", a, b)

    pertama, *tengah, terakhir = [1, 2, 3, 4, 5]
    print("Starred unpacking:", pertama, tengah, terakhir)

    nilai, (uts, uas) = ("Rina", (75, 85))
    print("Unpacking bersarang:", nilai, uts, uas)

    data_siswa = ["Hayyan", "Rina", "Budi"]
    skor = [90, 85, 70]
    print("zip + enumerate:", list(enumerate(zip(data_siswa, skor), start=1)))
    print("pasangkan():", pasangkan(data_siswa, skor))

    total, diterima = pola_pengiriman(1, 2, 3, awal=10)
    print("pola_pengiriman():", diterima, "total:", total)

    print("\n=== CONTOH PEMAKAIAN ===")
    belanja = (("kopi", 18000), ("roti", 12000), ("kopi", 18000))
    print("Total belanja:", total_belanja(belanja))
    print("Kata unik:", sorted(kata_unik("Rust cepat, Python Rust di sini!")))
    print("Ringkasan:", ringkasan_nilai(("Hayyan", (80, 90))))


def latihan() -> None:
    """Latihan kecil dengan assert supaya bisa dicek otomatis."""
    assert total_belanja((("a", 1), ("b", 2))) == 3
    assert total_belanja(()) == 0

    assert kata_unik("Apa apa, APA!") == {"apa"}
    assert kata_unik("  ") == set()

    assert pasangkan(["a", "b"], [1, 2]) == {"a": 1, "b": 2}

    assert ringkasan_nilai(("Budi", (70, 80))) == (
        "Budi: UTS=70, UAS=80, rata-rata=75.0"
    )

    total, diterima = pola_pengiriman(2, 4, awal=1)
    assert diterima == [3, 5]
    assert total == 8

    print("Latihan materi 23: semua assert lolos.")


if __name__ == "__main__":
    demo()
    latihan()
