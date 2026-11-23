# Materi 03: Perulangan for dan while

print("For loop dengan range:")
for i in range(1, 6):
    print("  iterasi ke -", i)

print("For loop dengan string:")
for huruf in "Rust":
    print("  huruf:", huruf)

print("For loop dengan list:")
buah = ["apel", "mangga", "jeruk"]
for b in buah:
    print("  buah:", b)

print("For loop dengan enumerate:")
for idx, b in enumerate(buah, start=1):
    print(f"  {idx}. {b}")

print("While loop:")
counter = 3
while counter > 0:
    print("  hitung mundur:", counter)
    counter -= 1
print("  Selesai!")

print("Break dan continue:")
for i in range(1, 10):
    if i == 5:
        break
    if i % 2 == 0:
        continue
    print("  ganjil:", i)

print("Nested loop (tabel perkalian 1-3):")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"  {i} x {j} = {i * j}")

print("Loop dengan else:")
for i in range(3):
    print("  angka:", i)
print("  loop selesai tanpa break")

print("Sum 1..10 =", sum(range(1, 11)))
