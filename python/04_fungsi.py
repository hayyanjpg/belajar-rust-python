# Materi 04: Fungsi Dasar

def sapa(nama):
    print(f"Halo, {nama}!")


def tambah(a, b):
    return a + b


def bagi(a, b=2):
    if b == 0:
        return "Tidak bisa bagi nol"
    return a / b


def stats(angka_list):
    return len(angka_list), min(angka_list), max(angka_list), sum(angka_list)


def hitung_total(*harga):
    total = 0
    for h in harga:
        total += h
    return total


def buat_profil(**data):
    for kunci, nilai in data.items():
        print(f"  {kunci}: {nilai}")


def faktorial(n):
    if n <= 1:
        return 1
    return n * faktorial(n - 1)


def celsius_ke_fahrenheit(c):
    return c * 9 / 5 + 32


sapa("Hayyan")
print("Tambah 10 + 5 =", tambah(10, 5))
print("Bagi 10 / 4  =", bagi(10, 4))
print("Bagi 10 / 0  =", bagi(10, 0))
print("Stats       =", stats([4, 8, 15, 16, 23, 42]))
print("Total belanja:", hitung_total(15000, 22000, 5000))

print("Profil:")
buat_profil(nama="Hayyan", umur=20, kota="Jakarta")

print("Faktorial 5 =", faktorial(5))
print("Fahrenheit dari 100C =", celsius_ke_fahrenheit(100))