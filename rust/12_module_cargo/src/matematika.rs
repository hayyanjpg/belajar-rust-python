//! Module `matematika`: kumpulan fungsi dan konstanta matematika.

/// Konstanta PI bisa diakses dari luar sebagai `matematika::PI`.
pub const PI: f64 = 3.14159;

pub fn tambah(a: i32, b: i32) -> i32 {
    a + b
}

pub fn faktorial(n: u64) -> u64 {
    (1..=n).product()
}

/// Operasi yang bisa gagal mengembalikan `Result`, bukan panic.
pub fn bagi(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Tidak bisa membagi dengan nol".to_string())
    } else {
        Ok(a / b)
    }
}

/// Nested module: `matematika::geometri`.
pub mod geometri {
    // `super::` = module induk (`matematika`), tempat PI berada.
    use super::PI;

    pub fn luas_lingkaran(r: f64) -> f64 {
        PI * r * r
    }

    pub fn keliling_lingkaran(r: f64) -> f64 {
        2.0 * PI * r
    }

    /// Nested module lagi: `matematika::geometri::persegi`.
    pub mod persegi {
        pub fn luas(sisi: f64) -> f64 {
            sisi * sisi
        }

        pub fn keliling(sisi: f64) -> f64 {
            4.0 * sisi
        }
    }
}

// ============================================
// UNIT TEST DI DALAM MODULE
// ============================================
// Jalankan dengan: cargo test
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tambah_benar() {
        assert_eq!(tambah(2, 3), 5);
        assert_eq!(tambah(-1, 1), 0);
    }

    #[test]
    fn faktorial_benar() {
        assert_eq!(faktorial(0), 1);
        assert_eq!(faktorial(1), 1);
        assert_eq!(faktorial(5), 120);
    }

    #[test]
    fn bagi_dengan_nol_error() {
        assert!(bagi(10.0, 0.0).is_err());
        assert_eq!(bagi(10.0, 2.0).unwrap(), 5.0);
    }

    #[test]
    fn geometri_benar() {
        let luas = geometri::persegi::luas(4.0);
        assert_eq!(luas, 16.0);
        assert!((geometri::luas_lingkaran(1.0) - PI).abs() < 1e-9);
    }
}
