# Materi 07: File Handling - JSON, CSV, Text, Binary
# Penjelasan: Python punya built-in module untuk I/O file.
# Selalu gunakan 'with' statement (context manager) agar file auto-close.

import csv
import json
from pathlib import Path

# ============================================
# KONFIGURASI PATH
# ============================================
DATA_DIR = Path("data_latihan")
DATA_DIR.mkdir(exist_ok=True)

FILE_JSON = DATA_DIR / "mahasiswa.json"
FILE_CSV = DATA_DIR / "mahasiswa.csv"
FILE_TXT = DATA_DIR / "catatan.txt"
FILE_BIN = DATA_DIR / "data.bin"

# Sample data
MAHASISWA_DATA = [
    {
        "nim": "2021001",
        "nama": "Hayyan",
        "jurusan": "Informatika",
        "ipk": 3.85,
        "aktif": True,
    },
    {
        "nim": "2021002",
        "nama": "Rina",
        "jurusan": "Sistem Informasi",
        "ipk": 3.65,
        "aktif": True,
    },
    {
        "nim": "2021003",
        "nama": "Budi",
        "jurusan": "Teknik Informatika",
        "ipk": 3.40,
        "aktif": False,
    },
    {
        "nim": "2021004",
        "nama": "Sari",
        "jurusan": "Informatika",
        "ipk": 3.90,
        "aktif": True,
    },
]


# ============================================
# 1. TEXT FILE (READ/WRITE/APPEND)
# ============================================
def tulis_text():
    """Menulis file teks dengan mode 'w' (write/overwrite)"""
    with open(FILE_TXT, "w", encoding="utf-8") as f:
        f.write("=== Catatan Mahasiswa ===\n")
        f.writelines(
            f"{m['nim']} | {m['nama']} | {m['jurusan']} | IPK: {m['ipk']}\n"
            for m in MAHASISWA_DATA
        )
    print(f"[TXT] Ditulis ke {FILE_TXT}")


def baca_text():
    """Membaca file teks dengan mode 'r' (read)"""
    with open(FILE_TXT, "r", encoding="utf-8") as f:
        isi = f.read()
    print(f"[TXT] Isi file:\n{isi}")


def tambah_text():
    """Menambah ke file dengan mode 'a' (append)"""
    with open(FILE_TXT, "a", encoding="utf-8") as f:
        f.write("\n--- Tambahan ---\n")
        f.write("Data diperbarui pada 2026\n")
    print(f"[TXT] Ditambahkan ke {FILE_TXT}")


def baca_per_baris():
    """Membaca baris per baris (memory efficient untuk file besar)"""
    with open(FILE_TXT, "r", encoding="utf-8") as f:
        for nomor, baris in enumerate(f, 1):
            print(f"  Baris {nomor}: {baris.rstrip()}")


# ============================================
# 2. JSON (JavaScript Object Notation)
# ============================================
def tulis_json():
    """Serialisasi Python object -> JSON file"""
    with open(FILE_JSON, "w", encoding="utf-8") as f:
        json.dump(MAHASISWA_DATA, f, indent=2, ensure_ascii=False)
    print(f"[JSON] Ditulis ke {FILE_JSON}")


def baca_json() -> list[dict]:
    """Deserialisasi JSON file -> Python object"""
    with open(FILE_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[JSON] Dibaca {len(data)} record:")
    for m in data:
        print(f"  {m['nim']} - {m['nama']} ({m['jurusan']}) IPK: {m['ipk']}")
    return data


def json_dumps_loads():
    """json.dumps (string) vs json.dump (file)"""
    json_string = json.dumps(MAHASISWA_DATA, indent=2, ensure_ascii=False)
    print(f"[JSON] String JSON:\n{json_string[:100]}...")

    # Parsing string JSON
    parsed = json.loads(json_string)
    print(f"[JSON] Parse string -> {len(parsed)} objek")


def json_custom_encoder():
    """Custom JSON Encader untuk tipe non-standard (datetime, set, dll.)"""
    from datetime import datetime

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, set):
                return list(obj)
            return super().default(obj)

    data_dengan_waktu = {
        "mahasiswa": MAHASISWA_DATA[0],
        "waktu_buat": datetime.now(),
        "tags": {"python", "json", "rust"},
    }
    with open(DATA_DIR / "custom.json", "w", encoding="utf-8") as f:
        json.dump(data_dengan_waktu, f, cls=CustomEncoder, indent=2)
    print("[JSON] Custom encoder written")


