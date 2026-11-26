# Materi 27: Logging dan Argparse
"""Materi pencatatan log dan pembuatan CLI dengan subcommand.

Jalankan dengan: python 27_logging_argparse.py
Contoh CLI: python 27_logging_argparse.py -v tambah "Belajar Rust"
"""

import argparse
import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)


def bangun_parser() -> argparse.ArgumentParser:
    """Bangun parser dengan tiga subcommand: tambah, daftar, selesai."""
    parser = argparse.ArgumentParser(
        prog="catatan",
        description="Contoh CLI sederhana untuk latihan argparse.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="tampilkan log level DEBUG",
    )

    sub = parser.add_subparsers(dest="perintah", required=True)

    tambah = sub.add_parser("tambah", help="tambah catatan baru")
    tambah.add_argument("judul", help="judul catatan")

    sub.add_parser("daftar", help="tampilkan semua catatan")

    selesai = sub.add_parser("selesai", help="tandai catatan selesai")
    selesai.add_argument("id", type=int, help="nomor catatan")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Titik masuk CLI. Mengembalikan 0 jika sukses."""
    args = bangun_parser().parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    logger.debug("argumen yang diterima: %s", args)

    match args.perintah:
        case "tambah":
            logger.info("Menambah catatan: %s", args.judul)
            print(f"Ditambahkan: {args.judul}")
        case "daftar":
            logger.info("Menampilkan daftar catatan")
            print("Daftar catatan: (contoh) belajar Rust, belajar Python")
        case "selesai":
            logger.info("Menandai catatan %s selesai", args.id)
            print(f"Catatan #{args.id} ditandai selesai")
        case _:
            logger.error("Perintah tidak dikenali: %s", args.perintah)
            return 1

    return 0


def demo() -> None:
    print("=== DEMO CLI (memanggil main dengan argumen) ===")
    for argv in [
        ["tambah", "Belajar logging"],
        ["daftar"],
        ["--verbose", "selesai", "2"],
    ]:
        print(f"\n$ python 27_logging_argparse.py {' '.join(argv)}")
        kode = main(argv)
        print("exit code:", kode)


def latihan() -> None:
    parser = bangun_parser()

    args = parser.parse_args(["tambah", "Judul baru"])
    assert args.perintah == "tambah"
    assert args.judul == "Judul baru"
    assert args.verbose is False

    args = parser.parse_args(["--verbose", "selesai", "7"])
    assert args.verbose is True
    assert args.id == 7

    assert main(["daftar"]) == 0
    assert main(["tambah", "Catatan uji"]) == 0

    print("Latihan materi 27: semua assert lolos.")


if __name__ == "__main__":
    demo()
    latihan()
