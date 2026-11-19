# Materi 13: Standard Library - re (Regular Expression)
# Regex digunakan untuk pencocokan pola string, validasi, ekstraksi, dan substitusi.

import re

# ============================================
# 1. Dasar Regex
# ============================================
print("=== 1. Dasar Regex ===")

# Pola dasar
# . = karakter apa saja (kecuali newline)
# \d = digit [0-9]
# \D = non-digit
# \w = word character [a-zA-Z0-9_]
# \W = non-word character
# \s = whitespace (spasi, tab, newline)
# \S = non-whitespace

# ============================================
# 2. Fungsi-fungsi Utama re
# ============================================
print("\n=== 2. Fungsi Utama ===")

# re.search() - cari pola di mana saja dalam string
teks = "Email saya: hayyan@example.com dan dia: test@domain.org"
pola_email = r"[\w\.-]+@[\w\.-]+\.\w+"
match = re.search(pola_email, teks)
if match:
    print(f"Ditemukan: {match.group()}")

# re.match() - cari di AWAL string
match = re.match(r"Email", teks)
if match:
    print(f"Match di awal: {match.group()}")

# re.findall() - cari SEMUA kemunculan
emails = re.findall(pola_email, teks)
print(f"Semua email: {emails}")

# re.finditer() - iterator match objects
for m in re.finditer(pola_email, teks):
    print(f"  {m.group()} di posisi {m.start()}-{m.end()}")

# re.sub() - substitusi
teks_baru = re.sub(pola_email, "[EMAIL]", teks)
print(f"Substitusi: {teks_baru}")

# re.split() - split berdasarkan pola
parts = re.split(r"\s+", "kata1   kata2\tkata3\nkata4")
print(f"Split: {parts}")

# ============================================
# 3. Karakter Khusus & Quantifier
# ============================================
print("\n=== 3. Quantifier ===")

# * = 0 atau lebih
# + = 1 atau lebih
# ? = 0 atau 1
# {n} = tepat n kali
# {n,} = minimal n kali
# {n,m} = antara n sampai m kali

# Contoh: nomor telepon Indonesia
pola_hp = r"^(\+62|62|0)8\d{8,11}$"
nomor_list = ["081234567890", "6281234567890", "+6281234567890", "08123"]
for n in nomor_list:
    valid = bool(re.match(pola_hp, n))
    print(f"  {n}: {'Valid' if valid else 'Invalid'}")

# ============================================
# 4. Grouping & Capturing
# ============================================
print("\n=== 4. Grouping ===")

# ( ) = capturing group
# (?: ) = non-capturing group
# (?P<name> ) = named group

# Parsing tanggal
pola_tanggal = r"(?P<tanggal>\d{2})/(?P<bulan>\d{2})/(?P<tahun>\d{4})"
teks_tgl = "Lahir: 15/05/2000, Nikah: 20/06/2025"
for m in re.finditer(pola_tanggal, teks_tgl):
    print(f"  Tanggal: {m.group('tanggal')}, Bulan: {m.group('bulan')}, Tahun: {m.group('tahun')}")
    print(f"  Groups: {m.groups()}")
    print(f"  Groupdict: {m.groupdict()}")

# ============================================
# 5. Flags (Opsi)
# ============================================
print("\n=== 5. Flags ===")

# re.IGNORECASE / re.I - case insensitive
# re.MULTILINE / re.M - ^ dan $ match per baris
# re.DOTALL / re.S - . match termasuk newline
# re.VERBOSE / re.X - verbose mode (boleh spasi & komentar)

# Case insensitive
pola = re.compile(r"python", re.IGNORECASE)
print(f"Case insensitive: {pola.findall('Python PYTHON python PyThOn')}")

# Verbose mode - pola yang readable
pola_verbose = re.compile(r"""
    \d{3}   # 3 digit awal
    [- ]?   # pemisah opsional
    \d{4}   # 4 digit tengah
    [- ]?   # pemisah opsional
    \d{4}   # 4 digit akhir
""", re.VERBOSE)

print(f"Verbose: {pola_verbose.findall('0812-3456-7890 0812 3456 7890')}")

# ============================================
# 6. Lookaround (Assertion)
# ============================================
print("\n=== 6. Lookaround ===")

# Positive lookahead (?=...) - pasti diikuti oleh
# Negative lookahead (?!...) - TIDAK diikuti oleh
# Positive lookbehind (?<=...) - pasti didahului oleh
# Negative lookbehind (?<!...) - TIDAK didahului oleh

# Cari kata yang diikuti "python" (lookahead)
teks = "saya belajar python programming dan python scripting"
kata_sebelum_python = re.findall(r"\w+(?=\s+python)", teks)
print(f"Kata sebelum 'python': {kata_sebelum_python}")

# Cari angka yang TIDAK diikuti "px" (negative lookahead)
teks = "ukuran: 10px 20 30px 40"
angka_bukan_px = re.findall(r"\d+(?!px)", teks)
print(f"Angka bukan px: {angka_bukan_px}")

# ============================================
# 7. Contoh Praktis
# ============================================
print("\n=== 7. Contoh Praktis ===")

