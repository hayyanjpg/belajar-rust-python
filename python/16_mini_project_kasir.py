# Materi 16: Mini Project - Kasir Sederhana
# Menggabungkan materi sebelumnya: OOP, exception, file JSON, type hints,
# comprehension, dan standard library.
#
# Jalankan demo   : python 16_mini_project_kasir.py
# Mode interaktif: python 16_mini_project_kasir.py --interactive

from __future__ import annotations

import json
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


# ============================================
# 1. CUSTOM EXCEPTION
# ============================================
class StokTidakCukup(Exception):
    """Dilempar saat jumlah yang diminta melebihi stok."""

    def __init__(self, nama: str, diminta: int, tersedia: int) -> None:
        self.nama = nama
        self.diminta = diminta
        self.tersedia = tersedia
        super().__init__(
            f"Stok {nama} tidak cukup: diminta {diminta}, tersedia {tersedia}"
        )


class ProdukTidakDitemukan(Exception):
    """Dilempar saat produk tidak ada di katalog."""


# ============================================
# 2. MODEL DATA
# ============================================
@dataclass
class Produk:
    nama: str
    harga: int
    stok: int

    def __post_init__(self) -> None:
        if self.harga < 0:
            raise ValueError("Harga tidak boleh negatif")
        if self.stok < 0:
            raise ValueError("Stok tidak boleh negatif")


@dataclass
class ItemKeranjang:
    produk: Produk
    jumlah: int

    @property
    def subtotal(self) -> int:
        return self.produk.harga * self.jumlah


# ============================================
# 3. KATALOG & KERANJANG
# ============================================
class Katalog:
    def __init__(self) -> None:
        self._produk: dict[str, Produk] = {}

    def tambah(self, produk: Produk) -> None:
        self._produk[produk.nama.lower()] = produk

    def cari(self, nama: str) -> Produk:
        try:
            return self._produk[nama.lower()]
        except KeyError as exc:
            raise ProdukTidakDitemukan(f"Produk '{nama}' tidak ada") from exc

    def semua(self) -> list[Produk]:
        return list(self._produk.values())

    def ke_dict(self) -> list[dict[str, int | str]]:
        return [
            {"nama": p.nama, "harga": p.harga, "stok": p.stok}
            for p in self._produk.values()
        ]

    @classmethod
    def dari_dict(cls, data: list[dict[str, int | str]]) -> Katalog:
        katalog = cls()
        for item in data:
            katalog.tambah(
                Produk(str(item["nama"]), int(item["harga"]), int(item["stok"]))
            )
        return katalog


class Keranjang:
    def __init__(self) -> None:
        self.items: list[ItemKeranjang] = []

    def tambah(self, produk: Produk, jumlah: int = 1) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih dari 0")
        if jumlah > produk.stok:
            raise StokTidakCukup(produk.nama, jumlah, produk.stok)

        produk.stok -= jumlah
        for item in self.items:
            if item.produk is produk:
                item.jumlah += jumlah
                return
        self.items.append(ItemKeranjang(produk, jumlah))

    @property
    def total(self) -> int:
        return sum(item.subtotal for item in self.items)

    def struk(self, diskon_persen: float = 0.0, pajak_persen: float = 11.0) -> str:
        if not 0 <= diskon_persen <= 100:
            raise ValueError("Diskon harus 0-100")
        if not 0 <= pajak_persen <= 100:
            raise ValueError("Pajak harus 0-100")

        baris = ["=" * 44, "STRUK BELANJA".center(44), "=" * 44]
        for item in self.items:
            baris.append(
                f"{item.produk.nama:<16} {item.jumlah:>3} x "
                f"{rupiah(item.produk.harga):>12} {rupiah(item.subtotal):>12}"
            )

        subtotal = self.total
        diskon = int(subtotal * diskon_persen / 100)
        setelah_diskon = subtotal - diskon
        pajak = int(setelah_diskon * pajak_persen / 100)
        total_akhir = setelah_diskon + pajak

        baris.extend(
            [
                "-" * 44,
                f"{'Subtotal':<30} {rupiah(subtotal):>13}",
                f"{'Diskon (' + str(diskon_persen) + '%)':<30} {rupiah(-diskon):>13}",
                f"{'Pajak (' + str(pajak_persen) + '%)':<30} {rupiah(pajak):>13}",
                "=" * 44,
                f"{'TOTAL':<30} {rupiah(total_akhir):>13}",
                "=" * 44,
            ]
        )
        return "\n".join(baris)


