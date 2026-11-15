// Materi 01: Hello World dan Print

fn main() {
    println!("Hello, world!");
    println!("Halo, Rust!");

    print!("Print tanpa newline");
    println!(" -> lanjutan di baris yang sama");

    let nama = "Hayyan";
    let umur = 20;

    println!("Nama saya {}", nama);
    println!("Umur saya {} tahun", umur);

    println!("Nama: {nama}, Umur: {umur}");
    println!("Positional: {} {}", "Rust", 2026);

    println!("{0} adalah bahasa sistem yang aman. {0} fokus pada performa.", "Rust");

    let a = 10;
    let b = 3;

    println!("Penjumlahan : {} + {} = {}", a, b, a + b);
    println!("Pengurangan : {} - {} = {}", a, b, a - b);
    println!("Perkalian   : {} * {} = {}", a, b, a * b);
    println!("Pembagian   : {} / {} = {}", a, b, a / b);
    println!("Sisa bagi   : {} % {} = {}", a, b, a % b);

    let pi = 3.14159;
    println!("Pi dibulatkan 2 angka: {:.2}", pi);

    println!("Hex: {:X}, Binary: {:b}, Octal: {:o}", 255, 5, 8);

    println!("Debug trait: {:?}", (1, "dua", 3.0));
    println!("Pretty debug: {:#?}", vec![1, 2, 3]);
}