# Validasi email kompleks
email_pattern = re.compile(
    r"^(?P<local>[a-zA-Z0-9._%+-]+)"
    r"@"
    r"(?P<domain>[a-zA-Z0-9.-]+)"
    r"\."
    r"(?P<tld>[a-zA-Z]{2,})$"
)

emails_test = [
    "user@example.com",
    "user.name@sub.domain.co.id",
    "user+tag@example.org",
    "invalid@",
    "@invalid.com",
    "user@domain",
]

for email in emails_test:
    m = email_pattern.match(email)
    if m:
        print(f"  Valid: {email} -> local={m.group('local')}, domain={m.group('domain')}, tld={m.group('tld')}")
    else:
        print(f"  Invalid: {email}")

# Ekstrak hashtag
teks_sosmed = "Belajar #Python #Regex #Programming seru! #BelajarPython"
hashtags = re.findall(r"#(\w+)", teks_sosmed)
print(f"Hashtag: {hashtags}")

# Normalisasi spasi
teks_berantakan = "Ini    teks\t dengan\n\nbanyak   spasi"
normal = re.sub(r"\s+", " ", teks_berantakan).strip()
print(f"Normalisasi: '{normal}'")

# Masking kartu kredit (simpan 4 digit terakhir)
cc = "1234 5678 9012 3456"
masked = re.sub(r"\d(?=\d{4})", "*", cc)
print(f"Masked CC: {masked}")

# Parsing log
log = '127.0.0.1 - - [19/Nov/2026:10:30:45 +0700] "GET /api/user HTTP/1.1" 200 1234'
log_pattern = re.compile(
    r'(?P<ip>\S+) '
    r'(?P<ident>\S+) '
    r'(?P<user>\S+) '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<request>[^"]+)" '
    r'(?P<status>\d+) '
    r'(?P<size>\d+)'
)
m = log_pattern.match(log)
if m:
    print(f"Log parsed: IP={m.group('ip')}, Status={m.group('status')}, Request={m.group('request')}")

# ============================================
# 8. Compile untuk Performa
# ============================================
print("\n=== 8. Compile Pattern ===")

# Jika pola dipakai berulang, compile sekali
EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_REGEX = re.compile(r"(\+62|62|0)8\d{8,11}")

# Pakai
data = "kontak: hayyan@test.com, 081234567890, admin@site.org"
print(f"Emails: {EMAIL_REGEX.findall(data)}")
print(f"Phones: {PHONE_REGEX.findall(data)}")

# ============================================
# LATIHAN TAMBAHAN
# ============================================
print("\n=== LATIHAN TAMBAHAN ===")

# Latihan 1: Validasi password
# Min 8 char, 1 uppercase, 1 lowercase, 1 digit, 1 simbol
def validasi_password(pwd: str) -> bool:
    if len(pwd) < 8:
        return False
    if not re.search(r"[A-Z]", pwd):
        return False
    if not re.search(r"[a-z]", pwd):
        return False
    if not re.search(r"\d", pwd):
        return False
    if not re.search(r"[!@#$%^&*]", pwd):
        return False
    return True

passwords = ["Pass123!", "weak", "Pass123", "PASS123!", "pass123!"]
for p in passwords:
    print(f"  {p}: {'Valid' if validasi_password(p) else 'Invalid'}")

# Latihan 2: Ekstrak URL
def ekstrak_url(teks: str) -> list:
    url_pattern = re.compile(
        r'https?://'
        r'(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        r'(?:/[-\w%!$&\'()*+,;=:@.]*)*'
    )
    return url_pattern.findall(teks)

teks_url = "Kunjungi https://github.com dan http://example.com/path?query=1"
print(f"URL: {ekstrak_url(teks_url)}")

# Latihan 3: Validasi IP Address
def validasi_ipv4(ip: str) -> bool:
    pattern = re.compile(
        r"^"
        r"(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
        r"$"
    )
    return bool(pattern.match(ip))

ips = ["192.168.1.1", "255.255.255.255", "256.1.1.1", "10.0.0", "1.2.3.4.5"]
for ip in ips:
    print(f"  {ip}: {'Valid' if validasi_ipv4(ip) else 'Invalid'}")

# Latihan 4: Parsing CSV sederhana (tanpa csv module)
def parse_csv_line(line: str) -> list:
    # Handle quoted fields dengan koma di dalam
    pattern = re.compile(r'(?:^|,)("(?:[^"]|"")*"|[^,]*)')
    fields = []
    for match in pattern.finditer(line):
        field = match.group(1)
        if field.startswith('"') and field.endswith('"'):
            field = field[1:-1].replace('""', '"')
        fields.append(field)
    return fields

csv_lines = [
    'nama,umur,kota',
    '"Hayyan",25,"Jakarta"',
    '"Nashrulloh, Jr.",30,"Bandung, Jawa Barat"',
]
for line in csv_lines:
    print(f"  {parse_csv_line(line)}")

# Latihan 5: Replace dengan fungsi
def capitalize_match(match):
    return match.group().upper()

teks = "kata1 kata2 kata3"
result = re.sub(r"\b\w+\b", capitalize_match, teks)
print(f"Capitalize all: {result}")