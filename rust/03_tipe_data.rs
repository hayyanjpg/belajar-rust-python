// Materi 03: Tipe Data Dasar

fn main() {
    // Integer bertipe data eksplisit
    let angka_int: i32 = 42;
    let angka_u32: u32 = 100;
    let besar: i64 = 9_000_000_000;
    let kecil: u8 = 255;
    println!("i32 = {}, u32 = {}, i64 = {}, u8 = {}", angka_int, angka_u32, besar, kecil);

    // Float
    let pi: f64 = 3.14159;
    let suhu: f32 = 36.6;
    println!("f64 = {}, f32 = {}", pi, suhu);

    // Boolean
    let aktif: bool = true;
    let nonaktif: bool = false;
    println!("aktif = {}, nonaktif = {}", aktif, nonaktif);

    // Karakter (selalu 4 byte, unicode scalar value)
    let huruf: char = 'A';
    let emoji: char = '🦀';
    println!("char = {}, char emoji = {}", huruf, emoji);

    // Tuple
    let orang: (&str, i32, f64) = ("Hayyan", 20, 170.5);
    println!("Nama = {}, Umur = {}, Tinggi = {}", orang.0, orang.1, orang.2);
    let (nama, umur, tinggi) = orang;
    println!("Destructuring: {} | {} | {}", nama, umur, tinggi);

    // Array (ukuran tetap)
    let angka_arr: [i32; 5] = [1, 2, 3, 4, 5];
    println!("Array = {:?}", angka_arr);
    println!("Panjang array = {}", angka_arr.len());

    let nol = [0; 3];
    println!("Array berisi nol = {:?}", nol);

    // Slice
    let slice: &[i32] = &angka_arr[1..4];
    println!("Slice = {:?}", slice);

    // Operasi aritmatika dengan tipe berbeda (perlu casting)
    let total: i32 = angka_u32 as i32 + angka_int;
    println!("Casting u32 -> i32, total = {}", total);

    // Operator perbandingan dan logika
    println!("5 > 3          = {}", 5 > 3);
    println!("5 == 5         = {}", 5 == 5);
    println!("true && false  = {}", true && false);
    println!("true || false  = {}", true || false);
    println!("!true          = {}", !true);

    // Operator bit
    println!("5 & 3 = {}, 5 | 3 = {}, 5 ^ 3 = {}", 5 & 3, 5 | 3, 5 ^ 3);

    // String: &str (borrowed) vs String (owned, growable)
    let s_str: &str = "Halo Rust";
    let mut s_owned: String = String::from("Halo ");
    s_owned.push_str("Rust");
    println!("&str = {}, String = {}", s_str, s_owned);
    println!("Panjang String = {}", s_owned.len());

    // Konversi tipe: parse
    let teks = "123";
    let angka_dari_teks: i32 = teks.parse().unwrap();
    println!("parse \"123\" -> i32 = {}", angka_dari_teks + 1);

    // Konversi ke String
    let angka_lagi = 7;
    println!("to_string() -> \"{}\"", angka_lagi.to_string());
}