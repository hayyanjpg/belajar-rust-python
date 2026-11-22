// Materi 08: Error Handling - Result, Option, ? Operator, Custom Error
// Penjelasan: Rust tidak punya exception. Gunakan Result<T, E> untuk operasi yg bisa gagal,
// dan Option<T> untuk nilai yg mungkin tidak ada. Operator ? = early return error.

use std::fmt;
use std::error::Error;
use std::fs::File;
use std::io::{self, Read, Write};
use std::num::ParseIntError;

// ============================================
// 1. OPTION<T> - Nilai yang mungkin tidak ada
// ============================================
fn cari_indeks(haystack: &[i32], needle: i32) -> Option<usize> {
    for (i, &v) in haystack.iter().enumerate() {
        if v == needle {
            return Some(i);
        }
    }
    None
}

fn demo_option() {
    println!("\n--- OPTION<T> ---");
    let data = vec![10, 20, 30, 40, 50];

    match cari_indeks(&data, 30) {
        Some(idx) => println!("  Ditemukan di index: {}", idx),
        None => println!("  Tidak ditemukan"),
    }

    // Method Option
    let hasil = cari_indeks(&data, 99);
    println!("  unwrap_or: {}", hasil.unwrap_or(0));
    println!("  unwrap_or_else: {}", hasil.unwrap_or_else(|| data.len()));
    println!("  map: {:?}", hasil.map(|i| i * 2));
    println!("  and_then: {:?}", hasil.and_then(|i| if i > 2 { Some(i) } else { None }));
    println!("  or: {:?}", hasil.or(Some(999)));
    println!("  is_some: {}, is_none: {}", hasil.is_some(), hasil.is_none());

    // Expect & unwrap (panic jika None - HANYA untuk testing/prototyping)
    // println!("{}", hasil.expect("Harus ada")); // PANIC!
    // println!("{}", hasil.unwrap()); // PANIC!
}

// ============================================
// 2. RESULT<T, E> - Operasi yang bisa gagal
// ============================================
fn bagi(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Pembagian dengan nol".to_string())
    } else {
        Ok(a / b)
    }
}

fn parse_int(s: &str) -> Result<i32, ParseIntError> {
    s.parse::<i32>()
}

fn demo_result() {
    println!("\n--- RESULT<T, E> ---");

    match bagi(10.0, 2.0) {
        Ok(v) => println!("  10/2 = {}", v),
        Err(e) => println!("  Error: {}", e),
    }

    match bagi(10.0, 0.0) {
        Ok(v) => println!("  10/0 = {}", v),
        Err(e) => println!("  Error (seharusnya): {}", e),
    }

    // Method Result
    let ok: Result<i32, &str> = Ok(42);
    let err: Result<i32, &str> = Err("Gagal");

    println!("  ok.unwrap_or(0): {}", ok.unwrap_or(0));
    println!("  err.unwrap_or(0): {}", err.unwrap_or(0));
    println!("  ok.map(|x| x*2): {:?}", ok.map(|x| x * 2));
    println!("  err.map(|x| x*2): {:?}", err.map(|x| x * 2));
    println!("  ok.and_then: {:?}", ok.and_then(|x| if x > 10 { Ok(x / 2) } else { Err("kecil") }));
    println!("  err.or_else: {:?}", err.or_else(|_| Ok(999)));

    // Parse int
    match parse_int("123") {
        Ok(n) => println!("  Parse '123' = {}", n),
        Err(e) => println!("  Error: {}", e),
    }
    match parse_int("abc") {
        Ok(n) => println!("  Parse 'abc' = {}", n),
        Err(e) => println!("  Error (seharusnya): {}", e),
    }
}

// ============================================
// 3. OPERATOR ? (Question Mark) - Early Return
// ============================================
fn baca_file_ke_string(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // Return Err jika gagal
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;  // Return Err jika gagal
    Ok(contents)
}

fn parse_dan_kali(s: &str) -> Result<i32, ParseIntError> {
    let n: i32 = s.parse()?;  // Auto-convert ParseIntError ke Result error
    Ok(n * 2)
}

