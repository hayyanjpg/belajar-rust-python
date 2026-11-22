// Materi 02: Variabel dan Mutability
// Penjelasan: Rust default-nya immutable (tidak bisa diubah). Gunakan `mut` untuk mutable.
// Shadowing: mendeklarasikan variabel baru dengan nama yg sama (bisa beda tipe).

use std::sync::atomic::{AtomicU32, Ordering};

fn main() {
    let x = 5;
    println!("x = {}", x);

    // x = 6; // ERROR: tidak bisa diubah karena immutable

    let mut y = 10;
    println!("y sebelum diubah = {}", y);
    y = 20;
    println!("y sesudah diubah = {}", y);

    y += 5;
    println!("y setelah += 5 = {}", y);

    // Konstanta: wajib annotasi tipe, nama SCREAMING_SNAKE_CASE, tidak bisa mut
    const MAX_POINTS: u32 = 100_000;
    println!("Konstanta MAX_POINTS = {}", MAX_POINTS);

    // Shadowing: let baru menutupi (shadow) variabel sebelumnya
    let z = 5;
    let z = z * 2;
    println!("Shadowing z = {}", z);

    let z = z + 1;
    println!("Shadowing z lagi = {}", z);

    // Shadowing bisa ganti tipe data (berbeda dengan mut)
    let spasi = "   ";
    let spasi = spasi.len();
    println!("Shadowing dengan tipe berbeda = {}", spasi);

    let spaces = "   ";
    let spaces = spaces.len();
    println!("Nama sama, tipe berubah &str -> usize: {}", spaces);

    let mut counter = 0;
    counter = counter + 1;
    println!("Counter = {}", counter);

    // Destructuring tuple
    let (a, b) = (1, 2);
    println!("Destructuring tuple: a = {}, b = {}", a, b);

    let angka = 42;
    println!("Angka = {}", angka);

    // ============================================
    // LATIHAN TAMBAHAN (Exercise)
    // ============================================

    // Latihan 1: Scope & shadowing di block berbeda
    println!("\n=== Latihan 1: Scope & Shadowing ===");
    let nilai = 100;
    println!("Outer nilai = {}", nilai);
    {
        let nilai = 200;  // shadowing hanya di dalam block ini
        println!("Inner nilai = {}", nilai);
        let nilai = nilai + 50;
        println!("Inner shadow lagi = {}", nilai);
    }
    println!("Outer setelah block = {}", nilai);  // kembali ke 100

    // Latihan 2: Multiple mutable bindings & move semantics
    println!("\n=== Latihan 2: Mutable Binding & Move ===");
    let s1 = String::from("Hello");
    let mut s2 = s1;  // move: s1 tidak valid lagi
    s2.push_str(", World");
    println!("s2 = {}", s2);
    // println!("{}", s1); // ERROR: borrow of moved value

    // Latihan 3: Const vs static (static punya alamat memori tetap)
    println!("\n=== Latihan 3: Const vs Static ===");
    const PI: f64 = 3.14159265359;
    // Mutable static (`static mut`) butuh unsafe dan rawan race condition.
    // Alternatif yang aman: atomic, bisa dipakai lintas thread tanpa unsafe.
    static COUNTER: AtomicU32 = AtomicU32::new(0);
    COUNTER.fetch_add(1, Ordering::SeqCst);
    println!("CONST PI = {}", PI);
    println!("STATIC COUNTER (atomic) = {}", COUNTER.load(Ordering::SeqCst));

    // Latihan 4: Type inference dengan anotasi eksplisit
    println!("\n=== Latihan 4: Type Inference ===");
    let default_int = 42;        // default i32
    let default_float = 3.14;    // default f64
    let eksplisit_u8: u8 = 255;  // anotasi tipe wajib
    let eksplisit_f32: f32 = 2.5;
    println!("default_int (i32) = {}", default_int);
    println!("default_float (f64) = {}", default_float);
    println!("eksplisit_u8 = {}", eksplisit_u8);
    println!("eksplisit_f32 = {}", eksplisit_f32);

    // Latihan 5: Destructuring struct & array
    println!("\n=== Latihan 5: Destructuring Struct & Array ===");
    struct Titik { x: i32, y: i32 }
    let p = Titik { x: 10, y: 20 };
    let Titik { x, y } = p;
    println!("Titik: x={}, y={}", x, y);

    let arr = [1, 2, 3, 4, 5];
    let [first, second, ..] = arr;  // .. = sisa elemen (diabaikan)
    println!("Array: first={}, second={}", first, second);

    // Latihan 6: Mutable reference vs immutable reference
    println!("\n=== Latihan 6: Borrowing Rules ===");
    let mut data = vec![1, 2, 3];
    {
        let ref1 = &data;      // immutable borrow #1
        let ref2 = &data;      // immutable borrow #2 (boleh banyak)
        println!("Immutable refs: {:?}, {:?}", ref1, ref2);
    } // borrow berakhir di akhir scope ini
    // let mut_ref = &mut data; // ERROR kalau masih ada immutable borrow aktif
    let mut_ref = &mut data; // OK sekarang
    mut_ref.push(4);
    println!("Mutable ref: {:?}", mut_ref);
}