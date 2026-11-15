// Materi 05: Ownership Dasar

fn main() {
    // 1. Tipe Copy (data di stack) — disalin, keduanya tetap valid
    let x = 5;
    let y = x;
    println!("x = {}, y = {} -> Copy, keduanya valid", x, y);

    // 2. Tipe non-Copy (data di heap) — ownership DIPINDAH
    let s1 = String::from("Hello");
    let s2 = s1;
    println!("s2 = {} -> s1 sudah tidak valid setelah dipindah", s2);

    // 3. clone() menyalin data di heap
    let a = String::from("Rust");
    let b = a.clone();
    println!("a = {}, b = {} -> clone, keduanya valid", a, b);

    // 4. Scope dan drop otomatis
    {
        let s3 = String::from("di dalam scope");
        println!("{}", s3);
    }
    println!("s3 sudah di-drop saat keluar scope");

    // 5. Borrowing immutable (&T) — hanya boleh membaca
    let s5 = String::from("Borrowing");
    print_panjang(&s5);
    println!("s5 masih valid: {}", s5);

    // 6. Borrowing mutable (&mut T) — boleh mengubah
    let mut s6 = String::from("hello");
    ubah(&mut s6);
    println!("s6 setelah diubah: {}", s6);

    // 7. Aturan borrow: banyak &T boleh, hanya satu &mut T
    let s7 = String::from("banyak immutable borrow");
    let r1 = &s7;
    let r2 = &s7;
    println!("{} dan {}", r1, r2);

    let mut s8 = String::from("mut");
    let m1 = &mut s8;
    m1.push_str("ated");
    println!("m1 = {}", m1);

    // 8. Ownership berpindah ke fungsi lalu dikembalikan
    let s9 = String::from("dipindah lalu dikembalikan");
    let s10 = ambil_dan_kembalikan(s9);
    println!("{}", s10);

    // 9. Mengembalikan tuple agar data tidak hilang
    let s11 = String::from("cek panjang");
    let (teks, panjang) = hitung_panjang(s11);
    println!("\"{}\" panjangnya {}", teks, panjang);

    // 10. Ownership pada slice / collection
    let angka = vec![1, 2, 3, 4, 5];
    println!("total = {}", jumlahkan(&angka));
    println!("angka masih valid = {:?}", angka);
}

fn print_panjang(s: &String) {
    println!("panjang '{}' = {}", s, s.len());
}

fn ubah(s: &mut String) {
    s.push_str(", world");
}

fn ambil_dan_kembalikan(mut s: String) -> String {
    s.push_str("!");
    s
}

fn hitung_panjang(s: String) -> (String, usize) {
    let panjang = s.len();
    (s, panjang)
}

fn jumlahkan(ns: &[i32]) -> i32 {
    let mut total = 0;
    for &n in ns {
        total += n;
    }
    total
}