//! Module `util::teks`: helper untuk memanipulasi teks.

/// Ubah huruf pertama setiap kata menjadi kapital.
pub fn kapitalisasi(teks: &str) -> String {
    teks.split_whitespace()
        .map(|kata| {
            let mut chars = kata.chars();
            match chars.next() {
                Some(pertama) => {
                    pertama.to_uppercase().collect::<String>() + chars.as_str()
                }
                None => String::new(),
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}

/// Potong teks maksimal `maks` karakter, tambahkan "..." jika terpotong.
pub fn potong(teks: &str, maks: usize) -> String {
    if teks.chars().count() <= maks {
        return teks.to_string();
    }
    let terpotong: String = teks.chars().take(maks).collect();
    format!("{}...", terpotong)
}

/// Hitung jumlah kata.
pub fn hitung_kata(teks: &str) -> usize {
    teks.split_whitespace().count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn kapitalisasi_benar() {
        assert_eq!(kapitalisasi("halo dunia rust"), "Halo Dunia Rust");
        assert_eq!(kapitalisasi(""), "");
    }

    #[test]
    fn potong_benar() {
        assert_eq!(potong("rust", 10), "rust");
        assert_eq!(potong("belajar rust", 7), "belajar...");
    }

    #[test]
    fn hitung_kata_benar() {
        assert_eq!(hitung_kata("satu dua tiga"), 3);
        assert_eq!(hitung_kata("   "), 0);
    }
}
