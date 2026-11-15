# Materi 02: Percabangan if / elif / else

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

if umur >= 17 and nilai >= 80:
    print("Lolos seleksi mandiri")

if nilai >= 80 or umur < 17:
    print("Salah satu kondisi terpenuhi")

if not (nilai < 70):
    print("Nilai tidak di bawah 70")

status = "Lulus" if nilai >= 70 else "Tidak Lulus"
print("Hasil ternary:", status)

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