# Materi 12: Standard Library - datetime, time, calendar
# Python standard library menyediakan modul untuk manipulasi waktu dan tanggal.

import calendar
import time as time_module
from datetime import UTC, date, datetime, time, timedelta, timezone

# ============================================
# 1. datetime - Tanggal dan Waktu
# ============================================
print("=== 1. datetime ===")

# datetime.now() - waktu lokal saat ini
now = datetime.now()
print(f"Sekarang: {now}")

# datetime.today() - tanggal hari ini (tanpa timezone)
today = datetime.today()  # noqa: DTZ002 - contoh waktu lokal tanpa timezone
print(f"Hari ini: {today}")

# datetime.now(UTC) - waktu UTC (utcnow() sudah deprecated)
utc_now = datetime.now(UTC)
print(f"UTC: {utc_now}")

# datetime.fromtimestamp() - dari timestamp Unix
ts = 1700000000
dt_from_ts = datetime.fromtimestamp(ts)
print(f"Dari timestamp {ts}: {dt_from_ts}")

# Membuat datetime spesifik
custom_dt = datetime(2024, 12, 25, 10, 30, 45)
print(f"Custom: {custom_dt}")

# Parsing string ke datetime
dt_str = "2024-12-25 10:30:45"
parsed = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
print(f"Parsed: {parsed}")

# Format datetime ke string
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"Formatted: {formatted}")

# Format Indonesia
id_format = now.strftime("%d %B %Y, %H:%M WIB")
print(f"Format ID: {id_format}")

# ============================================
# 2. date - Hanya Tanggal
# ============================================
print("\n=== 2. date ===")

today_date = date.today()
print(f"Tanggal hari ini: {today_date}")

custom_date = date(2024, 12, 25)
print(f"Natal 2024: {custom_date}")

# Operasi date
tomorrow = today_date + timedelta(days=1)
yesterday = today_date - timedelta(days=1)
print(f"Besok: {tomorrow}, Kemarin: {yesterday}")

# Selisih hari
natal = date(2024, 12, 25)
selisih = natal - today_date
print(f"Hari menuju natal: {selisih.days} hari")

# ============================================
# 3. time - Hanya Waktu
# ============================================
print("\n=== 3. time ===")

waktu = time(14, 30, 45)
print(f"Waktu: {waktu}")

# Dengan microsecond
waktu_detail = time(14, 30, 45, 123456)
print(f"Detail: {waktu_detail}")

# ============================================
# 4. timedelta - Selisih Waktu
# ============================================
print("\n=== 4. timedelta ===")

# Membuat timedelta
td = timedelta(days=7, hours=3, minutes=30, seconds=15)
print(f"1 minggu 3 jam 30 menit 15 detik: {td}")

# Operasi timedelta
now = datetime.now()
minggu_depan = now + timedelta(weeks=1)
print(f"Minggu depan: {minggu_depan}")

# Total detik
total_detik = td.total_seconds()
print(f"Total detik: {total_detik}")

# ============================================
# 5. timezone - Zona Waktu
# ============================================
print("\n=== 5. timezone ===")

# UTC
utc = UTC
dt_utc = datetime.now(utc)
print(f"UTC aware: {dt_utc}")

# WIB (UTC+7)
wib = timezone(timedelta(hours=7))
dt_wib = datetime.now(wib)
print(f"WIB aware: {dt_wib}")

# Konversi timezone
dt_wib_converted = dt_utc.astimezone(wib)
print(f"UTC ke WIB: {dt_wib_converted}")

# ============================================
# 6. time module - Fungsi Waktu Lower-level
# ============================================
print("\n=== 6. time module ===")

# Timestamp Unix (detik sejak epoch)
ts_sekarang = time_module.time()
print(f"Timestamp: {ts_sekarang}")

# Sleep
print("Sleep 0.5 detik...")
time_module.sleep(0.5)
print("Selesai")

# time.localtime() - struct_time lokal
local = time_module.localtime()
print(f"Local time: {local}")

# time.gmtime() - struct_time UTC
gmt = time_module.gmtime()
print(f"GMT time: {gmt}")

