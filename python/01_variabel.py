# Materi 01: Variabel dan Tipe Data Dasar

nama = "Hayyan"
umur = 20
tinggi = 170.5
is_active = True

print("Nama   :", nama)
print("Umur   :", umur)
print("Tinggi :", tinggi)
print("Aktif  :", is_active)

print("Tipe nama     :", type(nama))
print("Tipe umur     :", type(umur))
print("Tipe tinggi   :", type(tinggi))
print("Tipe is_active:", type(is_active))

x, y, z = 1, 2, 3
print("Multiple assignment:", x, y, z)

PI = 3.14159
print("Konstanta PI =", PI)

umur_str = str(umur)
umur_float = float(umur)
print("Umur -> str :", umur_str, type(umur_str).__name__)
print("Umur -> float:", umur_float, type(umur_float).__name__)