# ============================================
# 3. CSV (Comma-Separated Values)
# ============================================
def tulis_csv():
    """Menulis CSV dengan csv.DictWriter"""
    fieldnames = ["nim", "nama", "jurusan", "ipk", "aktif"]
    with open(FILE_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # Tulis header
        writer.writerows(MAHASISWA_DATA)
    print(f"[CSV] Ditulis ke {FILE_CSV}")


def baca_csv() -> list[dict]:
    """Membaca CSV dengan csv.DictReader"""
    with open(FILE_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    print(f"[CSV] Dibaca {len(data)} record:")
    for row in data:
        print(f"  {row['nim']} - {row['nama']} - {row['jurusan']} - IPK: {row['ipk']}")
    return data


def tulis_csv_list():
    """Menulis CSV dengan csv.writer (list of lists)"""
    FILE_CSV2 = DATA_DIR / "mahasiswa2.csv"
    header = ["NIM", "Nama", "Jurusan", "IPK"]
    rows = [
        ["2021001", "Hayyan", "Informatika", "3.85"],
        ["2021002", "Rina", "Sistem Informasi", "3.65"],
    ]
    with open(FILE_CSV2, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"[CSV] List-based written to {FILE_CSV2}")


def baca_csv_dengan_tipe():
    """Membaca CSV & konversi tipe data manual"""
    with open(FILE_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["ipk"] = float(row["ipk"])
            row["aktif"] = row["aktif"] == "True"
            print(f"  Typed: {row}")


# ============================================
# 4. BINARY FILE (bytes)
# ============================================
def tulis_biner():
    """Menulis file biner (bytes)"""
    data_bytes = b"Ini data biner: \x00\x01\x02\x03\xff\xfe"
    with open(FILE_BIN, "wb") as f:
        f.write(data_bytes)

    # Serialize struktur data dengan struct module
    import struct

    with open(DATA_DIR / "struct.bin", "wb") as f:
        for m in MAHASISWA_DATA:
            # Format: 10s (string 10 byte), 20s, 20s, f (float), ? (bool)
            nim_b = m["nim"].encode()[:10].ljust(10, b"\x00")
            nama_b = m["nama"].encode()[:20].ljust(20, b"\x00")
            jur_b = m["jurusan"].encode()[:20].ljust(20, b"\x00")
            packed = struct.pack(
                "10s20s20sf?", nim_b, nama_b, jur_b, m["ipk"], m["aktif"]
            )
            f.write(packed)
    print("[BIN] Binary file written")


def baca_biner():
    """Membaca file biner"""
    with open(FILE_BIN, "rb") as f:
        data = f.read()
    print(f"[BIN] Raw bytes: {data}")

    import struct

    with open(DATA_DIR / "struct.bin", "rb") as f:
        record_size = struct.calcsize("10s20s20sf?")
        while chunk := f.read(record_size):
            nim_b, nama_b, jur_b, ipk, aktif = struct.unpack("10s20s20sf?", chunk)
            print(
                f"  NIM: {nim_b.decode().strip()}, Nama: {nama_b.decode().strip()}, "
                f"Jurusan: {jur_b.decode().strip()}, IPK: {ipk}, Aktif: {aktif}"
            )


# ============================================
# 5. PATHLIB (Modern File Path Handling)
# ============================================
def demo_pathlib():
    """pathlib.Path - OOP approach untuk filesystem (Python 3.4+)"""
    base = Path("data_latihan")

    # Operasi path
    print(f"[Pathlib] Absolute: {base.absolute()}")
    print(f"[Pathlib] Exists: {base.exists()}")
    print(f"[Pathlib] Is dir: {base.is_dir()}")

    # List files
    print("[Pathlib] Files in dir:")
    for f in base.iterdir():
        print(f"  {f.name} ({f.stat().st_size} bytes)")

    # Glob pattern
    print("[Pathlib] *.json files:")
    for f in base.glob("*.json"):
        print(f"  {f}")

    # Read/write shortcut
    test_file = base / "pathlib_test.txt"
    test_file.write_text("Ditulis via pathlib", encoding="utf-8")
    print(f"[Pathlib] Read: {test_file.read_text(encoding='utf-8')}")


# ============================================
# 6. ERROR HANDLING FILE I/O
# ============================================
def baca_dengan_error_handling(filepath: Path):
    """Best practice: handle FileNotFoundError, PermissionError, dll."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[Error] File tidak ditemukan: {filepath}")
    except PermissionError:
        print(f"[Error] Tidak punya izin baca: {filepath}")
    except OSError as e:
        print(f"[Error] OS error: {e}")
    return None


# ============================================
# 7. CONTEXT MANAGER KUSTOM (with statement)
# ============================================
class TimerContext:
    """Custom context manager untuk timing operasi file"""

    def __enter__(self):
        import time

        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time

        self.end = time.perf_counter()
        print(f"[Timer] Durasi: {(self.end - self.start)*1000:.2f} ms")
        return False  # Propagate exception jika ada


# ============================================
# MAIN DEMO
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("DEMO FILE HANDLING PYTHON: JSON, CSV, TEXT, BINARY")
    print("=" * 60)

    # Text
    print("\n--- TEXT FILE ---")
    tulis_text()
    baca_text()
    print("\nBaca per baris:")
    baca_per_baris()
    tambah_text()

    # JSON
    print("\n--- JSON ---")
    tulis_json()
    baca_json()
    json_dumps_loads()
    json_custom_encoder()

    # CSV
    print("\n--- CSV ---")
    tulis_csv()
    baca_csv()
    tulis_csv_list()
    print("\nDengan konversi tipe:")
    baca_csv_dengan_tipe()

    # Binary
    print("\n--- BINARY ---")
    tulis_biner()
    baca_biner()

    # Pathlib
    print("\n--- PATHLIB ---")
    demo_pathlib()

    # Error handling
    print("\n--- ERROR HANDLING ---")
    baca_dengan_error_handling(Path("tidak_ada.txt"))

    # Custom context manager
    print("\n--- CUSTOM CONTEXT MANAGER ---")
    with TimerContext():
        import time

        time.sleep(0.1)
        tulis_json()

    print("\n=== SELESAI ===")
