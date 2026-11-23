//! Unit test lanjutan untuk materi 12 (Module System & Cargo).
//!
//! File ini sengaja dipisah dari `matematika.rs` dan `util/teks.rs` supaya
//! mudah dibaca: semua pengujian tambahan berkumpul di satu tempat.
//!
//! Jalankan dengan: `cargo test`

use crate::{info_crate, matematika, util::teks, VERSI};

#[test]
fn tambah_menangani_negatif_dan_nol() {
    assert_eq!(matematika::tambah(-5, 3), -2);
    assert_eq!(matematika::tambah(0, 0), 0);
    assert_eq!(matematika::tambah(i32::MAX - 1, 1), i32::MAX);
}

#[test]
fn faktorial_nilai_besar() {
    assert_eq!(matematika::faktorial(10), 3_628_800);
    assert_eq!(matematika::faktorial(20), 2_432_902_008_176_640_000);
}

#[test]
fn bagi_mengembalikan_hasil_desimal() {
    assert!((matematika::bagi(10.0, 4.0).unwrap() - 2.5).abs() < f64::EPSILON);
    assert!((matematika::bagi(1.0, 3.0).unwrap() - 1.0 / 3.0).abs() < f64::EPSILON);
}

#[test]
fn bagi_nol_memiliki_pesan_error() {
    let error = matematika::bagi(10.0, 0.0).unwrap_err();
    assert_eq!(error, "Tidak bisa membagi dengan nol");
}

#[test]
fn konstanta_pi_sesuai_ekspektasi() {
    assert!((matematika::PI - 3.14159).abs() < f64::EPSILON);
}

#[test]
fn luas_lingkaran_radius_dua() {
    let luas = matematika::geometri::luas_lingkaran(2.0);
    assert!((luas - 4.0 * matematika::PI).abs() < 1e-9);
}

#[test]
fn keliling_lingkaran_radius_dua() {
    let keliling = matematika::geometri::keliling_lingkaran(2.0);
    assert!((keliling - 4.0 * matematika::PI).abs() < 1e-9);
}

#[test]
fn persegi_menghitung_luas_dan_keliling() {
    use matematika::geometri::persegi;

    assert_eq!(persegi::luas(7.5), 56.25);
    assert_eq!(persegi::keliling(7.5), 30.0);
}

#[test]
fn kapitalisasi_spasi_berlebih() {
    assert_eq!(
        teks::kapitalisasi("  halo   dunia  rust "),
        "Halo Dunia Rust"
    );
    assert_eq!(teks::kapitalisasi("rust\nstudy"), "Rust Study");
}

#[test]
fn potong_menghitung_karakter_bukan_byte() {
    assert_eq!(teks::potong("héllo", 3), "hél...");
    assert_eq!(teks::potong("🚀rust", 1), "🚀...");
}

#[test]
fn potong_batas_pas_tidak_memotong() {
    assert_eq!(teks::potong("rust", 4), "rust");
    assert_eq!(teks::potong("", 0), "");
}

#[test]
fn hitung_kata_dengan_tab_dan_newline() {
    assert_eq!(teks::hitung_kata("satu\tdua\ntiga"), 3);
    assert_eq!(teks::hitung_kata("\n  \t"), 0);
}

#[test]
fn info_crate_mengandung_versi() {
    assert!(!VERSI.is_empty());
    assert_eq!(info_crate(), format!("belajar_module v{}", VERSI));
}
