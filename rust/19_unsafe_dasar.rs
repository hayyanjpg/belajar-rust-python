// Materi 19: Unsafe Rust - Kapan dan Mengapa (Hati-hati)
// `unsafe` TIDAK mematikan borrow checker. Ia hanya mengizinkan 5 hal:
//   1. dereference raw pointer (*const T / *mut T)
//   2. memanggil unsafe function / block
//   3. mengimplementasikan unsafe trait (unsafe impl)
//   4. mengakses static mut
//   5. mendeklarasikan/panggil fungsi dari C (FFI)
//
// Tanggung jawab pembuktian keamanan berpindah dari compiler ke programmer.
// Aturan emas: bungkus unsafe di dalam API safe yang kecil dan terdokumentasi.
//
// Kompilasi: rustc --edition 2021 19_unsafe_dasar.rs -o unsafe_dasar
// Jalankan tes: rustc --edition 2021 --test 19_unsafe_dasar.rs -o tes && ./tes

use std::cell::Cell;
use std::mem::MaybeUninit;
use std::rc::Rc;

// ------------------------------------------------------------
// 1. POINTER
// ------------------------------------------------------------
unsafe fn baca_pointer(ptr: *const i32) -> i32 {
    // Di Rust 2024, block unsafe di dalam unsafe fn harus eksplisit.
    // Kebiasaan ini juga disarankan di edition 2021.
    unsafe { *ptr }
}

fn demo_pointer() {
    println!("\n--- RAW POINTER ---");

    let mut angka = 10_i32;
    let penunjuk: *mut i32 = &mut angka as *mut i32;

    unsafe {
        *penunjuk = 42;
        println!("  nilai setelah ditulis lewat pointer: {}", *penunjuk);
    }
    println!("  nilai variabel aslinya juga berubah: {angka}");

    let tetap: *const i32 = &angka;
    println!("  baca lewat unsafe fn: {}", unsafe { baca_pointer(tetap) });

    // Pointer boleh null; dereference null = undefined behavior.
    let kosong: *const i32 = std::ptr::null();
    println!("  pointer null? {}", kosong.is_null());

    // Contoh AMAN: Slice::from_raw_parts hanya valid jika pointer dan
    // panjangnya benar-benar berasal dari data yang hidup.
    let data = [1_i32, 2, 3];
    let slide = unsafe { std::slice::from_raw_parts(data.as_ptr(), data.len()) };
    println!("  slice dari raw parts: {slide:?}");
}

// ------------------------------------------------------------
// 2. MAYBEUNINIT
// ------------------------------------------------------------
fn demo_maybeuninit() {
    println!("\n--- MAYBEUNINIT ---");

    // Memory dialokasikan sebelum nilai diinisialisasi.
    let mut kotak = MaybeUninit::<i32>::uninit();
    kotak.write(99);

    // assume_init() hanya boleh dipanggil setelah write().
    let hasil = unsafe { kotak.assume_init() };
    println!("  hasil assume_init: {hasil}");

    // Alternatif yang LEBIH aman: pakai MaybeUninit::new().
    let sudah_terisi = MaybeUninit::new(7);
    println!("  MaybeUninit::new: {}", unsafe { sudah_terisi.assume_init() });
}

// ------------------------------------------------------------
// 3. STATIC MUT (DILARANG KERAS DI KODE PRODUKSI)
// ------------------------------------------------------------
static mut PENGHITUNG: i32 = 0;

fn naikkan_penghitung() {
    unsafe {
        PENGHITUNG += 1;
    }
}

#[allow(static_mut_refs)] // Contoh sengaja; di kode baru pakai Atomic/Mutex.
fn demo_static_mut() {
    println!("\n--- STATIC MUT ---");
    naikkan_penghitung();
    naikkan_penghitung();
    unsafe {
        println!("  penghitung: {PENGHITUNG}");
    }
    println!("  Masalahnya: akses bersama tanpa sinkronisasi = data race.");
    println!("  Gunakan AtomicUsize / Mutex instead.");
}

