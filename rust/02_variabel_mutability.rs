// Materi 02: Variabel dan Mutability

fn main() {
    let x = 5;
    println!("x = {}", x);

    // x = 6; // ERROR: tidak bisa diubah

    let mut y = 10;
    println!("y sebelum diubah = {}", y);
    y = 20;
    println!("y sesudah diubah = {}", y);

    y += 5;
    println!("y setelah += 5 = {}", y);

    const MAX_POINTS: u32 = 100_000;
    println!("Konstanta MAX_POINTS = {}", MAX_POINTS);

    let z = 5;
    let z = z * 2;
    println!("Shadowing z = {}", z);

    let z = z + 1;
    println!("Shadowing z lagi = {}", z);

    let spasi = "   ";
    let spasi = spasi.len();
    println!("Shadowing dengan tipe berbeda = {}", spasi);

    let spaces = "   ";
    let spaces = spaces.len();
    println!("Nama sama, tipe berubah &str -> usize: {}", spaces);

    let mut counter = 0;
    counter = counter + 1;
    println!("Counter = {}", counter);

    let (a, b) = (1, 2);
    println!("Destructuring tuple: a = {}, b = {}", a, b);

    let angka = 42;
    println!("Angka = {}", angka);
}