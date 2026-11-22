// Materi 07: Enum & Pattern Matching
// Penjelasan: Enum = tipe data yang bisa memiliki beberapa varian.
// match = ekspresi pattern matching yang exhaustive (harus cover semua kasus).

// ============================================
// 1. ENUM DASAR
// ============================================
#[derive(Debug, Clone, PartialEq)]
enum StatusMahasiswa {
    Aktif,
    Cuti,
    Lulus,
    DropOut,
}

#[derive(Debug, Clone, PartialEq)]
enum Jurusan {
    Informatika,
    SistemInformasi,
    TeknikInformatika,
    IlmuKomputer,
    Lainnya(String),  // Varian dengan data
}

// Enum dengan data pada setiap varian
#[derive(Debug, Clone, PartialEq)]
enum Nilai {
    Huruf(char),           // A, B, C, D, E
    Angka(f32),            // 0.0 - 100.0
    PassFail(bool),        // true = Pass, false = Fail
    Detail { skor: u32, max: u32 },  // Struct-like variant
}

// Enum recursive (butuh Box untuk ukuran tidak terbatas)
#[derive(Debug, Clone, PartialEq)]
enum List<T> {
    Kosong,
    Kons(T, Box<List<T>>),
}


// ============================================
// 2. PATTERN MATCHING DASAR
// ============================================
fn cek_status(status: &StatusMahasiswa) -> &'static str {
    match status {
        StatusMahasiswa::Aktif => "Sedang belajar",
        StatusMahasiswa::Cuti => "Sementara berhenti",
        StatusMahasiswa::Lulus => "Sudah lulus",
        StatusMahasiswa::DropOut => "Keluar tanpa lulus",
    }
}

fn deskripsi_jurusan(jurusan: &Jurusan) -> String {
    match jurusan {
        Jurusan::Informatika => "IF - Fokus pemrograman & algoritma".to_string(),
        Jurusan::SistemInformasi => "SI - Fokus sistem & bisnis".to_string(),
        Jurusan::TeknikInformatika => "TI - Fokus hardware & software".to_string(),
        Jurusan::IlmuKomputer => "IK - Fokus teori & riset".to_string(),
        Jurusan::Lainnya(nama) => format!("Lainnya: {}", nama),
    }
}


// ============================================
// 3. MATCH DENGAN DATA (DESTRUCTURING)
// ============================================
fn konversi_nilai(nilai: Nilai) -> String {
    match nilai {
        Nilai::Huruf(h) => format!("Grade: {}", h),
        Nilai::Angka(a) => {
            let grade = if a >= 90.0 { 'A' }
                        else if a >= 80.0 { 'B' }
                        else if a >= 70.0 { 'C' }
                        else if a >= 60.0 { 'D' }
                        else { 'E' };
            format!("Skor: {:.1} -> Grade: {}", a, grade)
        }
        Nilai::PassFail(passed) => {
            if passed { "Lulus".to_string() } else { "Tidak Lulus".to_string() }
        }
        Nilai::Detail { skor, max } => {
            let persen = (skor as f32 / max as f32) * 100.0;
            format!("Detail: {}/{} ({:.1}%)", skor, max, persen)
        }
    }
}


// ============================================
// 4. MATCH GUARD (if di match arm)
// ============================================
fn kategori_umur(umur: u8) -> &'static str {
    match umur {
        0..=12 if umur < 5 => "Balita",
        0..=12 => "Anak-anak",
        13..=17 => "Remaja",
        18..=59 => "Dewasa",
        60..=u8::MAX => "Lansia",
    }
}

fn proses_nilai_dengan_guard(nilai: Nilai) -> String {
    match nilai {
        Nilai::Angka(n) if n >= 85.0 => "Excellent".to_string(),
        Nilai::Angka(n) if n >= 70.0 => "Good".to_string(),
        Nilai::Angka(n) if n >= 50.0 => "Average".to_string(),
        Nilai::Angka(_) => "Perlu perbaikan".to_string(),
        _ => "Format tidak dikenali".to_string(),
    }
}


// ============================================
// 5. MATCH BINDING (@) - Bind value while matching
// ============================================
fn match_dengan_at(nilai: Nilai) -> String {
    match nilai {
        Nilai::Angka(n @ 0.0..=50.0) => format!("Rendah: {}", n),
        Nilai::Angka(n @ 50.0..=100.0) => format!("Tinggi: {}", n),
        Nilai::Detail { skor: s @ 0..=50, .. } => format!("Skor rendah: {}", s),
        _ => "Lainnya".to_string(),
    }
}


