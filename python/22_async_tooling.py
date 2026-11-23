"""
22_async_tooling.py - Async Programming dan Tooling Python

Tahap 5: Spesialisasi - Async & Tooling
Materi: asyncio, aiohttp, mypy, black, ruff
"""

import asyncio
import time

# ============================================================================
# 1. ASYNCIO - Pemrograman Asinkron
# ============================================================================


async def fetch_data(delay, id):
    """Simulasi pengambilan data dengan delay"""
    print(f"Task {id}: mulai, menunggu {delay} detik...")
    await asyncio.sleep(delay)
    print(f"Task {id}: selesai setelah {delay} detik")
    return {"id": id, "data": f"hasil_task_{id}", "delay": delay}


async def demo_asyncio_gather():
    """Menjalankan multiple async task secara bersamaan dengan gather"""
    print("=== DEMO ASYNCIO GATHER ===")
    start = time.time()

    tasks = [
        fetch_data(1, 1),
        fetch_data(2, 2),
        fetch_data(1, 3),
    ]

    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    print(f"\nHasil: {results}")
    print(f"Waktu total: {elapsed:.2f} detik (sekedarnya 4 detik jika sequential)")


async def demo_asyncio_create_task():
    """Membuat task secara terpisah"""
    print("\n=== DEMO ASYNCIO CREATE_TASK ===")

    task1 = asyncio.create_task(fetch_data(1, 1))
    task2 = asyncio.create_task(fetch_data(2, 2))

    print("Menunggu task selesai...")
    result1 = await task1
    result2 = await task2

    print(f"Hasil task 1: {result1}")
    print(f"Hasil task 2: {result2}")


# ============================================================================
# 2. AIOHTTP - HTTP Client Asinkron
# ============================================================================


async def demo_aiohttp():
    print("\n=== DEMO AIOHTTP ===")
    print("Catatan: Install dengan 'pip install aiohttp'")
    print("Memerlukan koneksi internet")
    print("""
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        # Ambil data dari multiple endpoint secara bersamaan
        urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3',
        ]
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(r['title'])

asyncio.run(main())
    """)


# ============================================================================
# 3. TOOLING: MYPY, BLACK, RUFF
# ============================================================================


def demo_tooling():
    print("\n=== DEMO TOOLING (MYPY, BLACK, RUFF) ===")
    print("Install: pip install mypy black ruff")
    print("""
# --- MYPY (Static Type Checker) ---
# Jalankan: mypy nama_file.py
# Contoh kode dengan type hints:
from typing import List, Optional

def greet(names: List[str]) -> str:
    return ", ".join(names)

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Budi", 2: "Siti"}
    return users.get(user_id)

# --- BLACK (Code Formatter) ---
# Jalankan: black nama_file.py
# Secara otomatis memformat kode sesuai PEP 8

# --- RUFF (Linter + Formatter, sangat cepat) ---
# Jalankan: ruff check nama_file.py   (linting)
# Jalankan: ruff format nama_file.py  (formatting)
    """)


def latihan_asyncio():
    print("\n=== LATIHAN ASYNCIO ===")
    print("Buat fungsi async yang mengambil data dari 3 URL secara bersamaan")
    print("Gunakan asyncio.gather dan aiohttp.ClientSession")


def latihan_tooling():
    print("\n=== LATIHAN TOOLING ===")
    print("1. Jalankan 'mypy' pada file ini dan perbaiki error tipe data")
    print("2. Jalankan 'black' untuk memformat kode")
    print("3. Jalankan 'ruff check' untuk mencari potensi bug")


if __name__ == "__main__":
    asyncio.run(demo_asyncio_gather())
    asyncio.run(demo_asyncio_create_task())
    asyncio.run(demo_aiohttp())
    demo_tooling()
    latihan_asyncio()
    latihan_tooling()
    print("\nDemo async & tooling selesai.")
