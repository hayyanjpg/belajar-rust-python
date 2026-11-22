// Materi 13: Lifetime
// Penjelasan: Lifetime ('a) adalah cara compiler memastikan reference selalu valid.
// Lifetime TIDAK mengubah umur data; ia hanya memberi tahu compiler hubungan umur
// antar-reference. Sebagian besar lifetime sudah di-infer otomatis (lifetime elision).

use std::fmt::Display;

// ============================================
// 1. MASALAH YANG DISELESAIKAN LIFETIME
// ============================================
// Fungsi ini TIDAK bisa dikompilasi tanpa anotasi lifetime:
//
//   fn terpanjang_tanpa_lifetime(x: &str, y: &str) -> &str { ... }
//
// Compiler tidak tahu apakah reference yang dikembalikan terikat ke x atau y,
// jadi ia tidak bisa menjamin hasilnya masih valid.

// Solusi: beri tahu bahwa hasil hidup selama kedua input hidup.
fn terpanjang<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() >= y.len() {
        x
    } else {
        y
    }
}

fn demo_fungsi_lifetime() {
    println!("\n--- FUNGSI DENGAN LIFETIME ---");

    let a = String::from("Rust");
    let b = "Python";
    println!("  terpanjang: {}", terpanjang(&a, b));

    let hasil;
    {
        let sementara = String::from("sementara");
        // hasil hidup lebih lama dari `sementara`, jadi ini ERROR kalau dipakai
        // di luar scope. Contoh aman: pakai di dalam scope.
        hasil = terpanjang(&sementara, "abc");
        println!("  di dalam scope: {}", hasil);
    }
    // println!("{}", hasil); // ERROR: `sementara` sudah drop
}

// ============================================
// 2. LIFETIME ELISION (OTOMATIS)
// ============================================
// Aturan elision:
// 1. Tiap parameter reference mendapat lifetime sendiri.
// 2. Jika hanya ada SATU parameter reference, output memakai lifetime itu.
// 3. Jika ada `&self`/`&mut self`, output memakai lifetime self.

// Output otomatis terikat ke `kata` (satu-satunya input reference).
fn kata_pertama(kata: &str) -> &str {
    kata.split_whitespace().next().unwrap_or("")
}

// Output otomatis terikat ke `&self`.
struct Teks<'a> {
    isi: &'a str,
}

impl<'a> Teks<'a> {
    // Terikat ke lifetime struct ('a), bukan ke &self
    fn isi(&self) -> &'a str {
        self.isi
    }

    // Terikat ke &self (karena memakai data milik self)
    fn awal(&self) -> &str {
        &self.isi[..self.isi.len().min(5)]
    }
}

fn demo_elision() {
    println!("\n--- ELISION ---");

    let kalimat = String::from("belajar rust itu menyenangkan");
    println!("  kata_pertama: {}", kata_pertama(&kalimat));

    let teks = Teks { isi: &kalimat };
    println!("  isi  : {}", teks.isi());
    println!("  awal : {}", teks.awal());
}

// ============================================
// 3. STRUCT DENGAN LIFETIME
// ============================================
// Struct ini tidak memiliki String; ia hanya meminjam data.
// Artinya data pemilik harus hidup lebih lama dari struct.
#[derive(Debug)]
struct Kutipan<'a> {
    teks: &'a str,
    sumber: &'a str,
}

impl<'a> Kutipan<'a> {
    fn new(teks: &'a str, sumber: &'a str) -> Self {
        Kutipan { teks, sumber }
    }

    fn teks(&self) -> &'a str {
        self.teks
    }

    fn ringkas(&self, maks: usize) -> &'a str {
        if self.teks.len() <= maks {
            self.teks
        } else {
            &self.teks[..maks]
        }
    }

    fn tampilkan(&self) {
        println!("  \"{}\" - {}", self.teks, self.sumber);
    }
}

fn demo_struct_lifetime() {
    println!("\n--- STRUCT DENGAN LIFETIME ---");

    let sumber = String::from("Rust Book");
    let teks = String::from("Rust membuat kita percaya pada compiler.");

    let kutipan = Kutipan::new(&teks, &sumber);
    kutipan.tampilkan();
    println!("  teks   : {}", kutipan.teks());
    println!("  ringkas: {}", kutipan.ringkas(20));
    println!("  debug  : {:?}", kutipan);
}

// ============================================
// 4. MULTIPLE LIFETIME
// ============================================
// Dua reference dengan umur berbeda tetap bisa disimpan bersama.
#[derive(Debug)]
struct DuaTeks<'a, 'b> {
    kiri: &'a str,
    kanan: &'b str,
}

impl<'a, 'b> DuaTeks<'a, 'b> {
    fn kiri(&self) -> &'a str {
        self.kiri
    }

    fn kanan(&self) -> &'b str {
        self.kanan
    }
}

// Output memakai lifetime `'a` saja (hanya kiri yang boleh dikembalikan).
fn ambil_kiri<'a, 'b>(kiri: &'a str, _kanan: &'b str) -> &'a str {
    kiri
}

fn demo_multiple_lifetime() {
    println!("\n--- MULTIPLE LIFETIME ---");

    let panjang = String::from("teks yang hidup lama");
    let hasil;
    {
        let pendek = String::from("pendek");
        let dua = DuaTeks {
            kiri: &panjang,
            kanan: &pendek,
        };
        println!("  kiri : {}", dua.kiri());
        println!("  kanan: {}", dua.kanan());
        hasil = ambil_kiri(&panjang, &pendek);
    }
    // `pendek` sudah drop, tapi `hasil` hanya terikat ke `panjang`, jadi aman.
    println!("  hasil setelah scope: {}", hasil);
}

