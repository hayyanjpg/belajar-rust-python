//! Contoh crate kecil untuk memahami alur `cargo publish`.
//!
//! Crate ini sengaja dibuat sederhana hanya untuk latihan. Nama paketnya
//! mungkin sudah dipakai orang lain di crates.io; ganti nama sebelum publish.

/// Buat sapaan sederhana.
///
/// ```
/// assert_eq!(belajar_publish_contoh::sapaan("Rust"), "Halo, Rust!");
/// ```
pub fn sapaan(nama: &str) -> String {
    format!("Halo, {nama}!")
}

/// Hitung kuadrat bilangan bulat.
pub fn kuadrat(n: i64) -> i64 {
    n * n
}

/// Rata-rata data; `None` jika data kosong.
pub fn rata_rata(data: &[f64]) -> Option<f64> {
    if data.is_empty() {
        return None;
    }
    Some(data.iter().sum::<f64>() / data.len() as f64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sapaan_benar() {
        assert_eq!(sapaan("Dunia"), "Halo, Dunia!");
        assert_eq!(sapaan(""), "Halo, !");
    }

    #[test]
    fn kuadrat_benar() {
        assert_eq!(kuadrat(0), 0);
        assert_eq!(kuadrat(-4), 16);
        assert_eq!(kuadrat(7), 49);
    }

    #[test]
    fn rata_rata_benar() {
        assert_eq!(rata_rata(&[2.0, 4.0, 6.0]), Some(4.0));
        assert_eq!(rata_rata(&[]), None);
    }
}
