# Materi 28: Mini Project - Todo CLI
"""Mini project menggabungkan dataclass, JSON, exception, dan argparse.

Jalankan demo: python 28_mini_project_todo.py
Contoh CLI   : python 28_mini_project_todo.py --berkas todo.json tambah "Belajar Rust"
"""

from __future__ import annotations

import argparse
import json
import tempfile
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class TodoError(Exception):
    """Error khusus untuk operasi todo."""


@dataclass
class Tugas:
    id: int
    judul: str
    selesai: bool = False
    dibuat: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def ke_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def dari_dict(cls, data: dict[str, Any]) -> Tugas:
        return cls(
            id=int(data["id"]),
            judul=str(data["judul"]),
            selesai=bool(data.get("selesai", False)),
            dibuat=str(data.get("dibuat", "")),
        )

    def __str__(self) -> str:
        tanda = "x" if self.selesai else " "
        return f"[{tanda}] {self.id}. {self.judul}"


class TodoManager:
    """Kelola daftar tugas dan menyimpannya ke file JSON."""

    def __init__(self, berkas: Path) -> None:
        self.berkas = berkas
        self._tugas: list[Tugas] = []
        self.muat()

    def muat(self) -> None:
        if not self.berkas.exists():
            return
        try:
            data = json.loads(self.berkas.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TodoError(f"Gagal membaca {self.berkas}: {exc}") from exc

        if not isinstance(data, list):
            raise TodoError("Format file todo harus berupa list")

        self._tugas = [Tugas.dari_dict(item) for item in data if isinstance(item, dict)]

    def simpan(self) -> None:
        try:
            self.berkas.parent.mkdir(parents=True, exist_ok=True)
            isi = json.dumps(
                [tugas.ke_dict() for tugas in self._tugas],
                ensure_ascii=False,
                indent=2,
            )
            self.berkas.write_text(isi, encoding="utf-8")
        except OSError as exc:
            raise TodoError(f"Gagal menulis {self.berkas}: {exc}") from exc

    def _cari(self, id_tugas: int) -> Tugas:
        for tugas in self._tugas:
            if tugas.id == id_tugas:
                return tugas
        raise TodoError(f"Tugas #{id_tugas} tidak ditemukan")

    def tambah(self, judul: str) -> Tugas:
        if not judul.strip():
            raise TodoError("Judul tidak boleh kosong")
        id_baru = max((t.id for t in self._tugas), default=0) + 1
        tugas = Tugas(id=id_baru, judul=judul.strip())
        self._tugas.append(tugas)
        self.simpan()
        return tugas

    def tandai_selesai(self, id_tugas: int) -> Tugas:
        tugas = self._cari(id_tugas)
        tugas.selesai = True
        self.simpan()
        return tugas

    def hapus(self, id_tugas: int) -> Tugas:
        tugas = self._cari(id_tugas)
        self._tugas.remove(tugas)
        self.simpan()
        return tugas

    def daftar(self) -> list[Tugas]:
        return list(self._tugas)


def bangun_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="Todo CLI sederhana")
    parser.add_argument(
        "--berkas",
        type=Path,
        default=Path("data_latihan/todo.json"),
        help="lokasi file JSON (default: data_latihan/todo.json)",
    )
    sub = parser.add_subparsers(dest="perintah", required=True)

    tambah = sub.add_parser("tambah", help="tambah tugas")
    tambah.add_argument("judul")

    selesai = sub.add_parser("selesai", help="tandai tugas selesai")
    selesai.add_argument("id", type=int)

    hapus = sub.add_parser("hapus", help="hapus tugas")
    hapus.add_argument("id", type=int)

    sub.add_parser("daftar", help="tampilkan semua tugas")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = bangun_parser().parse_args(argv)
    manager = TodoManager(args.berkas)

    try:
        if args.perintah == "tambah":
            tugas = manager.tambah(args.judul)
            print(f"Ditambahkan: {tugas}")
        elif args.perintah == "selesai":
            tugas = manager.tandai_selesai(args.id)
            print(f"Selesai: {tugas}")
        elif args.perintah == "hapus":
            tugas = manager.hapus(args.id)
            print(f"Dihapus: {tugas}")
        elif args.perintah == "daftar":
            daftar = manager.daftar()
            print("Daftar tugas:")
            for tugas in daftar:
                print(f"  {tugas}")
            if not daftar:
                print("  (kosong)")
            print(f"Total: {len(daftar)} tugas")
        else:
            print(f"Perintah tidak dikenali: {args.perintah}")
            return 1
    except TodoError as exc:
        print(f"Error: {exc}")
        return 1

    return 0


def demo() -> None:
    print("=== DEMO MINI PROJECT (memakai folder sementara) ===")
    with tempfile.TemporaryDirectory() as folder:
        berkas = Path(folder) / "todo.json"
        manager = TodoManager(berkas)

        manager.tambah("Belajar Python")
        manager.tambah("Belajar Rust")
        manager.tandai_selesai(1)
        print("Isi manager:")
        for tugas in manager.daftar():
            print(" ", tugas)

        print("JSON tersimpan:")
        print(berkas.read_text(encoding="utf-8"))

        # Manager baru membaca data dari file yang sama.
        ulang = TodoManager(berkas)
        print("Dibaca ulang:", [str(tugas) for tugas in ulang.daftar()])

        ulang.hapus(2)
        print("Setelah hapus:", [str(tugas) for tugas in ulang.daftar()])


def latihan() -> None:
    with tempfile.TemporaryDirectory() as folder:
        berkas = Path(folder) / "todo.json"
        manager = TodoManager(berkas)

        assert manager.daftar() == []
        assert manager.tambah("Satu").id == 1
        assert manager.tambah("Dua").id == 2
        assert len(TodoManager(berkas).daftar()) == 2

        assert manager.tandai_selesai(1).selesai is True
        assert manager.hapus(2).judul == "Dua"
        assert len(manager.daftar()) == 1

        try:
            manager.tambah("   ")
        except TodoError:
            pass
        else:
            raise AssertionError("judul kosong seharusnya error")

        try:
            manager.tandai_selesai(999)
        except TodoError:
            pass
        else:
            raise AssertionError("id tidak ada seharusnya error")

    print("Latihan materi 28: semua assert lolos.")


if __name__ == "__main__":
    demo()
    latihan()
