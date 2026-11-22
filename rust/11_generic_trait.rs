// Materi 11: Generic & Trait
// Penjelasan: Generic membuat kode bisa dipakai untuk banyak tipe tanpa duplikasi.
// Trait mendefinisikan perilaku (seperti interface). Kombinasinya adalah inti
// polymorphism di Rust: static dispatch (generic) dan dynamic dispatch (dyn Trait).

use std::fmt::{self, Display};
use std::ops::Add;

// ============================================
// 1. GENERIC FUNCTION
// ============================================
// T: PartialOrd + Copy artinya T harus bisa dibandingkan dan di-copy.
fn terbesar<T: PartialOrd + Copy>(a: T, b: T) -> T {
    if a > b {
        a
    } else {
        b
    }
}

// Generic dengan beberapa parameter tipe
fn pasangan<T, U>(pertama: T, kedua: U) -> (T, U) {
    (pertama, kedua)
}

fn demo_generic_function() {
    println!("\n--- GENERIC FUNCTION ---");

    println!("  terbesar(3, 7) = {}", terbesar(3, 7));
    println!("  terbesar(2.5, 1.5) = {}", terbesar(2.5, 1.5));
    println!("  terbesar('a', 'z') = {}", terbesar('a', 'z'));
    println!("  terbesar(\"apel\", \"jeruk\") = {}", terbesar("apel", "jeruk"));

    let p = pasangan(1, "satu");
    println!("  pasangan(1, \"satu\") = {:?}", p);
}

// ============================================
// 2. GENERIC STRUCT
// ============================================
#[derive(Debug, Clone, PartialEq)]
struct Pasangan<T, U> {
    pertama: T,
    kedua: U,
}

// impl generik: berlaku untuk semua T dan U
impl<T, U> Pasangan<T, U> {
    fn new(pertama: T, kedua: U) -> Self {
        Pasangan { pertama, kedua }
    }

    fn tukar(self) -> Pasangan<U, T> {
        Pasangan {
            pertama: self.kedua,
            kedua: self.pertama,
        }
    }
}

// impl dengan bound: method hanya tersedia jika T dan U bisa di-Display
impl<T: Display, U: Display> Pasangan<T, U> {
    fn tampilkan(&self) -> String {
        format!("({}, {})", self.pertama, self.kedua)
    }
}

// impl dengan bound di salah satu tipe saja
impl<T: PartialOrd, U> Pasangan<T, U> {
    fn terbesar_pertama<'a>(&'a self, lain: &'a T) -> &'a T {
        if self.pertama > *lain {
            &self.pertama
        } else {
            lain
        }
    }
}

fn demo_generic_struct() {
    println!("\n--- GENERIC STRUCT ---");

    let koordinat = Pasangan::new(3, 4);
    println!("  koordinat: {:?}", koordinat);
    println!("  tampilkan: {}", koordinat.tampilkan());

    let campuran = Pasangan::new("umur", 20);
    println!("  campuran: {:?}", campuran);
    println!("  tampilkan: {}", campuran.tampilkan());
    println!("  tukar: {:?}", campuran.tukar());

    let angka = Pasangan::new(10, "sepuluh");
    println!("  terbesar_pertama(&15): {}", angka.terbesar_pertama(&15));
}

// ============================================
// 3. TRAIT: DEFINISI PERILAKU
// ============================================
trait BangunDatar {
    // Method wajib (tanpa implementasi)
    fn nama(&self) -> &'static str;
    fn luas(&self) -> f64;
    fn keliling(&self) -> f64;

    // Default method: memakai method lain dari trait yang sama
    fn ringkasan(&self) -> String {
        format!(
            "{:<10} luas={:>8.2} keliling={:>8.2}",
            self.nama(),
            self.luas(),
            self.keliling()
        )
    }
}

struct Persegi {
    sisi: f64,
}

struct Lingkaran {
    jari_jari: f64,
}

struct Segitiga {
    a: f64,
    b: f64,
    c: f64,
}

impl BangunDatar for Persegi {
    fn nama(&self) -> &'static str {
        "Persegi"
    }

    fn luas(&self) -> f64 {
        self.sisi * self.sisi
    }

    fn keliling(&self) -> f64 {
        4.0 * self.sisi
    }
}

impl BangunDatar for Lingkaran {
    fn nama(&self) -> &'static str {
        "Lingkaran"
    }

    fn luas(&self) -> f64 {
        std::f64::consts::PI * self.jari_jari * self.jari_jari
    }

    fn keliling(&self) -> f64 {
        2.0 * std::f64::consts::PI * self.jari_jari
    }
}