// ============================================
// 6. MATCH PADA REFERENCE (& / &mut)
// ============================================
fn match_ref(nilai: &Nilai) -> String {
    match nilai {
        &Nilai::Huruf(h) => format!("Ref Huruf: {}", h),
        &Nilai::Angka(a) => format!("Ref Angka: {}", a),
        _ => "Ref Lainnya".to_string(),
    }
}

fn match_mut_ref(nilai: &mut Nilai) {
    match nilai {
        Nilai::Angka(ref mut a) => *a += 5.0,  // Mutate through reference
        _ => {}
    }
}


// ============================================
// 7. IF LET & WHILE LET (Syntactic sugar untuk match single pattern)
// ============================================
fn demo_if_let() {
    let nilai = Nilai::Angka(85.0);

    // if let: match satu pattern, ignore lain
    if let Nilai::Angka(n) = nilai {
        println!("  if let: Nilai angka = {}", n);
    }

    // while let: loop sampai pattern tidak match
    let mut stack = vec![
        Nilai::Huruf('A'),
        Nilai::Angka(90.0),
        Nilai::PassFail(true),
    ];

    while let Some(Nilai::Angka(n)) = stack.pop() {
        println!("  while let pop angka: {}", n);
    }
}


// ============================================
// 8. ENUM METHOD (impl pada enum)
// ============================================
impl Nilai {
    fn to_angka(&self) -> Option<f32> {
        match self {
            Nilai::Angka(n) => Some(*n),
            Nilai::Huruf(h) => Some(match h {
                'A' => 95.0, 'B' => 85.0, 'C' => 75.0, 'D' => 65.0, _ => 50.0,
            }),
            Nilai::PassFail(p) => Some(if *p { 80.0 } else { 40.0 }),
            Nilai::Detail { skor, max } => Some(*skor as f32 / *max as f32 * 100.0),
        }
    }

    fn is_lulus(&self) -> bool {
        self.to_angka().map_or(false, |n| n >= 60.0)
    }

    fn deskripsi(&self) -> String {
        match self {
            Nilai::Huruf(h) => format!("Grade {}", h),
            Nilai::Angka(n) => format!("Skor {:.1}", n),
            Nilai::PassFail(p) => format!("{}", if *p { "Pass" } else { "Fail" }),
            Nilai::Detail { skor, max } => format!("{}/{}", skor, max),
        }
    }
}


// ============================================
// 9. OPTION & RESULT SEBAGAI ENUM (Built-in)
// ============================================
fn demo_option_result() {
    println!("\n--- OPTION & RESULT ---");

    // Option<T>: Some(T) | None
    let ada: Option<i32> = Some(42);
    let tidak_ada: Option<i32> = None;

    // Pattern matching Option
    match ada {
        Some(n) => println!("  Some: {}", n),
        None => println!("  None"),
    }

    // if let untuk Option
    if let Some(n) = tidak_ada {
        println!("  Ada: {}", n);
    } else {
        println!("  Kosong (None)");
    }

    // Method Option
    println!("  unwrap_or: {}", tidak_ada.unwrap_or(0));
    println!("  map: {:?}", ada.map(|x| x * 2));
    println!("  and_then: {:?}", ada.and_then(|x| if x > 10 { Some(x / 2) } else { None }));

    // Result<T, E>: Ok(T) | Err(E)
    let ok: Result<i32, &str> = Ok(100);
    let err: Result<i32, &str> = Err("Something went wrong");

    match ok {
        Ok(v) => println!("  Ok: {}", v),
        Err(e) => println!("  Err: {}", e),
    }

    match err {
        Ok(v) => println!("  Ok: {}", v),
        Err(e) => println!("  Err (seharusnya): {}", e),
    }

    // Operator ? (hanya di fungsi yang return Result/Option)
    fn bagi(a: f64, b: f64) -> Result<f64, String> {
        if b == 0.0 {
            Err("Pembagian dengan nol".to_string())
        } else {
            Ok(a / b)
        }
    }

    let hasil = bagi(10.0, 2.0);
    println!("  bagi(10, 2) = {:?}", hasil);

    // Chaining dengan ? (butuh fungsi yang return Result)
    fn hitung(a: f64, b: f64, c: f64) -> Result<f64, String> {
        let x = bagi(a, b)?;
        let y = bagi(x, c)?;
        Ok(y)
    }
    println!("  hitung(100, 2, 5) = {:?}", hitung(100.0, 2.0, 5.0));
}


