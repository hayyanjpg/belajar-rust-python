//! Materi 12: Module System & Cargo
//!
//! Crate ini adalah library. File `main.rs` adalah binary yang memakainya.
//! Struktur:
//! - `matematika`      : module di file `matematika.rs`
//! - `util`            : module di folder `util/` (butuh `mod.rs`)
//! - `util::teks`      : submodule di `util/teks.rs`
//!
//! Aturan penting:
//! - `pub` membuat item bisa diakses dari luar module.
//! - `mod` mendaftarkan module; `use` mempersingkat path.
//! - `crate::` menunjuk root crate, `super::` menunjuk module induk, `self::` module ini.

pub mod matematika;
pub mod util;

/// Versi crate diambil otomatis dari `Cargo.toml` saat compile.
pub const VERSI: &str = env!("CARGO_PKG_VERSION");

pub fn info_crate() -> String {
    format!("belajar_module v{}", VERSI)
}
