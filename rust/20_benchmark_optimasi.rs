// Materi 20: Benchmark Sederhana & Optimasi Memori
// Tujuan: melihat perbedaan biaya alokasi, iterasi, dan ukuran tipe data.
// Catatan: hasil microbenchmark tidak absolut. Jalankan dengan --release
// untuk angka yang lebih representative:
//   rustc --edition 2021 -O 20_benchmark_optimasi.rs -o bench
//
// Jalankan tes: rustc --edition 2021 --test 20_benchmark_optimasi.rs -o tes && ./tes

use std::hint::black_box;
use std::mem::size_of;
use std::time::{Duration, Instant};

const N: usize = 20_000;

fn ukur<F: FnOnce() -> R, R>(f: F) -> (Duration, R) {
    let mulai = Instant::now();
    let hasil = f();
    (mulai.elapsed(), hasil)
}

fn push_tanpa_kapasitas() -> Vec<i32> {
    let mut data = Vec::new();
    for i in 0..N {
        data.push(black_box(i as i32));
    }
    data
}

fn push_dengan_kapasitas() -> Vec<i32> {
    // with_capacity mengalokasi sekali, bukan berkali-kali saat Vec tumbuh.
    let mut data = Vec::with_capacity(N);
    for i in 0..N {
        data.push(black_box(i as i32));
    }
    data
}

fn jumlah_iter(data: &[i64]) -> i64 {
    data.iter().copied().sum()
}

fn jumlah_loop(data: &[i64]) -> i64 {
    let mut total = 0_i64;
    for &nilai in data {
        total += nilai;
    }
    total
}

fn demo_waktu() {
    println!("\n--- BENCHMARK WAKTU ({N} iterasi) ---");

    let (waktu1, hasil1) = ukur(push_tanpa_kapasitas);
    let (waktu2, hasil2) = ukur(push_dengan_kapasitas);
    println!("  Vec::new()          : {waktu1:?} (len={})", hasil1.len());
    println!("  Vec::with_capacity  : {waktu2:?} (len={})", hasil2.len());
    println!("  sama isinya         : {}", hasil1 == hasil2);

    let data: Vec<i64> = (1..=1_000_000_i64).collect();
    let (waktu3, jumlah1) = ukur(|| jumlah_iter(&data));
    let (waktu4, jumlah2) = ukur(|| jumlah_loop(&data));
    println!("  iter().sum()        : {waktu3:?} -> {jumlah1}");
    println!("  for loop eksplisit  : {waktu4:?} -> {jumlah2}");
    println!("  hasil sama          : {}", jumlah1 == jumlah2);
    println!("  compiler sering mengoptimasi keduanya menjadi kode yang sama.");
}

fn demo_memori() {
    println!("\n--- UKURAN TIPE (byte) ---");
    println!("  bool            : {}", size_of::<bool>());
    println!("  i32             : {}", size_of::<i32>());
    println!("  i64             : {}", size_of::<i64>());
    println!("  Option<i32>     : {}", size_of::<Option<i32>>());
    println!("  Option<&str>    : {}", size_of::<Option<&str>>());
    println!("  &str (fat ptr)  : {}", size_of::<&str>());
    println!("  String          : {}", size_of::<String>());
    println!("  Vec<i32>        : {}", size_of::<Vec<i32>>());
    println!("  [i32; 4] (stack): {}", size_of::<[i32; 4]>());

    println!("\n--- STACK vs HEAP ---");
    let di_stack = [1_i32, 2, 3, 4];
    let di_heap = vec![1_i32, 2, 3, 4];
    println!("  array: {:?}, alamat: {:p}", di_stack, &di_stack);
    println!("  Vec  : {:?}, alamat: {:p}", di_heap, di_heap.as_ptr());
    println!("  Vec menyimpan pointer + kapasitas di stack, datanya di heap.");
}

fn demo_optimasi_tambahan() {
    println!("\n--- OPTIMASI LAIN ---");

    // Hindari collect() hanya untuk langsung dijumlahkan.
    let angka = [1_u64, 2, 3, 4, 5];
    let langsung: u64 = angka.iter().map(|n| n * n).sum();
    println!("  map + sum tanpa collect: {langsung}");

    // Hindari kloning String saat cukup meminjam &str.
    let nama = String::from("Hayyan");
    let pinjam: &str = &nama;
    println!("  pinjam &str '{pinjam}' lebih murah dari clone(): {}", name_len(pinjam));

    // Layout enum bisa dioptimasi dengan reordering field.
    println!("  Option<NonZeroU32> = {} byte (niche optimization)", std::mem::size_of::<Option<std::num::NonZeroU32>>());
}

fn name_len(teks: &str) -> usize {
    teks.len()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn kapasitas_tidak_mengubah_isi() {
        assert_eq!(push_tanpa_kapasitas(), push_dengan_kapasitas());
    }

    #[test]
    fn dua_cara_summasi_sama() {
        let data = vec![1_i64, 2, 3, 4, 5];
        assert_eq!(jumlah_iter(&data), jumlah_loop(&data));
        assert_eq!(jumlah_iter(&data), 15);
    }

    #[test]
    fn ukuran_tipe_wajar() {
        assert_eq!(size_of::<i32>(), 4);
        assert_eq!(size_of::<i64>(), 8);
        assert_eq!(size_of::<[i32; 4]>(), 16);
        assert!(size_of::<&str>() > size_of::<&i32>());
    }

    #[test]
    fn name_len_benar() {
        assert_eq!(name_len("Rust"), 4);
    }
}

fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO BENCHMARK & OPTIMASI MEMORI");
    println!("{}", "=".repeat(50));

    demo_waktu();
    demo_memori();
    demo_optimasi_tambahan();

    println!("\n=== SELESAI ===");
}
