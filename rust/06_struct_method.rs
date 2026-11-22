// Materi 06: Struct & Method Implementation
// Penjelasan: Struct = custom data type yang mengelompokkan field terkait.
// impl block = tempat mendefinisikan method & associated function untuk struct.

use std::fmt;

// ============================================
// 1. STRUCT DASAR
// ============================================
#[derive(Debug, Clone, PartialEq)]
struct Mahasiswa {
    nama: String,
    nim: String,
    jurusan: String,
    ipk: f32,
    aktif: bool,
}

// Tuple struct (mirip tuple tapi punya nama)
#[derive(Debug, Clone, PartialEq)]
struct Titik2D(f64, f64);

#[derive(Debug, Clone, PartialEq)]
struct WarnaRGB(u8, u8, u8);

// Unit struct (tidak punya field, seperti marker)
#[derive(Debug, Clone, PartialEq)]
struct Marker;


// ============================================
// 2. IMPLEMENTASI METHOD & ASSOCIATED FUNCTION
// ============================================
impl Mahasiswa {
    // Associated function (static method) - tidak butuh &self
    fn baru(nama: &str, nim: &str, jurusan: &str) -> Self {
        Self {
            nama: nama.to_string(),
            nim: nim.to_string(),
            jurusan: jurusan.to_string(),
            ipk: 0.0,
            aktif: true,
        }
    }

    // Factory method dengan validasi
    fn dengan_ipk(nama: &str, nim: &str, jurusan: &str, ipk: f32) -> Result<Self, String> {
        if !(0.0..=4.0).contains(&ipk) {
            return Err(format!("IPK tidak valid: {} (harus 0.0-4.0)", ipk));
        }
        Ok(Self {
            nama: nama.to_string(),
            nim: nim.to_string(),
            jurusan: jurusan.to_string(),
            ipk,
            aktif: true,
        })
    }

    // Method immutable borrow (&self) - read only
    fn perkenalkan(&self) -> String {
        format!("Halo, saya {} ({}) dari {}", self.nama, self.nim, self.jurusan)
    }

    fn info_lengkap(&self) -> String {
        format!(
            "Mahasiswa: {} | NIM: {} | Jurusan: {} | IPK: {:.2} | Status: {}",
            self.nama,
            self.nim,
            self.jurusan,
            self.ipk,
            if self.aktif { "Aktif" } else { "Non-aktif" }
        )
    }

    // Method mutable borrow (&mut self) - bisa modify
    fn set_ipk(&mut self, ipk_baru: f32) -> Result<(), String> {
        if !(0.0..=4.0).contains(&ipk_baru) {
            return Err("IPK harus 0.0-4.0".to_string());
        }
        self.ipk = ipk_baru;
        Ok(())
    }

    fn nonaktifkan(&mut self) {
        self.aktif = false;
    }

    // Method yang consume self (move ownership) - langka, untuk builder pattern
    fn upgrade_jurusan(self, jurusan_baru: String) -> Self {
        Self {
            jurusan: jurusan_baru,
            ..self
        }
    }

    // Method dengan generic parameter
    fn bandingkan_ipk<T: HasIpk>(&self, other: &T) -> bool {
        self.ipk > other.ipk()
    }
}

// Trait untuk generic method di atas
trait HasIpk {
    fn ipk(&self) -> f32;
}

impl HasIpk for Mahasiswa {
    fn ipk(&self) -> f32 {
        self.ipk
    }
}


// ============================================
// 3. IMPL UNTUK TUPLE STRUCT
// ============================================
impl Titik2D {
    fn baru(x: f64, y: f64) -> Self {
        Self(x, y)
    }

    fn jarak_dari_origin(&self) -> f64 {
        (self.0.powi(2) + self.1.powi(2)).sqrt()
    }

    fn geser(&mut self, dx: f64, dy: f64) {
        self.0 += dx;
        self.1 += dy;
    }

    // Associated function (static)
    fn origin() -> Self {
        Self(0.0, 0.0)
    }
}

impl WarnaRGB {
    fn hex(&self) -> String {
        format!("#{:02X}{:02X}{:02X}", self.0, self.1, self.2)
    }

    fn grayscale(&self) -> u8 {
        // Formula luminance
        (0.299 * self.0 as f32 + 0.587 * self.1 as f32 + 0.114 * self.2 as f32) as u8
    }
}


// ============================================
// 4. TRAIT IMPL UNTUK STRUCT (Polymorphism)
// ============================================
trait CetakInfo {
    fn cetak(&self);
    fn tipe(&self) -> &'static str;
}

impl CetakInfo for Mahasiswa {
    fn cetak(&self) {
        println!("  [{}] {}", self.tipe(), self.info_lengkap());
    }

    fn tipe(&self) -> &'static str {
        "Mahasiswa"
    }
}

impl CetakInfo for Titik2D {
    fn cetak(&self) {
        println!("  [{}] ({}, {}) - jarak: {:.2}", self.tipe(), self.0, self.1, self.jarak_dari_origin());
    }

    fn tipe(&self) -> &'static str {
        "Titik2D"
    }
}


// ============================================
// 5. BUILDER PATTERN
// ============================================
#[derive(Default)]
struct MahasiswaBuilder {
    nama: Option<String>,
    nim: Option<String>,
    jurusan: Option<String>,
    ipk: Option<f32>,
}

impl MahasiswaBuilder {
    fn new() -> Self {
        Self::default()
    }

    fn nama(mut self, nama: &str) -> Self {
        self.nama = Some(nama.to_string());
        self
    }