// ============================================
// 5. 'static
// ============================================
// 'static berarti reference hidup selama program berjalan.
// String literal (&str) selalu 'static.
static NAMA_BAHASA: &str = "Rust";

fn versi() -> &'static str {
    "1.0.0"
}

fn demo_static() {
    println!("\n--- 'static ---");
    println!("  static: {}", NAMA_BAHASA);
    println!("  versi : {}", versi());

    let literals: Vec<&'static str> = vec!["satu", "dua", "tiga"];
    println!("  literals: {:?}", literals);

    // Catatan: `String` yang di-leak juga bisa menjadi &'static str,
    // tapi hindari kecuali benar-benar perlu (memori tidak pernah dibebaskan).
}

// ============================================
// 6. LIFETIME BOUND PADA GENERIC
// ============================================
// T: Display + PartialOrd, dan kedua reference harus hidup selama 'a.
fn nilai_maks<'a, T>(a: &'a T, b: &'a T) -> &'a T
where
    T: PartialOrd + Display,
{
    if a > b {
        a
    } else {
        b
    }
}

fn demo_lifetime_bound() {
    println!("\n--- LIFETIME BOUND + GENERIC ---");

    let x = 10;
    let y = 25;
    println!("  maks(10, 25) = {}", nilai_maks(&x, &y));

    let s1 = String::from("apel");
    let s2 = String::from("mangga");
    println!("  maks(apel, mangga) = {}", nilai_maks(&s1, &s2));
}

// ============================================
// 7. STRUCT BERISI STRUCT DENGAN LIFETIME
// ============================================
#[derive(Debug)]
struct Artikel<'a> {
    judul: &'a str,
    isi: &'a str,
}

#[derive(Debug)]
struct Ulasan<'a> {
    artikel: &'a Artikel<'a>,
    komentar: &'a str,
}

impl<'a> Ulasan<'a> {
    fn ringkasan(&self) -> String {
        format!(
            "Ulasan untuk '{}' ({}): {}",
            self.artikel.judul, self.artikel.isi, self.komentar
        )
    }
}

fn demo_nested_lifetime() {
    println!("\n--- NESTED LIFETIME ---");

    let artikel = Artikel {
        judul: "Belajar Lifetime",
        isi: "Lifetime menjaga reference tetap valid.",
    };
    let ulasan = Ulasan {
        artikel: &artikel,
        komentar: "Penjelasannya jelas",
    };
    println!("  {}", ulasan.ringkasan());
    println!("  {:?}", ulasan);
}

// ============================================
// 8. LATIHAN
// ============================================
fn latihan() {
    println!("\n--- LATIHAN ---");

    // Latihan 1: kembalikan teks yang lebih pendek
    fn terpendek<'a>(x: &'a str, y: &'a str) -> &'a str {
        if x.len() <= y.len() {
            x
        } else {
            y
        }
    }
    println!("  1. terpendek: {}", terpendek("rust", "python"));

    // Latihan 2: struct dengan dua field reference dan method
    struct Pengguna<'a> {
        nama: &'a str,
        email: &'a str,
    }

    impl<'a> Pengguna<'a> {
        fn inisial(&self) -> String {
            self.nama
                .split_whitespace()
                .filter_map(|k| k.chars().next())
                .collect::<String>()
                .to_uppercase()
        }
    }

    let pengguna = Pengguna {
        nama: "Hayyan Nashrulloh",
        email: "hayyan@example.com",
    };
    println!("  2. inisial: {} <{}>", pengguna.inisial(), pengguna.email);

    // Latihan 3: generic + lifetime
    fn pertama_atau<'a, T>(items: &'a [T], default: &'a T) -> &'a T {
        items.first().unwrap_or(default)
    }

    let kosong: Vec<i32> = vec![];
    let cadangan = 99;
    println!("  3. pertama_atau: {}", pertama_atau(&kosong, &cadangan));

    // Latihan 4: 'static
    fn slogan() -> &'static str {
        "Fearless concurrency"
    }
    println!("  4. slogan: {}", slogan());

    // Latihan 5: lifetime pada method yang mengembalikan bagian dari self
    struct Kalimat<'a> {
        isi: &'a str,
    }

    impl<'a> Kalimat<'a> {
        fn dua_kata_pertama(&self) -> &'a str {
            let mut iter = self.isi.split_whitespace();
            let awal = iter.next().unwrap_or("");
            let kedua = iter.next().unwrap_or("");
            if kedua.is_empty() {
                awal
            } else {
                let akhir = awal.len() + 1 + kedua.len();
                &self.isi[..akhir]
            }
        }
    }

    let kalimat = Kalimat {
        isi: "lifetime membuat reference aman",
    };
    println!("  5. dua kata: {}", kalimat.dua_kata_pertama());
}

// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO LIFETIME RUST");
    println!("{}", "=".repeat(50));

    demo_fungsi_lifetime();
    demo_elision();
    demo_struct_lifetime();
    demo_multiple_lifetime();
    demo_static();
    demo_lifetime_bound();
    demo_nested_lifetime();
    latihan();

    println!("\n=== SELESAI ===");
}
