// Materi 23: Trait Object dan Generic
// Kompilasi: rustc --edition 2021 23_trait_object_dan_generic.rs -o materi23
// Jalankan tes: rustc --edition 2021 --test 23_trait_object_dan_generic.rs -o materi23_test

use std::f64::consts::PI;
use std::fmt::Display;

/// Trait sederhana yang object-safe: semua method hanya memakai `&self`.
trait Bentuk {
    fn nama(&self) -> &str;
    fn luas(&self) -> f64;
}

#[derive(Debug, Clone, Copy)]
struct Kotak {
    sisi: f64,
}

#[derive(Debug, Clone, Copy)]
struct Lingkaran {
    jari: f64,
}

impl Bentuk for Kotak {
    fn nama(&self) -> &str {
        "kotak"
    }

    fn luas(&self) -> f64 {
        self.sisi * self.sisi
    }
}

impl Bentuk for Lingkaran {
    fn nama(&self) -> &str {
        "lingkaran"
    }

    fn luas(&self) -> f64 {
        PI * self.jari * self.jari
    }
}

/// Generic: compiler membuat versi fungsi untuk tiap tipe konkret.
fn luas_generic<T: Bentuk>(bentuk: &T) -> f64 {
    bentuk.luas()
}

/// Trait object: satu collection bisa berisi beberapa tipe berbeda.
fn total_luas(bentuk: &[Box<dyn Bentuk>]) -> f64 {
    bentuk.iter().map(|b| b.luas()).sum()
}

/// Generic dengan beberapa bound sekaligus.
fn lebih_besar<T: PartialOrd + Display + Copy>(a: T, b: T) -> T {
    if a > b {
        a
    } else {
        b
    }
}

fn main() {
    let kotak = Kotak { sisi: 3.0 };
    let lingkaran = Lingkaran { jari: 2.0 };

    println!("{} → luas {}", kotak.nama(), luas_generic(&kotak));
    println!("{} → luas {}", lingkaran.nama(), luas_generic(&lingkaran));

    let kumpulan: Vec<Box<dyn Bentuk>> = vec![Box::new(kotak), Box::new(lingkaran)];
    println!("total luas: {:.4}", total_luas(&kumpulan));
    println!("lebih besar: {}", lebih_besar(10, 7));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn luas_kotak_lingkaran() {
        assert_eq!(Kotak { sisi: 3.0 }.luas(), 9.0);
        let lingkaran = Lingkaran { jari: 1.0 };
        assert!((lingkaran.luas() - PI).abs() < f64::EPSILON);
    }

    #[test]
    fn total_luas_campuran() {
        let kumpulan: Vec<Box<dyn Bentuk>> = vec![
            Box::new(Kotak { sisi: 2.0 }),
            Box::new(Lingkaran { jari: 1.0 }),
        ];
        let hasil = total_luas(&kumpulan);
        assert!((hasil - (4.0 + PI)).abs() < 1e-9);
    }

    #[test]
    fn generic_lebih_besar() {
        assert_eq!(lebih_besar(3, 9), 9);
        assert_eq!(lebih_besar(4.5, 1.2), 4.5);
    }
}