    fn nim(mut self, nim: &str) -> Self {
        self.nim = Some(nim.to_string());
        self
    }

    fn jurusan(mut self, jurusan: &str) -> Self {
        self.jurusan = Some(jurusan.to_string());
        self
    }

    fn ipk(mut self, ipk: f32) -> Self {
        self.ipk = Some(ipk);
        self
    }

    fn build(self) -> Result<Mahasiswa, String> {
        Ok(Mahasiswa {
            nama: self.nama.ok_or("Nama wajib")?,
            nim: self.nim.ok_or("NIM wajib")?,
            jurusan: self.jurusan.ok_or("Jurusan wajib")?,
            ipk: self.ipk.unwrap_or(0.0),
            aktif: true,
        })
    }
}


// ============================================
// 6. DERIVE MACRO & CUSTOM DEBUG
// ============================================
#[derive(Debug)]
struct DenganDerive {
    x: i32,
    y: String,
}

struct TanpaDerive {
    x: i32,
    y: String,
}

impl fmt::Debug for TanpaDerive {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("TanpaDerive")
            .field("x", &self.x)
            .field("y", &self.y)
            .finish()
    }
}


// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO STRUCT & METHOD IMPL RUST");
    println!("{}", "=".repeat(50));

    // 1. Struct dasar
    println!("\n--- STRUCT DASAR ---");
    let mhs1 = Mahasiswa::baru("Hayyan", "2021001", "Informatika");
    println!("{}", mhs1.perkenalkan());

    // 2. Factory dengan validasi
    println!("\n--- FACTORY DENGAN VALIDASI ---");
    match Mahasiswa::dengan_ipk("Rina", "2021002", "SI", 3.85) {
        Ok(m) => println!("Berhasil: {}", m.info_lengkap()),
        Err(e) => println!("Error: {}", e),
    }
    match Mahasiswa::dengan_ipk("Budi", "2021003", "TI", 5.0) {
        Ok(m) => println!("Berhasil: {}", m.info_lengkap()),
        Err(e) => println!("Error (seharusnya): {}", e),
    }

    // 3. Mutable method
    println!("\n--- MUTABLE METHOD ---");
    let mut mhs2 = Mahasiswa::baru("Sari", "2021004", "Informatika");
    println!("Sebelum: IPK = {:.2}", mhs2.ipk);
    mhs2.set_ipk(3.95).unwrap();
    println!("Sesudah: IPK = {:.2}", mhs2.ipk);
    mhs2.nonaktifkan();
    println!("Status setelah nonaktifkan: {}", if mhs2.aktif { "Aktif" } else { "Non-aktif" });

    // 4. Consuming method (move)
    println!("\n--- CONSUMING METHOD (MOVE) ---");
    let mhs3 = Mahasiswa::baru("Joko", "2021005", "Sistem Informasi");
    let mhs3_upgraded = mhs3.upgrade_jurusan("Teknik Informatika".to_string());
    println!("Jurusan baru: {}", mhs3_upgraded.jurusan);
    // mhs3 tidak bisa dipakai lagi (moved)

    // 5. Tuple struct
    println!("\n--- TUPLE STRUCT ---");
    let p1 = Titik2D::baru(3.0, 4.0);
    println!("Titik: {:?}", p1);
    println!("Jarak dari origin: {:.2}", p1.jarak_dari_origin());

    let mut p2 = Titik2D::origin();
    println!("Origin: {:?}", p2);
    p2.geser(1.0, 1.0);
    println!("Setelah geser: {:?}", p2);

    // 6. WarnaRGB
    println!("\n--- WARNA RGB ---");
    let merah = WarnaRGB(255, 0, 0);
    println!("Merah: {} (hex), Grayscale: {}", merah.hex(), merah.grayscale());

    // 7. Trait polymorphism
    println!("\n--- TRAIT POLYMORPHISM ---");
    let items: Vec<Box<dyn CetakInfo>> = vec![
        Box::new(Mahasiswa::baru("A", "1", "IT")),
        Box::new(Titik2D(1.0, 1.0)),
    ];
    for item in &items {
        item.cetak();
    }

    // 8. Builder pattern
    println!("\n--- BUILDER PATTERN ---");
    let mhs_builder = MahasiswaBuilder::new()
        .nama("Builder")
        .nim("999")
        .jurusan("Builder Jurusan")
        .ipk(4.0)
        .build();
    match mhs_builder {
        Ok(m) => println!("Built: {}", m.info_lengkap()),
        Err(e) => println!("Build error: {}", e),
    }

    // 9. Generic method dengan trait bound
    println!("\n--- GENERIC METHOD ---");
    let mhs_a = Mahasiswa::dengan_ipk("A", "1", "IT", 3.5).unwrap();
    let mhs_b = Mahasiswa::dengan_ipk("B", "2", "IT", 3.8).unwrap();
    println!("mhs_a > mhs_b IPK? {}", mhs_a.bandingkan_ipk(&mhs_b));

    // 10. Debug derive vs manual
    println!("\n--- DEBUG DERIVE VS MANUAL ---");
    let d1 = DenganDerive { x: 1, y: "hello".to_string() };
    let d2 = TanpaDerive { x: 2, y: "world".to_string() };
    println!("Field d1: x={}, y={}", d1.x, d1.y);
    println!("Derive: {:?}", d1);
    println!("Manual: {:?}", d2);

    // 11. Unit struct
    println!("\n--- UNIT STRUCT ---");
    let m = Marker;
    println!("Marker: {:?}", m);

    println!("\n=== SELESAI ===");
}