# time.strftime() - format struct_time
fmt = time_module.strftime("%Y-%m-%d %H:%M:%S", local)
print(f"Formatted: {fmt}")

# ============================================
# 7. calendar - Kalender
# ============================================
print("\n=== 7. calendar ===")

# Kalender bulan
print("Desember 2024:")
print(calendar.month(2024, 12))

# Kalender tahun
# print(calendar.calendar(2024))

# Cek tahun kabisat
print(f"2024 kabisat: {calendar.isleap(2024)}")
print(f"2023 kabisat: {calendar.isleap(2023)}")

# Hari pertama dan jumlah hari dalam bulan
first_weekday, num_days = calendar.monthrange(2024, 2)
print(f"Februari 2024: hari pertama={first_weekday} (0=Senin), jumlah hari={num_days}")

# Iterasi minggu
print("\nMinggu ke-minggu Februari 2024:")
for week in calendar.monthcalendar(2024, 2):
    print(week)

# ============================================
# 8. zoneinfo - Zona Waktu Modern (Python 3.9+)
# ============================================
print("\n=== 8. zoneinfo (Python 3.9+) ===")

try:
    from zoneinfo import ZoneInfo

    # Zona waktu IANA
    jakarta = ZoneInfo("Asia/Jakarta")
    dt_jakarta = datetime.now(jakarta)
    print(f"Jakarta: {dt_jakarta}")

    tokyo = ZoneInfo("Asia/Tokyo")
    dt_tokyo = datetime.now(tokyo)
    print(f"Tokyo: {dt_tokyo}")

    new_york = ZoneInfo("America/New_York")
    dt_ny = datetime.now(new_york)
    print(f"New York: {dt_ny}")

    # Konversi
    dt_tokyo_converted = dt_jakarta.astimezone(tokyo)
    print(f"Jakarta ke Tokyo: {dt_tokyo_converted}")

except ImportError:
    print("zoneinfo tidak tersedia (Python < 3.9)")

# ============================================
# LATIHAN TAMBAHAN
# ============================================
print("\n=== LATIHAN TAMBAHAN ===")


# Latihan 1: Hitung umur dari tanggal lahir
def hitung_umur(tanggal_lahir: date) -> int:
    today = date.today()
    umur = today.year - tanggal_lahir.year
    if (today.month, today.day) < (tanggal_lahir.month, tanggal_lahir.day):
        umur -= 1
    return umur


lahir = date(2000, 5, 15)
print(f"Umur (lahir 15 Mei 2000): {hitung_umur(lahir)} tahun")

# Latihan 2: Format tanggal Indonesia
bulan_id = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]


def format_indonesia(dt: datetime) -> str:
    return f"{dt.day} {bulan_id[dt.month - 1]} {dt.year}"


print(f"Format ID: {format_indonesia(datetime.now())}")


# Latihan 3: Hitung hari kerja
def hitung_hari_kerja(mulai: date, selesai: date) -> int:
    hari_kerja = 0
    current = mulai
    while current <= selesai:
        if current.weekday() < 5:  # 0-4 = Senin-Jumat
            hari_kerja += 1
        current += timedelta(days=1)
    return hari_kerja


mulai = date(2024, 12, 1)
selesai = date(2024, 12, 31)
print(f"Hari kerja Desember 2024: {hitung_hari_kerja(mulai, selesai)}")

# Latihan 4: Stopwatch sederhana
import time as t


def stopwatch():
    input("Tekan Enter untuk mulai...")
    start = t.perf_counter()
    input("Tekan Enter untuk berhenti...")
    end = t.perf_counter()
    print(f"Waktu: {end - start:.3f} detik")


# stopwatch()  # Uncomment untuk mencoba


# Latihan 5: Countdown timer
def countdown(detik: int):
    while detik > 0:
        menit, sisa = divmod(detik, 60)
        print(f"\r{menit:02d}:{sisa:02d}", end="", flush=True)
        t.sleep(1)
        detik -= 1
    print("\rWaktu habis!")


# countdown(10)  # Uncomment untuk mencoba 10 detik
