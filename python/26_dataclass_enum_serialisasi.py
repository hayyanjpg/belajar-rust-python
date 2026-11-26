# Materi 26: Dataclass, Enum, dan Serialisasi JSON
"""Model data rapi dengan dataclass + enum, lalu convert ke/dari JSON.

Jalankan dengan: python 26_dataclass_enum_serialisasi.py
"""

from __future__ import annotations

import json
from dataclasses import asdict, astuple, dataclass, field, replace
from enum import Enum, IntEnum, auto
from typing import Any


class StatusPesanan(Enum):
    """Enum: nilai stabil dan mudah dibaca, bukan string bebas."""

    MENUNGGU = auto()
    DIPROSES = auto()
    SELESAI = auto()


class Prioritas(IntEnum):
    """IntEnum bisa dibandingkan dengan int biasa."""

    RENDAH = 1
    SEDANG = 2
    TINGGI = 3


@dataclass
class Produk:
    """dataclass otomatis membuat __init__, __repr__, __eq__, dll."""

    nama: str
    harga: int
    tags: list[str] = field(default_factory=list)

    def ringkas(self) -> str:
        return f"{self.nama} ({self.harga})"


@dataclass(frozen=True, slots=True)
class Pesanan:
    """frozen = immutable; slots = lebih hemat memori."""

    id: int
    produk: Produk
    status: StatusPesanan = StatusPesanan.MENUNGGU
    prioritas: Prioritas = Prioritas.SEDANG


def ke_dict(pesanan: Pesanan) -> dict[str, Any]:
    """asdict() mengubah nested dataclass menjadi dict biasa."""
    data = asdict(pesanan)
    data["status"] = pesanan.status.name
    data["prioritas"] = int(pesanan.prioritas)
    return data


def dari_dict(data: dict[str, Any]) -> Pesanan:
    """Bangun kembali Pesanan dari dict hasil JSON."""
    produk_data = data["produk"]
    if not isinstance(produk_data, dict):
        raise TypeError("field 'produk' harus berupa object")

    return Pesanan(
        id=int(data["id"]),
        produk=Produk(
            nama=str(produk_data["nama"]),
            harga=int(produk_data["harga"]),
            tags=list(produk_data.get("tags", [])),
        ),
        status=StatusPesanan[str(data["status"])],
        prioritas=Prioritas(int(data["prioritas"])),
    )


def ke_json(pesanan: Pesanan) -> str:
    """JSON tidak tahu Enum, jadi kita ubah ke nama/int dulu."""
    return json.dumps(ke_dict(pesanan), ensure_ascii=False)


def dari_json(teks: str) -> Pesanan:
    data = json.loads(teks)
    if not isinstance(data, dict):
        raise TypeError("JSON harus berupa object")
    return dari_dict(data)


def demo() -> None:
    print("=== ENUM ===")
    print("Status:", list(StatusPesanan))
    print("Status sekarang:", StatusPesanan.DIPROSES.name, StatusPesanan.DIPROSES.value)
    print("Prioritas tinggi > sedang:", Prioritas.TINGGI > Prioritas.SEDANG)

    print("\n=== DATACLASS ===")
    kopi = Produk("Kopi Susu", 18000, ["minuman", "panas"])
    print("Produk:", kopi)
    print("Ringkas:", kopi.ringkas())
    print("astuple:", astuple(kopi))

    pesanan = Pesanan(1, kopi, StatusPesanan.DIPROSES, Prioritas.TINGGI)
    print("Pesanan:", pesanan)
    print("Transfer:")

    # replace() membuat salinan dengan sebagian field diubah.
    selesai = replace(pesanan, status=StatusPesanan.SELESAI)
    print("  versi selesai:", selesai)
    print("  pesanan awal tetap:", pesanan.status)

    print("\n=== SERIALISASI ===")
    teks = ke_json(pesanan)
    print("JSON:", teks)
    kembali = dari_json(teks)
    print("Hasil JSON -> objek:", kembali)
    print("Sama dengan semula:", kembali == pesanan)


def latihan() -> None:
    produk = Produk("Roti", 12000)
    pesanan = Pesanan(7, produk)

    assert pesanan.status is StatusPesanan.MENUNGGU
    assert ke_dict(pesanan)["status"] == "MENUNGGU"
    assert dari_json(ke_json(pesanan)) == pesanan

    assert int(Prioritas.TINGGI) == 3
    assert StatusPesanan["MENUNGGU"].name == "MENUNGGU"

    ubah = replace(pesanan, status=StatusPesanan.SELESAI)
    assert ubah.status is StatusPesanan.SELESAI
    assert pesanan.status is StatusPesanan.MENUNGGU

    produk.tags.append("makanan")
    assert produk.tags == ["makanan"]

    print("Latihan materi 26: semua assert lolos.")


if __name__ == "__main__":
    demo()
    latihan()
