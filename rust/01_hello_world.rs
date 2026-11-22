// Materi 01: Hello World dan Print
// Penjelasan: println! adalah macro (bukan fungsi) untuk output ke stdout dengan newline.
// print! sama tapi tanpa newline. Macro di Rust diakhiri dengan !.

fn main() {
    println!("Hello, world!");
    println!("Halo, Rust!");

    print!("Print tanpa newline");
    println!(" -> lanjutan di baris yang sama");

    let nama = "Hayyan";
    let umur = 20;

    // Format string dengan {} placeholder
    println!("Nama saya {}", nama);
    println!("Umur saya {} tahun", umur);

    // Named arguments (Rust 2021+): gunakan nama variabel langsung di format string
    println!("Nama: {nama}, Umur: {umur}");

    // Positional arguments: index eksplisit {0}, {1}
    println!("Positional: {} {}", "Rust", 2026);

    // Reuse argument dengan index
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

    // Format khusus: X=hex uppercase, b=binary, o=octal
    println!("Hex: {:X}, Binary: {:b}, Octal: {:o}", 255, 5, 8);

    // Debug trait {:?} untuk struct/tuple/collection yang implement Debug
    println!("Debug trait: {:?}", (1, "dua", 3.0));
    println!("Pretty debug: {:#?}", vec![1, 2, 3]);

    // ============================================
    // LATIHAN TAMBAHAN (Exercise)
    // ============================================

    // Latihan 1: Format width & alignment (padding)
    println!("\n=== Latihan 1: Width & Alignment ===");
    println!("|{:>10}|{:<10}|{:^10}|", "Rata kanan", "Rata kiri", "Tengah");
    println!("|{:>10}|{:<10}|{:^10}|", 100, 200, 300);
    println!("|{:>10.2}|{:<10.2}|{:^10.2}|", 3.14159, 2.71828, 1.41421);

    // Latihan 2: Format bilangan dengan prefix & padding nol
    println!("\n=== Latihan 2: Prefix & Zero Padding ===");
    println!("Desimal : {}", 42);
    println!("Hex     : {:#X} (dengan 0x)", 42);
    println!("Biner   : {:#b} (dengan 0b)", 42);
    println!("Oktal   : {:#o} (dengan 0o)", 42);
    println!("Padding0: {:0>8}", 42);  // 8 karakter, rata kanan, isi nol di kiri

    // Latihan 3: Escape karakter & raw string
    println!("\n=== Latihan 3: Escape & Raw String ===");
    println!("Baris 1\nBaris 2\tTab");
    println!(r#"Raw string: \n \t "quote" "#);  // r#"..."# = raw string literal

    // Latihan 4: Debug struct dengan derive
    println!("\n=== Latihan 4: Debug Struct ===");
    #[derive(Debug)]
    struct Mahasiswa {
        nama: &'static str,
        nim: u32,
        ipk: f32,
    }
    let mhs = Mahasiswa { nama: "Hayyan", nim: 2021001, ipk: 3.85 };
    println!("Field    : nama={}, nim={}, ipk={}", mhs.nama, mhs.nim, mhs.ipk);
    println!("Debug    : {:?}", mhs);
    println!("Pretty   : {:#?}", mhs);

    // Latihan 5: eprint! & eprintln! untuk stderr (error output)
    println!("\n=== Latihan 5: stderr vs stdout ===");
    eprintln!("Ini ke stderr (error output)");
    println!("Ini ke stdout (normal output)");

    // Latihan 6: Format pointer address & pointer ke fungsi
    println!("\n=== Latihan 6: Pointer Address ===");
    let val = 42;
    let ptr = &val as *const i32;
    println!("Alamat val: {:p}", ptr);
    println!("Fungsi main: {:p}", main as *const ());
}