// ============================================
// 10. ENUM REKURSIF (List, Tree)
// ============================================
impl<T> List<T> {
    fn baru() -> Self {
        List::Kosong
    }

    fn prepend(self, val: T) -> Self {
        List::Kons(val, Box::new(self))
    }

    fn len(&self) -> usize {
        match self {
            List::Kosong => 0,
            List::Kons(_, tail) => 1 + tail.len(),
        }
    }

    fn to_vec(&self) -> Vec<&T> {
        let mut v = Vec::new();
        let mut current = self;
        while let List::Kons(head, tail) = current {
            v.push(head);
            current = tail;
        }
        v
    }
}


// ============================================
// 11. MATCH EXHAUSTIVENESS (Compiler memastikan semua kasus tertangani)
// ============================================
fn exhaustive_match(status: StatusMahasiswa) {
    match status {
        StatusMahasiswa::Aktif => println!("  Aktif"),
        StatusMahasiswa::Cuti => println!("  Cuti"),
        StatusMahasiswa::Lulus => println!("  Lulus"),
        StatusMahasiswa::DropOut => println!("  DropOut"),
        // Jika varian baru ditambah ke enum, ini akan error compile!
    }
}


// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO ENUM & PATTERN MATCHING RUST");
    println!("{}", "=".repeat(50));

    // 1. Enum dasar
    println!("\n--- ENUM DASAR ---");
    for status in [
        StatusMahasiswa::Aktif,
        StatusMahasiswa::Cuti,
        StatusMahasiswa::Lulus,
        StatusMahasiswa::DropOut,
    ] {
        println!("Status: {:?} -> {}", status, cek_status(&status));
    }

    for jurusan in [
        Jurusan::Informatika,
        Jurusan::SistemInformasi,
        Jurusan::TeknikInformatika,
        Jurusan::IlmuKomputer,
        Jurusan::Lainnya("Bisnis Digital".to_string()),
    ] {
        println!("Jurusan: {:?} -> {}", jurusan, deskripsi_jurusan(&jurusan));
    }

    // 2. Enum dengan data
    println!("\n--- ENUM DENGAN DATA ---");
    let nilai_list = vec![
        Nilai::Huruf('A'),
        Nilai::Angka(87.5),
        Nilai::PassFail(true),
        Nilai::Detail { skor: 85, max: 100 },
    ];

    for n in &nilai_list {
        println!("  {:?} -> {}", n, konversi_nilai(n.clone()));
    }

    // 3. Match guard
    println!("\n--- MATCH GUARD ---");
    for umur in [3, 10, 15, 25, 65] {
        println!("  Umur {} -> {}", umur, kategori_umur(umur));
    }

    for n in &nilai_list {
        println!("  Guard: {:?} -> {}", n, proses_nilai_dengan_guard(n.clone()));
    }

    // 4. Match binding (@)
    println!("\n--- MATCH BINDING (@) ---");
    for n in &nilai_list {
        println!("  @: {:?} -> {}", n, match_dengan_at(n.clone()));
    }

    // 5. Match reference
    println!("\n--- MATCH REFERENCE ---");
    for n in &nilai_list {
        println!("  Ref: {}", match_ref(n));
    }

    let mut n_mut = Nilai::Angka(50.0);
    println!("  Sebelum mut: {:?}", n_mut);
    match_mut_ref(&mut n_mut);
    println!("  Sesudah mut: {:?}", n_mut);

    // 6. If let & while let
    println!("\n--- IF LET & WHILE LET ---");
    demo_if_let();

    // 7. Enum method
    println!("\n--- ENUM METHOD ---");
    for n in &nilai_list {
        println!("  {:?} -> to_angka: {:?}, lulus: {}, desc: {}",
                 n, n.to_angka(), n.is_lulus(), n.deskripsi());
    }

    // 8. Option & Result
    demo_option_result();

    // 9. Recursive enum
    println!("\n--- RECURSIVE ENUM (List) ---");
    let kosong: List<i32> = List::baru();
    println!("  List kosong: {:?}, len: {}", kosong, kosong.len());
    let list = List::Kosong
        .prepend(3)
        .prepend(2)
        .prepend(1);
    println!("  List: {:?}", list);
    println!("  Len: {}", list.len());
    println!("  To vec: {:?}", list.to_vec());

    // 10. Exhaustiveness
    println!("\n--- EXHAUSTIVE MATCH ---");
    exhaustive_match(StatusMahasiswa::Lulus);

    println!("\n=== SELESAI ===");
}