# ============================================
# 4. UTILITAS
# ============================================
def rupiah(nilai: int) -> str:
    """Format angka menjadi 'Rp1.234.567'."""
    tanda = "-" if nilai < 0 else ""
    angka = f"{abs(nilai):,}".replace(",", ".")
    return f"{tanda}Rp{angka}"


def simpan_katalog(katalog: Katalog, path: Path) -> None:
    path.write_text(json.dumps(katalog.ke_dict(), indent=2), encoding="utf-8")


def muat_katalog(path: Path) -> Katalog:
    if not path.exists():
        raise FileNotFoundError(f"File katalog tidak ditemukan: {path}")
    return Katalog.dari_dict(json.loads(path.read_text(encoding="utf-8")))


# ============================================
# 5. DEMO
# ============================================
def demo() -> None:
    print("=" * 44)
    print("DEMO MINI PROJECT: KASIR SEDERHANA")
    print("=" * 44)

    katalog = Katalog()
    for produk in [
        Produk("Keyboard", 350_000, 5),
        Produk("Mouse", 150_000, 3),
        Produk("Flashdisk", 90_000, 10),
        Produk("Headset", 450_000, 2),
    ]:
        katalog.tambah(produk)

    print("\nKatalog:")
    for p in katalog.semua():
        print(f"  {p.nama:<10} {rupiah(p.harga):>12}  stok: {p.stok}")

    keranjang = Keranjang()
    keranjang.tambah(katalog.cari("Keyboard"), 2)
    keranjang.tambah(katalog.cari("Mouse"))
    keranjang.tambah(katalog.cari("Flashdisk"), 3)

    print("\n" + keranjang.struk(diskon_persen=10, pajak_persen=11))

    # Simulasi error: stok tidak cukup
    print("\nUji error handling:")
    try:
        keranjang.tambah(katalog.cari("Headset"), 5)
    except StokTidakCukup as e:
        print(f"  StokTidakCukup: {e}")

    try:
        katalog.cari("Monitor")
    except ProdukTidakDitemukan as e:
        print(f"  ProdukTidakDitemukan: {e}")

    # Simpan & muat katalog dari JSON (file sementara, tidak masuk repo)
    path = Path(tempfile.gettempdir()) / "belajar_python_katalog.json"
    simpan_katalog(katalog, path)
    katalog_baru = muat_katalog(path)
    path.unlink(missing_ok=True)

    print("\nSetelah simpan & muat JSON:")
    for p in katalog_baru.semua():
        print(f"  {p.nama:<10} {rupiah(p.harga):>12}  stok: {p.stok}")

    print("\n=== SELESAI ===")


# ============================================
# 6. MODE INTERAKTIF
# ============================================
def interaktif() -> None:
    katalog = Katalog()
    for produk in [
        Produk("Keyboard", 350_000, 5),
        Produk("Mouse", 150_000, 3),
        Produk("Flashdisk", 90_000, 10),
    ]:
        katalog.tambah(produk)

    keranjang = Keranjang()

    while True:
        print("\n=== KASIR ===")
        print("1. Lihat katalog")
        print("2. Tambah ke keranjang")
        print("3. Lihat struk")
        print("4. Keluar")

        pilihan = input("Pilih menu: ").strip()
        try:
            if pilihan == "1":
                for p in katalog.semua():
                    print(f"  {p.nama:<10} {rupiah(p.harga):>12}  stok: {p.stok}")
            elif pilihan == "2":
                nama = input("Nama produk: ").strip()
                jumlah = int(input("Jumlah: "))
                keranjang.tambah(katalog.cari(nama), jumlah)
                print("  Ditambahkan.")
            elif pilihan == "3":
                print(keranjang.struk())
            elif pilihan == "4":
                print("Terima kasih!")
                break
            else:
                print("  Menu tidak dikenal.")
        except (StokTidakCukup, ProdukTidakDitemukan, ValueError) as e:
            print(f"  Error: {e}")


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        interaktif()
    else:
        demo()
