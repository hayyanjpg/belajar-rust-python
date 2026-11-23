"""
20_automasi.py - Automation & Web Scraping dengan requests dan BeautifulSoup

Tahap 5: Spesialisasi - Automation & Scripting
Materi: requests, beautifulsoup4, REST API client, web scraping, file automation
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time


# ============================================================================
# 1. REQUESTS - REST API Client
# ============================================================================

def demo_requests():
    print("=== DEMO REQUESTS ===")

    # Contoh GET request ke public API (JSONPlaceholder)
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1', timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response JSON: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error saat request: {e}")
        print("Catatan: Pastikan terkoneksi internet untuk menjalankan demo ini")

    # Contoh POST request
    try:
        new_post = {
            'title': 'Belajar Python',
            'body': 'Materi automation dan scraping',
            'userId': 1
        }
        response = requests.post(
            'https://jsonplaceholder.typicode.com/posts',
            json=new_post,
            timeout=10
        )
        print(f"\nPOST Status: {response.status_code}")
        print(f"POST Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error saat POST: {e}")

    # Contoh dengan header dan parameter
    try:
        params = {'userId': 1}
        headers = {'Accept': 'application/json'}
        response = requests.get(
            'https://jsonplaceholder.typicode.com/posts',
            params=params,
            headers=headers,
            timeout=10
        )
        posts = response.json()
        print(f"\nJumlah post user 1: {len(posts)}")
        print(f"Judul post pertama: {posts[0]['title']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    # Mengunduh file
    try:
        img_response = requests.get('https://via.placeholder.com/150', timeout=10)
        os.makedirs('data_latihan', exist_ok=True)
        with open('data_latihan/placeholder.jpg', 'wb') as f:
            f.write(img_response.content)
        print(f"\nGambar diunduh, ukuran: {len(img_response.content)} bytes")
    except requests.exceptions.RequestException as e:
        print(f"Error mengunduh gambar: {e}")


# ============================================================================
# 2. BEAUTIFULSOUP4 - Web Scraping
# ============================================================================

def demo_beautifulsoup():
    print("\n=== DEMO BEAUTIFULSOUP ===")

    # HTML contoh untuk scraping (tanpa koneksi internet)
    html_contoh = '''
    <html>
        <head><title>Halaman Contoh</title></head>
        <body>
            <h1 class="judul">Belajar Web Scraping</h1>
            <div class="konten">
                <p class="paragraf">Ini adalah paragraf pertama.</p>
                <p class="paragraf">Ini adalah paragraf kedua.</p>
            </div>
            <ul class="daftar">
                <li class="item">Item 1</li>
                <li class="item">Item 2</li>
                <li class="item">Item 3</li>
            </ul>
            <table>
                <tr><th>Nama</th><th>Nilai</th></tr>
                <tr><td>Budi</td><td>85</td></tr>
                <tr><td>Siti</td><td>90</td></tr>
            </table>
            <a href="https://example.com" class="link">Link External</a>
        </body>
    </html>
    '''

    soup = BeautifulSoup(html_contoh, 'html.parser')

    # Cari oleh tag
    judul = soup.find('h1')
    print(f"Judul (h1): {judul.text if judul else 'Tidak ditemukan'}")

    # Cari oleh class
    paragrafs = soup.find_all('p', class_='paragraf')
    print(f"\nParagraf ({len(paragrafs)} item):")
    for p in paragrafs:
        print(f"  - {p.text}")

    # Cari oleh CSS selector
    items = soup.select('.daftar .item')
    print(f"\nItem daftar ({len(items)} item):")
    for item in items:
        print(f"  - {item.text}")

    # Cari link
    link = soup.find('a', class_='link')
    print(f"\nLink: {link.get('href') if link else 'Tidak ditemukan'}")
    print(f"Text link: {link.text if link else 'Tidak ditemukan'}")

    # Scraping tabel
    table = soup.find('table')
    if table:
        print("\nTabel:")
        for row in table.find_all('tr'):
            cells = [cell.text for cell in row.find_all(['th', 'td'])]
            print(f"  {' | '.join(cells)}")


def demo_scraping_senyawa():
    """Contoh gabungan requests + BeautifulSoup (memerlukan internet)"""
    print("\n=== DEMO SCRAPING SENYWA (memerlukan internet) ===")
    print("Contoh struktur scraping halaman web nyata:")
    print("""
import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

# Ambil semua judul h1
for h1 in soup.find_all('h1'):
    print(h1.text.strip())

# Ambil semua link
for a in soup.find_all('a', href=True):
    print(a['href'], a.text.strip())
    """)


# ============================================================================
# 3. FILE AUTOMATION
# ============================================================================

def demo_file_automation():
    print("\n=== DEMO FILE AUTOMATION ===")

    os.makedirs('data_latihan/automasi', exist_ok=True)

    # Buat beberapa file contoh
    for i in range(1, 4):
        with open(f'data_latihan/automasi/file_{i}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Ini adalah file ke-{i}\nDibuat oleh skrip automasi Python")

    # Daftar file dalam direktori
    print("File di folder automasi:")
    for fname in os.listdir('data_latihan/automasi'):
        fpath = os.path.join('data_latihan/automasi', fname)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            print(f"  {fname} ({size} bytes)")

    # Baca semua file dan gabungkan
    gabungan = []
    for fname in sorted(os.listdir('data_latihan/automasi')):
        fpath = os.path.join('data_latihan/automasi', fname)
        if os.path.isfile(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                gabungan.append(f.read())

    with open('data_latihan/automasi/gabungan.txt', 'w', encoding='utf-8') as f:
        f.write("\n---\n".join(gabungan))

    print("\nSemua file digabungkan ke data_latihan/automasi/gabungan.txt")


def latihan_requests():
    print("\n=== LATIHAN REQUESTS ===")
    print("Buat fungsi yang mengambil data dari API dan menampilkan judul 5 postingan pertama")
    print("Endpoint: https://jsonplaceholder.typicode.com/posts")


def latihan_beautifulsoup():
    print("\n=== LATIHAN BEAUTIFULSOUP ===")
    print("Buat fungsi yang mengekstrak semua link dari halaman HTML")
    print("Gunakan BeautifulSoup dengan parser 'html.parser'")


if __name__ == '__main__':
    demo_requests()
    demo_beautifulsoup()
    demo_scraping_senyawa()
    demo_file_automation()
    latihan_requests()
    latihan_beautifulsoup()
    print("\nDemo selesai. Lihat folder data_latihan/ untuk hasil automasi.")
