# Materi 01: Variabel dan Tipe Data Dasar
# Penjelasan: Variabel adalah wadah untuk menyimpan data. Python bersifat dynamic typing,
# artinya tipe data ditentukan otomatis saat runtime berdasarkan nilai yang ditugaskan.

nama = "Hayyan"          # tipe str (string) - teks
umur = 20                # tipe int (integer) - bilangan bulat
tinggi = 170.5           # tipe float - bilangan desimal
is_active = True         # tipe bool (boolean) - True/False

print("Nama   :", nama)
print("Umur   :", umur)
print("Tinggi :", tinggi)
print("Aktif  :", is_active)

# Memeriksa tipe data dengan fungsi type()
print("Tipe nama     :", type(nama))
print("Tipe umur     :", type(umur))
print("Tipe tinggi   :", type(tinggi))
print("Tipe is_active:", type(is_active))

# Multiple assignment: menetapkan beberapa variabel sekaligus
x, y, z = 1, 2, 3
print("Multiple assignment:", x, y, z)

# Konstanta: konvensi nama huruf besar (PI, MAX_SIZE, dll.)
# Python tidak memiliki keyword const, ini hanya konvensi penamaan
PI = 3.14159
print("Konstanta PI =", PI)

# Casting / konversi tipe data
umur_str = str(umur)       # int -> str
umur_float = float(umur)   # int -> float
print("Umur -> str :", umur_str, type(umur_str).__name__)
print("Umur -> float:", umur_float, type(umur_float).__name__)

# ============================================
# LATIHAN TAMBAHAN (Exercise)
# ============================================

# Latihan 1: Tukar nilai dua variabel tanpa variabel sementara
a = 10
b = 20
print(f"\nLatihan 1 - Sebelum tukar: a={a}, b={b}")
a, b = b, a  # Pythonic swap
print(f"Latihan 1 - Sesudah tukar: a={a}, b={b}")

# Latihan 2: Hitung luas dan keliling persegi panjang
panjang = 12
lebar = 8
luas = panjang * lebar
keliling = 2 * (panjang + lebar)
print(f"\nLatihan 2 - Persegi panjang: panjang={panjang}, lebar={lebar}")
print(f"  Luas = {luas}, Keliling = {keliling}")

# Latihan 3: Konversi suhu Celsius ke Fahrenheit & Kelvin
celsius = 37.0
fahrenheit = celsius * 9/5 + 32
kelvin = celsius + 273.15
print(f"\nLatihan 3 - Suhu {celsius}°C = {fahrenheit:.1f}°F = {kelvin:.2f}K")

# Latihan 4: Format string dengan f-string (lebih efisien & readable)
produk = "Laptop"
harga = 12_500_000  # underscore sebagai pemisah ribuan (Python 3.6+)
print(f"\nLatihan 4 - Produk: {produk}, Harga: Rp{harga:,}")

# Latihan 5: Boolean expression & short-circuit evaluation
is_member = True
diskon = 0.15 if is_member else 0
print(f"\nLatihan 5 - Member: {is_member}, Diskon: {diskon*100:.0f}%")