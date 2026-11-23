# Materi 05: List dan Dictionary
from typing import Any

print("=== LIST ===")
buah = ["apel", "mangga", "jeruk", "pisang"]
print("List awal:", buah)
print("Index 0  :", buah[0])
print("Index -1 :", buah[-1])
print("Slice 1:3:", buah[1:3])
print("Panjang  :", len(buah))

buah.append("anggur")
buah.insert(1, "melon")
buah.remove("jeruk")
print("Setelah modifikasi:", buah)

buah[0] = "apel hijau"
print("Setelah update index 0:", buah)
print("Sorted:", sorted(buah))

angka = [5, 3, 9, 1, 7]
angka.sort()
print("Angka terurut:", angka)
print("Total:", sum(angka), "Max:", max(angka), "Min:", min(angka))

print("List comprehension kuadrat:", [n * n for n in range(1, 6)])
print("List comprehension genap   :", [n for n in range(10) if n % 2 == 0])

print("\n=== DICTIONARY ===")
mahasiswa = {
    "nama": "Hayyan",
    "umur": 20,
    "jurusan": "Informatika",
    "ipk": 3.85,
}

print("Dict awal:", mahasiswa)
print("Ambil nama  :", mahasiswa["nama"])
print("Ambil get   :", mahasiswa.get("asal", "tidak ada"))

mahasiswa["semester"] = 5
mahasiswa["ipk"] = 3.9
del mahasiswa["umur"]
print("Setelah diubah:", mahasiswa)

print("Keys  :", list(mahasiswa.keys()))
print("Values:", list(mahasiswa.values()))
print("Items :")
for kunci, nilai in mahasiswa.items():
    print(f"  {kunci} = {nilai}")

print("Dict comprehension:", {n: n * n for n in range(1, 6)})

daftar_mahasiswa: list[dict[str, Any]] = [
    {"nama": "Hayyan", "ipk": 3.9},
    {"nama": "Rina", "ipk": 3.5},
    {"nama": "Budi", "ipk": 3.1},
]
print("\nMahasiswa dengan IPK > 3.4:")
for m in daftar_mahasiswa:
    if m["ipk"] > 3.4:
        print(" ", m["nama"], m["ipk"])
