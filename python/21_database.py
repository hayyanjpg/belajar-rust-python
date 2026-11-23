"""
21_database.py - Database dengan sqlite3 dan SQLAlchemy

Tahap 5: Spesialisasi - Database
Materi: sqlite3, SQLAlchemy ORM, CRUD, migrasi, koneksi database
"""

import os
import sqlite3

# ============================================================================
# 1. SQLITE3 - Database bawaan Python
# ============================================================================


def demo_sqlite3():
    print("=== DEMO SQLITE3 ===")

    db_path = "data_latihan/belajar.db"
    os.makedirs("data_latihan", exist_ok=True)

    # Koneksi ke database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Buat tabel
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pegawai (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            jabatan TEXT,
            gaji INTEGER,
            tanggal_gabung TEXT
        )
    """)
    conn.commit()
    print("Tabel 'pegawai' dibuat")

    # Insert data
    pegawai_list = [
        ("Budi", "Programmer", 7000000, "2026-01-15"),
        ("Siti", "Desainer", 6500000, "2026-02-20"),
        ("Joko", "Manajer", 12000000, "2025-08-10"),
        ("Ani", "HRD", 8000000, "2026-03-05"),
    ]
    cursor.executemany(
        "INSERT INTO pegawai (nama, jabatan, gaji, tanggal_gabung) VALUES (?, ?, ?, ?)",
        pegawai_list,
    )
    conn.commit()
    print(f"Dimasukkan {len(pegawai_list)} data pegawai")

    # Select semua data
    cursor.execute("SELECT * FROM pegawai")
    rows = cursor.fetchall()
    print("\nSemua pegawai:")
    for row in rows:
        print(
            f"  ID: {row[0]}, Nama: {row[1]}, Jabatan: {row[2]}, Gaji: {row[3]}, Gabung: {row[4]}"
        )

    # Select dengan WHERE
    cursor.execute("SELECT nama, gaji FROM pegawai WHERE gaji > 7000000")
    high_salary = cursor.fetchall()
    print("\nPegawai dengan gaji > 7.000.000:")
    for row in high_salary:
        print(f"  {row[0]}: {row[1]}")

    # Update data
    cursor.execute("UPDATE pegawai SET gaji = 7500000 WHERE nama = ?", ("Budi",))
    conn.commit()
    print("\nGaji Budi diupdate ke 7.500.000")

    # Delete data
    cursor.execute("DELETE FROM pegawai WHERE nama = ?", ("Ani",))
    conn.commit()
    print("Data Ani dihapus")

    # Tampilkan setelah update/delete
    cursor.execute("SELECT * FROM pegawai")
    rows = cursor.fetchall()
    print("\nPegawai setelah update dan delete:")
    for row in rows:
        print(f"  ID: {row[0]}, Nama: {row[1]}, Jabatan: {row[2]}, Gaji: {row[3]}")

    # Menutup koneksi
    conn.close()
    print("\nKoneksi database ditutup")


def latihan_sqlite3():
    print("\n=== LATIHAN SQLITE3 ===")
    print("Buat tabel 'produk' dengan kolom: id, nama, harga, stok")
    print("Masukkan 5 data produk, lalu tampilkan produk dengan stok < 20")


# ============================================================================
# 2. SQLALCHEMY - ORM (Object Relational Mapper)
# ============================================================================


def demo_sqlalchemy():
    print("\n=== DEMO SQLALCHEMY ===")
    print("Catatan: Install dengan 'pip install sqlalchemy'")
    print("""
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Buat engine SQLite
engine = create_engine('sqlite:///data_latihan/belajar_orm.db', echo=True)
Base = declarative_base()

# Definisikan model
class Pegawai(Base):
    __tablename__ = 'pegawai'

    id = Column(Integer, primary_key=True)
    nama = Column(String(100), nullable=False)
    jabatan = Column(String(100))
    gaji = Column(Integer)
    tanggal_gabung = Column(DateTime, default=datetime.utcnow)

# Buat semua tabel
Base.metadata.create_all(engine)

# Buat session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data
pegawai_baru = Pegawai(nama='Budi', jabatan='Programmer', gaji=7000000)
session.add(pegawai_baru)
session.commit()

# Query semua
semua_pegawai = session.query(Pegawai).all()
for p in semua_pegawai:
    print(f"{p.nama} - {p.jabatan} - {p.gaji}")

# Query dengan filter
pegawai_tinggi = session.query(Pegawai).filter(Pegawai.gaji > 7000000).all()
for p in pegawai_tinggi:
    print(f"Gaji tinggi: {p.nama} - {p.gaji}")

# Update
pegawai = session.query(Pegawai).filter_by(nama='Budi').first()
if pegawai:
    pegawai.gaji = 7500000
    session.commit()

# Hapus
session.query(Pegawai).filter_by(nama='Budi').delete()
session.commit()
    """)


def latihan_sqlalchemy():
    print("\n=== LATIHAN SQLALCHEMY ===")
    print("Buat model 'Produk' dengan kolom: id, nama, harga, stok, kategori")
    print("Lakukan operasi CRUD: create, read, update, delete")


if __name__ == "__main__":
    demo_sqlite3()
    latihan_sqlite3()
    demo_sqlalchemy()
    latihan_sqlalchemy()