impl BangunDatar for Segitiga {
    fn nama(&self) -> &'static str {
        "Segitiga"
    }

    fn luas(&self) -> f64 {
        // Rumus Heron
        let s = (self.a + self.b + self.c) / 2.0;
        (s * (s - self.a) * (s - self.b) * (s - self.c)).sqrt()
    }

    fn keliling(&self) -> f64 {
        self.a + self.b + self.c
    }

    // Override default method
    fn ringkasan(&self) -> String {
        format!(
            "{:<10} sisi={:.1},{:.1},{:.1} luas={:.2}",
            self.nama(),
            self.a,
            self.b,
            self.c,
            self.luas()
        )
    }
}

// ============================================
// 4. STATIC DISPATCH (GENERIC) vs DYNAMIC DISPATCH (dyn Trait)
// ============================================
// Generic: compiler membuat versi khusus untuk tiap tipe (monomorphization).
fn total_luas<T: BangunDatar>(items: &[T]) -> f64 {
    items.iter().map(|b| b.luas()).sum()
}

// dyn Trait: satu fungsi untuk semua tipe, dipilih saat runtime (vtable).
fn total_luas_dinamis(items: &[Box<dyn BangunDatar>]) -> f64 {
    items.iter().map(|b| b.luas()).sum()
}

fn cetak_semua<T, I>(items: I)
where
    I: IntoIterator<Item = T>,
    T: Display,
{
    for (i, item) in items.into_iter().enumerate() {
        println!("    {}. {}", i + 1, item);
    }
}

fn demo_trait() {
    println!("\n--- TRAIT ---");

    let persegi = Persegi { sisi: 4.0 };
    let lingkaran = Lingkaran { jari_jari: 3.0 };
    let segitiga = Segitiga { a: 3.0, b: 4.0, c: 5.0 };

    println!("  {}", persegi.ringkasan());
    println!("  {}", lingkaran.ringkasan());
    println!("  {}", segitiga.ringkasan());

    // Static dispatch: Vec<Persegi> saja
    let kumpulan_persegi = vec![Persegi { sisi: 2.0 }, Persegi { sisi: 5.0 }];
    println!("  total luas persegi: {:.2}", total_luas(&kumpulan_persegi));

    // Dynamic dispatch: campur berbagai tipe dalam satu Vec
    let campuran: Vec<Box<dyn BangunDatar>> = vec![
        Box::new(Persegi { sisi: 4.0 }),
        Box::new(Lingkaran { jari_jari: 3.0 }),
        Box::new(Segitiga { a: 3.0, b: 4.0, c: 5.0 }),
    ];
    println!("  total luas campuran: {:.2}", total_luas_dinamis(&campuran));

    println!("  cetak_semua:");
    cetak_semua(campuran.iter().map(|b| b.ringkasan()));
}

// ============================================
// 5. TRAIT BOUND & WHERE CLAUSE
// ============================================
fn nilai_maksimum<T>(items: &[T]) -> Option<&T>
where
    T: PartialOrd,
{
    items.iter().max_by(|a, b| a.partial_cmp(b).unwrap())
}

// Beberapa bound sekaligus
fn ulangi<T>(item: T, kali: usize) -> String
where
    T: Display + Clone,
{
    (0..kali)
        .map(|_| item.clone().to_string())
        .collect::<Vec<_>>()
        .join(" | ")
}

fn demo_trait_bound() {
    println!("\n--- TRAIT BOUND ---");

    let angka = [4, 9, 2, 7, 5];
    println!("  nilai_maksimum: {:?}", nilai_maksimum(&angka));

    let kata = ["apel", "mangga", "jeruk"];
    println!("  nilai_maksimum kata: {:?}", nilai_maksimum(&kata));

    println!("  ulangi(\"ha\", 3): {}", ulangi("ha", 3));
}

// ============================================
// 6. ASSOCIATED TYPE
// ============================================
trait Ringkas {
    type Output;

    fn ringkas(&self) -> Self::Output;
}

impl Ringkas for Persegi {
    type Output = String;

    fn ringkas(&self) -> Self::Output {
        format!("persegi({}x{})", self.sisi, self.sisi)
    }
}

impl Ringkas for Pasangan<i32, i32> {
    type Output = i32;

    fn ringkas(&self) -> Self::Output {
        self.pertama + self.kedua
    }
}

fn demo_associated_type() {
    println!("\n--- ASSOCIATED TYPE ---");

    let p = Persegi { sisi: 3.0 };
    println!("  Persegi -> {}", p.ringkas());

    let angka = Pasangan::new(20, 22);
    println!("  Pasangan -> {}", angka.ringkas());
}