// ------------------------------------------------------------
// 4. UNSAFE TRAIT & IMPL
// ------------------------------------------------------------
unsafe trait TandaKhusus {}

#[derive(Debug)]
struct Penanda {
    nilai: Cell<i32>,
    bersama: Rc<i32>,
}

// CONTOH UNSOUND: Rc tidak Send, tapi kita paksa. Jangan tiru!
// Hanya dipakai di sini untuk menunjukkan bahwa compiler mempercayai kita.
unsafe impl Send for Penanda {}
unsafe impl TandaKhusus for Penanda {}

fn butuh_tanda<T: TandaKhusus>(_nilai: &T) {}

fn demo_unsafe_trait() {
    println!("\n--- UNSAFE TRAIT / IMPL ---");
    let penanda = Penanda {
        nilai: Cell::new(5),
        bersama: Rc::new(1),
    };
    penanda.nilai.set(6);
    butuh_tanda(&penanda);
    println!("  jumlah pemilik Rc: {}", Rc::strong_count(&penanda.bersama));
    println!("  penanda: {penanda:?}");
    println!("  Cell mengizinkan mutasi lewat &self (interior mutability).");
    println!("  unsafe impl Send untuk Rc di atas TIDAK aman secara logika.");
}

// ------------------------------------------------------------
// 5. FFI (FOREIGN FUNCTION INTERFACE)
// ------------------------------------------------------------
// Fungsi Rust dengan ABI C masih aman dipanggil dari Rust.
extern "C" fn kali_dua(n: i32) -> i32 {
    n * 2
}

fn demo_ffi() {
    println!("\n--- FFI ---");
    println!("  extern \"C\" fn kali_dua(3) = {}", kali_dua(3));
    println!("  Blok `extern \"C\" {{ fn ...; }}` untuk simbol C butuh unsafe.");
    println!("  Contoh nyata: libc, SQLite, OpenSSL, dan sebagainya.");
}

// ------------------------------------------------------------
// 6. CONTOH API SAFE DI ATAS UNSAFE
// ------------------------------------------------------------
/// Ambil elemen pertama slice tanpa panic dan tanpa mengembalikan referensi
/// yang bisa keluar dari blok unsafe. Ini contoh pembungkus yang baik.
fn pertama_atau_nol(data: &[i32]) -> i32 {
    if data.is_empty() {
        return 0;
    }
    let ptr: *const i32 = data.as_ptr();
    unsafe { *ptr }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pointer_dan_fungsi_unsafe() {
        let angka = 17;
        assert_eq!(unsafe { baca_pointer(&angka as *const i32) }, 17);

        let mut ubah = 1;
        let ptr = &mut ubah as *mut i32;
        unsafe {
            *ptr = 8;
        }
        assert_eq!(ubah, 8);
    }

    #[test]
    fn maybeuninit_terisi() {
        let mut nilai = MaybeUninit::<u32>::uninit();
        nilai.write(123);
        assert_eq!(unsafe { nilai.assume_init() }, 123);
    }

    #[test]
    fn api_safe_di_atas_unsafe() {
        assert_eq!(pertama_atau_nol(&[4, 5, 6]), 4);
        assert_eq!(pertama_atau_nol(&[]), 0);
    }

    #[test]
    fn extern_c_bisa_dipanggil() {
        assert_eq!(kali_dua(21), 42);
    }
}

fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO UNSAFE RUST (GUNAKAN DENGAN HATI-HATI)");
    println!("{}", "=".repeat(50));

    demo_pointer();
    demo_maybeuninit();
    demo_static_mut();
    demo_unsafe_trait();
    demo_ffi();

    println!("\n--- PEMBUNGKUS API SAFE ---");
    println!("  pertama_atau_nol([9, 8]) = {}", pertama_atau_nol(&[9, 8]));

    println!("\n=== SELESAI ===");
}
