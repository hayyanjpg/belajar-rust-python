// Materi 12: Module System & Cargo (binary)
// Jalankan dari folder ini:
//   cargo run
//   cargo test
//   cargo build --release
//
// Perhatikan path import di bawah: crate ini bernama `belajar_module`
// (sesuai `name` di Cargo.toml), bukan nama folder.

// `use` mempersingkat path. `self` di sini berarti module `matematika` itu sendiri.
use belajar_module::matematika::{self, geometri};
use belajar_module::util::teks;

// Re-export dari `util::mod.rs` bisa dipakai langsung.
use belajar_module::util::kapitalisasi;

// Alias dengan `as`
use belajar_module::info_crate;

fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO MODULE SYSTEM & CARGO");
    println!("{}", "=".repeat(50));

    // 1. Info crate (env! dibaca saat compile)
    println!("\n--- INFO CRATE ---");
    println!("  {}", info_crate());

    // 2. Memanggil fungsi module
    println!("\n--- MATEMATIKA ---");
    println!("  tambah(2, 3) = {}", matematika::tambah(2, 3));
    println!("  faktorial(5) = {}", matematika::faktorial(5));
    println!("  PI = {}", matematika::PI);

    match matematika::bagi(10.0, 4.0) {
        Ok(v) => println!("  bagi(10, 4) = {:.2}", v),
        Err(e) => println!("  Error: {}", e),
    }
    match matematika::bagi(10.0, 0.0) {
        Ok(v) => println!("  bagi(10, 0) = {:.2}", v),
        Err(e) => println!("  Error (seharusnya): {}", e),
    }

    // 3. Nested module
    println!("\n--- NESTED MODULE ---");
    println!("  luas lingkaran r=7  : {:.2}", geometri::luas_lingkaran(7.0));
    println!("  keliling lingkaran r=7: {:.2}", geometri::keliling_lingkaran(7.0));
    println!("  luas persegi sisi=4 : {:.2}", geometri::persegi::luas(4.0));
    println!("  keliling persegi    : {:.2}", geometri::persegi::keliling(4.0));

    // 4. Module util dan re-export
    println!("\n--- MODULE UTIL ---");
    let kalimat = "belajar rust dan cargo itu menyenangkan";
    println!("  asli        : {}", kalimat);
    println!("  kapitalisasi: {}", kapitalisasi(kalimat));
    println!("  via teks    : {}", teks::kapitalisasi("module system"));
    println!("  potong      : {}", teks::potong(kalimat, 20));
    println!("  jumlah kata : {}", teks::hitung_kata(kalimat));

    // 5. Alias module
    println!("\n--- ALIAS ---");
    use belajar_module::matematika as mtk;
    println!("  mtk::tambah(100, 200) = {}", mtk::tambah(100, 200));

    // 6. Path absolut crate
    println!("\n--- PATH crate:: / super:: ---");
    println!(
        "  belajar_module::matematika::PI = {}",
        belajar_module::matematika::PI
    );
    println!("  Di dalam library, `crate::` menunjuk root crate dan `super::` module induk.");

    println!("\nJalankan `cargo test` untuk melihat unit test di dalam module.");
    println!("\n=== SELESAI ===");
}