// Fungsi yang memakai ? bertipe Result
fn hitung_total(file_path: &str) -> Result<i32, Box<dyn Error>> {
    let content = baca_file_ke_string(file_path)?;
    let numbers: Result<Vec<i32>, _> = content
        .lines()
        .map(|line| line.trim().parse::<i32>())
        .collect();
    let sum: i32 = numbers?.iter().sum();
    Ok(sum)
}

fn demo_question_mark() {
    println!("\n--- OPERATOR ? ---");

    // Buat file dummy
    let test_file = "test_numbers.txt";
    std::fs::write(test_file, "10\n20\n30\n").ok();

    match hitung_total(test_file) {
        Ok(sum) => println!("  Total dari file: {}", sum),
        Err(e) => println!("  Error: {}", e),
    }

    // Parse dengan ?
    match parse_dan_kali("21") {
        Ok(v) => println!("  parse_dan_kali('21') = {}", v),
        Err(e) => println!("  Error: {}", e),
    }
    match parse_dan_kali("abc") {
        Ok(v) => println!("  parse_dan_kali('abc') = {}", v),
        Err(e) => println!("  Error (seharusnya): {}", e),
    }

    // Bersihkan
    std::fs::remove_file(test_file).ok();
}

// ============================================
// 4. CUSTOM ERROR TYPE
// ============================================
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(ParseIntError),
    Validasi(String),
    TidakDitemukan(String),
}

// Implement Display untuk user-facing error
impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::Io(e) => write!(f, "I/O error: {}", e),
            AppError::Parse(e) => write!(f, "Parse error: {}", e),
            AppError::Validasi(msg) => write!(f, "Validasi gagal: {}", msg),
            AppError::TidakDitemukan(item) => write!(f, "Tidak ditemukan: {}", item),
        }
    }
}

// Implement Error trait (butuh Debug + Display)
impl Error for AppError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            AppError::Io(e) => Some(e),
            AppError::Parse(e) => Some(e),
            _ => None,
        }
    }
}

// From trait untuk konversi otomatis dengan ?
impl From<io::Error> for AppError {
    fn from(err: io::Error) -> Self {
        AppError::Io(err)
    }
}

impl From<ParseIntError> for AppError {
    fn from(err: ParseIntError) -> Self {
        AppError::Parse(err)
    }
}

// Fungsi yang return custom error
fn proses_data_custom(input: &str) -> Result<i32, AppError> {
    if input.is_empty() {
        return Err(AppError::Validasi("Input kosong".to_string()));
    }

    let n: i32 = input.parse()?;  // Auto-convert via From<ParseIntError>

    if n < 0 {
        return Err(AppError::Validasi("Angka harus positif".to_string()));
    }

    if n > 100 {
        return Err(AppError::TidakDitemukan(format!("Angka > 100: {}", n)));
    }

    Ok(n * 2)
}

fn demo_custom_error() {
    println!("\n--- CUSTOM ERROR ---");

    let test_cases = ["", "50", "-5", "150", "abc"];
    for tc in test_cases {
        match proses_data_custom(tc) {
            Ok(v) => println!("  '{}' -> OK: {}", tc, v),
            Err(e) => println!("  '{}' -> Error: {}", tc, e),
        }
    }

    // Error chaining dengan source()
    let err = proses_data_custom("abc").unwrap_err();
    println!("  Error: {}", err);
    if let Some(src) = err.source() {
        println!("  Source: {}", src);
    }
}

