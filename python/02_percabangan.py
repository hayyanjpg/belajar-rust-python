# Materi 02: Percabangan if / elif / else
# Penjelasan: Percabangan mengontrol alur program berdasarkan kondisi.
# Python menggunakan indentasi (bukan kurung kurawal) untuk menandai blok kode.

nilai = 85

if nilai >= 90:
    grade = "A"
elif nilai >= 80:
    grade = "B"
elif nilai >= 70:
    grade = "C"
else:
    grade = "D"

print("Nilai:", nilai, "-> Grade:", grade)

umur = 17
if umur >= 17:
    print("Dewasa: boleh buat KTP")
else:
    print("Belum dewasa")

# Operator logika: and, or, not
if umur >= 17 and nilai >= 80:
    print("Lolos seleksi mandiri")

if nilai >= 80 or umur < 17:
    print("Salah satu kondisi terpenuhi")

if not (nilai < 70):
    print("Nilai tidak di bawah 70")

# Ternary operator (conditional expression): nilai_if_true if kondisi else nilai_if_false
status = "Lulus" if nilai >= 70 else "Tidak Lulus"
print("Hasil ternary:", status)

# Match-case (Python 3.10+) - alternatif switch case
hari = 6
if hari == 1:
    print("Senin")
elif hari == 2:
    print("Selasa")
elif hari == 3:
    print("Rabu")
elif hari == 4:
    print("Kamis")
elif hari == 5:
    print("Jumat")
elif hari == 6:
    print("Sabtu")
else:
    print("Minggu")

# ============================================
# LATIHAN TAMBAHAN (Exercise)
# ============================================

# Latihan 1: Penentuan bilangan genap/ganjil & positif/negatif/nol
angka = -7
print(f"\nLatihan 1 - Angka: {angka}")
if angka == 0:
    print("  Nol")
elif angka > 0:
    print("  Positif", "- Genap" if angka % 2 == 0 else "  Ganjil")
else:
    print("  Negatif", "- Genap" if angka % 2 == 0 else "  Ganjil")

# Latihan 2: Kalkulator sederhana dengan match-case (Python 3.10+)
a, b, op = 15, 5, "*"
print(f"\nLatihan 2 - Kalkulator: {a} {op} {b}")
hasil: int | float | str
match op:
    case "+":
        hasil = a + b
    case "-":
        hasil = a - b
    case "*":
        hasil = a * b
    case "/":
        hasil = a / b if b != 0 else "Error: div by zero"
    case "//":
        hasil = a // b if b != 0 else "Error: div by zero"
    case "%":
        hasil = a % b if b != 0 else "Error: div by zero"
    case "**":
        hasil = a**b
    case _:
        hasil = "Operator tidak dikenal"
print(f"  Hasil = {hasil}")

# Latihan 3: Kategorisasi BMI (Body Mass Index)
berat, tinggi_m = 68, 1.70
bmi = berat / (tinggi_m**2)
print(f"\nLatihan 3 - BMI: berat={berat}kg, tinggi={tinggi_m}m -> BMI={bmi:.1f}")
if bmi < 18.5:
    kategori = "Kurus"
elif bmi < 25:
    kategori = "Normal"
elif bmi < 30:
    kategori = "Gemuk"
else:
    kategori = "Obesitas"
print(f"  Kategori: {kategori}")

# Latihan 4: Nested if - cek kelulusan dengan syarat tambahan
nilai_ujian, absensi = 78, 85
print(f"\nLatihan 4 - Nilai={nilai_ujian}, Absensi={absensi}%")
if nilai_ujian >= 70:
    if absensi >= 75:
        print("  LULUS: Nilai & absensi memenuhi syarat")
    else:
        print("  TIDAK LULUS: Absensi < 75%")
else:
    print("  TIDAK LULUS: Nilai < 70")

# Latihan 5: Ternary operator bersarang (nested ternary)
skor = 88
grade_detail = (
    "A" if skor >= 90 else ("B" if skor >= 80 else ("C" if skor >= 70 else "D"))
)
print(f"\nLatihan 5 - Skor {skor} -> Grade detail: {grade_detail}")

# Latihan 6: Pattern matching dengan guard (Python 3.10+)
print("\nLatihan 6 - Match dengan guard:")
for angka in [3, 10, 15, 22, 7]:
    match angka:
        case x if x < 5:
            print(f"  {x} -> Kecil (<5)")
        case x if x % 2 == 0:
            print(f"  {x} -> Genap")
        case _:
            print(f"  {x} -> Ganjil >= 5")