// ============================================
// 7. OPERATOR OVERLOADING & DERIVE TRAIT
// ============================================
#[derive(Debug, Clone, Copy, PartialEq, Default)]
struct Titik {
    x: f64,
    y: f64,
}

impl Add for Titik {
    type Output = Titik;

    fn add(self, other: Titik) -> Titik {
        Titik {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Display for Titik {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({:.1}, {:.1})", self.x, self.y)
    }
}

// Derive PartialOrd + Ord agar bisa dibandingkan dan diurutkan
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
struct NilaiUjian {
    nilai: u32,
    nama: String,
}

fn demo_operator_derive() {
    println!("\n--- OPERATOR OVERLOADING & DERIVE ---");

    let a = Titik { x: 1.0, y: 2.0 };
    let b = Titik { x: 3.0, y: 4.0 };
    println!("  {} + {} = {}", a, b, a + b);
    println!("  default: {}", Titik::default());

    let mut daftar = vec![
        NilaiUjian { nilai: 85, nama: "Rina".to_string() },
        NilaiUjian { nilai: 95, nama: "Hayyan".to_string() },
        NilaiUjian { nilai: 90, nama: "Budi".to_string() },
    ];
    daftar.sort(); // urut berdasarkan field pertama (nilai), lalu nama
    for n in &daftar {
        println!("  {}: {}", n.nama, n.nilai);
    }
}

// ============================================
// 8. RETURN impl Trait
// ============================================
fn kuadrat_pertama(n: u32) -> impl Iterator<Item = u32> {
    (1..=n).map(|x| x * x)
}

fn demo_impl_trait() {
    println!("\n--- RETURN impl Trait ---");

    let hasil: Vec<u32> = kuadrat_pertama(5).collect();
    println!("  kuadrat 1..=5: {:?}", hasil);
}

// ============================================
// LATIHAN
// ============================================
fn latihan() {
    println!("\n--- LATIHAN ---");

    // Latihan 1: generic function untuk mencari nilai terkecil
    fn terkecil<T: PartialOrd + Copy>(items: &[T]) -> Option<T> {
        items.iter().copied().reduce(|a, b| if a < b { a } else { b })
    }
    println!("  1. terkecil: {:?}", terkecil(&[7, 3, 9, 1, 5]));

    // Latihan 2: generic struct untuk hasil operasi
    #[derive(Debug)]
    enum Hasil<T, E> {
        Sukses(T),
        Gagal(E),
    }

    fn bagi(a: f64, b: f64) -> Hasil<f64, String> {
        if b == 0.0 {
            Hasil::Gagal("pembagian dengan nol".to_string())
        } else {
            Hasil::Sukses(a / b)
        }
    }
    println!("  2. bagi(10, 2): {:?}", bagi(10.0, 2.0));
    println!("     bagi(10, 0): {:?}", bagi(10.0, 0.0));

    // Latihan 3: trait dengan default method
    trait Suara {
        fn nama(&self) -> &'static str;
        fn suara(&self) -> &'static str {
            "..."
        }
        fn perkenalan(&self) -> String {
            format!("{} bersuara {}", self.nama(), self.suara())
        }
    }

    struct Kucing;
    struct Anjing;

    impl Suara for Kucing {
        fn nama(&self) -> &'static str {
            "Kucing"
        }
        fn suara(&self) -> &'static str {
            "meong"
        }
    }

    impl Suara for Anjing {
        fn nama(&self) -> &'static str {
            "Anjing"
        }
        fn suara(&self) -> &'static str {
            "guk guk"
        }
    }

    println!("  3. {}", Kucing.perkenalan());
    println!("     {}", Anjing.perkenalan());

    // Latihan 4: trait object untuk koleksi campuran
    let hewan: Vec<Box<dyn Suara>> = vec![Box::new(Kucing), Box::new(Anjing)];
    for h in &hewan {
        println!("  4. {}", h.perkenalan());
    }

    // Latihan 5: implement trait Display untuk struct sendiri
    struct Uang(u32);

    impl Display for Uang {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "Rp{},{:03}", self.0 / 1000, self.0 % 1000)
        }
    }
    println!("  5. {}", Uang(250_000));
}

// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO GENERIC & TRAIT RUST");
    println!("{}", "=".repeat(50));

    demo_generic_function();
    demo_generic_struct();
    demo_trait();
    demo_trait_bound();
    demo_associated_type();
    demo_operator_derive();
    demo_impl_trait();
    latihan();

    println!("\n=== SELESAI ===");
}
