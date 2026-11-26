# Test pytest untuk Materi 23: Tuple, Set, dan Unpacking Lanjutan
"""Test untuk modul bernomor.

Nama file materi diawali angka sehingga tidak bisa di-import dengan
`import 23_...`. `importlib.import_module` mengatasi hal ini dan dipakai
di sini supaya materi tetap bisa diuji otomatis.
"""

import importlib
from types import ModuleType

import pytest

materi: ModuleType = importlib.import_module("23_tuple_set_unpacking")


def test_tuple_dan_total_belanja() -> None:
    belanja = (("kopi", 18000), ("roti", 12000), ("es", 5000))
    assert materi.total_belanja(belanja) == 35000
    assert materi.total_belanja(()) == 0


def test_kata_unik_membersihkan_tanda_baca() -> None:
    assert materi.kata_unik("Rust, Python! rust?") == {"rust", "python"}
    assert materi.kata_unik(". , !") == set()


def test_pasangkan_zip_strict() -> None:
    assert materi.pasangkan(["a", "b"], [1, 2]) == {"a": 1, "b": 2}

    with pytest.raises(ValueError):
        materi.pasangkan(["a", "b"], [1])


def test_ringkasan_nilai_unpacking_bersarang() -> None:
    hasil = materi.ringkasan_nilai(("Sari", (60, 80)))
    assert hasil == "Sari: UTS=60, UAS=80, rata-rata=70.0"


def test_pola_pengiriman_args_dan_keyword_only() -> None:
    total, diterima = materi.pola_pengiriman(1, 3, 5, awal=10)
    assert diterima == [11, 13, 15]
    assert total == 39


def test_fungsi_latihan_dalam_materi() -> None:
    # latihan() memakai assert; panggil untuk memastikan tidak ada yang gagal.
    materi.latihan()
