// Integration test: menguji crate seolah-olah kita adalah pemakai luar.
// Berada di folder `tests/`, sehingga hanya bisa memakai item `pub`.
// Jalankan dengan: cargo test

use belajar_module::info_crate;
use belajar_module::matematika::geometri::persegi::{keliling, luas};
use belajar_module::matematika::geometri::{keliling_lingkaran, luas_lingkaran};
use belajar_module::matematika::{bagi, faktorial, tambah, PI};
use belajar_module::util::teks::{hitung_kata, kapitalisasi, potong};

#[test]
fn info_crate_mengandung_versi() {
    let info = info_crate();
    assert!(info.starts_with("belajar_module v"));
    assert_eq!(
        info,
        format!("belajar_module v{}", env!("CARGO_PKG_VERSION"))
    );
}

#[test]
fn aritmetika_dasar() {
    assert_eq!(tambah(2, 3), 5);
    assert_eq!(faktorial(0), 1);
    assert_eq!(faktorial(6), 720);
}

#[test]
fn pembagian_mengembalikan_result() {
    assert_eq!(bagi(9.0, 3.0), Ok(3.0));
    assert!(bagi(1.0, 0.0).is_err());
}

#[test]
fn geometri_persegi() {
    assert_eq!(luas(4.0), 16.0);
    assert_eq!(keliling(4.0), 16.0);
}

#[test]
fn geometri_lingkaran_memakai_pi() {
    assert!((luas_lingkaran(1.0) - PI).abs() < 1e-9);
    assert!((keliling_lingkaran(1.0) - 2.0 * PI).abs() < 1e-9);
    assert!((luas_lingkaran(2.0) - 4.0 * PI).abs() < 1e-9);
}

#[test]
fn kapitalisasi_teks() {
    assert_eq!(kapitalisasi("halo dunia rust"), "Halo Dunia Rust");
    assert_eq!(kapitalisasi(""), "");
}

#[test]
fn potong_teks() {
    assert_eq!(potong("belajar rust", 7), "belajar...");
    assert_eq!(potong("rust", 10), "rust");
}

#[test]
fn hitung_kata_dari_teks() {
    assert_eq!(hitung_kata("satu dua tiga"), 3);
    assert_eq!(hitung_kata("   "), 0);
}

#[test]
fn kombinasi_beberapa_modul() {
    let teks = "belajar rust hari ini";
    let ringkas = potong(&kapitalisasi(teks), 10);
    let total = tambah(hitung_kata(teks) as i32, faktorial(3) as i32);

    assert_eq!(ringkas, "Belajar Ru...");
    assert_eq!(total, 10);
}