// ============================================
// 5. RESULT COMBINATORS (map, and_then, or_else, map_err)
// ============================================
fn demo_combinators() {
    println!("\n--- RESULT COMBINATORS ---");

    let ok: Result<i32, &str> = Ok(10);
    let err: Result<i32, &str> = Err("error");

    // map: transform Ok value
    println!("  ok.map(|x| x*2): {:?}", ok.map(|x| x * 2));
    println!("  err.map(|x| x*2): {:?}", err.map(|x| x * 2));

    // map_err: transform Err value
    println!("  ok.map_err(|e| e.len()): {:?}", ok.map_err(|e| e.len()));
    println!("  err.map_err(|e| e.len()): {:?}", err.map_err(|e| e.len()));

    // and_then: chain operations that return Result
    fn safe_div(a: i32, b: i32) -> Result<i32, &str> {
        if b == 0 { Err("div by zero") } else { Ok(a / b) }
    }
    println!("  ok.and_then(|x| safe_div(x,2)): {:?}", ok.and_then(|x| safe_div(x, 2)));
    println!("  ok.and_then(|x| safe_div(x,0)): {:?}", ok.and_then(|x| safe_div(x, 0)));

    // or_else: recovery from error
    println!("  err.or_else(|_| Ok(999)): {:?}", err.or_else(|_| Ok(999)));

    // unwrap_or / unwrap_or_else
    println!("  err.unwrap_or(0): {}", err.unwrap_or(0));
    println!("  err.unwrap_or_else(|e| e.len()): {}", err.unwrap_or_else(|e| e.len()));
}

// ============================================
// 6. PANIC vs RESULT - Kapan gunakan mana?
// ============================================
fn demo_panic_vs_result() {
    println!("\n--- PANIC vs RESULT ---");

    // Gunakan Result untuk error yang DAPAT DIRECOVER (expected failures)
    fn bagi_aman(a: i32, b: i32) -> Result<i32, String> {
        if b == 0 {
            Err("Div by zero".to_string())
        } else {
            Ok(a / b)
        }
    }

    // Gunakan panic! untuk BUG / invariant violation (unrecoverable)
    fn get_first(items: &[i32]) -> i32 {
        // Precondition: slice tidak kosong - ini BUG kalau kosong
        items.first().copied().expect("Slice tidak boleh kosong - ini bug programmer")
    }

    println!("  bagi_aman(10, 2): {:?}", bagi_aman(10, 2));
    println!("  bagi_aman(10, 0): {:?}", bagi_aman(10, 0));
    println!("  get_first(&[1,2,3]): {}", get_first(&[1, 2, 3]));
    // get_first(&[]); // PANIC! - ini bug, bukan error yang diharapkan
}

// ==========================================--
// 7. TRY FROM / TRY INTO (Fallible Conversion)
// ============================================
fn demo_try_from() {
    println!("\n--- TRY FROM / TRY INTO ---");

    let besar: i64 = 1000;
    let kecil: i8 = match kecil.try_from(besar) {
        Ok(v) => v,
        Err(e) => {
            println!("  Konversi i64->i8 gagal: {}", e);
            0
        }
    };

    let ok: i8 = 50;
    match i16::try_from(ok) {
        Ok(v) => println!("  i8->i16 OK: {}", v),
        Err(e) => println!("  Error: {}", e),
    }
}

// ============================================
// 8. ANYHOW / THISERROR (External Crates - Demo Konsep)
// ============================================
// Catatan: Di project nyata, gunakan crate `thiserror` untuk custom error
// dan `anyhow` untuk application error handling.
// Contoh konsep (tanpa dependency eksternal):

#[derive(Debug)]
struct MyError {
    msg: String,
}

impl fmt::Display for MyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "MyError: {}", self.msg)
    }
}

impl Error for MyError {}

fn fungsi_dengan_anyhow_konsep() -> Result<String, MyError> {
    // anyhow::Context::context() menambah konteks ke error
    let data = std::fs::read_to_string("tidak_ada.txt")
        .map_err(|e| MyError { msg: format!("Gagal baca file: {}", e) })?;

    Ok(data)
}

fn demo_external_crates_konsep() {
    println!("\n--- EXTERNAL CRATES KONSEP (thiserror/anyhow) ---");
    match fungsi_dengan_anyhow_konsep() {
        Ok(s) => println!("  OK: {} chars", s.len()),
        Err(e) => println!("  Error (konsep anyhow): {}", e),
    }
}

// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO ERROR HANDLING RUST: RESULT, OPTION, ?, CUSTOM ERROR");
    println!("{}", "=".repeat(50));

    demo_option();
    demo_result();
    demo_question_mark();
    demo_custom_error();
    demo_combinators();
    demo_panic_vs_result();
    demo_try_from();
    demo_external_crates_konsep();

    println!("\n=== SELESAI ===");
}